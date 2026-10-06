"""Execute CAN211 flag consumers: CAN21A values and protected latch7978.

Original ECU functions and helpers, synthetic RAM and explicit call order.
No sender attribution, physical units, full scheduler or actuator model.
"""
from fractions import Fraction
import hashlib
import itertools
import json

from verify_can201_byte6 import ECU, TCU, w, r
from sh_exact_float import SHExactFloat, exact_bits, exact_value
from sh_software_arithmetic import SHSoftwareArithmetic


FLAGS = [(13, 12, 0x6A20), (10, 9, 0x6A21), (5, 4, 0x6A23),
         (2, 0, 0x6A25), (1, 0, 0x6A26)]


def f(e, a, value):
    w(e, a, exact_bits(value), 4)


def rf(e, a):
    return exact_value(r(e, a, 4))


def protected_byte(e, a, value):
    w(e, a, (value << 8) | (value ^ 255), 2)


def check_protected_float(e, a, expected):
    assert rf(e, a) == expected, (hex(a), rf(e, a), expected)
    bits = r(e, a, 4)
    checksum = ~((bits >> 16) + (bits & 65535)) & 65535
    assert r(e, a+4, 2) == r(e, a+6, 2) == checksum
    assert 0x15522 in e.visited


def receive211(e, flags):
    w(e, 0x6A10, 11000, 2)
    w(e, 0x6A12, 0xDEAD, 2)
    w(e, 0x6A14, flags, 2)
    w(e, 0x6A16, 0xBEEF, 2)
    e.run(0x34B8C)
    e.run(0x34BB2)
    e.run(0x349CA)


def receive21a(e, word0=11000, word1=12000):
    w(e, 0x6AA8, word0, 2)
    w(e, 0x6AAA, word1, 2)
    w(e, 0x6AAC, 0xDEADBEEF, 4)
    e.run(0x3572A)
    e.run(0x35750)
    assert r(e, 0x6AB6, 2) == word0 and r(e, 0x6AB8, 2) == word1
    assert r(e, 0x6AB4) == 20


def normalize(e, word0, word1, fresh, inhibit, flags):
    e.run(0x3558E)
    first = -10000 if word0 == 65535 or not fresh else max(word0-10000, -1000)
    second = (-10000 if word1 in (65534, 65535) or not fresh or inhibit == 1
              or not any(flags) else min(word1-10000, 10000))
    assert r(e, 0x6AB0, 2) == word0 and r(e, 0x6AB2, 2) == word1
    assert rf(e, 0x6A9C) == first
    check_protected_float(e, 0x6AA0, second)
    return first, second


def latch(e, enabled, count, requests, old, prior_bits=0x55, prior_state=0,
          state=0, timer=0, source=900, current_bits=0):
    protected_byte(e, 0x722E, enabled)
    protected_byte(e, 0x7978, old)
    w(e, 0x7974, count, 2)
    for address, value in zip((0x6E57, 0x6A20, 0x797A), requests):
        w(e, address, value)
    for address, value in [(0x7987, prior_bits), (0x7985, prior_state),
                           (0x797B, state), (0x75B0, timer), (0x73C4, current_bits)]:
        w(e, address, value)
    f(e, 0x6DB4, source)
    expected = (0 if not enabled or not count else 1 if 1 in requests
                or ((prior_bits & 128 or timer > 0) and prior_state == 0
                    and state == 1 and source < 900) else old)
    e.run(0x4E80C)
    assert r(e, 0x7978, 2) == (expected << 8) | (expected ^ 255)
    assert r(e, 0x7985) == state
    assert r(e, 0x7987) == (prior_bits & 127) | (128 if current_bits & 16 else 0)
    return expected


