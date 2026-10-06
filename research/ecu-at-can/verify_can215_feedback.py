"""Original ECU CAN215 -> TCU base/request -> CAN216 -> same ECU spark state.

Explicit model, admission, diagnostic-summary and timer fixtures. Original
functions execute; no physical CAN controller, real scheduler or unit claim.
"""
from fractions import Fraction
import hashlib
import itertools
import json

from verify_can201_byte6 import ECU, TCU, w, r
from sh_exact_float import SHExactFloat, exact_bits
from sh_software_arithmetic import SHSoftwareArithmetic
from sh_subset import signed
from verify_tcu_spark_requests import ramp_fixture
from verify_spark_interaction import paired


def clamp(x, low=-32768, high=32767):
    return min(high, max(low, x))


def sender(primary, offset, invalid=0, mode=0x80):
    e = SHExactFloat(ECU)
    w(e, 0x734A, mode); w(e, 0x6E2E, invalid)
    for a, value in [(0x71EC, primary), (0x71B4, 30), (0x71C4, offset)]:
        w(e, a, exact_bits(value), 4)
    for i in range(8):
        w(e, 0x6B50+i, 0xA5)
    e.run(0x369D6); e.run(0x36A28)
    return e, bytes(r(e, 0x6B50+i) for i in range(8))


def receive(t, payload):
    for i, value in enumerate(payload):
        w(t, 0x8F2C+i, value)
    t.run(0x1ACF0)


def expected_decode(first, offset, old_first, old_offset):
    offset_valid = offset != 65535
    converted_offset = clamp((offset-512)*10) if offset_valid else old_offset
    valid = first != 65535 and offset_valid
    converted_first = clamp((first-512)*10-converted_offset) if valid else old_first
    return converted_offset, 2 if offset_valid else 1, converted_first, 2 if valid else 1


