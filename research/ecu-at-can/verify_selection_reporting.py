"""TCU candidate -> admission/state update -> CAN231 -> ECU one-hot state.

Original functions execute completely under explicit RAM and timer fixtures.
No vehicle, wall-clock, physical gear or actuator timing simulation.
"""
import itertools
import json
from verify_can201_byte6 import ECU, TCU, w, r
from sh_relative_branch import SHRelativeBranch
from sh_subset import SH as ECUInteger


def initialized(old):
    t = SHRelativeBranch(TCU)
    w(t, 0x606F, old)
    t.run(0x48BC0)
    assert [r(t, a) for a in [0x8081, 0x8085, 0x9C85, 0x9C86, 0x9C80]] == [old]*5
    assert r(t, 0x9C87) == 255
    w(t, 0x8080, 6)
    return t


def report(t):
    t.run(0x19414, 1)
    payload = bytes(r(t, 0x8EED+i) for i in range(8))
    e = ECUInteger(ECU)
    e.sr = 0xF0
    w(e, 0x734A, 0x80)
    w(e, 0x734C, 1)
    for i, value in enumerate(payload):
        w(e, 0x6ABC+i, value)
    e.run(0x35BB8)
    e.run(0x3585C)
    state = r(t, 0x8081)
    flags = [r(e, 0x6ACB+i) for i in range(6)]
    assert payload[0] >> 4 == state+1
    assert flags == [int(i == state) for i in range(6)]
    return {'accepted': state, 'candidate': r(t, 0x9C85), 'next': r(t, 0x9C86),
            'transition_code': r(t, 0x9C87), 'pending': r(t, 0x9C8A) & 1,
            'cached': r(t, 0x606F), 'can231': payload.hex(' '), 'ecu_flags': flags}


def main():
    cache_cases = 0
    for index, value in itertools.product([0, 0x12, 0x13, 0x10C, 0x10D, 0x110], range(256)):
        t = SHRelativeBranch(TCU)
        address = 0x605C+index if index < 0x10D else 0x626E+index-0x10D
        w(t, address-1, 0xA5);w(t, address+1, 0x5A)
        t.r[5] = value
        assert t.run(0x244FA, index) == 0
        assert r(t, address) == value
        assert t.run(0x24532, index) & 255 == value
        assert [r(t, address-1), r(t, address+1)] == [0xA5, 0x5A]
        cache_cases += 1

    matrix = []
    state_cases = 0
    for old, requested, block, override in itertools.product(range(6), range(6), [0, 4], range(2)):
        t = initialized(old)
        w(t, 0x8084, requested)
        w(t, 0x9545, block)
        w(t, 0x916C, override)
        next_state = requested if override else old+(requested > old)-(requested < old)
        expected = old if block else next_state
        t.run(0x48C08)
        assert r(t, 0x9C85) == requested
        assert r(t, 0x9C86) == r(t, 0x8085) == next_state
        assert r(t, 0x8081) == r(t, 0x606F) == expected
        assert bool(r(t, 0x9C8A) & 1) == bool(block and next_state != old)
        row = report(t)
        assert 0x48F58 in t.visited if not block and expected != old else True
        if not block and not override:
            matrix.append({'old': old, 'requested': requested, **row})
        state_cases += 1

    admission = []
    t = initialized(0)
    w(t, 0x8084, 5)
    for call, blocked in enumerate([4, 4, 0, 0, 0, 0, 0], 1):
        w(t, 0x9545, blocked)
        t.run(0x48C08)
        row = report(t)
        assert row['accepted'] == max(0, call-2)
        admission.append({'call': call, 'gate9545': blocked, **row})

    delay = []
    for gate9410, low_input, duration in [(0, -5121, 37), (4, 0, 18)]:
        t = initialized(0)
        w(t, 0x8084, 1)
        w(t, 0x9340, low_input, 2)
        w(t, 0x9410, gate9410)
        for tick in [0, duration-1, duration, duration+1]:
            w(t, 0x815F, tick)
            t.run(0x48C08)
            row = report(t)
            # 9410 also participates in later acceptance; only37-count path
            # is asserted to accept immediately when the candidate releases.
            assert r(t, 0x9C74) == (255 if tick < duration else 1)
            if gate9410 == 0:
                assert row['accepted'] == int(tick >= duration)
            delay.append({'timer_fixture': tick, 'configured_delay': duration,
                          'gate9410': gate9410, 'source9340': low_input,
                          'candidate_return9c74': r(t, 0x9C74), **row})

    # The always-blocking9545 condition dominates the916C bypass in48174.
    admission_cases = 0
    for transition, code, block, override in itertools.product(range(30), range(28), [0, 4], range(2)):
        if not block and not override:
            continue  # Detailed normal transition-dependent gates are separate work.
        t = SHRelativeBranch(TCU)
        w(t, 0x9545, block);w(t, 0x916C, override)
        t.r[5] = code
        value = t.run(0x48174, transition)
        assert value == (0 if block else 1)
        admission_cases += 1

    print(json.dumps({'scope': __doc__.strip(), 'cache_cases': cache_cases,
                      'paired_state_cases': state_cases, 'admission_gate_cases': admission_cases,
                      'stock_one_step_matrix': matrix, 'blocked_then_admitted': admission,
                      'delayed_candidates': delay,
                      'limits': 'Other RAM inputs start atzero;48BC0 initializes statefromcache. Gateproducers andclockunits unproved.8081 is accepted softwarestate, not proof of mechanically attainedgear. Full44CFE candidate calculation remains outside this verifier.'}, indent=2))


if __name__ == '__main__':
    main()
