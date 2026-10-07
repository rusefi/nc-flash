"""Original three limit producers and a seven-call production caller segment.

Stock finite RTZ behavior; physical units and full task scheduling remain open.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

import verify_control_contributions as prior
import verify_control_normalized_inputs as inputs
import verify_control_normalized_contribution as downstream
import verify_control_magnitude as magnitude
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_model_sources import lookup1
from verify_control_sources import sample_points

ROOT = Path(__file__).resolve().parent


def separated(first, second):
    tolerance = number(0x314CC)
    return first < q(second - tolerance) or first > q(second + tolerance)


def accumulator_limit(e):
    want = 0
    if r(e, 0x6938) == 1:
        want = lookup1(0xA38DC, rf(e, 0x67DC))
        if r(e, 0x67C4) != 0:
            want = min(want, number(0xDB1E0))
    run(e, 0x314F8)
    assert rf(e, 0x6814) == want


def factor(e):
    want = rf(e, 0x6810)
    if separated(number(0xDB1F4), number(0xDB1F0)):
        ratio = q(q(rf(e, 0x6DB4) - number(0xDB1F0)) /
                  q(number(0xDB1F4) - number(0xDB1F0)))
        want = inputs.clamp(ratio, number(0xDB1F8), 1)
    run(e, 0x3140C)
    assert rf(e, 0x6810) == want == 1  # stock lower and upper are both one


def sum_limit(e):
    mode = r(e, 0x7016)
    active = r(e, 0x6910, 2) > 0
    base, old, scale = [rf(e, a) for a in [0x6814, 0x680C, 0x6810]]
    if r(e, 0x693D) == 0 and active:
        want, branch = 0, 'zero'
    elif mode == 0 and active:
        want, branch = q(base * lookup1(0xA37F8, rf(e, 0x682C))), 'curve'
    else:
        target = old
        if separated(number(0xDB1E4), number(0xDB1E8)):
            ratio = q(q(rf(e, 0x6DB4) - number(0xDB1E8)) /
                      q(number(0xDB1E4) - number(0xDB1E8)))
            ratio = inputs.clamp(ratio, number(0xDB1EC), 1 if mode == 0 else scale)
            target = q(base * ratio)
        if mode == 0:
            want, branch = min(q(old + number(0xDB1DC)), target), 'slew'
        elif r(e, 0x7010) == 1:
            want, branch = q(base * scale), 'mode_override'
        else:
            want, branch = target, 'target'
    run(e, 0x31318)
    assert rf(e, 0x680C) == want, (branch, want, rf(e, 0x680C))
    return branch


def segment(e):
    accumulator_limit(e)
    for index in range(3):
        inputs.term(e, index)
    factor(e)
    sum_limit(e)
    inputs.summed(e)


def direct():
    counts = dict(accumulator=0, factor=0, sum=0, caller=0)
    branches = {}
    for flag, cap, value in itertools.product([0, 1, 2, 255], [0, 1, 255], sample_points(0xA38DC)):
        e = fixture(); w(e, 0x6938, flag); w(e, 0x67C4, cap); f(e, 0x67DC, value)
        accumulator_limit(e); counts['accumulator'] += 1
    for value, old in itertools.product([-100, 0, 499, 500, 501, 550, 800, 1000], [-10, 0, 1, 100]):
        e = fixture(); f(e, 0x6DB4, value); f(e, 0x6810, old)
        factor(e); counts['factor'] += 1
    for mode, timer, gate, override, value, old in itertools.product(
            [0, 1, 2, 255], [0, 1, 65535], [0, 1, 2], [0, 1, 2],
            [400, 500, 505, 525, 550, 600], [0, 1, 100]):
        e = fixture()
        for a, v in [(0x7016, mode), (0x693D, gate), (0x7010, override)]: w(e, a, v)
        w(e, 0x6910, timer, 2)
        for a, v in [(0x6814, 50), (0x680C, old), (0x6810, 1), (0x682C, q(1/2)), (0x6DB4, value)]: f(e, a, v)
        branch = sum_limit(e); branches[branch] = branches.get(branch, 0) + 1
        counts['sum'] += 1
    # Cover curve knots and nondefault factor input independently of3140C.
    for value, scale in itertools.product(sample_points(0xA37F8), [0, q(1/2), 2]):
        for mode in [0, 1]:
            e = fixture(); w(e, 0x7016, mode); w(e, 0x693D, 1); w(e, 0x6910, 1, 2)
            for a, v in [(0x6814, 20), (0x680C, 30), (0x6810, scale), (0x682C, value), (0x6DB4, 540)]: f(e, a, v)
            branch = sum_limit(e); branches[branch] = branches.get(branch, 0) + 1
            counts['sum'] += 1
    functions = [0x314F8, 0x3153A, 0x31598, 0x31606, 0x3140C, 0x31318, 0x312D4]
    for mode, timer, gate, inhibit in itertools.product([0, 1, 2], [0, 1], [0, 1], [0, 2]):
        e = fixture(); prepare(e)
        w(e, 0x7016, mode); w(e, 0x6910, timer, 2); w(e, 0x693D, gate); w(e, 0x7002, inhibit)
        f(e, 0x6800, 1); f(e, 0x6804, -1)
        other = copy.deepcopy(e); segment(e); pc = 0x187C2; sp = other.r[15]; seen = []
        for _ in range(100000):
            if pc == 0x187EC: break
            if pc in functions: seen.append(pc)
            nxt, delay = other.instruction(pc)
            if delay:
                _, nested = other.instruction(pc + 2); assert not nested
            pc = nxt
        else: raise AssertionError('caller instruction bound')
        assert seen == functions and other.r[15] == sp
        assert other.sr & 0xF0 == e.sr & 0xF0
        assert [r(other, a, 4) for a in [0x6814, 0x6818, 0x6820, 0x6824, 0x6810, 0x680C, 0x6808]] == [r(e, a, 4) for a in [0x6814, 0x6818, 0x6820, 0x6824, 0x6810, 0x680C, 0x6808]]
        counts['caller'] += 1
    return counts, branches


def prepare(e):
    inputs.prepare(e)
    for a, v in [(0x6814, 0), (0x6810, 0), (0x680C, 0), (0x67DC, 2000), (0x6DB4, 540), (0x682C, q(1/2))]: f(e, a, v)
    for a, v in [(0x6938, 1), (0x67C4, 1), (0x693D, 1)]: w(e, a, v)
    w(e, 0x6910, 0, 2)


def step(e, call):
    f(e, 0x67FC, 8 if call <= 20 else 10 if call <= 100 else 6 if call <= 180 else 11)
    f(e, 0x684C, 0 if call <= 20 or 141 <= call <= 220 else 100)
    # Inhibit while the uninhibited sum is positive, unlike the prior replay.
    w(e, 0x7002, 2 if 61 <= call <= 70 else 0)
    inputs.error(e); inputs.difference(e); segment(e); inputs.publish(e)
    update, divisor = downstream.group(e)
    row = magnitude.integrated_step(e, call)
    row.update(input_limits=[float(rf(e, a)) for a in [0x6814, 0x6810, 0x680C]],
               upstream_terms=[float(rf(e, a)) for a in [0x6818, 0x6820, 0x6824]],
               upstream_inhibit=r(e, 0x7002), published6cc8=float(rf(e, 0x6CC8)),
               normalized_contribution=float(rf(e, 0x8118)), normalized_updated=update,
               normalized_divisor=float(divisor))
    return row


def main():
    counts, branches = direct(); print('Direct:', counts, branches, flush=True)
    rows, boundaries = prior.lifecycle(prepare=prepare, upstream=step, checkpoints={20, 21, 60, 61, 70, 71, 100, 101, 180, 181})
    inhibited = [row for row in rows if 61 <= row['call'] <= 70]
    assert inhibited and all(row['published6cc8'] == 0 and sum(row['upstream_terms']) > 0 for row in inhibited)
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                  tcu_sha256=hashlib.sha256(TCU).hexdigest(), direct=counts, sum_branches=branches,
                  serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320,
                  lifecycle=rows)
    (ROOT / 'control-input-limits-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Retained:', 320, 'paired:', len(boundaries), flush=True)


if __name__ == '__main__': main()
