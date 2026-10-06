"""Original production of ascending qualification mode8086 and source history.

Upstream samples and call cadence are explicit; accepted/next state, local
flags and the mode producer are executed through their original instructions.
"""
import itertools
import json

from sh_relative_branch import SHRelativeBranch
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_ascending_map import lifecycle
from verify_tcu_ascending_phase import ObservedQualification


def source_latch(old, source, previous, state, transition, measured):
    special = source in [10, 17]
    direction = 1 if transition in range(5) else 2 if transition in range(5, 12) else 0
    value = old
    if not special or state == 2 and direction == 2:
        value = 0
    if special and (previous not in [10, 17] or measured >= 1211 or measured < 558 or state == 1):
        value = 1
    return value


def mode_model(selected, source, measured, flag_acd, flag_c00, flag_bfc, old84, old8a, source82):
    request = selected == 2 and (source in [10, 17, 13, 14] or bool((flag_acd | flag_c00) & 16))
    flags84 = (old84 & 254) | int(request)
    held = bool(old8a & 2)
    if measured < 2793 and request:
        held = True
    if measured >= 2980 or not request:
        held = False
    flags8a = (old8a & ~2) | (2 if held else 0)
    inhibit = bool(flag_bfc & 32) and request and (measured >= 12198 or source not in [10, 17])
    flags8a = (flags8a & ~4) | (4 if inhibit else 0)
    source83 = int(request and not flags8a & 6)
    mode = int(source82 == 1 if selected == 0 else source in [10, 17] if selected == 1
               else source83 == 1 if selected == 2 else False)
    return mode, flags84, flags8a, source83


def mode_inputs(t, use_next, next_state):
    selected = (next_state if use_next & 255 else r(t, 0x8081)) & 255
    return (selected, r(t, 0x9B40), signed(r(t, 0x80EA, 2), 16),
            r(t, 0x9ACD), r(t, 0x9C00), r(t, 0x9BFC), r(t, 0x9C84), r(t, 0x9C8A), r(t, 0x9C82))


def check_mode(t, use_next=0, next_state=0):
    args = mode_inputs(t, use_next, next_state)
    expected = mode_model(*args)
    t.r[5] = next_state
    t.run(0x49260, use_next)
    actual = tuple(r(t, a) for a in [0x8086, 0x9C84, 0x9C8A, 0x9C83])
    assert actual == expected, (args, actual, expected)
    return dict(selected_state=args[0], source=args[1], measured=args[2], mode=actual[0],
                flags84=actual[1], flags8a=actual[2], source83=actual[3])


class ObservedMode(ObservedQualification):
    def __init__(self):
        super().__init__()
        self.pending_mode = None
        self.mode_checks = []

    def instruction(self, pc):
        if pc == 0x49260:
            args = mode_inputs(self, self.r[4], self.r[5])
            self.pending_mode = (args, mode_model(*args))
        if pc == 0x492D4:
            args, expected = self.pending_mode
            actual = tuple(r(self, a) for a in [0x8086, 0x9C84, 0x9C8A, 0x9C83])
            assert actual == expected, (args, actual, expected)
            self.mode_checks.append(dict(selected_state=args[0], source=args[1],
                measured=args[2], mode=actual[0], flags84=actual[1], flags8a=actual[2]))
            self.pending_mode = None
        return super().instruction(pc)


def main():
    assert [int.from_bytes(TCU[a:a+2], 'big') for a in range(0x773BC, 0x773C6, 2)] == [1211, 558, 2793, 2980, 12198]
    t = SHRelativeBranch(TCU)
    classified = 0
    for transition in [*range(14), 255, 256, 65535, 65536, 65541]:
        code = transition & 65535
        expected = 1 if code < 5 else 2 if code < 12 else 0
        assert t.run(0x49110, transition) == expected
        classified += 1
    latch_cases = 0
    for source, previous, state, transition, measured, old in itertools.product(
            [0, 10, 17, 13, 14, 255], [0, 10, 17], [0, 1, 2, 255], [0, 5, 11, 12],
            [557, 558, 559, 1210, 1211, 32768, 65535], [0, 1, 2]):
        for a, v in [(0x9B40, source), (0x9C89, previous), (0x9C91, state), (0x9C82, old)]:
            w(t, a, v)
        w(t, 0x80EA, measured, 2)
        expected = source_latch(old, source, previous, state, transition, signed(measured, 16))
        t.run(0x4905C, transition)
        assert (r(t, 0x9C82), r(t, 0x9C89)) == (expected, source)
        latch_cases += 1
    producers = 0
    for state, source, measured, flags, source82 in itertools.product(
            [0, 1, 2, 3, 5, 255], [0, 10, 17, 13, 14, 255],
            [2792, 2793, 2979, 2980, 12197, 12198, 32768],
            [(0, 0, 0), (16, 0, 0), (0, 16, 32), (0, 0, 32)], [0, 1, 2]):
        for a, v in [(0x8081, state), (0x9B40, source), (0x9C82, source82),
                     (0x9ACD, flags[0]), (0x9C00, flags[1]), (0x9BFC, flags[2]),
                     (0x9C84, 0xA4), (0x9C8A, 0xFB), (0x9C83, 255)]:
            w(t, a, v)
        w(t, 0x80EA, measured, 2)
        check_mode(t)
        producers += 1
    choices = 0
    for use_next, accepted, proposed in itertools.product([0, 1, 2, 255, 256], range(6), range(6)):
        w(t, 0x8081, accepted); w(t, 0x9B40, 10); w(t, 0x9BFC, 0)
        w(t, 0x9C82, 1); w(t, 0x80EA, 4672, 2)
        check_mode(t, use_next, proposed)
        choices += 1
    retained = []
    w(t, 0x8081, 2); w(t, 0x9B40, 10); w(t, 0x9BFC, 0); w(t, 0x9C8A, 0)
    for measured in [3000, 2793, 2792, 2793, 2979, 2980, 2793]:
        w(t, 0x80EA, measured, 2)
        retained.append(check_mode(t))
    assert [row['mode'] for row in retained] == [1, 1, 0, 0, 0, 1, 1]
    traces = []
    samples = {80: 5000, 81: 6000, 84: 5900, 86: 5750, 88: 5500,
               90: 5250, 92: 5100, 94: 5051, 96: 5050, 98: 5000}
    for source in [0, 10]:
        observed = ObservedMode()
        def upstream(t, call):
            w(t, 0x9B40, source)
            t.run(0x4905C, r(t, 0x9C87))
            check_mode(t)
        trace = lifecycle(25000, samples=samples, t=observed, calls=192, upstream=upstream)
        assert observed.pending_mode is None and len(observed.mode_checks) == 193
        assert {row['mode'] for row in observed.mode_checks[1:]} == {int(source == 10)}
        traces.append(dict(source=source, trace=trace, mode_checks=observed.mode_checks,
            phase_checks=observed.phase_checks, initial_checks=observed.initial_checks,
            release_checks=len(observed.release_checks)))
    print(json.dumps(dict(scope=__doc__, classifier_cases=classified, source_latch_cases=latch_cases,
        mode_producer_cases=producers, selection_cases=choices, retained_hysteresis=retained,
        manager_calls=384, manager_traces=traces,
        limits='8086 is produced, not injected. 9B40 and other upstream source fields remain fixtures; scheduling of source producer once per cycle is explicit, not a proved task cadence. Physical state/units and full overlap remain open.'), indent=2))


if __name__ == '__main__':
    main()
