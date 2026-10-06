"""Original ascending phase qualifier: counters, crossing latch and ECU lifecycle.

Tests qualification, departure and initial-delay neighbor branches.
Measured sources, call cadence and paired ECU coefficients remain fixtures.
"""
import itertools
import json

from sh_relative_branch import SHRelativeBranch
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_ascending_map import lifecycle
from verify_tcu_ascending_release import ObservedRelease
from verify_tcu_phase_policy import initial_delay_model


def initial_model(t, index):
    code = r(t, 0x95DE+15*index)
    if code in range(5, 12):
        admitted, delay = initial_delay_model(code, r(t, 0x808C),
            r(t, 0x95DF+15*index), r(t, 0x8380+2*index, 2))
        return admitted, delay, False, False
    assert code in range(5)
    selector = r(t, 0x808D)
    delay = TCU[0x70A6C+6*code+selector]
    following = (index+1) % 16
    next_code = r(t, 0x95DE+15*following)
    position = (index-r(t, 0x96C4)) % 16
    next_ready = (position+1 < r(t, 0x96C5) and next_code < 5 and
                  signed(r(t, 0x8380+2*following, 2), 16) >= 2*TCU[0x70A6C+6*next_code+selector])
    prior_code = r(t, 0x95DE+15*((index-1) % 16))
    prior_override = r(t, 0x95DF+15*index) != 0 and prior_code >= 5
    if next_ready or prior_override:
        delay = 0
    return int(signed(r(t, 0x8380+2*index, 2), 16) >= 2*delay), delay, next_ready, prior_override


def initial_setup(t, index, code, selector=0, operation=0, layout='single',
                  prior_code=0, next_code=3, next_timer=0, timer=0):
    head = (index-1) % 16 if layout == 'tail' else index
    for address, value, size in [(0x96C4, head, 1), (0x96C5, 1 if layout == 'single' else 2, 1),
            (0x95DE+15*index, code, 1), (0x95DF+15*index, operation, 1), (0x808D, selector, 1),
            (0x95DE+15*((index-1) % 16), prior_code, 1),
            (0x95DE+15*((index+1) % 16), next_code, 1),
            (0x8380+2*((index+1) % 16), next_timer, 2), (0x8380+2*index, timer, 2)]:
        w(t, address, value, size)


def model(code, mode, enable, operation, measured, lower, upper, a, b, flags):
    band = (code in [2, 3, 4] or code in [0, 1] and mode == 1) and lower <= measured < upper
    below = code in [0, 1] and mode == 0 and measured < upper
    if measured >= lower:
        flags |= 2
    a = min(a+1, 255) if band else 0
    b = min(b+1, 255) if below else 0
    first_count = TCU[0x770BE] if operation in [0x12, 0x13] else TCU[0x70B06+2*code+(enable & 1)]
    first = band and a >= first_count
    second = below and b >= TCU[0x70B10+2*code+(enable & 1)] and bool(flags & 2)
    done = bool(first or second)
    if done:
        flags &= ~2
    return int(done), a, b, flags


def setup(t, index, code, mode=0, enable=1, operation=0, measured=1000,
          lower=872, upper=1128, a=0, b=0, flags=0):
    for address, value, size in [(0x8086, mode, 1), (0x9410, enable, 1),
                                (0x80EE, measured, 2), (0x9704, lower, 4),
                                (0x9700, upper, 4), (0x96CF+index, a, 1),
                                (0x96DF+index, b, 1), (0x971A, flags, 1)]:
        w(t, address, value, size)
    t.r[5], t.r[6] = code, operation


def inputs(t, index, code, operation):
    return (code, r(t, 0x8086), r(t, 0x9410), operation,
            signed(r(t, 0x80EE, 2), 16), signed(r(t, 0x9704, 4), 32),
            signed(r(t, 0x9700, 4), 32), r(t, 0x96CF+index),
            r(t, 0x96DF+index), r(t, 0x971A))


