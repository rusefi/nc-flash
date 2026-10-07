"""Original 684C production, retained shaping and diagnostic substitution.

Stock finite RTZ models; synthetic input/mode schedule. Physical meanings,
diagnostic-mode authorization and remote DSC/actuator behavior stay unproved.
"""
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import verify_control_input_gates as gates
from verify_control_input_gates import inputs, downstream, magnitude, prior
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_control_input_history import checksum
from verify_model_sources import lookup1, lookup2, map2_info
from verify_control_sources import sample_points
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent
CAP = number(0xDB784+4*((ECU[0xE2636]-1)&255))


def separated(a, b, tolerance):
    return a < q(b-tolerance) or a > q(b+tolerance)


def diagnostic_model(e, value):
    mode = r(e, 0x960E) if r(e, 0x966C)&64 else 0
    raw = r(e, 0x963C, 2)
    scale = number(0x8B9C8)
    if mode == 0:
        raw = max(0, min(65535, int(q(q(value/scale)+Fraction(1, 2)))))
    elif mode in [5, 7]:
        value = q(scale*raw)
    return value, raw, mode


def diagnostic(e, value):
    want, raw, mode = diagnostic_model(e, value)
    e.fr[4] = rtz_bits(value); run(e, 0x8B960)
    assert exact_value(e.fr[0]) == want
    assert r(e, 0x963C, 2) == raw and r(e, 0x960E) == mode


def target(e):
    close = not separated(rf(e, 0x6808), rf(e, 0x6814), number(0x319F4))
    if r(e, 0x69BB) == 1 and r(e, 0x69BA) == 1:
        want, branch = q(CAP*number(0xDB1FC)), 'special'
    elif r(e, 0x6938) == 0:
        want, branch = 0, 'disabled'
    elif close:
        want, branch = CAP, 'near_limit'
    else:
        want, branch = lookup2(0xA3A10, rf(e, 0x67DC), rf(e, 0x6808)), 'map'
    run(e, 0x318E4); assert rf(e, 0x683C) == want
    return branch


def filtered(e):
    value, old = rf(e, 0x683C), rf(e, 0x6840)
    weight = q(1-q(1-number(0xDB1A8)))
    want = q(value+q(weight*q(old-value)))
    if abs(q(value-want)) < number(0x31A2C): want = value
    run(e, 0x31964); assert rf(e, 0x6840) == want


def extrapolated(e):
    value, old = rf(e, 0x6840), rf(e, 0x6974)
    factor = number(0xDB1AC); divisor = q(1-factor)
    want = rf(e, 0x6844)
    if separated(divisor, 0, number(0x31A3C)):
        want = inputs.clamp(q(q(value-q(factor*old))/divisor), 0, CAP)
    run(e, 0x31986)
    assert rf(e, 0x6844) == want and rf(e, 0x6974) == value


def inhibit(e):
    want = int(rf(e, 0x67D4) >= number(0xDB170) or rf(e, 0x67D0) >= number(0xDB174))
    run(e, 0x307C0); assert r(e, 0x6937) == want


def scaled(e):
    lo, hi = number(0xDB1B0), number(0xDB1B4)
    want = rf(e, 0x6848)
    if separated(hi, lo, number(0x31B60)):
        factor = inputs.clamp(q(q(rf(e, 0x6DB4)-lo)/q(hi-lo)), number(0xDB1B8), 1)
        want = q(rf(e, 0x6844)*factor)
    run(e, 0x31A4C)
    assert rf(e, 0x6848) == want == rf(e, 0x6844)  # stock clamp1..1


def published(e):
    enabled = separated(rf(e, 0x6808), 0, number(0x31B84)) and r(e, 0x6937) != 1 and not r(e, 0x695B)&2
    first, second = rf(e, 0x6968), rf(e, 0x696C)
    if enabled:
        first, second = lookup1(0xA38E8, rf(e, 0x6848)), lookup1(0xA38F4, rf(e, 0x6DB4))
        candidate = min(inputs.clamp(first, 0, number(0x31BAC)), second)
    else:
        candidate = 0
    output, raw, mode = diagnostic_model(e, candidate)
    run(e, 0x31A9C)
    assert [rf(e, a) for a in [0x6968, 0x696C, 0x69A0, 0x684C]] == [first, second, candidate, output]
    assert r(e, 0x963C, 2) == raw and r(e, 0x960E) == mode
    checksum(e, 0x684C)
    return enabled


def group(e):
    branch = target(e); filtered(e); extrapolated(e); inhibit(e); scaled(e); enabled = published(e)
    return branch, enabled


