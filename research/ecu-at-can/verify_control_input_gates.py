"""Six upstream ECU producers and original fourteen-call control segment.

Finite RTZ arithmetic, stock calibrations and explicit retained scheduling.
No DSC sender, physical input units or full application scheduler inferred.
"""
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import verify_control_input_limits as limits
from verify_control_input_limits import inputs, downstream, magnitude, prior
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_model_sources import lookup1, axis, position, interpolate
from verify_control_sources import sample_points
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent


def neighbors(value):
    bits = rtz_bits(value)
    assert value > 0
    return [exact_value(bits+i) for i in [-1, 0, 1]]


def scaled(e):
    want = q(rf(e, 0x6DB4)*number(0xDB144))
    run(e, 0x30C04)
    assert rf(e, 0x67DC) == want


def upper_gate(e):
    permit = (r(e, 0x7346) == 1 and r(e, 0x65D0) == 0) or ECU[0xDB0B8] != 0
    want = int(permit and rf(e, 0x67D0) >= number(0xDB1D8) and r(e, 0x6929) == 0)
    run(e, 0x30860)
    assert r(e, 0x6939) == want


def scale_gate(e):
    value, old = rf(e, 0x67DC), r(e, 0x6938)
    hi = number(0xDB180); lo = q(hi-number(0xDB184))
    want = 0 if value < lo else 1 if value >= hi else old
    run(e, 0x307EC)
    assert r(e, 0x6938) == want


def map_gate(e):
    value, axis, old = rf(e, 0x6DB4), rf(e, 0x6D20), r(e, 0x693D)
    hi = lookup1(0xA37E0, axis); lo = q(hi-lookup1(0xA37EC, axis))
    want = 0 if value < lo else 1 if value > hi and ECU[0xDB0B9] == 1 else old
    run(e, 0x30BA4)
    assert r(e, 0x693D) == want


def ratio(e):
    base = lookup1(0xA37E0, rf(e, 0x6D20))
    divisor = q(rf(e, 0x7020)-base)
    update = abs(divisor) > number(0x31888)
    want = inputs.clamp(q(q(rf(e, 0x6DB4)-base)/divisor), 0, 1) if update else rf(e, 0x682C)
    run(e, 0x3174C)
    assert rf(e, 0x682C) == want
    return update


def timer(e):
    if r(e, 0x7016) == 1:
        want = 0
    elif r(e, 0x73C4)&128:
        descriptor = 0xA37D4
        n = int.from_bytes(ECU[descriptor:descriptor+2], 'big')
        xp = int.from_bytes(ECU[descriptor+4:descriptor+8], 'big')
        vp = int.from_bytes(ECU[descriptor+8:descriptor+12], 'big')
        i, weight = position(axis(xp, n), rf(e, 0x6D20))
        a = int.from_bytes(ECU[vp+2*i:vp+2*i+2], 'big')
        b = int.from_bytes(ECU[vp+2*min(i+1, n-1):vp+2*min(i+1, n-1)+2], 'big')
        want = int(interpolate(a, b, weight)) & 65535
    else:
        want = max(0, r(e, 0x6910, 2)-1)
    run(e, 0x3181C)
    assert r(e, 0x6910, 2) == want


def segment(e):
    scaled(e); upper_gate(e); inputs.error(e); inputs.difference(e)
    scale_gate(e); map_gate(e); ratio(e); limits.segment(e)


def direct():
    counts = dict(scaled=0, upper_gate=0, scale_gate=0, map_gate=0, ratio=0, timer=0)
    for value in [-100, 0, Fraction(1, 8), 300, 350, 500, 540, 550, 800, 1100, 3000, 10000]:
        e = fixture(); f(e, 0x6DB4, value); scaled(e); counts['scaled'] += 1
    for gate, inhibit, other, value in itertools.product([0, 1, 2, 255], [0, 1, 2, 255],
            [0, 1, 2, 255], [0, *neighbors(number(0xDB1D8)), 100]):
        e = fixture()
        for a, v in [(0x7346, gate), (0x65D0, other), (0x6929, inhibit)]: w(e, a, v)
        f(e, 0x67D0, value); upper_gate(e); counts['upper_gate'] += 1
    hi = number(0xDB180); lo = q(hi-number(0xDB184))
    for old, value in itertools.product([0, 1, 2, 255], [-1, 0, *neighbors(lo), *neighbors(hi), 1000]):
        e = fixture(); w(e, 0x6938, old); f(e, 0x67DC, value)
        scale_gate(e); counts['scale_gate'] += 1
    for axis, old in itertools.product(sample_points(0xA37E0), [0, 1, 2, 255]):
        hi = lookup1(0xA37E0, axis); lo = q(hi-lookup1(0xA37EC, axis))
        for value in [-1, 0, *neighbors(lo), *neighbors(hi), 2000]:
            e = fixture(); f(e, 0x6D20, axis); f(e, 0x6DB4, value); w(e, 0x693D, old)
            map_gate(e); counts['map_gate'] += 1
    for axis in sample_points(0xA37E0):
        base = lookup1(0xA37E0, axis)
        for value, denominator, old in itertools.product(
                [0, base-1, base, base+1, base+1000], [0, *neighbors(base), base+1000], [-2, Fraction(1, 2), 2]):
            e = fixture()
            for a, v in [(0x6D20, axis), (0x6DB4, value), (0x7020, denominator), (0x682C, old)]: f(e, a, v)
            ratio(e); counts['ratio'] += 1
    for mode, flags, old, value in itertools.product([0, 1, 2, 255], [0, 1, 128, 255],
            [0, 1, 32768, 65535], sample_points(0xA37D4)):
        e = fixture(); w(e, 0x7016, mode); w(e, 0x73C4, flags); w(e, 0x6910, old, 2)
        f(e, 0x6D20, value); timer(e); counts['timer'] += 1
    return counts