def check(t, index, code, operation):
    args = inputs(t, index, code, operation)
    expected = model(*args)
    t.r[5], t.r[6] = code, operation
    got = t.run(0x32614, index)
    actual = (got, r(t, 0x96CF+index), r(t, 0x96DF+index), r(t, 0x971A))
    assert actual == expected, (index, args, actual, expected)
    return dict(index=index, measured=args[4], code=code, mode=args[1],
                returned=got, band_count=actual[1], below_count=actual[2], flags=actual[3])


class ObservedQualification(ObservedRelease):
    def __init__(self):
        super().__init__()
        self.phase_checks = []
        self.pending_phase = None
        self.cycle = 0
        self.pending_initial = None
        self.initial_checks = 0

    def instruction(self, pc):
        if pc == 0x11014:
            self.cycle += 1
        if pc == 0x317E4:
            index = self.r[4] & 65535
            self.pending_initial = initial_model(self, index)
        if pc == 0x31972:
            assert self.r[0] == self.pending_initial[0]
            self.pending_initial = None
            self.initial_checks += 1
        if pc == 0x32614:
            index, code, operation = [self.r[i] & 65535 for i in [4, 5, 6]]
            args = inputs(self, index, code, operation)
            self.pending_phase = (index, args, model(*args))
        if pc == 0x327A0:
            index, args, expected = self.pending_phase
            actual = (self.r[0], r(self, 0x96CF+index), r(self, 0x96DF+index), r(self, 0x971A))
            assert actual == expected, (index, args, actual, expected)
            self.phase_checks.append(dict(call=self.cycle, index=index, code=args[0],
                mode=args[1], measured=args[4], lower=args[5], upper=args[6],
                prior_band_count=args[7], prior_below_count=args[8], prior_flags=args[9],
                returned=actual[0], band_count=actual[1], below_count=actual[2], flags=actual[3]))
            self.pending_phase = None
        return super().instruction(pc)


