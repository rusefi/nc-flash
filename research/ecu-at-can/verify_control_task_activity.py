"""Independent activity hysteresis/countdown oracles, including task boundaries.

Finite inputs, no real startup or cadence claim. Complete mode0 dispatcher
attempts retain known bounded harness failures after the target routines.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from probe_control_task import Probe
from sh_control_task import ControlTaskArithmetic
import verify_control_raw_inputs as raw
from verify_control_contributions import ECU, w, r, f, rf, number

ROOT = Path(__file__).resolve().parent
ENTRIES = [0x77F62, 0x77F12, 0x77F46]
ORDER = [0x399B0, 0x74DF8, *ENTRIES, 0x6CD96, 0x6CE24,
         0x6CF06, 0x6CFD8, 0x6D876, 0x6D904, 0x6D9E6]


def expected(e, entry):
    memory = raw.application(e)
    if entry == 0x77F62:
        sample = rf(e, 0x6CB0)
        value = r(e, 0x91E6)
        if sample >= number(0xE0CF8):
            value = 1
        elif sample < number(0xE0CF8) - number(0xE0CFC):
            value = 0
        address = 0x91E6
    elif entry == 0x77F12:
        value = (ECU[0xE0CF6] if r(e, 0x70F0) == 1 or r(e, 0x91E6) == 0
                 else max(0, r(e, 0x91E4) - 1))
        address = 0x91E4
    elif entry == 0x77F46:
        value, address = int(r(e, 0x91E4) > 0), 0x91E5
    else:
        raise AssertionError(entry)
    raw.expected_write(memory, address, value, 1)
    return memory


def check(e, entry):
    want = expected(e, entry)
    preserved = e.r[8:16].copy()
    e.run(entry)
    assert raw.application(e) == want
    assert e.r[8:16] == preserved and e.sr & ~1 == 0xF0


class Observed(Probe):
    def __init__(self):
        super().__init__()
        self.pending = None
        self.boundaries = []

    def instruction(self, pc):
        if self.pending is not None and pc == self.pending['return']:
            saved = self.pending
            assert raw.application(self) == saved.pop('expected')
            assert self.r[15] == saved.pop('stack')
            saved['after'] = [r(self, a) for a in [0x91E4, 0x91E5, 0x91E6]]
            self.boundaries.append(saved)
            self.pending = None
        if pc in ENTRIES:
            assert self.pending is None
            self.pending = dict(entry=pc, expected=expected(self, pc),
                                return_=self.pr, stack=self.r[15],
                                before=[r(self, a) for a in [0x91E4, 0x91E5, 0x91E6]],
                                sample_bits=r(self, 0x6CB0, 4), reset=r(self, 0x70F0))
            self.pending['return'] = self.pending.pop('return_')
        return super().instruction(pc)


def main():
    assert (number(0xE0CF8), number(0xE0CFC), ECU[0xE0CF6]) == (10, 1, 10)
    counts = dict(hysteresis=0, countdown=0, publication=0)
    epsilon = Fraction(1, 1048576)
    for value, old in itertools.product(
        [-1, 0, 9-epsilon, 9, 9+epsilon, 10-epsilon, 10, 10+epsilon, 100],
        range(256)
    ):
        e = ControlTaskArithmetic(); f(e, 0x6CB0, value); w(e, 0x91E6, old)
        check(e, 0x77F62); counts['hysteresis'] += 1
    for counter, reset, latch in itertools.product(range(256), [0, 1, 2, 255], [0, 1, 2, 255]):
        e = ControlTaskArithmetic()
        for a, value in [(0x91E4, counter), (0x70F0, reset), (0x91E6, latch)]:
            w(e, a, value)
        check(e, 0x77F12); counts['countdown'] += 1
    for counter, old in itertools.product(range(256), [0, 1, 2, 255]):
        e = ControlTaskArithmetic(); w(e, 0x91E4, counter); w(e, 0x91E5, old)
        check(e, 0x77F46); counts['publication'] += 1
    rows = []
    for phase in range(8):
        e = Observed(); w(e, 0x5360, phase); stack = e.r[15]
        try:
            e.run(0x18DC8, limit=1000000)
            status = 'returned'
            assert e.r[15] == stack
        except (ValueError, NotImplementedError) as exc:
            status = type(exc).__name__ + ': ' + str(exc)
        # These are exact known harness gaps, not successful whole-task tests.
        wanted_status = ('ValueError: Unsupported write FFFFF000/1' if phase in [1, 5]
                         else 'NotImplementedError: Opcode 201D at 000047F0' if phase == 3
                         else 'returned')
        assert status == wanted_status, (phase, status)
        assert e.entries == (ORDER if phase in [1, 5] else [0x399B0])
        assert [x['entry'] for x in e.boundaries] == (ENTRIES if phase in [1, 5] else [])
        assert e.pending is None and r(e, 0x5360) == phase + 1
        rows.append(dict(initial_phase=phase, final_phase=r(e, 0x5360), status=status,
                         target_entries=e.entries, activity_boundaries=e.boundaries))
    result = dict(rom_sha256=hashlib.sha256(ECU).hexdigest(), direct_checks=counts,
                  mode0_task_attempts=rows, completed_tasks=5,
                  verified_activity_boundaries=sum(len(x['activity_boundaries']) for x in rows),
                  scope=__doc__)
    (ROOT / 'control-task-activity-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(counts, 'completed tasks: 5; verified activity boundaries: 6')


if __name__ == '__main__':
    main()
