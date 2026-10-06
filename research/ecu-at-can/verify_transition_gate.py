"""Execute the TCU acceptance-gate producer and its CAN231/ECU consequences.

Unchanged ROM instructions, no helper stubs. RAM states are explicit fixtures;
the scheduler, physical mode meanings and mechanical gear attainment are not
modeled. Other RAM starts at zero except the documented state initializer.
"""
import hashlib
import itertools
import json

from verify_can201_byte6 import ECU, TCU, w, r
from verify_selection_reporting import initialized, report
from sh_relative_branch import SHRelativeBranch


def expected_gate(flags, requested, previous, state_a, state_b):
    armed = bool(flags & 4) or requested in (0, 5)
    retained = requested == previous or requested == 255
    active = state_a == 2 or state_b == 2
    return 4 if armed and retained and active else 0


def gate_case(flags, requested, previous, a, b):
    t = SHRelativeBranch(TCU)
    for address, value in [(0x9544, 0xA5), (0x9545, flags), (0x9546, 0x5A),
                           (0x954D, previous), (0x9594, a), (0x959C, b)]:
        w(t, address, value)
    t.run(0x2D1BC, requested)
    expected = (flags & ~4) | expected_gate(flags, requested, previous, a, b)
    assert r(t, 0x9545) == expected
    assert [r(t, address) for address in (0x9544, 0x9546, 0x954D, 0x9594, 0x959C)] == [0xA5, 0x5A, previous, a, b]


def main():
    # All flag bytes preserve their other seven bits, representative modes
    # cover both arming values, ordinary values, signed bytes and FF sentinel.
    modes = [0, 1, 4, 5, 6, 127, 128, 255]
    states = [(1, 1), (2, 1), (1, 2), (2, 2)]
    gate_cases = 0
    for args in itertools.product(range(256), modes, modes, states):
        flags, requested, previous, (a, b) = args
        gate_case(flags, requested, previous, a, b)
        gate_cases += 1
    byte_cases = 0
    for value in range(256):
        for flags in (0, 4):
            # Sweep every requested/previous byte for equal and unequal modes.
            for requested, previous in [(value, value), (value, 5), (5, value), (255, value)]:
                gate_case(flags, requested, previous, 2, 1)
                byte_cases += 1
            # Sweep every source byte, including sign-extended getter results.
            for a, b in [(value, 1), (1, value)]:
                gate_case(flags, 5, 5, a, b)
                byte_cases += 1

    producer_cases = 0
    for source_a, source_b in itertools.product(range(256), [0, 1, 2, 128, 255]):
        t = SHRelativeBranch(TCU)
        w(t, 0x9564, source_a); w(t, 0x9558, source_b)
        t.run(0x2F008); t.run(0x2F214)
        w(t, 0x81CE, 0x55); w(t, 0x81D7, 0x66)
        t.run(0x2F010); t.run(0x2F222)
        assert r(t, 0x9594) == (2 if source_a == 2 or source_b == 2 else 1)
        assert r(t, 0x959C) == (2 if source_a == 2 else 1)
        assert r(t, 0x81CE) == (0 if source_a == 2 or source_b == 2 else 0x55)
        assert r(t, 0x81D7) == (0 if source_a == 2 else 0x66)
        producer_cases += 1

    paired = []
    for old, mode, flags, (a, b) in itertools.product([0, 3, 5], modes, [0, 4], states):
        t = initialized(old)  # Includes application class8080=6.
        for address, value in [(0x954D, mode), (0x9545, flags), (0x9594, a), (0x959C, b)]:
            w(t, address, value)
        returned = t.run(0x2C7B0) & 255
        gate = expected_gate(flags, returned, mode, a, b)
        assert r(t, 0x9545) & 4 == gate
        assert r(t, 0x954D) == returned
        assert r(t, 0x954C) == 6
        assert 0x2D1BC in t.visited
        w(t, 0x8084, 5)
        t.run(0x48C08)
        row = report(t)
        assert row['accepted'] == (old if gate else min(old+1, 5))
        paired.append({'old': old, 'previous_mode': mode, 'old_flags': flags,
                       'state9594': a, 'state959c': b, 'returned_mode': returned,
                       'gate': gate, **row})

    # Produce active states through the original writers, then retain the
    # same local mode while releasing the states through their reset functions.
    lifecycle = []
    t = initialized(0)
    w(t, 0x954D, 5); w(t, 0x8084, 5)
    t.run(0x2F008); t.run(0x2F214)
    w(t, 0x9564, 2)
    t.run(0x2F010); t.run(0x2F222)
    for call in range(7):
        if call == 2:
            t.run(0x2F0B0); t.run(0x2F4A8)
        returned = t.run(0x2C7B0) & 255
        assert returned == 5
        gate = r(t, 0x9545) & 4
        t.run(0x48C08)
        row = report(t)
        assert row['accepted'] == max(0, call-1)
        assert gate == (4 if call < 2 else 0)
        lifecycle.append({'call': call+1, 'mode': returned, 'gate': gate,
                          'state9594': r(t, 0x9594), 'state959c': r(t, 0x959C), **row})

    print(json.dumps({'scope': __doc__.strip(),
                      'rom_sha256': {'ECU': hashlib.sha256(ECU).hexdigest(),
                                     'TCU': hashlib.sha256(TCU).hexdigest()},
                      'gate_cases': gate_cases, 'byte_sweep_cases': byte_cases,
                      'source_producer_cases': producer_cases,
                      'paired_caller_cases': len(paired), 'paired_matrix': paired,
                      'producer_to_ecu_lifecycle': lifecycle,
                      'limits': '9564/9558 inputs and caller invocation order are fixtures. Source producers and physical meaning remain open. Full44CFE candidate production and scheduler are not executed.'}, indent=2))


if __name__ == '__main__':
    main()