def main():
    t = SHRelativeBranch(TCU)
    timer_cases = 0
    neighbors = [(0, 3, 17), (0, 3, 18), (7, 3, 17), (7, 3, 18), (0, 8, 32767), (7, 8, 32767)]
    for code, selector, layout, op, (prior, following, following_timer), timer in itertools.product(
            range(5), range(6), ['single', 'head', 'tail'], [0, 0x17], neighbors,
            [-1, 0, 17, 18, 32767, 32768]):
        index = 15 if timer_cases % 2 else 0
        initial_setup(t, index, code, selector, op, layout, prior, following, following_timer, timer)
        expected = initial_model(t, index)
        assert t.run(0x317E4, index) == expected[0]
        timer_cases += 1
    departures = 0
    for code, reference, timer, flags, delta in itertools.product(range(5), [-1000, 0, 1000],
            [17, 18, 19], [0, 2, 16, 18, 4, 32, 128], [-129, -128, -127, 0, 128]):
        initial_setup(t, 0, code, timer=timer)
        w(t, 0x9218+4*TCU[0x5D428+code], reference, 4)
        w(t, 0x80EE, reference+delta, 2); w(t, 0x92C6, flags)
        t.r[5] = code
        expected = 1 if not flags & 0x12 and timer >= 18 and delta < -128 else -1
        assert signed(t.run(0x3241C, 0), 32) == expected
        departures += 1
    direct = 0
    for code, mode, enable, operation in itertools.product(range(5), [0, 1, 2, 255],
                                                          [0, 1, 0xFE, 0xFF], [0, 0x12, 0x13, 0x17]):
        ca = TCU[0x770BE] if operation in [0x12, 0x13] else TCU[0x70B06+2*code+(enable & 1)]
        cb = TCU[0x70B10+2*code+(enable & 1)] if code < 2 else 20
        for measured, (a, b), flags in itertools.product([871, 872, 1000, 1127, 1128, 32768, 65535],
                [(0, 0), (ca-2, cb-2), (ca-1, cb-1), (ca, cb), (254, 255)], [0xA5, 0xA7]):
            index = 15 if direct % 2 else 0
            setup(t, index, code, mode, enable, operation, measured, a=a, b=b, flags=flags)
            check(t, index, code, operation)
            direct += 1
    wrapper = 0
    for index, code, inhibit in itertools.product([0, 15], range(5), range(256)):
        setup(t, index, code, mode=1, enable=1, a=254, b=77, flags=0xA7,
              lower=54321, upper=12345)
        w(t, 0x92C6, inhibit)
        w(t, 0x9218+4*TCU[0x5D446+code], 1000, 4)
        t.r[5], t.r[6] = code, 0
        got = signed(t.run(0x324CE, index), 32)
        if inhibit & 0x12:
            assert got == -1
            assert (r(t, 0x96CF+index), r(t, 0x96DF+index), r(t, 0x971A)) == (254, 77, 0xA7)
            assert (r(t, 0x9704, 4), r(t, 0x9700, 4)) == (54321, 12345)
        else:
            assert got == 2
            assert (r(t, 0x96CF+index), r(t, 0x96DF+index), r(t, 0x971A)) == (255, 0, 0xA5)
            assert (r(t, 0x9704, 4), r(t, 0x9700, 4)) == (872, 1128)
        wrapper += 1
    retained = []
    setup(t, 0, 0, mode=0, enable=0, flags=0xA5)
    # Counts can build while below the lower bound, but cannot finish before
    # a crossing has been remembered. Crossing above the upper bound resets
    # the below counter and still sets the shared crossing flag.
    for measured in [800]*22 + [1200] + [800]*20 + [800, 1000, 800]:
        w(t, 0x80EE, measured, 2)
        retained.append(check(t, 0, 0, 0))
    assert [i+1 for i, row in enumerate(retained) if row['returned']] == [43, 45]
    shared = []
    setup(t, 0, 0, mode=0, enable=0, measured=800, b=19, flags=0)
    shared.append(check(t, 0, 0, 0))  # Count20 alone is not enough.
    setup(t, 15, 2, mode=1, enable=0, measured=1200, a=0, b=0, flags=r(t, 0x971A))
    shared.append(check(t, 15, 2, 0))  # A different record sets global latch.
    w(t, 0x8086, 0); w(t, 0x80EE, 800, 2)
    shared.append(check(t, 0, 0, 0))  # First record now qualifies below lower.
    assert [row['returned'] for row in shared] == [0, 0, 1]
    assert r(t, 0x96CF+15) == r(t, 0x96DF+15) == 0
    # Mode change preserves the latch; each ineligible counter resets on call.
    mode_rows = []
    setup(t, 0, 1, mode=2, enable=1, measured=1000, a=19, b=19, flags=0)
    mode_rows.append(check(t, 0, 1, 0))
    w(t, 0x8086, 0); w(t, 0x80EE, 800, 2)
    for _ in range(20):
        mode_rows.append(check(t, 0, 1, 0))
    assert mode_rows[-1]['returned'] == 1
    observed = ObservedQualification()
    samples = {80: 5000, 81: 6000, 84: 5900, 86: 5750, 88: 5500,
               90: 5250, 92: 5100, 94: 5051, 96: 5050, 98: 5000}
    trace = lifecycle(25000, samples=samples, t=observed, calls=160)
    assert observed.pending_phase is None
    assert [row['call'] for row in observed.phase_checks if row['returned']] == [80, 111]
    assert next(row for row in observed.phase_checks if row['call'] == 111)['below_count'] == 20
    assert observed.pending_initial is None
    print(json.dumps(dict(scope=__doc__, initial_timer_cases=timer_cases,
        departure_cases=departures, qualifier_cases=direct, wrapper_cases=wrapper,
        retained_crossing=retained, shared_latch=shared, retained_mode_change=mode_rows,
        manager_calls=160, manager_phase_checks=observed.phase_checks,
        manager_initial_checks=observed.initial_checks,
        manager_release_checks=len(observed.release_checks), manager_trace=trace,
        limits='Shared-latch and neighbor probes are bounded function executions, not a complete overlapping ring lifecycle. Actual8086 producer, composite transitions and task timing remain separate work.'), indent=2))


if __name__ == '__main__':
    main()
