"""Original TCU event queues -> request state machine -> CAN216/ECU spark.

Original allocation, creation, queue draining, callbacks and release execute.
Application measurements/phase records and timer samples are explicit inputs.
"""
import itertools
import json
import random

from sh_relative_branch import SHRelativeBranch
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_spark_interaction import paired
from verify_tcu_request_maps import interpolate, duration_address

WATCH = {0x4C3C0, 0x4C3CA, 0x2FBEE, 0x2FAA2, 0x4CB9C, 0x2FEF8,
         0x4CBA8, 0x4CC2A, 0x4CC5A, 0x4CC90, 0x4CCA4, 0x4CD18,
         0x4CDF2, 0x4CE5E, 0x4CE7A, 0x4CEC6, 0x4CEF2, 0x4CF08,
         0x4CF3A, 0x4CF6A, 0x4D010, 0x4D142, 0x4BFDA}


class ObservedTCU(SHRelativeBranch):
    def __init__(self):
        super().__init__(TCU)
        self.calls = []

    def instruction(self, pc):
        if pc in WATCH:
            self.calls.append(pc)
        return super().instruction(pc)


def fixture():
    t = ObservedTCU()
    for fn in [0x15D04, 0x1FB18, 0x4C69A, 0x4CA64, 0x4BEF8,
               0x4C0F8, 0x4C288, 0x4C3C0, 0x4CB9C]:
        t.run(fn)
    assert r(t, 0xB038, 4) == 0x5E418
    assert r(t, 0xB04C, 4) == 0xFFFFA34C
    assert r(t, 0xB050, 4) == 0x06010100
    assert r(t, 0xA2B8) == r(t, 0xA34C) == 1
    assert r(t, 0x9F3C, 4) == 0x007FFFFF
    w(t, 0x80B4, 250, 2); t.run(0x216D8)
    return t


def message(t, group, operation, pointer=0):
    t.r[5], t.r[6], t.r[7] = 0, (group << 16) | operation, pointer
    assert t.run(0x4C2A0, 0) == 0
    t.run(0x4C316, 0, limit=100000)
    assert r(t, 0xA1AC) == 0


def phase(t, code, value):
    # Existing application phase-record ring, separate from request ring.
    w(t, 0x96C4, 0); w(t, 0x96C5, 1)
    w(t, 0x95DE, code); w(t, 0x95E1, value)