def main():
    assert ECU[0x3792C:0x3793C].hex() == '0000021a01070800ffff6aa801000000'
    assert ECU[0xB8247] == 20
    assert ECU[0xB81B2] == 1  #Stock calibration disables216bit7 ->6E57.
    for address, expected in [(0xB826C, -1000), (0xB8270, 10000), (0xCDDB8, 900)]:
        assert exact_value(int.from_bytes(ECU[address:address+4], 'big')) == expected
    e = SHExactFloat(ECU)
    e.run(0x35538)
    assert rf(e, 0x6A9C) == -10000 and r(e, 0x6AB4) == 20
    check_protected_float(e, 0x6AA0, -10000)

    words = [0, 1, 8999, 9000, 9001, 9999, 10000, 10001, 19999,
             20000, 20001, 32767, 32768, 65533, 65534, 65535]
    numeric_cases = 0
    for a, b, fresh, inhibit in itertools.product(words, words, [0, 1, 255], [0, 1, 2, 255]):
        e = SHExactFloat(ECU)
        receive21a(e, a, b)
        w(e, 0x6AB4, fresh)
        w(e, 0x7190, inhibit)
        w(e, 0x6A20, 1)
        normalize(e, a, b, fresh, inhibit, [1])
        numeric_cases += 1

    flag_cases = 0
    bits = [0, 1, 2, 4, 5, 9, 10, 12, 13]
    for pattern, fault, fresh211 in itertools.product(range(512), [0, 1], [0, 20]):
        payload = sum(((pattern >> i) & 1) << bit for i, bit in enumerate(bits))
        e = SHExactFloat(ECU)
        w(e, 0x69E1, fault)
        receive211(e, payload)
        w(e, 0x6A1E, fresh211)
        e.run(0x349CA)
        expected = [int(bool(payload & (1 << request)) and not
                        (fault or payload & (1 << inhibit))) for request, inhibit, _ in FLAGS]
        assert [r(e, address) for _, _, address in FLAGS] == expected
        receive21a(e)
        normalize(e, 11000, 12000, 20, 0, expected)
        # Real unpack/normalizer produced6A20; do not replace it before latch.
        protected_byte(e, 0x722E, 1)
        w(e, 0x7974, 1, 2)
        protected_byte(e, 0x7978, 0)
        e.run(0x4E80C)
        assert r(e, 0x7978, 2) == (0x1FE if expected[0] else 0xFF)
        flag_cases += 1

    nonboolean_cases = 0
    for _, _, address in FLAGS:
        for value in [1, 2, 128, 255]:
            e = SHExactFloat(ECU)
            receive21a(e)
            w(e, address, value)
            normalize(e, 11000, 12000, 20, 0, [value])
            nonboolean_cases += 1

    countdown_cases = 0
    for old, reset, mode, sr in itertools.product([0, 1, 19, 20, 255], [0, 1, 255],
                                                 [0, 127, 128, 255], [0, 0xF0, 0x301]):
        e = SHExactFloat(ECU)
        e.sr = sr
        # Suppress3894's optional scheduler tail using its real context gate.
        w(e, 0x12C8, 0xFFFF12D0, 4)
        w(e, 0x12D1, 1)
        for address, value in [(0x6AB4, old), (0x69E0, reset), (0x735A, mode)]:
            w(e, address, value)
        e.run(0x35674)
        assert r(e, 0x6AB4) == (20 if reset or mode & 128 else max(old-1, 0))
        assert e.sr == sr & 0xF0  #3880 saves interrupt mask, not the whole SR.
        assert 0x3D78 not in e.visited
        countdown_cases += 1

    latch_cases = 0
    for enabled, count, a, b, c, old in itertools.product([0, 1, 255], [0, 1, 65535],
                                                        [0, 1, 2, 255], [0, 1, 2, 255],
                                                        [0, 1, 2, 255], [0, 1]):
        latch(SHExactFloat(ECU), enabled, count, [a, b, c], old)
        latch_cases += 1
    edge_cases = 0
    for prior, oldstate, state, timer, source, current, old in itertools.product(
            [0x55, 0xD5], [0, 1, 2], [0, 1, 2], [0, 1, 255],
            [Fraction(1799, 2), 900, Fraction(1801, 2)], [0, 16, 255], [0, 1]):
        latch(SHExactFloat(ECU), 1, 1, [0, 0, 0], old, prior, oldstate, state, timer, source, current)
        edge_cases += 1

    initializer_cases = 0
    for enabled in [0, 1, 2, 255]:
        e = SHExactFloat(ECU)
        protected_byte(e, 0x722E, enabled)
        protected_byte(e, 0x7978, 1)
        e.run(0x4E7F4)
        assert r(e, 0x7984) == enabled and r(e, 0x7978, 2) == 255
        initializer_cases += 1

    paired_at_cases = 0
    for source, traction, fresh in itertools.product(range(256), [0, 1], [0, 20]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x98A0, source)
        w(t, 0x92C6, 0x20)  #Unrelated measurement byte4 invalid.
        t.run(0x18F8C, 1)
        e = SHExactFloat(ECU)
        for i in range(8):
            w(e, 0x6A40+i, r(t, 0x8EFD+i))
        for address, value in [(0x734A, 0x80), (0x734C, 1), (0x6A5D, fresh)]:
            w(e, address, value)
        e.run(0x35034)
        e.run(0x34CEC)
        assert (r(t, 0x8F04) >> 7) == r(e, 0x6A5F) == source & 1
        w(e, 0x6E57, 255)
        e.run(0x3B450)
        assert r(e, 0x6E57) == 0
        receive211(e, traction << 13)
        protected_byte(e, 0x722E, 1)
        protected_byte(e, 0x7978, 0)
        w(e, 0x7974, 1, 2)
        e.run(0x4E80C)
        assert r(e, 0x7978, 2) == (0x1FE if traction else 255)
        paired_at_cases += 1

    # Retained history means the current73C4 bit cannot satisfy the same pass.
    e = SHExactFloat(ECU)
    assert latch(e, 1, 1, [0, 0, 0], 0, state=0, source=899, current_bits=16) == 0
    w(e, 0x797B, 1)
    w(e, 0x73C4, 0)
    e.run(0x4E80C)
    assert r(e, 0x7978, 2) == 0x1FE and r(e, 0x7987) == 0x55
    e.run(0x4E80C)
    assert r(e, 0x7978, 2) == 0x1FE
    w(e, 0x7974, 0, 2)
    e.run(0x4E80C)
    assert r(e, 0x7978, 2) == 255

    lifecycle = []
    e = SHExactFloat(ECU)
    receive21a(e)
    w(e, 0x12C8, 0xFFFF12D0, 4)
    w(e, 0x12D1, 1)
    for address in [0x722A, 0x7353, 0x6B04, 0x722E]:
        w(e, address, 1)
    w(e, 0x7974, 1, 2)
    protected_byte(e, 0x7978, 0)
    for step in range(23):
        if step:
            e.run(0x35674)
        if step == 22:
            receive21a(e)
        # Only21A expires; fresh211 and the other grouped counter stay present.
        receive211(e, 1 << 13)
        e.run(0x347B8)
        e.run(0x349CA)
        counter = 20 if step == 22 else max(20-step, 0)
        flag = int(counter > 0)
        assert r(e, 0x6AB4) == counter and r(e, 0x69E1) == 1-flag
        assert r(e, 0x6A20) == flag
        values = normalize(e, 11000, 12000, counter, 0, [flag])
        e.run(0x4E80C)
        # Loss ofCAN211 request does not clear the already-set7978 latch.
        assert r(e, 0x7978, 2) == 0x1FE
        lifecycle.append(dict(call=step, receipt21a=counter, fault=r(e, 0x69E1),
                              flag6a20=flag, field0=values[0], field1=values[1], latch7978=1))
    protected_byte(e, 0x722E, 0)
    e.run(0x4E80C)
    assert r(e, 0x7978, 2) == 255
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                         tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                         scope=__doc__.strip(), numeric_cases=numeric_cases,
                         integrated_flag_cases=flag_cases, nonboolean_flag_cases=nonboolean_cases,
                         countdown_cases=countdown_cases, latch_cases=latch_cases,
                         edge_cases=edge_cases, initializer_cases=initializer_cases,
                         paired_at_cases=paired_at_cases,
                         history_sequence_calls=4, receipt_lifecycle=lifecycle,
                         final_disable_clears_latch=True), indent=2))


if __name__ == '__main__':
    main()
