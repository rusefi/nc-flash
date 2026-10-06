"""Execute stock CAN211 conversion -> pattern selection -> cylinder mask.

Original instructions, bounded finite RTZ arithmetic and explicit scheduling.
This is not a peripheral, crank sensor, DSC or complete ECU simulation.
"""
from fractions import Fraction
import hashlib
import itertools
import json

from verify_model_sources import (ECU, SHModelFloat, initialize_sources, lookup2,
                                  MAPS, quadratic, rounded, number, w, r, f, rf)
from verify_spark_interaction import TRACTION, GATES
from sh_exact_float import exact_bits


def pattern(index, phase, selector=0, active=1):
    level = 0 if index == 0 else ECU[(0xC4FD4 if selector == 0 else 0xC4FD8)
                                    + min(index, ECU[0xE2630])-1]
    level = min(level, 7) if active else 0
    if level == 0:
        return 0
    if level == 7 or phase > 3:
        return 255
    return ECU[0xC4FBB + 4*((level-1)//2) + phase]


def flags(request, thresholds, old):
    h = number(0xC11F0)
    result = [1 if request >= t else 0 if request < rounded(t-h) else o
              for t, o in zip(thresholds, old)]
    result.append(int(rounded(request-number(0xC11F4)) > number(0x3FC3C)))
    return result


def index_from_flags(values):
    return next((i for i, v in enumerate(values) if v == 1), 4)


def source_case(x=2000, y=Fraction(1, 2), variant=0, command=25):
    e = initialize_sources(x=x, y=y, variant=variant)
    f(e, 0x7A84, command)
    e.run(0x3F35C)
    for branch, out, raw in [(1, 0x7124, 0x719C), (0, 0x711C, 0x7194),
                             (3 if variant == 1 else 2, 0x7128, 0x71A0)]:
        a, b, c = [lookup2(addr, x, y) for addr in MAPS[branch]]
        q = quadratic(a, b, c, command)
        total = rounded(rounded(q+rf(e, 0x71D0))+rf(e, 0x71D8))
        assert rf(e, raw) == q and rf(e, out) == total
    base = rf(e, 0x7128)
    assert [rf(e, a) for a in [0x712C, 0x7130, 0x7134]] == [
        rounded(rounded(base*n)/4) for n in [3, 2, 1]]
    return e


def event(e, event_id, advance=True):
    w(e, 0x6DF2, event_id)
    e.run(0x45D60)
    if advance:
        e.run(0x45E18)
    e.run(0x45E74)
    e.run(0x4603C)
    e.run(0x1F864)
    assert e.r[0] & 65535 == r(e, 0x736A, 2)


def main():
    counts = {}
    assert ECU[0xC11E6] == 0 and ECU[0xC4FB8] == 0
    assert number(0xC11F0) == 5 and ECU[0xCC187] == 7
    assert ECU[0xC4FC8] == 40
    producers = 0
    for x, y, variant, command in itertools.product(
            [500, 2250, 8000], [Fraction(0), Fraction(15, 32), Fraction(1)],
            [0, 1, 2], [0, 25, 50]):
        source_case(x, y, variant, command)
        producers += 1
    counts['threshold_producers'] = producers

    hysteresis = 0
    thresholds = [Fraction(60), Fraction(40), Fraction(20)]
    points = [Fraction(-1), Fraction(0), Fraction(3, 4), Fraction(97, 128),
              Fraction(49, 64), Fraction(100)]
    points += [t+delta for t in thresholds for delta in [-6, -5, -4, 0, 1]]
    for request, old in itertools.product(points, itertools.product([0, 1, 2], repeat=3)):
        e = SHModelFloat(ECU)
        f(e, 0x715C, request)
        for a, t in zip([0x712C, 0x7130, 0x7134], thresholds): f(e, a, t)
        for a, v in zip([0x7188, 0x7189, 0x718A], old): w(e, a, v)
        e.run(0x3FAFC)
        expected = flags(request, thresholds, old)
        assert [r(e, a) for a in [0x7188, 0x7189, 0x718A, 0x718B]] == expected
        e.run(0x3FD4C)
        assert r(e, 0x7181) == index_from_flags(expected)
        hysteresis += 1
    counts['hysteresis_and_priority'] = hysteresis

    selections = 0
    for old, gate in itertools.product(itertools.product([0, 1, 2], repeat=4), [0, 1, 2]):
        e = SHModelFloat(ECU)
        for a, v in zip([0x7188, 0x7189, 0x718A, 0x718B], old): w(e, a, v)
        w(e, 0x6590, gate)
        e.run(0x3FD4C); e.run(0x3FD9C)
        assert r(e, 0x7181) == index_from_flags(old)
        assert r(e, 0x7182) == (index_from_flags(old) if gate else 0)
        selections += 1
    counts['priority_and_enable'] = selections

    masks = 0
    for index, phase, selector, active in itertools.product(range(6), [0, 1, 2, 3, 4, 255],
                                                          [0, 1, 2], [0, 1, 2]):
        e = SHModelFloat(ECU)
        for a, v in [(0x7182, index), (0x74F2, phase), (0x6542, selector), (0x718C, active)]:
            w(e, a, v)
        e.run(0x40660)
        expected = pattern(index, phase, selector, active)
        assert r(e, 0x74F1) == expected
        assert r(e, 0x71F0) == (expected.bit_count() if active == 1 else 0)
        masks += 1
    counts['mask_and_count'] = masks

    phases = 0
    for level, countdown, position, phase in itertools.product(range(9), [0, 1, 2, 40, 255],
                                                              range(8), [0, 1, 2, 3, 4, 255]):
        e = SHModelFloat(ECU)
        for a, v in [(0x74F0, level), (0x74F3, countdown), (0x7492, position), (0x74F2, phase)]:
            w(e, a, v)
        expected = (0 if level not in range(1, 7) else 40 if countdown == 0
                    else countdown-1 if position == 7 else countdown)
        next_phase = ((0 if phase == 3 else (phase+1)&255) if expected == 0 else phase)
        e.run(0x462CA)
        assert (r(e, 0x74F3), r(e, 0x74F2)) == (expected, next_phase)
        phases += 1
    counts['phase_and_countdown'] = phases

    cycles = 0
    for gate, event_id, active, prior, position in itertools.product(
            [0, 1, 2], range(8), [0, 1, 2], [0, 1], range(8)):
        e = SHModelFloat(ECU)
        for a, v in [(0x6DFE, gate), (0x6DF2, event_id), (0x718C, active),
                     (0x749B, prior), (0x7492, position), (0x7493, 4), (0x7494, 3)]: w(e, a, v)
        e.run(0x45D60)
        cylinder = {2: 1, 0: 2, 4: 3, 6: 4}.get(event_id, 0) if gate == 1 else 4
        alternate = {0: 1, 6: 2, 2: 3, 4: 4}.get(event_id, 0) if gate == 1 else 3
        assert (r(e, 0x7493), r(e, 0x7494)) == (cylinder, alternate)
        expected = position
        if gate == 1 and cylinder:
            expected = 0 if active == 1 and prior == 0 else (position+1) % 8
        e.run(0x45E18)
        assert r(e, 0x7492) == expected
        cycles += 1
    counts['event_mapping_and_position'] = cycles

    samples = 0
    # Exhaust every pattern byte/position/cylinder, with other status bits and
    # an independent TCU inhibition already present. Recompute the shared mask.
    for mask, position, cylinder in itertools.product(range(256), range(8), range(1, 5)):
        e = SHModelFloat(ECU)
        for a, v in [(0x6DFE, 1), (0x718C, 1), (0xA488, 1), (0x7493, cylinder),
                     (0x7492, position), (0x74F1, mask), (0x78D3, 0x80)]: w(e, a, v)
        for c in range(1, 5): w(e, 0x749E+c, 0xE5)
        e.run(0x45E74)
        assert r(e, 0x749E+cylinder) == 0xA5  # clear old local inhibition
        selected = (mask >> position) & 1
        assert r(e, 0x749A) == selected and r(e, 0x749B) == 1
        e.run(0x4603C)
        assert [r(e, 0x749E+c) for c in range(1, 5)] == [
            0xA5 | (selected << 6) if c == cylinder else 0xE5 for c in range(1, 5)]
        expected = (15 & ~(1 << (cylinder-1))) | (selected << (cylinder-1)) | 8
        assert r(e, 0x736A, 2) == expected and r(e, 0x7368) == int(bool(expected))
        samples += 1
    counts['pattern_event_inhibition'] = samples

    history = 0
    for gate, cylinder, old, current, timer in itertools.product([0, 1, 2], [0, 1, 4],
                                                               [0, 1, 2], [0, 1, 2], [0, 1, 11]):
        e = SHModelFloat(ECU)
        for a, v in [(0x6DFE, gate), (0x7493, cylinder), (0x74EE, old),
                     (0x7534, current), (0x7498, timer), (0x749A, 2), (0x749B, 2)]: w(e, a, v)
        for c in range(1, 5): w(e, 0x749E+c, 0xE5)
        e.run(0x45E74); e.run(0x4603C)
        expected = (10 if old == 1 and current == 0 else max(timer-1, 0)) if gate == 1 else timer
        assert r(e, 0x7498) == expected
        assert r(e, 0x74EE) == (current if gate == 1 else old)
        assert [r(e, 0x749E+c) for c in range(1, 5)] == [
            0xA5 if gate == 1 and c == cylinder else 0xE5 for c in range(1, 5)]
        history += 1
    counts['sampling_gates_and_history'] = history

    rotations = []
    e = SHModelFloat(ECU)
    for a, v in [(0x7182, 1), (0x718C, 1), (0xA488, 1), (0x6DFE, 1)]: w(e, a, v)
    expected_phase, expected_timer = 0, 0
    for step in range(1280):
        e.run(0x40660)
        assert r(e, 0x74F1) == pattern(1, expected_phase)
        assert r(e, 0x71F0) == 2
        event(e, [2, 0, 4, 6][step % 4])
        pos = step % 8
        assert r(e, 0x7492) == pos
        expected_timer = 40 if expected_timer == 0 else expected_timer-1 if pos == 7 else expected_timer
        previous = expected_phase
        if expected_timer == 0: expected_phase = (expected_phase+1) % 4
        e.run(0x462CA)
        assert (r(e, 0x74F3), r(e, 0x74F2)) == (expected_timer, expected_phase)
        if expected_phase != previous:
            rotations.append({'event_call': step+1, 'next_phase': expected_phase})
    assert rotations == [{'event_call': 320*(i+1), 'next_phase': (i+1) % 4} for i in range(4)]
    counts['rotation_lifecycle_events'] = 1280

    paired = []
    for request, enabled, phase, tcu_mask in itertools.product([0, 10, 20, 40, 100],
                                                              [0, 1], range(4), [0, 5, 15]):
        e = source_case()
        for a, v in {**GATES, 0x734A: 0x80, 0x6590: enabled, 0xA488: 1,
                     0x6DFE: 1, 0x74F2: phase}.items(): w(e, a, v)
        f(e, 0x7140, 200)
        w(e, 0x6A10, 10000+request, 2)
        # Original receive/normalize/model conversion and active latch.
        for fn in TRACTION[:9]: e.run(fn)
        converted = rf(e, 0x715C)
        thresholds = [rf(e, a) for a in [0x712C, 0x7130, 0x7134]]
        expected_flags = flags(converted, thresholds, [0, 0, 0])
        for fn in [0x3FAFC, 0x3FD4C, 0x3FD9C, 0x40660]: e.run(fn)
        index = index_from_flags(expected_flags) if enabled else 0
        expected_pattern = pattern(index, phase, active=r(e, 0x718C))
        assert r(e, 0x7182) == index and r(e, 0x74F1) == expected_pattern
        assert r(e, 0x71F0) == expected_pattern.bit_count()
        for c in range(1, 5): w(e, 0x78CF+c, 0x80 if tcu_mask & (1 << (c-1)) else 0)
        trajectory = []
        local = [0]*4
        for step, event_id in enumerate([2, 0, 4, 6]*2):
            # Nonactive path starts by incrementing position; active entry resets.
            event(e, event_id)
            pos = step if r(e, 0x718C) == 1 else (step+1) % 8
            assert r(e, 0x7492) == pos
            c = {2: 1, 0: 2, 4: 3, 6: 4}[event_id]
            local[c-1] = (expected_pattern >> pos) & 1
            expected_mask = sum(bit << i for i, bit in enumerate(local)) | tcu_mask
            assert r(e, 0x736A, 2) == expected_mask
            trajectory.append({'position': pos, 'cylinder': c, 'mask': expected_mask})
        paired.append({'can211_word0': 10000+request, 'enabled': enabled, 'phase': phase,
                       'converted_request': float(converted), 'index': index,
                       'pattern': expected_pattern, 'count': r(e, 0x71F0),
                       'tcu_mask_fixture': tcu_mask, 'events': trajectory})
    counts['can211_to_event_mask'] = len(paired)
    result = {'ecu_sha256': hashlib.sha256(ECU).hexdigest(), 'counts': counts,
              'paired_cases': paired, 'rotation_lifecycle': rotations,
              'limits': 'Explicit scheduling and RAM sources; TCU per-cylinder flags are fixtures. '
                        'No DSC sender attribution, physical timing, final output peripherals or roof behavior.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