def main():
    assert TCU[0x5C81A:0x5C81E].hex() == TCU[0x5C822:0x5C826].hex() == '0101fe00'
    assert TCU[0x5C5B4:0x5C5BC].hex() == '010a0000010a0000'
    assert TCU[0x5FD50:0x5FD58].hex() == '241824182418fc18'
    encoder_cases = 0
    values = [-600, -512, Fraction(-1023, 2), 0, Fraction(31, 64), Fraction(1, 2), 25, 65022, 70000]
    for primary, offset, invalid, mode in itertools.product(values, [-5, 0, 5], [0, 1, 2, 255], [0, 0x40, 0x80, 0xC0]):
        e, payload = sender(primary, offset, invalid, mode)
        if mode == 0:
            assert payload == bytes([0xA5]*8)
        else:
            for word, value in zip([0, 2, 4], [primary, 30, offset]):
                expected = 65535 if invalid == 1 else clamp(int(value+512+Fraction(1, 2)), 0, 65534)
                assert int.from_bytes(payload[word:word+2], 'big') == expected
        encoder_cases += 1

    conversion_cases = 0
    values = [0, 1, 511, 512, 537, 1000, 3788, 3789, 65534, 65535]
    for first, offset, old_first, old_offset in itertools.product(values, values, [-1234, 250], [-5120, 123]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x88E8, old_first, 2); w(t, 0x88E4, old_offset, 2)
        payload = first.to_bytes(2, 'big') + bytes.fromhex('021e') + offset.to_bytes(2, 'big') + bytes(2)
        receive(t, payload)
        expected_offset, ov, expected_first, fv = expected_decode(first, offset, old_first, old_offset)
        assert signed(r(t, 0x88E4, 2), 16) == expected_offset and r(t, 0x88E6) == ov
        assert signed(r(t, 0x88E8, 2), 16) == expected_first and r(t, 0x88EA) == fv
        conversion_cases += 1

    dependency_cases = 0
    for first, offset_status in itertools.product([0, 512, 537, 65535], [0, 1, 2, 3, 255]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x8F2C, first, 2); w(t, 0x88E6, offset_status)
        w(t, 0x88E4, 50, 2); w(t, 0x88E8, 123, 2)
        t.run(0x17854)
        valid = first != 65535 and offset_status == 2
        assert signed(r(t, 0x88E8, 2), 16) == (clamp((first-512)*10-50) if valid else 123)
        assert r(t, 0x88EA) == (2 if valid else 1 if first == 65535 or offset_status == 1 else 3)
        dependency_cases += 1

    policy_cases = 0
    for summary, validity, value in itertools.product(range(256), range(4), [-32768, -1001, 250, 10000]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0xA98C, summary); w(t, 0x88EA, validity); w(t, 0x88E8, value, 2)
        w(t, 0x80B4, -1200, 2)
        t.run(0x516E6)
        if validity == 2 and summary & 1:
            expected, status = value, 1
        elif summary & 4:
            expected, status = 9240, 4
        elif summary & 2:
            expected, status = 9240, 3
        else:
            expected, status = -1200, 2
        assert signed(r(t, 0x80B4, 2), 16) == clamp(expected, -1000, 9240)
        assert r(t, 0xA538) == status
        policy_cases += 1

    assert TCU[0x5FCC0:0x5FCC4].hex() == '1f202500'
    contributors = [g for g in range(0x49) if TCU[0x5EB86+16*g] in [0x1F, 0x20, 0x25]]
    assert contributors == [0x35, 0x36, 0x3B]
    mapping_cases = 0
    for group, state in itertools.product(range(0x49), [2, 4, 16]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0xA6EC+group, state)
        w(t, 0x88E8, 250, 2); w(t, 0x88EA, 2)
        for fn in [0x570F6, 0x57258, 0x516E6]:
            t.run(fn)
        active = group in contributors and state in [2, 4]
        assert bool(r(t, 0xA98C) & 8) == active
        assert r(t, 0x80B4, 2) == (9240 if active else 250)
        assert r(t, 0xA538) == (3 if state == 2 else 4) if active else r(t, 0xA538) == 1
        mapping_cases += 1

    examples = []
    for delta, offset, elapsed, cut in itertools.product([0, 15, 25, 35], [-5, 0, 5], [0, 5, 10], range(2)):
        e, payload = sender(delta+offset, offset)
        t = ramp_fixture(elapsed=elapsed)
        receive(t, payload)
        w(t, 0xA98C, 1)
        t.run(0x516E6); t.run(0x216D8)
        assert r(t, 0x92E4, 2) == delta*32
        t.run(0x2C234); t.run(0x1FB8C)
        source = r(t, 0x915A, 2)
        reduction = 320*(10-elapsed)//10
        assert source == (max(delta*32-reduction, 0) if elapsed < 10 else 32767)
        row = paired(source, 16, 1, 1, cut, t=t, e=e, model_offset=offset)
        examples.append({'primary71ec': delta+offset, 'offset71c4': offset,
                         'can215': payload.hex(' '), 'timer8170': elapsed,
                         'tcu_base92e4': delta*32, **row})

    lifecycle = []
    t = ramp_fixture()
    for primary, invalid, summary in [(25, 0, 1), (35, 0, 1), (0, 1, 1),
                                      (0, 1, 0), (0, 1, 4), (25, 0, 1)]:
        e, payload = sender(primary, 0, invalid)
        receive(t, payload); w(t, 0xA98C, summary)
        t.run(0x516E6); t.run(0x216D8); t.run(0x2C234); t.run(0x1FB8C)
        row = paired(r(t, 0x915A, 2), 16, 1, 1, 0, t=t, e=e)
        lifecycle.append({'primary': primary, 'invalid': invalid, 'summary_a98c': summary,
                          'can215': payload.hex(' '), 'validity88ea': r(t, 0x88EA),
                          'base80b4': r(t, 0x80B4, 2), 'status_a538': r(t, 0xA538), **row})
    assert [x['base80b4'] for x in lifecycle] == [250, 350, 350, 350, 9240, 250]
    assert [x['status_a538'] for x in lifecycle] == [1, 1, 2, 2, 4, 1]
    print(json.dumps({'scope': __doc__.strip(),
                      'rom_sha256': {'ECU': hashlib.sha256(ECU).hexdigest(), 'TCU': hashlib.sha256(TCU).hexdigest()},
                      'encoder_cases': encoder_cases, 'complete_callback_conversion_cases': conversion_cases,
                      'dependency_cases': dependency_cases, 'summary_policy_cases': policy_cases,
                      'diagnostic_group_cases': mapping_cases, 'contributing_groups': [hex(g) for g in contributors],
                      'feedback_cases': len(examples), 'feedback_matrix': examples,
                      'invalid_hold_substitute_recover': lifecycle,
                      'limits': 'ECU215 source/model coefficients and TCU active phase3 are fixtures. A98C is injected, not produced by timed diagnostics. CAN payload buffers are transferred explicitly; no ISR, real-time or physical-unit assertion.'}, indent=2))


if __name__ == '__main__':
    main()