def direct():
    counts = dict(diagnostic=0, target=0, filter=0, extrapolate=0, inhibit=0, scale=0, publish=0)
    scale = number(0x8B9C8)
    values = [-10, 0, Fraction(1, 3), 100, 200, 1000]
    values += [q(scale*q(n+Fraction(1, 2))) for n in [0, 1, 32767, 65534, 65535]]
    for mask, mode, raw, value in itertools.product([0, 63, 64, 255], [0, 1, 4, 5, 6, 7, 8, 255], [0, 1, 32768, 65535], values):
        e = fixture(); w(e, 0x966C, mask); w(e, 0x960E, mode); w(e, 0x963C, raw, 2)
        diagnostic(e, q(value)); counts['diagnostic'] += 1
    for first, second, gate, delta in itertools.product([0, 1, 2], [0, 1, 2], [0, 1, 2, 255],
            [-1, -number(0x319F4), 0, number(0x319F4), 1]):
        e = fixture(); w(e, 0x69BB, first); w(e, 0x69BA, second); w(e, 0x6938, gate)
        f(e, 0x6814, 50); f(e, 0x6808, q(50+delta)); f(e, 0x67DC, 1600)
        target(e); counts['target'] += 1
    xs, ys, _ = map2_info(0xA3A10)
    points = lambda xs: sorted(set([xs[0]-1, xs[-1]+1]+xs+[q((a+b)/2) for a,b in zip(xs,xs[1:])]))
    for x, y in itertools.product(points(xs), points(ys)):
        e = fixture(); w(e, 0x6938, 1); f(e, 0x67DC, x); f(e, 0x6808, y); f(e, 0x6814, 1000)
        target(e); counts['target'] += 1
    for value, old in itertools.product([-10, 0, Fraction(1, 65536), 1, CAP, 10], repeat=2):
        e = fixture(); f(e, 0x683C, value); f(e, 0x6840, old); filtered(e); counts['filter'] += 1
        f(e, 0x6840, value); f(e, 0x6974, old); f(e, 0x6844, -1)
        extrapolated(e); counts['extrapolate'] += 1
    for a, b in itertools.product(gates.neighbors(number(0xDB170)), gates.neighbors(number(0xDB174))):
        e = fixture(); f(e, 0x67D4, a); f(e, 0x67D0, b); inhibit(e); counts['inhibit'] += 1
    for value, source in itertools.product([-10, 0, CAP, 10], [-100, 0, 399, 400, 450, 500, 1000]):
        e = fixture(); f(e, 0x6844, value); f(e, 0x6DB4, source); scaled(e); counts['scale'] += 1
    for value, gate, flags, mode, mask in itertools.product(
            [-1, -number(0x31B84), 0, number(0x31B84), 1], [0, 1, 2, 255],
            [0, 1, 2, 3, 255], [0, 5, 7], [0, 64]):
        e = fixture()
        for a, v in [(0x6808, value), (0x6848, 2), (0x6DB4, 525), (0x6968, -7), (0x696C, -9)]: f(e, a, v)
        for a, v in [(0x6937, gate), (0x695B, flags), (0x960E, mode), (0x966C, mask)]: w(e, a, v)
        w(e, 0x963C, 30000, 2); published(e); counts['publish'] += 1
    for x, y in itertools.product(sample_points(0xA38E8), sample_points(0xA38F4)):
        e = fixture(); f(e, 0x6808, 1); f(e, 0x6848, x); f(e, 0x6DB4, y)
        published(e); counts['publish'] += 1
    return counts


