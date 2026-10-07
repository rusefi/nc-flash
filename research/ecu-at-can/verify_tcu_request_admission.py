"""Original upstream creation, captured axes, gate hysteresis and cancellation.

Application source words/fault flags are explicit inputs. No physical signal
names, interrupt timebase, or complete boot/task execution are inferred.
"""
import itertools
import json
import random

from sh_relative_branch import SHRelativeBranch
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_dispatch import fixture, ObservedTCU, curve
from verify_spark_interaction import paired

SOURCES = [(0x92C6, 2), (0x92C6, 5), (0x92CA, 0), (0x92CA, 1),
           (0x92CC, 1), (0x92CC, 2), (0x92CD, 3), (0x92CD, 4), (0x92D0, 2)]
CALLBACKS = [0x30B28, 0x239B2, 0x30A88, 0x310F8,
             0x312E8, 0x23BF6, 0x30710, 0x30C54]


def gate_model(old, override, difference, measured_a, measured_b, speed, second_axis, selector, axis):
    if override & 1:
        result = old | 5
        if signed(difference, 16) >= 1920:
            return result | 2
        if signed(difference, 16) < 1600:
            return result & ~2
        return result
    result = old
    first_axis = min((signed(speed, 16)*4) & 0xFFFFFFFF, 65535)
    lower = curve(0x700C8, first_axis) >> 1
    if measured_b < lower:
        result &= ~4
    elif measured_b >= (lower+512) & 65535:
        result |= 4
    lower = curve(0x700C8, second_axis) >> 1
    broad = curve(0x700D3, second_axis) >> 1
    if measured_b < broad and measured_a < lower:
        result &= ~1
    elif measured_a >= (lower+512) & 65535:
        result |= 1
    bank = min(selector, 4)
    lower = curve(0x700DE+11*bank, axis) >> 1
    gap = int.from_bytes(TCU[0x70116+2*bank:0x70118+2*bank], 'big')
    if measured_b < lower:
        result &= ~2
    elif measured_b >= (lower+gap) & 65535:
        result |= 2
    return result


def cancelled(t):
    return any(not bool(r(t, a) & (1 << bit)) if a == 0x92D0
               else bool(r(t, a) & (1 << bit)) for a, bit in SOURCES)


class CreationTCU(ObservedTCU):
    def __init__(self):
        super().__init__()
        self.creation_callbacks = []

    def instruction(self, pc):
        if pc == 0x31A14:
            self.creation_callbacks.append(self.r[3])
        return super().instruction(pc)