def create(t, code=6, operation=0, event=42):
    w(t, 0x800B, 0); t.run(0x3138A, code)
    assert r(t, 0x808C) == 0
    map_x, map_y = (58, 73) if code == 7 else (63, 44)
    for a, value, size in [(0x80C2, 0, 2), (0x80C4, map_y*256, 2),
                           (0x80F6, (map_x*256-0x1900)//2, 2), (0x9410, 2, 1)]:
        w(t, a, value, size)
    phase(t, code, 1)
    w(t, 0x9218+4*TCU[0x5D446+code], 1000, 4)
    p = t.run(0x4C100)
    for i, value in enumerate([event, code, operation, 0]):
        t.write(p+i, value, 1)
    message(t, 5, 1, p)
    record = r(t, 0xA2BC, 4) & 65535
    assert record == 0x9F40  # Real 20-byte heap allocation in this fixture.
    assert r(t, record) == 2 and r(t, record+2) == 2
    assert r(t, 0xA2B8) == 2 and r(t, 0xA2BA) == 1
    assert r(t, 0xA202, 2) == 1
    assert {0x4C3CA, 0x2FBEE, 0x2FAA2, 0x4CBA8, 0x4CF6A} <= set(t.calls)
    return record


def service(t, measured, hold=0, decay=0):
    w(t, 0x80EE, measured, 2)
    w(t, 0x81F2, hold); w(t, 0x8115, decay)
    t.calls.clear()
    message(t, 5, 2)
    t.run(0x4C7AC); t.run(0x1FB8C)


def curve(a, x):
    n = TCU[a]
    return interpolate(x & 65535, [v*256 for v in TCU[a+1:a+1+n]],
                       [v*256 for v in TCU[a+1+n:a+1+2*n]])


def family(code, operation, special):
    f = {6: 1, 7: 2, 8: 3, 9: 4, 10: 7, 11: 3}.get(code, 0)
    if code == 7 and special:
        f = 5
    if operation == 0x18:
        f = 6
    elif operation == 0x17:
        f = 5
    return f


def thresholds(code, operation, special, axis, captured, ref, derivative):
    f = family(code, operation, special)
    factor = curve(0x76524+9*f, max(0, min(16383, signed(axis, 16)))*4) >> 8
    first = curve(0x76474+11*f, captured) >> 2
    second = curve(0x764CC+11*f, captured) >> 2
    return ref-first, ref-second, ref-signed(derivative, 16)*factor


def main():
    t = fixture()
    index_cases = 0
    for code, value in itertools.product(range(256), range(256)):
        bank = code % 5 if code < 10 else 5 if code == 10 else 6
        limits = TCU[0x70A20+5*bank:0x70A24+5*bank]
        w(t, 0x800B, value)
        t.run(0x3138A, code)
        assert r(t, 0x808C) == sum(value >= x for x in limits)
        index_cases += 1

    # Direct predicate tests isolate its independent arithmetic and phase gate.
    predicate_cases = 0
    rng = random.Random(216318)
    record = 0xA900
    for code, op, special, ph in itertools.product([0, 6, 7, 8, 9, 10, 11],
                                                   [0, 0x17, 0x18], [0, 1], [0, 1, 2, 127, 128, 255]):
        axis, captured = rng.randrange(65536), rng.randrange(65536)
        derivative = rng.choice([-256, 0, 10, 256]) & 65535
        ref = rng.choice([-1000, 1000, 5000])
        a, b, c = thresholds(code, op, special, axis, captured, ref, derivative)
        for measured in sorted({max(-32768, min(32767, x)) for x in [a-1, a, b-1, b, c-1, c]}):
            for off, value, size in [(1, code, 1), (8, op, 1), (14, captured, 2)]:
                w(t, record+off, value, size)
            phase(t, code, ph)
            for addr, value, size in [(0x80EA, axis, 2), (0x80EE, measured, 2),
                                      (0x80F0, derivative, 2), (0x95AE, special, 1),
                                      (0x9218+4*TCU[0x5D446+code], ref, 4)]:
                w(t, addr, value, size)
            t.r[5] = 0xFFFF0000+record
            expected = signed(ph, 8) >= 1 and (measured >= a or (measured >= b and measured >= c))
            assert t.run(0x4CD18) == int(expected), (code, op, axis, captured, measured, a, b, c)
            predicate_cases += 1

    hold_cases = 0
    for code, timer, threshold, speed in itertools.product([6, 7, 9, 10], [0, 2, 3, 255],
                                                          [0, 2, 3, 255], [-1, 0, 63, 64, 65, 32767]):
        w(t, record+1, code); w(t, 0x80D8, speed, 2)
        t.r[5], t.r[6] = threshold, 0xFFFF0000+record
        expected = timer >= threshold and (code != 9 or speed < 64)
        assert t.run(0x4D7CC, timer) == int(expected)
        hold_cases += 1

    threshold_table_cases = 0
    for code, op, flags, index in itertools.product(range(12), [0, 0x17, 0x18],
                                                   [0, 0x20, 0xFF], range(5)):
        for off, value in [(1, code), (8, op), (13, index), (18, flags)]:
            w(t, record+off, value)
        for fn, offset in [(0x4D350, 5), (0x4D3D8, 10)]:
            assert t.run(fn, 0xFFFF0000+record) == TCU[duration_address(code, op, flags)+offset+index]
            threshold_table_cases += 1

    lifecycle = []
    scenarios = [
        (6, 0, [(871, 0, 0, 2, 0), (872, 0, 0, 3, 1024),
                (872, 0, 0, 5, 1024), (872, 0, 24, 5, 522),
                (872, 0, 48, 5, 20), (872, 0, 49, None, None)]),
        (7, 0x17, [(487, 0, 0, 2, 0), (488, 0, 0, 3, 576),
                   (999, 0, 0, 3, 576), (1000, 0, 0, 4, 576),
                   (1000, 2, 0, 4, 576), (1000, 3, 0, 5, 576),
                   (1000, 3, 17, 5, 32), (1000, 3, 18, None, None)])]
    for code, op, steps in scenarios:
        t = fixture(); record = create(t, code, op)
        for measured, hold, decay, state, value in steps:
            service(t, measured, hold, decay)
            calls = list(t.calls)
            if state is None:
                assert r(t, 0xA202, 2) == r(t, 0xA2BA) == 0
                assert r(t, 0x9F3C, 4) == 0x007FFFFF
                assert bytes(r(t, record+i) for i in range(20)) == bytes(20)
                assert 0x4CF3A in calls and 0x4BFDA in calls and 0x4D142 not in calls
                source = 32767
            else:
                assert r(t, record) == state and r(t, record+4, 2) == value
                assert r(t, 0xA202, 2) == r(t, 0xA2BA) == 1
                source = max(800-value, 0) if value else 32767
                assert (0x4D010 if state in [3, 4] else 0x4D142 if state == 5 else 0x4CF6A) in calls
            assert r(t, 0x915A, 2) == source
            for cut in [0, 1]:
                lifecycle.append({'code': code, 'operation': op, 'measurement': measured,
                                  'hold_sample': hold, 'decay_sample': decay, 'record_state': state,
                                  'record_value': value, 'calls': [hex(x) for x in calls],
                                  **paired(source, 16, 1, 1, cut, t=t)})

    aborts = []
    for state in [2, 3, 4, 5]:
        for cause in ['guard916F', 'cancel_event']:
            t = fixture(); record = create(t, 7, 0x17)
            if state >= 3:
                service(t, 488)
            if state >= 4:
                service(t, 1000)
            if state >= 5:
                service(t, 1000, 3)
            assert r(t, record) == state
            t.calls.clear()
            if cause == 'guard916F':
                w(t, 0x916F, 1); message(t, 5, 2)
                assert 0x4CCA4 in t.calls
            else:
                p = t.run(0x4C100); t.write(p, 42, 1)
                message(t, 5, 3, p)
                assert 0x4CC2A in t.calls
            assert r(t, 0xA202, 2) == r(t, 0xA2BA) == 0
            assert r(t, 0x9F3C, 4) == 0x007FFFFF
            assert 0x4D010 not in t.calls and 0x4D142 not in t.calls
            t.run(0x4C7AC); t.run(0x1FB8C)
            assert r(t, 0x915A, 2) == 32767
            aborts.append({'from_state': state, 'cause': cause})

    print(json.dumps({'scope': __doc__, 'index_cases': index_cases,
                      'activation_predicate_cases': predicate_cases, 'hold_gate_cases': hold_cases,
                      'threshold_table_cases': threshold_table_cases,
                      'paired_lifecycle': lifecycle, 'aborts': aborts,
                      'limits': 'ROM event/request/heap lifecycle executes; measurements, application phase ring and timers are fixtures. Physical source units, task timing, producer of caller events and general concurrency remain open.'}, indent=2))


if __name__ == '__main__':
    main()
