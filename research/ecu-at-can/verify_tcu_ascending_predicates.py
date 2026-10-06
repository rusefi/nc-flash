"""Original ascending release admission and reactivation predicates.

Independent bounds/side-effect oracles plus manager-driven repeated entry.
Inputs, task cadence and ECU coefficients are explicit test fixtures.
"""
import itertools
import json

from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_slot2 import fixture, allocate, BANKS
from verify_tcu_request_dispatch import curve
from verify_tcu_ascending_map import RECORD, lifecycle
from verify_tcu_ascending_release import ObservedRelease, clamp, error, setup


def bounds(code, captured_axis, speed, derivative):
    bank = code if code in range(5) else 0
    offset = curve(0x7677E+9*bank, captured_axis) >> 2
    factor = curve(0x767AB+9*bank, 4*clamp(signed(speed, 16), 0, 16383)) >> 8
    dynamic = signed((-signed(derivative, 16)) & 65535, 16)*factor
    return offset, dynamic


def predicate(t, p, kind):
    code = r(t, p+1)
    reference = signed(r(t, 0x9218+4*TCU[0x5D446+code], 4), 32)
    offset, dynamic = bounds(code, r(t, p+14, 2), r(t, 0x80EA, 2), r(t, 0x80F0, 2))
    measured = signed(r(t, 0x80EE, 2), 16)
    first = signed((reference+offset) & 0xFFFFFFFF, 32)
    second = signed((reference+dynamic) & 0xFFFFFFFF, 32)
    if kind == 'release':
        result = int(measured < first or measured < second)
    else:
        result = int(r(t, 0x8081) >= 1 and bool(r(t, p+8) & 0x20)
                     and measured >= first and signed(r(t, 0x80F0, 2), 16) >= 0)
    captured = error(r(t, 0x80EE, 2), reference) & 65535 if kind == 'release' and result else r(t, p+10, 2)
    return result, captured, first, second


class ObservedPredicates(ObservedRelease):
    def __init__(self):
        super().__init__()
        self.pending_predicates = {}
        self.predicate_counts = {'release': 0, 'rearm': 0}
        self.admitted = []

    def instruction(self, pc):
        starts = {0x4DF3C: ('release', 0x4DFD8), 0x4DDA0: ('rearm', 0x4DE60)}
        if pc in starts:
            kind, end = starts[pc]
            p = self.r[5] & 65535
            expected = predicate(self, p, kind)
            self.pending_predicates[end] = (kind, p, expected,
                dict(measured=signed(r(self, 0x80EE, 2), 16), flags=r(self, p+8),
                     derivative=signed(r(self, 0x80F0, 2), 16), input8081=r(self, 0x8081)))
        if pc in self.pending_predicates:
            kind, p, expected, row = self.pending_predicates.pop(pc)
            assert (self.r[0], r(self, p+10, 2)) == expected[:2]
            self.predicate_counts[kind] += 1
            if expected[0]:
                self.admitted.append(dict(kind=kind, captured_error=signed(expected[1], 16),
                                          first_bound=expected[2], second_bound=expected[3], **row))
        return super().instruction(pc)


