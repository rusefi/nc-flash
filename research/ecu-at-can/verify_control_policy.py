"""Execute ECU feedback override and original missing-feedback admission.

Stock ROM, independent numeric/state oracles, synthetic serial peer and local
mode inputs. No physical timing, complete task scheduler or receiver firmware.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import random

from verify_control_reply import (
    ControlApplication, ECU, TCU, w, r, f, rf, protected, paired, publish,
    angle, selected, appcheck, payload, framed, number, q,
)
from verify_throttle_candidate import checksum
from verify_traction_flags import protected_byte


class ControlPolicy(ControlApplication):
    """Only add SHLL16, already modeled by SHIntegerArithmetic for TCU work."""
    def instruction(self, pc):
        op = self.read(pc, 2)
        if op & 0xF0FF == 0x4028:
            n = (op >> 8) & 15
            self.r[n] = (self.r[n] << 16) & 0xFFFFFFFF
            self.visited.add(pc)
            return pc + 2, False
        return super().instruction(pc)


def setup():
    e = ControlPolicy()
    for a, v in [(0x2114, 10.5), (0x211C, 11), (0x2124, 100), (0x212C, 12),
                 (0x5520, 15), (0x5534, 10)]:
        protected(e, a, v)
    w(e, 0x55EC, 0x9001, 2)
    protected_byte(e, 0x20A8, 0)
    return e


def override(e, closed_valid=True):
    closed = rf(e, 0x2114) if closed_valid else number(0xBADD8)
    feedback, candidate = rf(e, 0x5534), rf(e, 0x569C)
    enabled, previous = r(e, 0x566E), r(e, 0x552C)
    latch, high_count, low_count = r(e, 0x552D), r(e, 0x5528, 2), r(e, 0x552A, 2)
    high = q(closed + number(0xBB188))
    low = q(high - number(0xBB18C))
    latch = 1 if feedback >= high else 0 if feedback < low else latch
    if enabled != 1:
        output = high_count = low_count = 0
    elif previous == 0:
        initial = q(closed + number(0xBB17C))
        output = initial if feedback >= initial else min(low, q(candidate + closed))
    else:
        output = rf(e, 0x5520)
        if latch == 1:
            if high_count >= int.from_bytes(ECU[0xBB178:0xBB17A], 'big'):
                output = q(output - number(0xBB184))
                high_count = 0
            high_count = min(65535, high_count + 1)
            low_count = 0
        else:
            if low_count >= int.from_bytes(ECU[0xBB17A:0xBB17C], 'big'):
                output = q(output - number(0xBB190))
                low_count = 0
            low_count = min(65535, low_count + 1)
            high_count = 0
        output = max(number(0xBB180), output)
    stack = e.r[15]
    e.run(0x21D18)
    assert e.r[15] == stack
    actual = (rf(e, 0x5520), r(e, 0x5528, 2), r(e, 0x552A, 2), r(e, 0x552C), r(e, 0x552D))
    want = (output, high_count, low_count, enabled, latch)
    assert actual == want, (actual, want, feedback, candidate)
    checksum(e, 0x5520)
    return dict(output=float(output), high_count=high_count, low_count=low_count,
                previous=enabled, threshold=latch)


def gated_monitor(e):
    # For B4, ROM E1E00 is 00800000; AC2B0 is 8000. Thus only the
    # inverse mode-match result from 9A43A contributes to 9A244 admission.
    mode_mask = int.from_bytes(ECU[0xAC148 + 0xB4*2:0xAC14A + 0xB4*2], 'big')
    assert ECU[0xE1B30 + 0xB4*4:0xE1B34 + 0xB4*4] == bytes.fromhex('00800000')
    fault = r(e, 0x20A8)
    effective_fault = fault if r(e, 0x20A9) == fault ^ 255 else 0
    gate = int(bool(r(e, 0x99D8, 2) & mode_mask) and r(e, 0x567A) == 1 and not effective_fault)
    reset, good = r(e, 0x9462), r(e, 0x5578)
    bad_count, good_count, recovery = r(e, 0x57D2, 2), r(e, 0x57D0, 2), r(e, 0x57CD)
    if reset == 1:
        bad_count = good_count = fault = recovery = missing = 0
    else:
        missing = int(not good)
        if not gate:
            bad_count = good_count = 0
        elif good:
            if good_count >= int.from_bytes(ECU[0xE1006:0xE1008], 'big'):
                recovery = 1
            good_count = min(65535, good_count + 1)
            bad_count = 0
        else:
            if bad_count >= int.from_bytes(ECU[0xE1004:0xE1006], 'big'):
                fault = 1
            bad_count = min(65535, bad_count + 1)
            good_count = 0
    stack = e.r[15]
    e.run(0x285A4, limit=50000)
    assert e.r[15] == stack
    actual = tuple(r(e, a, size) for a, size in [(0x57CC, 1), (0x57D2, 2), (0x57D0, 2), (0x20A8, 1), (0x57CD, 1), (0x57CE, 1)])
    assert actual == (gate, bad_count, good_count, fault, recovery, missing), actual
    return dict(gate=gate, bad_count=bad_count, good_count=good_count, fault=fault, recovery=recovery)


def main():
    shift_cases = 0
    rng = random.Random(0x21D18)
    for n, value, sr in itertools.product(range(16), [0, 1, 0x8000, 0xFFFF, 0x80000000, 0xFFFFFFFF, rng.getrandbits(32)], [0, 0xF1]):
        e = ControlPolicy(); pc = 0xFFFFB000
        e.write(pc, 0x4028 | n << 8, 2)
        e.r[n] = value; e.sr = sr
        assert e.instruction(pc) == (pc+2, False)
        assert e.r[n] == (value % 65536) * 65536 and e.sr == sr
        shift_cases += 1
    direct = 0
    # Stock threshold equality, both sides, non-Boolean enables/history,
    # timing boundaries, floor and sign-extended counter edge cases.
    for mode, previous, feedback, candidate, count in itertools.product(
            [0, 1, 2], [0, 1, 2], [0, Fraction(10999, 1000), 11, Fraction(11001, 1000), 20],
            [-1, 0, 30], [0, 1, 2, 3, 32768, 65535]):
        e = setup(); w(e, 0x566E, mode); w(e, 0x552C, previous)
        w(e, 0x552D, direct % 3); w(e, 0x5528, count, 2); w(e, 0x552A, count, 2)
        f(e, 0x5534, q(feedback)); f(e, 0x569C, candidate)
        protected(e, 0x5520, [4, 5, 15][direct % 3])
        override(e); direct += 1
    defaults = 0
    for closed, corrupt, mode in itertools.product([0, 10.5, 20], [False, True], [0, 1, 2]):
        e = setup(); protected(e, 0x2114, closed)
        if corrupt:
            w(e, 0x2118, 0, 2); w(e, 0x211A, 0, 2)
        w(e, 0x566E, mode); f(e, 0x569C, 2)
        override(e, not corrupt); defaults += 1
    admission = 0
    for mode, enable, fault, corrupt, reset, good in itertools.product(
            [0, 1, 0x7FFF, 0x8000, 0x8001, 0xFFFF], [0, 1, 2], [0, 1, 2], [False, True], [0, 1, 2], [0, 1, 2]):
        e = setup(); w(e, 0x99D8, mode, 2); w(e, 0x567A, enable)
        protected_byte(e, 0x20A8, fault)
        if corrupt: w(e, 0x20A9, fault)
        w(e, 0x9462, reset); w(e, 0x5578, good)
        w(e, 0x57D2, [0, 24, 25, 65535][admission % 4], 2)
        w(e, 0x57D0, [0, 249, 250, 65535][admission % 4], 2)
        w(e, 0x57CD, 2)
        gated_monitor(e); admission += 1
    # Original TCU packers -> ECU models; replies are received by actual byte
    # service, decoded by 22224, then used for next-cycle command selection.
    e = setup(); w(e, 0x99D8, 0x8000, 2); w(e, 0x567A, 1)
    for a, v in [(0x6DC4, 100), (0x6D40, 20), (0x71D8, 3), (0x71D0, 4),
                 (0x71C4, 32), (0x7154, Fraction(1, 2)), (0x6DB4, 2000),
                 (0x7E0C, 40), (0x72F8, 50)]:
        f(e, a, v)
    appcheck(e, payload(), 2)
    history = []
    previous_command = rf(e, 0x56A0)
    for i, (mode, active, valid) in enumerate([(0, 0, True), (1, 1, True), (1, 1, False),
             (1, 1, False), (1, 1, True), (0, 0, True), (1, 0, True), (2, 1, True)]):
        p = bytearray(payload(seed=300+i, complement=valid)); p[4:6] = (400).to_bytes(2, 'big')
        base = len(e.tx); out = bytes(r(e, 0x437A+j) for j in range(38))
        e.run(0xE86E)
        for v in framed(p): e.rdr = v; e.run(0xE86E)
        assert bytes(e.tx[base:]) == framed(out)
        result = appcheck(e, p, r(e, 0x43A7), inject=False)
        quantized = max(0, min(65535, int(q(q(previous_command / number(0x22750)) + Fraction(1, 2)))))
        assert r(e, 0x437E, 2) == quantized
        # Full upstream ECU caller and actual TCU packers remain in the path.
        _, e = paired(3200, 1600, 10040, 10060, active, e=e); w(e, 0x718C, active)
        e.run(0xA477E, limit=100000); publish(e); angle(e)
        w(e, 0x566E, mode)
        result.update(override(e)); selected(e); previous_command = rf(e, 0x56A0)
        result.update(mode=mode, active=active, next_command=float(previous_command), monitor=gated_monitor(e))
        history.append(result)
    # Full gate+monitor after real rejected replies, without forcing 57CC.
    loss = []
    w(e, 0x57D2, 0, 2)
    for i in range(30):
        p = payload(complement=i >= 27, seed=500+i)
        e.run(0xE86E)
        for v in framed(p): e.rdr = v; e.run(0xE86E)
        appcheck(e, p, r(e, 0x43A7), inject=False)
        row = gated_monitor(e); row['call'] = i+1
        assert row['fault'] == int(i >= 25)
        assert row['gate'] == int(i < 26)
        if i >= 26: assert row['bad_count'] == row['good_count'] == 0
        loss.append(row)
    # Verified reset entry allows admission next call; good feedback's
    # recovery marker takes 251 enabled monitor calls from zero.
    e.run(0x28552); assert r(e, 0x20A8, 2) == 0x00FF
    recovery = []
    for i in range(251):
        row = gated_monitor(e)
        assert row['gate'] == 1 and row['fault'] == 0
        assert row['recovery'] == int(i >= 250)
        if i in [0, 248, 249, 250]: recovery.append(dict(call=i+1, **row))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
          shift_cases=shift_cases, override_cases=direct, default_cases=defaults, admission_cases=admission,
          paired_history=history, fault_lifecycle=loss, reset_recovery=recovery,
          limits='Explicit local 566E/567A/99D8 inputs and call order; synthetic peer. Full task, gate producers, recovery consumers, physical effects and time units remain open.'), indent=2))


if __name__ == '__main__':
    main()
