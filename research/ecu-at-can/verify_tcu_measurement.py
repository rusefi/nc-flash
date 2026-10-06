"""Original TCU capture history -> measurement/derivative/error -> CAN216 ECU.

Capture timestamps, elapsed-age samples and call order are synthetic. No sensor
hardware, physical units, real task timing or OEM roof receiver is modeled.
All firmware helpers execute their original instructions without stubs.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import SH, signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_phase_retirement import full_fixture, RetirementTCU, GROUPS
from verify_tcu_request_admission import periodic, paired_snapshot

ECU = (Path(__file__).resolve().parents[2] / 'examples/LFFEEE-stock.bin').read_bytes()
RESET = 18 << 12


def div(a, b):
    if not b:
        return 0 if not a else 0x7FFFFFFF if a > 0 else -0x80000000
    return signed((abs(a)//abs(b)) * (-1 if (a < 0) != (b < 0) else 1), 32)


def clamp(a, low=-0x80000000, high=0x7FFFFFFF):
    return min(high, max(low, a))


def model(history, head, angle=360):
    count = clamp(div(signed(angle, 16)*24, 360), -32768, 32767)
    total = signed(sum(history[(head-i) % 24] for i in range(max(0, count))), 32)
    period = div(clamp(total*24), count)
    return clamp(div(153600000, period), 0, 32767), period


def seed(t, history, head=0, age=0, prior=0):
    for i, value in enumerate(history):
        w(t, 0x9248+4*i, value, 4)
    for address, value in [(0x800D, head), (0x810C, age), (0x9244, prior)]:
        w(t, address, value)


def history(t):
    return [signed(r(t, 0x9248+4*i, 4), 32) for i in range(24)]


def wire(t, fault=False):
    # Use a clone: packet construction must not mutate the ongoing fixture.
    c = SHRotate(TCU)
    c.ram = dict(t.ram)
    w(c, 0x92C6, 0x20 if fault else 0)
    c.run(0x18F8C, 1)
    expected = 255 if fault else min(254, r(t, 0x80EE, 2)//96)
    assert r(c, 0x8F01) == expected
    e = SH(ECU)
    for i in range(8):
        w(e, 0x6A40+i, r(c, 0x8EFD+i))
    e.run(0x35034)
    assert r(e, 0x6A58) == expected
    return expected


def main():
    assert hashlib.sha256(TCU).hexdigest() == '8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    assert hashlib.sha256(ECU).hexdigest() == '7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08'
    assert TCU[0x76DE0] == 18 and TCU[0x77448] == 24
    assert int.from_bytes(TCU[0x76DE2:0x76DE4], 'big') == 360
    t = SHRotate(TCU)
    arithmetic = 0
    for a, b, shift in itertools.product(
            [-2147483648, -89478486, -1, 0, 1, 89478485, 2147483647],
            [-24, -1, 0, 1, 24], [0, 1, 8, 16, 31]):
        t.r[5], t.r[6] = b, shift
        actual = signed(t.run(0x10C4C, a, limit=100000), 32)
        # Python integers give an independent exact truncation oracle here.
        exact = abs(a*b)//(1 << shift) * (-1 if a*b < 0 else 1)
        assert actual == clamp(exact), (a, b, shift, actual, clamp(exact))
        arithmetic += 1
    division = 0
    for a, b in itertools.product([-2147483648, -153600000, -1, 0, 1, 153600000, 2147483647],
                                   [-2147483648, -24, -1, 0, 1, 24, 2147483647]):
        t.r[5] = b
        assert signed(t.run(0x10DA4, a), 32) == div(a, b)
        division += 1

    initialization = 0
    for sr in [0, 1, 0xF0, 0xF1, 0x300]:
        t.sr = sr
        seed(t, list(range(24)), 23, 5, 6)
        t.run(0x211C4)
        assert history(t) == [RESET]*24 and r(t, 0x800D) == 0
        assert r(t, 0x810C) == r(t, 0x9244) == 255 and r(t, 0x9238, 4) == 0x7FFFFFFF
        assert t.sr & ~1 == sr & ~1
        initialization += 1

    ingestion = 0
    for age, capture, head, counter in itertools.product(
            [0, 17, 18, 129, 130, 255],
            [-2147483648, -1, 0, 1, RESET-1, RESET, RESET+1, 0x7FFFF, 0x80000, 0x7FFFFFFF],
            [0, 22, 23], [0, 254, 255]):
        original = list(range(24))
        seed(t, original, head, age, 33)
        w(t, 0x800C, counter)
        w(t, 0x8908, capture, 4)
        t.run(0x211DC)
        value = min(RESET, 0x7FFFF if age >= 130 or capture > 0x7FFFF else capture)
        expected = list(original)
        new_head = (head+1) % 24
        expected[new_head] = value
        assert history(t) == expected and r(t, 0x800D) == new_head
        assert r(t, 0x9244) == age and r(t, 0x810C) == 0
        assert r(t, 0x800C) == min(255, counter+1)
        ingestion += 1

    timestamps = 0
    for previous, delta, age, counter in itertools.product(
            [0, 1, 0xFFFFFFF0], [0, 1, 9, 10, 300000, RESET*10, RESET*10+10, 0xFFFFFFFF],
            [0, 129, 130, 255], [0, 65534, 65535]):
        seed(t, [RESET]*24, 23, age)
        current = (previous+delta) & 0xFFFFFFFF
        w(t, 0x890C, previous, 4)
        w(t, 0x88F0, 999, 2)
        for address in [0x8900, 0x8902, 0x8904]:
            w(t, address, counter, 2)
        t.run(0x17A58, current)
        capture = delta//10
        expected = RESET if age >= 130 else min(RESET, capture)
        assert r(t, 0x890C, 4) == current and r(t, 0x8908, 4) == capture
        assert r(t, 0x9248, 4) == expected and r(t, 0x800D) == 0
        assert r(t, 0x88F0, 2) == 0
        assert all(r(t, a, 2) == min(65535, counter+1) for a in [0x8900, 0x8902, 0x8904])
        timestamps += 1

    freshness = 0
    for age, prior in itertools.product(range(256), [0, 17, 18, 127, 128, 255]):
        seed(t, [30000]*24, 23, age, prior)
        w(t, 0x800C, 177)
        t.macl = 0x12345678
        value = t.run(0x212F4, 360, limit=100000)
        if age >= 18 or prior >= 18:
            assert value == 0 and r(t, 0x9238, 4) == 0x7FFFFFFF
            assert history(t) == [RESET]*24 and r(t, 0x800D) == r(t, 0x800C) == 0
        else:
            assert value == 213 and r(t, 0x9238, 4) == 720000
            assert history(t) == [30000]*24 and r(t, 0x800D) == 23 and r(t, 0x800C) == 177
        assert t.macl == 0x12345678 and r(t, 0x810C) == age and r(t, 0x9244) == prior
        freshness += 1

    rng = random.Random(0x212F4)
    histories = [[v]*24 for v in [0, 1, 195, 196, 30000, RESET, -1, 0x7FFFFFFF, -0x80000000]]
    histories += [[1000+i*113 for i in range(24)]]
    histories += [[rng.randrange(-0x80000000, 0x80000000) for _ in range(24)] for _ in range(12)]
    calculations = 0
    for entries, head, angle in itertools.product(histories, [0, 1, 23], [-360, 0, 1, 14, 15, 30, 180, 359, 360, 375, 720]):
        seed(t, entries, head)
        expected, period = model(entries, head, angle)
        actual = t.run(0x212F4, angle, limit=100000)
        assert actual == expected and signed(r(t, 0x9238, 4), 32) == period, (head, angle, actual, expected, period)
        assert history(t) == entries and r(t, 0x800D) == head
        calculations += 1

    substitution = 0
    for fault, alternate, selected, kind, reference in itertools.product(
            [0, 0x10], [0, 1], range(7), [0, 255], [-65537, -32769, -1, 0, 32767, 32768, 2147483647]):
        seed(t, [30000]*24)
        for a, v in [(0x92C6, fault), (0xAC86, alternate), (0x8081, selected), (0x8080, kind)]:
            w(t, a, v)
        for i in range(7):
            w(t, 0x9218+4*i, reference if i == (6 if kind == 255 else selected) else 123, 4)
        t.run(0x2124C, limit=100000)
        expected = min(32767, reference) & 65535 if fault or alternate else 213
        assert r(t, 0x9234, 2) == expected
        assert r(t, 0x80EE, 2) == r(t, 0x9236, 2) == 213
        substitution += 1

    derivatives = 0
    for values in itertools.product([-32768, -1, 0, 1, 32767], repeat=4):
        current, a, b, c = values
        for addr, value in zip([0x9234, 0x923E, 0x9240, 0x9242], values):
            w(t, addr, value, 2)
        delta = (a-b-c+current)//4
        t.macl = 0x12345678
        t.run(0x2140C)
        assert r(t, 0x80F0, 2) == delta & 65535
        assert signed(r(t, 0x923C, 2), 16) == clamp(div(delta*6103, 256), -32768, 32767)
        assert [signed(r(t, addr, 2), 16) for addr in [0x923E, 0x9240, 0x9242]] == [current, a, b]
        assert t.macl == 0x12345678
        derivatives += 1

    # Stateful capture -> real producer -> original reference/error -> CAN216.
    # No direct writes to80EE,80D8 or9218 in this lifecycle.
    t = SHRotate(TCU)
    t.run(0x211C4)
    w(t, 0x80EC, 300, 2)
    t.run(0x2117C)
    t.run(0x30B20)
    t.run(0x30B28, 9)
    entries, head, saved_age = [RESET]*24, 0, 255
    rows = []
    for step in range(32):
        age = 255 if step == 0 else 18 if step == 27 else 0
        capture = None if step in [0, 27] else 30000
        if capture is not None:
            old_age = 255 if step == 1 else 18 if step == 28 else 0
            w(t, 0x810C, old_age)
            timestamp = (r(t, 0x890C, 4)+capture*10) & 0xFFFFFFFF
            t.run(0x17A58, timestamp)
            head = (head+1) % 24
            entries[head] = RESET if old_age >= 130 else capture
            saved_age = old_age
        else:
            w(t, 0x810C, age)
        old_error = signed(r(t, 0x95C0, 2), 16)
        t.run(0x2124C, limit=100000)
        if age >= 18 or saved_age >= 18:
            measured, period = 0, 0x7FFFFFFF
            entries, head = [RESET]*24, 0
        else:
            measured, period = model(entries, head)
        assert history(t) == entries and r(t, 0x800D) == head
        assert r(t, 0x80EE, 2) == measured and r(t, 0x9238, 4) == period
        t.run(0x30B9E)
        raw = clamp(measured-signed(r(t, 0x9228, 4), 32), -16319, 16319)
        assert signed(r(t, 0x95C0, 2), 16) == raw
        assert signed(r(t, 0x80D8, 2), 16) == (old_error+raw)//2
        rows.append({'step': step, 'captured': capture, 'current_age': r(t, 0x810C),
                     'previous_age': r(t, 0x9244), 'head': head, 'measurement': measured,
                     'period': period, 'filtered_error': signed(r(t, 0x80D8, 2), 16),
                     'can216_byte4': wire(t), 'can216_byte4_fault': wire(t, True)})
    shifts = []
    base = full_fixture()
    paired_shifts = 0
    for ring_head in [0, 15]:
        t = RetirementTCU()
        t.ram = dict(base.ram)
        t.run(0x211C4)
        # Fill the ring by original ingestion; two good capture ages qualify it.
        for _ in range(24):
            w(t, 0x810C, 0)
            timestamp = (r(t, 0x890C, 4)+10660) & 0xFFFFFFFF
            t.run(0x17A58, timestamp)
        t.run(0x2124C, limit=100000)
        assert r(t, 0x80EE, 2) == 6003
        w(t, 0x96C4, ring_head)
        w(t, 0x80EC, 7014, 2)
        t.run(0x2117C)
        w(t, 0x606F, 5)
        t.run(0x48BC0)
        for address, value in [(0x8080, 6), (0x8084, 4), (0x92D0, 4), (0xA93A, 1)]:
            w(t, address, value)
        for address, value in [(0x80EA, 4672), (0x80F6, 4224), (0x809C, 20000)]:
            w(t, address, value, 2)
        t.run(0x48C08, limit=1000000)
        record = r(t, 0xA2BC, 4) & 65535
        phase = 0x95D4+15*ring_head
        checkpoints, last = [], None
        for call in range(401):
            if call:
                t.run(0x11014)
                w(t, 0x810C, 0)  # Synthetic capture arrives between timer/service.
                interval = 10660 if call < 80 else 12800
                timestamp = (r(t, 0x890C, 4)+interval) & 0xFFFFFFFF
                t.run(0x17A58, timestamp)
                t.run(0x2124C, limit=100000)
                t.run(0x2117C)
                t.run(0x30B9E)
                t.run(0x31524, 2, limit=1000000)
                periodic(t)
            else:
                t.run(0x4C7AC)
                t.run(0x1FB8C)
            state = (r(t, phase+13), r(t, record), r(t, 0x96C5))
            if state != last or call in [79, 80, 102, 103, 104]:
                checkpoints.append({'call': call, 'phase': state[0], 'request': state[1],
                                    'active_count': state[2], 'measurement': r(t, 0x80EE, 2),
                                    'error': signed(r(t, 0x80D8, 2), 16),
                                    'measurement_can_byte4': wire(t), **paired_snapshot(t)})
                paired_shifts += 1
                last = state
            if not state[2]:
                break
        assert call < 400 and r(t, 0x8088) == 1 and r(t, 0xA2BA) == 0
        assert r(t, 0x915A, 2) == 0x7FFF and r(t, 0x80EE, 2) == 5000
        assert {group for index, group in t.acks if index == ring_head} == set(GROUPS)
        assert any(row['request'] == 4 for row in checkpoints)
        assert any(row['request'] == 5 for row in checkpoints)
        shifts.append({'ring_head': ring_head, 'retired_at': call, 'checkpoints': checkpoints})

    print(json.dumps({'scope': __doc__.strip(), 'tcu_sha256': hashlib.sha256(TCU).hexdigest(),
                      'ecu_sha256': hashlib.sha256(ECU).hexdigest(),
                      'multiply_shift_cases': arithmetic, 'guarded_division_cases': division,
                      'initialization_cases': initialization, 'capture_ingestion_cases': ingestion,
                      'timestamp_callback_cases': timestamps,
                      'freshness_cases': freshness, 'history_calculation_cases': calculations,
                      'substitution_cases': substitution, 'derivative_cases': derivatives,
                      'paired_measurement_can216_ecu_checks': len(rows)*2+paired_shifts,
                      'paired_request_can216_ecu_checks': paired_shifts,
                      'lifecycle': rows, 'capture_driven_shifts': shifts}, indent=2))


if __name__ == '__main__':
    main()