def retained_timer():
    e = fixture(); w(e, 0x7016, 0); f(e, 0x6D20, 80); w(e, 0x73C4, 128)
    timer(e); assert r(e, 0x6910, 2) == 800; w(e, 0x73C4, 0)
    rows = []
    for call in range(1, 802):
        timer(e)
        if call in [1, 799, 800, 801]: rows.append(dict(call=call, count=r(e, 0x6910, 2)))
    return rows


def caller_cases():
    functions = [0x30C04, 0x30860, 0x3127E, 0x312AA, 0x307EC, 0x30BA4, 0x3174C,
                 0x314F8, 0x3153A, 0x31598, 0x31606, 0x3140C, 0x31318, 0x312D4]
    addresses = [0x67DC, 0x6964, 0x6800, 0x6804, 0x6970, 0x682C,
                 0x6814, 0x6818, 0x6820, 0x6824, 0x6810, 0x680C, 0x6808]
    count = 0
    for mode, timer, inhibit, value, old in itertools.product([0, 1, 2], [0, 1], [0, 2], [299, 540, 551], [0, 255]):
        e = fixture(); prepare(e)
        for a, v in [(0x7016, mode), (0x7002, inhibit), (0x6938, old), (0x693D, old)]: w(e, a, v)
        w(e, 0x6910, timer, 2); f(e, 0x6DB4, value); f(e, 0x67FC, 10)
        other = copy.deepcopy(e); segment(e); pc = 0x18798; sp = other.r[15]; seen = []
        for _ in range(100000):
            if pc == 0x187EC: break
            if pc in functions: seen.append(pc)
            nxt, delay = other.instruction(pc)
            if delay:
                _, nested = other.instruction(pc+2); assert not nested
            pc = nxt
        else: raise AssertionError('caller instruction bound')
        assert seen == functions and other.r[15] == sp
        assert [r(other, a, 4) for a in addresses] == [r(e, a, 4) for a in addresses]
        assert [r(other, a) for a in [0x6938, 0x6939, 0x693D]] == [r(e, a) for a in [0x6938, 0x6939, 0x693D]]
        count += 1
    return count


def prepare(e):
    limits.prepare(e)
    f(e, 0x7020, 1200); f(e, 0x6D20, 80); f(e, 0x67D0, 10)
    w(e, 0x6929, 0); w(e, 0x6938, 0); w(e, 0x693D, 0)
    w(e, 0x7016, 0); old_flags = r(e, 0x73C4); w(e, 0x73C4, 128)
    timer(e); w(e, 0x73C4, old_flags)


def step(e, call):
    # Upstream inputs and scheduling remain fixtures, while gates/scale/ratio
    # and the downstream limits are computed from original instructions.
    source = 299 if call <= 20 else 560 if call <= 100 else 540 if call <= 180 else 250 if call <= 220 else 600
    f(e, 0x6DB4, source)
    f(e, 0x67FC, 8 if call <= 20 else 10 if call <= 100 else 6 if call <= 180 else 11)
    f(e, 0x684C, 0 if call <= 20 or 141 <= call <= 220 else 100)
    w(e, 0x7002, 2 if 61 <= call <= 70 else 0)
    timer(e); segment(e); inputs.publish(e); update, divisor = downstream.group(e)
    row = magnitude.integrated_step(e, call)
    row.update(gate_inputs=dict(source=source, axis=float(rf(e, 0x6D20)), denominator=float(rf(e, 0x7020))),
               produced_scale=float(rf(e, 0x67DC)), produced_ratio=float(rf(e, 0x682C)),
               produced_gates=[r(e, a) for a in [0x6938, 0x6939, 0x693D]],
               produced_timer=r(e, 0x6910, 2), timer_mode=r(e, 0x7016),
               limits=[float(rf(e, a)) for a in [0x6814, 0x6810, 0x680C]],
               terms=[float(rf(e, a)) for a in [0x6818, 0x6820, 0x6824]],
               published6cc8=float(rf(e, 0x6CC8)), normalized_contribution=float(rf(e, 0x8118)),
               normalized_updated=update, normalized_divisor=float(divisor))
    return row


def main():
    counts = direct(); counts['caller'] = caller_cases(); print('Direct', counts, flush=True)
    rows, boundaries = prior.lifecycle(prepare=prepare, upstream=step, checkpoints={20, 21, 60, 61, 70, 71, 100, 101, 180, 181, 220, 221})
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                  tcu_sha256=hashlib.sha256(TCU).hexdigest(), direct=counts, serial_cycles=320,
                  paired_can_updates=len(boundaries), can211_latch_updates=320,
                  retained_timer=retained_timer(), lifecycle=rows)
    (ROOT/'control-input-gates-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Retained', 320, 'paired', len(boundaries), flush=True)


if __name__ == '__main__': main()