def upstream(code=7, operation=0x17, head=0, t=None):
    if t is None:
        t = CreationTCU()
        t.ram = dict(fixture().ram)
    else:
        fixture(t)
    t.run(0x31524, 0)
    assert r(t, 0x8088) == 1 and r(t, 0x96C5) == 0
    w(t, 0x96C4, head)
    # Healthy input for the aggregate's inverted contributor, not a produced flag.
    w(t, 0x92D0, 4); w(t, 0xA93A, 1)
    for addr, value in [(0x80EA, 73*64), (0x80F6, (58*256-0x1900)//2),
                        (0x809C, 20000), (0x80EE, 1000)]:
        w(t, addr, value, 2)
    p = 0xFFFFA900
    for i, value in enumerate([code, operation, 0]):
        t.write(p+2*i, value, 2)
    t.r[5] = p
    t.run(0x31524, 1, limit=1000000)
    assert t.creation_callbacks == CALLBACKS
    assert r(t, 0x8088) == 2 and r(t, 0x8089) == code and r(t, 0x808A) == operation
    assert r(t, 0x96C4) == head and r(t, 0x96C5) == 1
    phase = 0x95D4+15*head
    assert [r(t, phase+i) for i in range(10, 15)] == [code, operation, 0, 0, 0]
    record = r(t, 0xA2BC, 4) & 65535
    assert record == 0x9F40 and r(t, 0xA2BA) == 1 and r(t, record) == 2
    assert r(t, record+14, 2) == r(t, 0x80C2, 2) == 73*128
    assert r(t, record+16, 2) == r(t, 0x80C4, 2) == 73*256
    assert r(t, 0xA1AC) == 0 and r(t, 0x9410) & 2
    return t, record, phase


def periodic(t):
    # Two admitted event4 calls always include exactly one group5 service.
    for _ in range(2):
        t.r[5] = 0
        t.run(0x31524, 4, limit=300000)
    t.run(0x4C7AC); t.run(0x1FB8C)


def paired_snapshot(t):
    # The older paired helper deliberately sets92C6 bit5 for CAN216 byte4.
    # That bit is a cancellation contributor once1FD24 runs. Keep its CAN
    # fixture changes out of the ongoing original request lifecycle.
    snapshot = SHRelativeBranch(TCU)
    snapshot.ram = dict(t.ram)
    return paired(r(t, 0x915A, 2), 10016, True, True, 0, t=snapshot)


def main():
    assert TCU[0x76E26] == 0  # Alternate reference-based calibration branch untested.
    t = SHRelativeBranch(TCU)
    rng = random.Random(0x9410916F)
    gate_cases = 0
    for old, bank, override in itertools.product([0, 1, 2, 4, 7, 0xF8, 0xFF], [0, 1, 2, 3, 4, 5, 255], [0, 1]):
        axis = rng.randrange(65536)
        low = curve(0x700DE+11*min(bank, 4), axis) >> 1
        gap = int.from_bytes(TCU[0x70116+2*min(bank, 4):0x70118+2*min(bank, 4)], 'big')
        for b, diff in itertools.product(sorted({0, 65535, max(0, low-1), low, low+gap-1, low+gap}),
                                         [1599, 1600, 1919, 1920, 65535]):
            a, speed, second = [rng.randrange(65536) for _ in range(3)]
            for addr, val, size in [(0x9410, old, 1), (0x916D, override, 1), (0x80F6, diff, 2),
                                    (0x809A, a, 2), (0x809C, b, 2), (0x80EE, speed, 2),
                                    (0x80C8, second, 2), (0x8081, bank, 1), (0x80C4, axis, 2)]:
                w(t, addr, val, size)
            expected = gate_model(old, override, diff, a, b, speed, second, bank, axis)
            t.run(0x23BF6)
            assert r(t, 0x9410) == expected, (old, bank, override, b, diff, expected, r(t, 0x9410))
            gate_cases += 1

    capture_cases = 0
    bounds = [0, 1, 16383, 16384, 20479, 20480, 32767, 32768, 32769, 49151, 49152, 65535]
    for a, b in itertools.product(bounds, repeat=2):
        w(t, 0x80EA, a, 2); w(t, 0x80EE, b, 2)
        w(t, 0x809A, 12345, 2); w(t, 0x809C, 54321, 2)
        t.run(0x312E8, 7)
        for value, raw, scaled in [(a, 0x80C2, 0x80C4), (b, 0x80C6, 0x80C8)]:
            expected = min((value*2) & 65535, 40960)
            assert r(t, raw, 2) == expected
            assert r(t, scaled, 2) == min(2*expected, 65535)
        assert r(t, 0x80CC, 2) == 12345 and r(t, 0x80CE, 2) == 54321
        capture_cases += 1

    aggregation_cases = 0
    t = SHRelativeBranch(TCU)
    for bitmap, prior in itertools.product(range(512), [0, 255]):
        for addr in range(0x92C4, 0x92D7):
            w(t, addr, 0)
        w(t, 0x92D0, 4); w(t, 0xA93A, 1); w(t, 0x916F, prior)
        for i, (addr, bit) in enumerate(SOURCES):
            if bitmap & (1 << i):
                w(t, addr, r(t, addr) ^ (1 << bit))
        t.run(0x1FD24)
        assert bool(r(t, 0x916F) & 1) == bool(bitmap)
        aggregation_cases += 1
    # Independently perturb every bit in the source interval, including noncontributors.
    perturbation_cases = 0
    for addr, bit in itertools.product(range(0x92C4, 0x92D7), range(8)):
        for source in range(0x92C4, 0x92D7):
            w(t, source, 0)
        w(t, 0x92D0, 4); w(t, addr, r(t, addr) ^ (1 << bit))
        t.run(0x1FD24)
        assert bool(r(t, 0x916F) & 1) == ((addr, bit) in SOURCES)
        perturbation_cases += 1
    for _ in range(256):
        for addr in range(0x92C4, 0x92D7):
            w(t, addr, rng.randrange(256))
        expected = cancelled(t)
        t.run(0x1FD24)
        assert bool(r(t, 0x916F) & 1) == expected
        aggregation_cases += 1

    creation_cases = 0
    for code, op, head in itertools.product([6, 7], [0, 0x17], [0, 15]):
        upstream(code, op, head)
        creation_cases += 1

    paths = []
    for source_addr, bit in SOURCES:
        t, record, phase = upstream()
        # Original event2 phase advancement, with the same explicit source words.
        for _ in range(2):
            t.r[5] = 0; t.run(0x31524, 2, limit=300000)
            t.r[5] = 0; t.run(0x31524, 4, limit=300000)
        assert r(t, phase+13) == 1 and r(t, record) == 3
        assert r(t, record+4, 2) == 576
        # Hold the state3 advance predicate false while exercising gate hysteresis.
        w(t, 0x9218+4*TCU[0x5D446+7], 5000, 4)
        # Selector0/axis73 produces lower4224, upper4992 in stock curve bank0.
        assert curve(0x700DE, 73*256) >> 1 == 4224
        timeline = []
        for measured, enabled in [(4223, False), (4991, False), (4992, True), (4224, True)]:
            w(t, 0x809C, measured, 2)
            t.run(0x1FD24); t.run(0x23BF6)
            assert not r(t, 0x916F) & 1
            assert bool(r(t, 0x9410) & 2) == enabled
            periodic(t)
            assert r(t, record) == 3 and r(t, 0xA2BA) == 1
            assert r(t, record+4, 2) == (576 if enabled else 0)
            timeline.append({'measured_809c': measured, 'enabled': enabled,
                             'state': 3, 'reduction': r(t, record+4, 2),
                             'paired': paired_snapshot(t)})
        w(t, source_addr, r(t, source_addr) ^ (1 << bit))
        t.run(0x1FD24)
        assert r(t, 0x916F) & 1
        periodic(t)
        assert r(t, 0xA2BA) == r(t, 0xA202, 2) == r(t, 0xA1AC) == 0
        assert r(t, 0x9F3C, 4) == 0x007FFFFF and r(t, record, 20) == 0
        timeline.append({'cancelled': True, 'paired': paired_snapshot(t)})
        w(t, source_addr, r(t, source_addr) ^ (1 << bit))
        t.run(0x1FD24); periodic(t)
        assert not r(t, 0x916F) & 1 and r(t, 0xA2BA) == 0
        timeline.append({'source_recovered': True, 'request_recreated': False})
        paths.append({'source': f'{source_addr:04X}', 'bit': bit, 'timeline': timeline})

    rejected = []
    for entry in [0x1E5F6, 0x126EC, 0x1220A]:
        t, _, _ = upstream()
        w(t, 0x8007, 3); w(t, 0x84F5, 2)
        try:
            t.run(entry, limit=1000000)
        except ValueError as error:
            assert str(error) == 'Unmapped read FFFFF810' and t.pc == 0x1412A
            rejected.append({'entry': f'{entry:X}', 'stop_pc': f'{t.pc:X}', 'reason': str(error)})
        else:
            raise AssertionError('Full-task probe unexpectedly completed')

    print(json.dumps({'status': 'passed', 'gate_cases': gate_cases,
                      'capture_cases': capture_cases, 'aggregation_cases': aggregation_cases,
                      'source_bit_perturbations': perturbation_cases,
                      'upstream_creation_cases': creation_cases,
                      'gate_and_cancel_lifecycles': paths, 'full_task_rejections': rejected,
                      'limits': 'Explicit application inputs and call order; no physical units, full boot, ISR or remote controller proof.'}, indent=2))


if __name__ == '__main__':
    main()