def caller_cases(full=False):
    functions = [0x318E4, 0x31964, 0x31986, 0x307C0, 0x31A4C, 0x31A9C]
    addresses = [0x683C, 0x6840, 0x6974, 0x6844, 0x6848, 0x6968, 0x696C, 0x69A0, 0x684C]
    if full:
        functions = [0x30C04, 0x30860, 0x3127E, 0x312AA, 0x307EC, 0x30BA4, 0x3174C,
                     0x314F8, 0x3153A, 0x31598, 0x31606, 0x3140C, 0x31318, 0x312D4]+functions
        addresses += [0x67DC, 0x6964, 0x6800, 0x6804, 0x6970, 0x682C,
                      0x6814, 0x6818, 0x6820, 0x6824, 0x6810, 0x680C, 0x6808]
    count = 0
    for value, mode, mask, flags, special in itertools.product([0, 1, 50], [0, 5, 7], [0, 64], [0, 2], [0, 1]):
        e = fixture(); prepare(e)
        f(e, 0x6808, value); f(e, 0x6814, 50); f(e, 0x67DC, 1600); f(e, 0x6DB4, 525)
        f(e, 0x67FC, value+8)
        for a, v in [(0x6938, 1), (0x960E, mode), (0x966C, mask), (0x695B, flags), (0x69BB, special), (0x69BA, special)]: w(e, a, v)
        w(e, 0x963C, 30000, 2)
        other = copy.deepcopy(e)
        if full: gates.segment(e)
        group(e); pc = 0x18798 if full else 0x187EC; sp = other.r[15]; seen = []
        for _ in range(100000):
            if pc == 0x18810: break
            if pc in functions: seen.append(pc)
            nxt, delay = other.instruction(pc)
            if delay:
                _, nested = other.instruction(pc+2); assert not nested
            pc = nxt
        else: raise AssertionError('caller bound')
        assert seen == functions and other.r[15] == sp
        assert [r(e, a, 4) for a in addresses] == [r(other, a, 4) for a in addresses]
        assert [r(e, a, n) for a, n in [(0x6937, 1), (0x960E, 1), (0x963C, 2)]] == [r(other, a, n) for a, n in [(0x6937, 1), (0x960E, 1), (0x963C, 2)]]
        assert [r(e, a) for a in [0x6938, 0x6939, 0x693D]] == [r(other, a) for a in [0x6938, 0x6939, 0x693D]]
        checksum(other, 0x684C); count += 1
    return count


def prepare(e):
    gates.prepare(e)
    for a in [0x683C, 0x6840, 0x6974, 0x6844, 0x6848, 0x6968, 0x696C, 0x69A0, 0x684C, 0x67D4]: f(e, a, 0)
    for a in [0x69BB, 0x69BA, 0x6937, 0x695B, 0x960E, 0x966C]: w(e, a, 0)


def step(e, call):
    source = 299 if call <= 20 else 560 if call <= 100 else 540 if call <= 180 else 250 if call <= 220 else 600
    f(e, 0x6DB4, source); f(e, 0x67FC, 8 if call <= 20 else 10 if call <= 100 else 6 if call <= 180 else 11)
    w(e, 0x7002, 2 if 61 <= call <= 70 else 0)
    if call == 101: w(e, 0x966C, 64); w(e, 0x960E, 5); w(e, 0x963C, 30000, 2)
    if call == 141: w(e, 0x966C, 0)  # original helper clears retained mode
    gates.timer(e); gates.segment(e); branch, enabled = group(e); inputs.publish(e)
    update, divisor = downstream.group(e); row = magnitude.integrated_step(e, call)
    row.update(secondary_branch=branch, secondary_enabled=enabled,
               secondary_values=[float(rf(e, a)) for a in [0x683C, 0x6840, 0x6844, 0x6848, 0x69A0, 0x684C]],
               diagnostic_mode=r(e, 0x960E), diagnostic_raw=r(e, 0x963C, 2),
               published6cc8=float(rf(e, 0x6CC8)), normalized_contribution=float(rf(e, 0x8118)),
               secondary_history=float(rf(e, 0x8120)), secondary_latch=r(e, 0x812A),
               normalized_updated=update, normalized_divisor=float(divisor))
    return row


def check_lifecycle(rows):
    by_call = {row['call']: row for row in rows}
    for call in [101, 120, 140]:
        row = by_call[call]
        assert row['secondary_values'][-2:] == [0, 91.552734375]
        assert row['diagnostic_mode'] == 5 and row['published6cc8'] == 0
    assert by_call[120]['secondary_latch'] == 1 and by_call[120]['normalized_contribution'] > 0
    assert by_call[141]['secondary_values'][-1] == 0 and by_call[141]['diagnostic_mode'] == 0
    assert by_call[141]['secondary_history'] > 0 and by_call[141]['normalized_contribution'] > 0
    assert by_call[160]['secondary_latch'] == 0


def main():
    counts = direct(); counts['caller'] = caller_cases(); counts['caller_twenty'] = caller_cases(full=True)
    print('Direct', counts, flush=True)
    rows, boundaries = prior.lifecycle(prepare=prepare, upstream=step, checkpoints={20, 21, 60, 61, 70, 71, 100, 101, 120, 140, 141, 160, 180, 181, 220, 221})
    check_lifecycle(rows)
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                  direct=counts, serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320, lifecycle=rows)
    (ROOT/'control-secondary-path-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Retained', 320, 'paired', len(boundaries), flush=True)


if __name__ == '__main__': main()