def main():
    t = fixture()
    handle = allocate(t, BANKS[0])
    helpers = 0
    for code, axis, speed, derivative in itertools.product([0, 1, 2, 3, 4, 5, 255],
            [0, 4000, 20000, 32767, 32768, 65535],
            [0, 4672, 12000, 16383, 16384, 32768, 65535], [0, 1, -1, -40, 32768]):
        setup(t, handle, code=code, speed=speed, derivative=derivative)
        w(t, RECORD+14, axis, 2)
        t.r[5], t.r[6] = 0xFFFFA984, 0xFFFF0000+RECORD
        t.run(0x4E314, 0xFFFFA980)
        assert (r(t, 0xA980, 4), signed(r(t, 0xA984, 4), 32)) == bounds(code, axis, speed, derivative & 65535)
        helpers += 1
    release_cases = 0
    rearm_cases = 0
    for code, derivative in itertools.product(range(5), [0, 1, -1, -40, -100, 32768]):
        setup(t, handle, code=code, derivative=derivative)
        w(t, RECORD+14, 4000, 2)
        offset, dynamic = bounds(code, 4000, 4672, derivative & 65535)
        # Signed16 measured samples around both independent signed32 sums.
        points = {0, 32767, 32768, 65535, 5000,
                  *((5000+v+d) & 65535 for v in [offset, dynamic] for d in [-1, 0, 1])}
        for measured in sorted(points):
            w(t, 0x80EE, measured, 2); w(t, RECORD+10, 0x1234, 2)
            expected = predicate(t, RECORD, 'release')
            t.r[5] = 0xFFFF0000+RECORD
            assert t.run(0x4DF3C) == expected[0]
            assert r(t, RECORD+10, 2) == expected[1]
            release_cases += 1
            for input8081, flags in itertools.product([0, 1, 255], [0, 0x20, 0xDF, 0xFF]):
                w(t, 0x8081, input8081); w(t, RECORD+8, flags)
                expected = predicate(t, RECORD, 'rearm')
                t.r[5] = 0xFFFF0000+RECORD
                assert t.run(0x4DDA0) == expected[0]
                assert r(t, RECORD+10, 2) == expected[1]
                rearm_cases += 1
    wrap_cases = 0
    for reference, measured in itertools.product([-2147483648, 2147483647, -32768, 32767],
                                                [0, 32767, 32768, 65535]):
        setup(t, handle, reference=reference, measured=measured, flags=0x20)
        w(t, 0x8081, 1); w(t, RECORD+14, 4000, 2)
        for kind, fn in [('release', 0x4DF3C), ('rearm', 0x4DDA0)]:
            expected = predicate(t, RECORD, kind)
            t.r[5] = 0xFFFF0000+RECORD
            assert t.run(fn) == expected[0]
            assert r(t, RECORD+10, 2) == expected[1]
            wrap_cases += 1
    transition_cases = 0
    for flags, timer in itertools.product(range(256), [0, 1, 255]):
        w(t, RECORD+8, flags); w(t, 0x8276, timer)
        w(t, RECORD+4, 640, 2); w(t, RECORD+6, 320, 2)
        t.r[5] = 0xFFFF0000+RECORD
        assert t.run(0x4DE6C) == 3
        assert r(t, RECORD+8) == flags | 0x10 and r(t, 0x8276) == 0
        assert (r(t, RECORD+4, 2), r(t, RECORD+6, 2)) == (640, 320)
        transition_cases += 1
    for flags, current in itertools.product(range(256), [0, 640, 32767, 32768, 65535]):
        w(t, RECORD+8, flags); w(t, RECORD+4, current, 2); w(t, RECORD+6, 0x1234, 2)
        t.r[5] = 0xFFFF0000+RECORD
        assert t.run(0x4DFE8) == 4
        assert r(t, RECORD+8) == flags | 0x20 and r(t, RECORD+6, 2) == current
        transition_cases += 1
    traces = []
    samples = {80: 5000, 81: 6000, 90: 5250, 92: 5100, 94: 5050,
               98: 6000, 102: 5250, 104: 5100, 106: 5050, 108: 5000}
    for enable in [0, None]:
        observed = ObservedPredicates()
        trace = lifecycle(25000, samples=samples, t=observed, calls=192,
                          rearm_input=enable, map_samples={98: 9728})
        assert not observed.pending_predicates and observed.release_checks
        reentries = [row for row in observed.admitted if row['kind'] == 'rearm']
        assert bool(reentries) == (enable is None)
        if enable is None:
            assert all(row['input8081'] == 2 for row in reentries)
        rebound = next(row for row in trace['checkpoints'] if row['call'] == 98)
        assert rebound['request'] == (1280 if enable == 0 else 768)
        traces.append(dict(forced_input8081=enable, trace=trace, predicate_counts=observed.predicate_counts,
            admitted_predicates=observed.admitted, release_checks=observed.release_checks))
    print(json.dumps(dict(scope=__doc__, bounds_cases=helpers, release_predicate_cases=release_cases,
        rearm_predicate_cases=rearm_cases, signed_wrap_cases=wrap_cases,
        state_transition_cases=transition_cases, manager_calls=384, manager_traces=traces,
        limits='Predicates verified against original opcodes. Input8081 is a fixture, not a proven physical selector. Phase qualification32614, task timing and upstream signal attribution remain open.'), indent=2))


if __name__ == '__main__':
    main()
