"""Stock ascending release: original bounds, ratio, capture and paired CAN path.

Direct callback records and upstream samples are explicit fixtures. Retained
manager trace uses real creation/dispatch with a stepped target approach.
No physical signal units, task cadence or hardware actuation is inferred.
"""
import itertools
import json

from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_slot2 import fixture, allocate, BANKS
from verify_tcu_request_dispatch import curve
from verify_tcu_request_admission import paired_snapshot
from verify_tcu_ascending_map import RECORD, ObservedAscending, lifecycle


def clamp(x, low=-32768, high=32767):
    return min(high, max(low, x))


def quotient(a, b):
    if not b:
        return 0 if not a else 32767 if a > 0 else -32768
    return clamp(abs(a)//abs(b) * (-1 if (a < 0) != (b < 0) else 1))


def bank(code):
    return code if code in range(5) else 0


def error(measured, reference):
    return clamp(signed((signed(measured, 16)-signed(reference, 32)) & 0xFFFFFFFF, 32))


def thresholds(code, selector, speed, derivative):
    b = bank(code)
    lower = int.from_bytes(TCU[0x76742+12*b+2*selector:0x76744+12*b+2*selector], 'big')
    axis = clamp(signed(speed, 16), 0, 16383)*4
    factor = curve(0x767D8+9*b, axis) >> 8
    dynamic = signed((-signed(derivative, 16)) & 65535, 16)*factor
    return lower, dynamic


def release(code, selector, speed, derivative, measured, reference,
            captured_error, current, captured_value, flags):
    delta = error(measured, reference)
    lower, dynamic = thresholds(code, selector, speed, derivative)
    progress = None
    result = 0
    if delta >= signed(lower, 16) and delta >= dynamic:
        progress = clamp(256-quotient(delta*256, signed(captured_error, 16)), 0, 256)
        # Verify stock calibration before using its reachable branch only.
        side = int(selector >= TCU[0x773F0+bank(code)])
        knee = TCU[0x768FF+2*bank(code)+side]
        assert knee == 0
        if not flags & 0x40:
            captured_value = current
            flags |= 0x40
        result = max(0, quotient(signed(captured_value, 16)*(256-progress), 256-knee))
    flags = (flags & 127) | (128 if result else 0)
    return result, captured_value, flags, progress, delta, dynamic


def setup(t, handle, code=1, selector=0, speed=4672, derivative=0,
          measured=6000, reference=5000, captured_error=1000,
          current=640, captured_value=1280, flags=0x20):
    for a, v, size in [(RECORD+1, code, 1), (RECORD+2, handle, 1),
                       (RECORD+4, current, 2), (RECORD+6, captured_value, 2),
                       (RECORD+8, flags, 1), (RECORD+10, captured_error, 2),
                       (RECORD+12, selector, 1), (0x80EA, speed, 2),
                       (0x80F0, derivative, 2), (0x80EE, measured, 2)]:
        w(t, a, v, size)
    index = TCU[0x5D446+code]
    w(t, 0x9218+4*index, reference, 4)


def check_release(t, handle):
    code, selector = r(t, RECORD+1), r(t, RECORD+12)
    args = (code, selector, r(t, 0x80EA, 2), r(t, 0x80F0, 2),
            r(t, 0x80EE, 2), r(t, 0x9218+4*TCU[0x5D446+code], 4),
            r(t, RECORD+10, 2), r(t, RECORD+4, 2), r(t, RECORD+6, 2), r(t, RECORD+8))
    expected = release(*args)
    t.r[5] = 0xFFFF0000+RECORD
    t.run(0x4E0EE)
    actual = (r(t, RECORD+4, 2), r(t, RECORD+6, 2), r(t, RECORD+8))
    assert actual == expected[:3], (args, actual, expected)
    assert r(t, BANKS[0]['base']+4*handle+2, 2) == expected[0]
    assert r(t, BANKS[0]['flags']+handle) == int(expected[0] > 0)
    t.run(0x4C7AC); t.run(0x1FB8C)
    source = max(800-expected[0], 0) if expected[0] not in [0, 32767] else 32767
    assert r(t, 0x915A, 2) == source, (args, expected, r(t, 0x915A, 2), source)
    return expected


class ObservedRelease(ObservedAscending):
    def __init__(self):
        super().__init__()
        self.release_checks = []
        self.pending_release = None

    def instruction(self, pc):
        if pc == 0x4E0EE:
            p = self.r[5] & 65535
            code = r(self, p+1)
            args = (code, r(self, p+12), r(self, 0x80EA, 2), r(self, 0x80F0, 2),
                    r(self, 0x80EE, 2), r(self, 0x9218+4*TCU[0x5D446+code], 4),
                    r(self, p+10, 2), r(self, p+4, 2), r(self, p+6, 2), r(self, p+8))
            self.pending_release = (p, args, release(*args))
        if pc == 0x4E2C6:
            p, args, expected = self.pending_release
            actual = (r(self, p+4, 2), r(self, p+6, 2), r(self, p+8))
            assert actual == expected[:3], (args, actual, expected)
            self.release_checks.append(dict(measured=args[4], captured_error=args[6],
                request=actual[0], captured_request=actual[1], flags=actual[2],
                progress=expected[3], error=expected[4], dynamic_bound=expected[5]))
            self.pending_release = None
        return super().instruction(pc)


def main():
    t = fixture()
    handle = allocate(t, BANKS[0])
    helpers = 0
    for a, b in itertools.product([-8388608, -256, 0, 256, 8388352],
                                   [-32768, -1, 0, 1, 32767]):
        t.r[5] = b
        assert signed(t.run(0x10D0C, a), 32) == quotient(a, b)
        helpers += 1
    differences = 0
    for index, measured, reference in itertools.product(range(7),
            [0, 32767, 32768, 65535], [-2147483648, -32769, -1, 0, 1, 32768, 2147483647]):
        w(t, 0x80EE, measured, 2); w(t, 0x9218+4*index, reference, 4)
        assert signed(t.run(0x4E2D6, index), 32) == error(measured, reference)
        differences += 1
    bounds = 0
    for code, selector, speed, derivative in itertools.product([0, 1, 2, 3, 4, 5, 255],
            range(6), [0, 4672, 10000, 16383, 16384, 32767, 32768, 65535],
            [0, 1, -1, -17, 32767, 32768]):
        setup(t, handle, code, selector, speed, derivative)
        t.r[5], t.r[6] = 0xFFFFA984, 0xFFFF0000+RECORD
        t.run(0x4E450, 0xFFFFA980)
        assert (r(t, 0xA980, 2), signed(r(t, 0xA984, 4), 32)) == thresholds(code, selector, speed, derivative & 65535)
        bounds += 1
    knees = 0
    for code, selector in itertools.product([0, 1, 2, 3, 4, 5, 255], range(256)):
        w(t, RECORD+1, code); w(t, RECORD+12, selector)
        t.r[5], t.r[6] = 0xFFFFA984, 0xFFFF0000+RECORD
        t.run(0x4E4DE, 0xFFFFA980)
        assert (r(t, 0xA980, 2), r(t, 0xA984, 2)) == (0, 64)
        knees += 1
    cases = 0
    for code, derivative, delta, flags in itertools.product(range(5), [0, -20, 32768],
            [-1, 0, 50, 51, 52, 59, 60, 100, 249, 500, 999, 1000, 1001],
            [0, 0x20, 0x60, 0xA0, 0xFF]):
        setup(t, handle, code=code, derivative=derivative, measured=5000+delta, flags=flags)
        check_release(t, handle)
        cases += 1
    capture_cases = 0
    for captured_error, current, captured, flags in itertools.product(
            [-32768, -1, 0, 1, 50, 1000, 32767], [0, 1, 640, 32767, 32768, 65535],
            [0, 320, 32768], [0x20, 0x60]):
        setup(t, handle, captured_error=captured_error, current=current,
              captured_value=captured, flags=flags, measured=5500)
        check_release(t, handle)
        capture_cases += 1
    gate_rows = []
    for enable, inhibit in itertools.product([0, 1, 6, 7], [0, 1, 255]):
        setup(t, handle, measured=5500)
        w(t, 0x9410, enable); w(t, 0x92D5, inhibit)
        expected = check_release(t, handle)
        assert expected[0] == 320
        gate_rows.append(dict(permission=enable, inhibit=inhibit, request=expected[0], **paired_snapshot(t)))
    sequence = []
    setup(t, handle)
    for delta in [1000, 900, 750, 500, 250, 100, 51, 50, 0, 500, 1000, 1500]:
        w(t, 0x80EE, 5000+delta, 2)
        expected = check_release(t, handle)
        sequence.append(dict(error=delta, request=expected[0], captured_request=expected[1],
                             flags=expected[2], progress=expected[3], **paired_snapshot(t)))
    observed = ObservedRelease()
    samples = {80: 5000, 81: 6000, 84: 5900, 86: 5750, 88: 5500, 90: 5250,
               92: 5100, 94: 5051, 96: 5050, 98: 5000}
    trace = lifecycle(25000, samples=samples, t=observed, calls=160)
    assert observed.release_checks and observed.pending_release is None
    assert any(0 < row['request'] < 1280 for row in observed.release_checks)
    print(json.dumps(dict(scope=__doc__, divide_cases=helpers, difference_cases=differences,
        threshold_cases=bounds, knee_cases=knees, release_boundary_cases=cases,
        capture_cases=capture_cases, gate_independence=gate_rows, retained_release_sequence=sequence,
        manager_calls=160, manager_trace=trace, manager_numeric_entries=observed.numeric_entries,
        manager_release_checks=observed.release_checks,
        limits='Stock knee0 branch only; unreachable alternate branch retained in disassembly. Explicit upstream inputs and timing, no ECU coefficient or physical-unit inference.'), indent=2))


if __name__ == '__main__':
    main()
