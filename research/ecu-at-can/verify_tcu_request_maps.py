"""Execute stock TCU first-list map and ramp producers through CAN216/ECU.

Explicit callback records and timer samples; no physical policy entry,
real-time scheduler, or physical units are assumed.
"""
import itertools
import json
import random

from verify_tcu_slot2 import fixture, allocate, BANKS
from verify_can201_byte6 import TCU, w, r
from verify_spark_interaction import paired
from sh_subset import signed

RECORD = 0xA900  # Isolated synthetic callback record, not firmware ownership.
MAPS = [0x7656C + 50*i for i in range(8)]
DURATIONS = [0x763FC + 15*i for i in range(8)]


def interpolate(x, axes, values):
    if x <= axes[0]:
        return values[0]
    if x >= axes[-1]:
        return values[-1]
    i = next(i for i in range(len(axes)-1) if x < axes[i+1])
    n = (values[i+1]-values[i]) * (x-axes[i])
    return values[i] + (abs(n)//(axes[i+1]-axes[i])) * (-1 if n < 0 else 1)


def table(a):
    nx, ny = TCU[a:a+2]
    xs = [v*256 for v in TCU[a+2:a+2+nx]]
    rows = [TCU[a+2+nx+j*(nx+1):a+2+nx+(j+1)*(nx+1)] for j in range(ny)]
    return xs, [row[0]*256 for row in rows], [[v*256 for v in row[1:]] for row in rows]


def lookup(a, x, y):
    xs, ys, rows = table(a)
    return interpolate(y & 65535, ys, [interpolate(x & 65535, xs, row) for row in rows])


def map_address(code, operation, flags):
    a = {6: 0x7659E, 7: 0x765D0, 8: 0x76602, 9: 0x76634,
         10: 0x766CA, 11: 0x76602}.get(code, 0x7656C)
    if code == 7 and flags & 0x20:
        a = 0x76698
    if operation == 0x18:
        a = 0x76666
    elif operation == 0x17:
        a = 0x76698
    return a


def duration_address(code, operation, flags):
    a = {6: 0x7640B, 7: 0x7641A, 8: 0x76429, 9: 0x76438,
         10: 0x76465, 11: 0x76429}.get(code, 0x763FC)
    if code == 7 and flags & 0x20:
        a = 0x76447
    if operation == 0x18:
        a = 0x76456
    elif operation == 0x17:
        a = 0x76447
    return a


def setup(t, handle, code=6, operation=0, flags=0, index=0, x=0, y=0):
    for off, val, size in [(1, code, 1), (2, handle, 1), (8, operation, 1),
                           (10, 0x1234, 2), (12, 3, 1), (13, index, 1),
                           (16, y, 2), (18, flags, 1)]:
        w(t, RECORD+off, val, size)
    w(t, 0x80F6, x, 2)
    w(t, 0x96CC, 0x789A, 2)


def callback(t, address):
    t.r[5] = 0xFFFF0000+RECORD
    return t.run(address)


def check_candidate(t, handle, value, flags):
    assert r(t, RECORD+4, 2) == value
    assert r(t, RECORD+18) == ((flags & 127) | (128 if value > 0 else 0))
    assert r(t, BANKS[0]['base']+4*handle+2, 2) == value
    assert r(t, BANKS[0]['flags']+handle) == int(value > 0)
    t.run(0x4C7AC)
    assert (r(t, 0x9160, 2), r(t, 0x9168)) == (value, 255 if value == 32767 else int(value > 0))
    t.run(0x1FB8C)
    source = max(800-value, 0) if value not in [0, 32767] else 32767
    assert r(t, 0x915A, 2) == source
    return source


def main():
    constructor_cases = 0
    for head, index in itertools.product([0, 7, 11], range(12)):
        t = fixture()
        w(t, 0xA2B9, head); w(t, 0xA2BA, 12)
        for i in range(12):
            w(t, 0xA2BC+12*i+6, 32+i)
        w(t, 0x808C, 4); w(t, 0x80C2, 0x1234, 2); w(t, 0x80C4, 0xABCD, 2)
        w(t, RECORD+18, 0x67)
        t.r[5], t.r[6], t.r[7] = 6, 0x17, 0xFFFF0000+RECORD
        assert t.run(0x4CBA8, 32+index) == 2
        assert [r(t, RECORD+i) for i in [1, 2, 8, 12, 13, 18]] == [6, 2, 0x17, index, 4, 0x67]
        assert [r(t, RECORD+i, 2) for i in [4, 6, 14, 16]] == [0, 0, 0x1234, 0xABCD]
        assert r(t, 0xA202, 2) == 1
        constructor_cases += 1
    t = fixture()
    handle = allocate(t, BANKS[0])
    clamp_cases = 0
    for value in [0, 1, 32766, 32767, 32768, 65535, 65536, 65537, 0xFFFFFFFF]:
        assert t.run(0x4D274, value) == (value if signed(value & 65535, 16) >= 0 else 0)
        clamp_cases += 1

    # Independent two-stage interpolation, exercising knots and midpoints.
    lookup_cases = 0
    for a in MAPS:
        xs, ys, _ = table(a)
        xx = sorted({0, 65535, *xs, *((p+q)//2 for p, q in zip(xs, xs[1:]))})
        yy = sorted({0, 65535, *ys, *((p+q)//2 for p, q in zip(ys, ys[1:]))})
        for x, y in itertools.product(xx, yy):
            t.r[5], t.r[6] = y, a
            actual = t.run(0x1078A, x)
            assert actual == lookup(a, x, y), (hex(a), x, y, actual, lookup(a, x, y))
            lookup_cases += 1

    # All stock offset curves are zero; executing the helper still checks
    # both enabled/disabled curve paths and their argument sources.
    for a in [0x766FC, 0x76705, 0x7670E, 0x76717, 0x76720]:
        assert TCU[a] == 4 and TCU[a+5:a+9] == bytes(4)
    duration_cases = 0
    for code, op, flags, index in itertools.product([0, 6, 7, 8, 9, 10, 11, 255],
                                                   [0, 0x17, 0x18], [0, 0x20], range(15)):
        setup(t, handle, code, op, flags, index)
        assert t.run(0x4D4CC, 0xFFFF0000+RECORD) == TCU[duration_address(code, op, flags)+index]
        duration_cases += 1

    producer_cases = 0
    rng = random.Random(216554)
    for code, op, flags in itertools.product([0, 6, 7, 8, 9, 10, 11, 255],
                                            [0, 0x17, 0x18], [0, 0x20, 0x40, 0xE7]):
        a = map_address(code, op, flags)
        xs, ys, _ = table(a)
        inputs = [(signed(((x-0x1900)//2) & 65535, 16), y) for x, y in zip(xs, ys)]
        inputs += [(rng.randrange(65536), rng.randrange(65536)) for _ in range(3)]
        for x, y in inputs:
            setup(t, handle, code, op, flags, x=x, y=y)
            expected = 0 if code == 7 and op == 0x18 else lookup(a, 2*signed(x & 65535, 16)+0x1900, y) >> 2
            # Complete two-output producer, sentinel-filled destinations.
            w(t, 0xA980, 0xDEADBEEF, 4); w(t, 0xA984, 0xCAFEBABE, 4)
            t.r[5], t.r[6] = 0xFFFFA984, 0xFFFF0000+RECORD
            t.run(0x4D554, 0xFFFFA980)
            assert (r(t, 0xA980, 4), r(t, 0xA984, 4)) == (expected, 0)
            for inhibit, enable in [(0, 2), (4, 2), (0, 0), (0xFB, 0xFF)]:
                w(t, 0x92D5, inhibit); w(t, 0x9410, enable)
                callback(t, 0x4D010)
                value = expected if not inhibit & 4 and enable & 2 else 0
                check_candidate(t, handle, value, flags)
                producer_cases += 1

    ramp_cases = 0
    for code, op, flags, index in itertools.product([0, 6, 7, 8, 9, 10, 11],
                                                   [0, 0x17, 0x18], [0, 0x20], [0, 5, 10, 14]):
        duration = TCU[duration_address(code, op, flags)+index]
        for start, timer in itertools.product([0, 1, 640, 1920, 32767, 32768, 65535],
                                              sorted({0, max(0, duration-1), duration, min(255, duration+1), 255})):
            setup(t, handle, code, op, flags, index)
            w(t, RECORD+6, start, 2); w(t, 0x8118, timer)
            w(t, 0x92D5, 0); w(t, 0x9410, 2)
            raw = start*(duration-timer)//duration if timer < duration else 0
            expected = max(signed(raw, 16), 0)
            callback(t, 0x4D142)
            check_candidate(t, handle, expected, flags)
            assert callback(t, 0x4CF08) == int(timer >= duration)
            ramp_cases += 1

    ramp_gate_cases = 0
    for inhibit, enable, flags in itertools.product([0, 4, 0xFB, 0xFF], [0, 2, 0xFD, 0xFF], [0, 0x80, 0xE7]):
        setup(t, handle, 6, 0, flags)
        w(t, RECORD+6, 640, 2); w(t, 0x8118, 0)
        w(t, 0x92D5, inhibit); w(t, 0x9410, enable)
        callback(t, 0x4D142)
        check_candidate(t, handle, 640 if not inhibit & 4 and enable & 2 else 0, flags)
        ramp_gate_cases += 1

    # Stock map value -> capture at ramp entry -> sampled full ramp -> ECU.
    lifecycle = []
    setup(t, handle, 6, 0, 0, 0, (63*256-0x1900)//2, 44*256)
    w(t, 0x92D5, 0); w(t, 0x9410, 2)
    callback(t, 0x4D010)
    assert r(t, RECORD+4, 2) == 1024
    w(t, 0x8118, 233)
    assert callback(t, 0x4CEF2) == 5
    assert r(t, RECORD+6, 2) == 1024 and r(t, 0x8118) == 0
    for timer in [0, 12, 24, 48, 49, 50]:
        w(t, 0x8118, timer)
        callback(t, 0x4D142)
        value = 1024*(49-timer)//49 if timer < 49 else 0
        source = check_candidate(t, handle, value, 0)
        for cut in [0, 1]:
            lifecycle.append({'timer_sample': timer, 'reduction': value,
                              **paired(source, 16, 1, 1, cut, t=t)})
    # The clear callback actively writes zero/mode0 into the allocated node.
    callback(t, 0x4CF6A)
    check_candidate(t, handle, 0, 0)
    print(json.dumps({'scope': __doc__, 'constructor_cases': constructor_cases, 'clamp_cases': clamp_cases,
                      'two_axis_lookup_cases': lookup_cases, 'duration_cases': duration_cases,
                      'map_producer_cases': producer_cases, 'ramp_cases': ramp_cases, 'ramp_gate_cases': ramp_gate_cases,
                      'paired_lifecycle': lifecycle,
                      'limits': 'Original ROM functions/helpers execute. Constructor queue, callback records, timer samples, gates and ECU coefficients are fixtures. Full dispatch, physical units and task timing remain open.'}, indent=2))


if __name__ == '__main__':
    main()
