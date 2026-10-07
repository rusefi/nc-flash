"""Execute original 30DBA/30DE2/33BAC before the verified 30FB6 target.

Finite RTZ inputs, independent arithmetic/map oracles, original caller slice
and explicit paired scheduling. No physical loop identity or cadence claim.
"""
import copy
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
import verify_control_upstream_target as upstream
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_throttle_candidate import protected
from verify_model_sources import lookup1
from verify_control_sources import sample_points
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent
MAPS = [0xA3834, 0xA3840, 0xA384C, 0xA3858]
OUTPUTS = [0x67F4, 0x67F8, 0x6908, 0x690C]


def active_gate(e):
    want = int((r(e, 0x6943) == 1 or r(e, 0x6944) == 1 or r(e, 0x695B) & 8)
        and r(e, 0x7346) == 1 and ECU[0xDB0C0] == 1)
    run(e, 0x31E56)
    assert r(e, 0x6940) == want == 0  # This exact stock image has DB0C0=0.


def inhibit(e):
    want = int(r(e, 0x6561) == 1 or r(e, 0x65AA) == 1)
    run(e, 0x30DBA)
    assert r(e, 0x6954) == want


def model(e):
    bits = r(e, 0x2160, 4)
    check = ~((bits >> 16) + (bits & 65535)) & 65535
    valid = check in [r(e, 0x2164, 2), r(e, 0x2166, 2)]
    mapped = lookup1(0xA3900, rf(e, 0x2160) if valid else number(0xDB240))
    delta = q(mapped - rf(e, 0x67C8))
    a, b, flags, stop, active, mode, other = [r(e, k) for k in
        [0x6943, 0x6944, 0x695B, 0x6954, 0x6940, 0x67CC, 0x7247]]
    value, branch = rf(e, 0x67F4), 'retain_raw_gate'
    special = mode == 1 or other == 1
    if (a == b == 0 and not flags & 8) or stop == 1:
        value, branch = Fraction(0), 'clear'
    elif active:
        branch = 'deadband'
        if abs(delta) >= number(0xDB2A4):
            value = q(value + q(number(0xDB2A8) * delta))
            branch = 'increment'
    elif a == 1 or flags & 8:
        address = 0xA3840 if special else 0xA3834
        value, branch = lookup1(address, rf(e, 0x67E4)), hex(address)
    elif b == 1:
        address = 0xA3858 if special else 0xA384C
        value, branch = lookup1(address, rf(e, 0x67E4)), hex(address)
    return value, mapped, branch, valid


def adjustment(e):
    value, mapped, branch, valid = model(e)
    run(e, 0x30DE2)
    assert rf(e, 0x67F4) == value, (branch, rf(e, 0x67F4), value)
    assert rf(e, 0x67F8) == mapped
    if not valid:
        assert r(e, 0x534C, 4) == 0xFFFF2160
    return branch


def rates(e):
    special = r(e, 0x67CC) == 1 or r(e, 0x7247) == 1
    up = 0xDB224 if special else 0xDB220
    down = 0xDB22C if special else 0xDB230 if r(e, 0x6956) == 1 else 0xDB228
    run(e, 0x33BAC)
    assert rf(e, 0x6908) == number(up) and rf(e, 0x690C) == number(down)


def group(e):
    inhibit(e)
    branch = adjustment(e)
    rates(e)
    return branch


def setup():
    e = upstream.setup()
    f(e, 0x67C8, 100)
    for address in [0x6561, 0x65AA, 0x6940, 0x6954, 0x6956]:
        w(e, address, 0)
    return e


def direct():
    counts = dict(active_gate=0, inhibit=0, gates=0, maps=0, boundary=0, rates=0, protection=0, random=0, distance=0)
    branches = {}
    for a, b, flags, raw in itertools.product([0, 1, 2, 255], [0, 1, 2, 255], [0, 8, 247, 255], [0, 1, 2, 255]):
        e = setup()
        for address, value in zip([0x6943, 0x6944, 0x695B, 0x7346], [a, b, flags, raw]): w(e, address, value)
        w(e, 0x6940, 255); active_gate(e); counts['active_gate'] += 1
    for a, b in itertools.product([0, 1, 2, 127, 128, 255], repeat=2):
        e = setup(); w(e, 0x6561, a); w(e, 0x65AA, b)
        inhibit(e); counts['inhibit'] += 1
    for a, b, flag, stop, active, mode in itertools.product(
            [0, 1, 2, 255], [0, 1, 2, 255], [0, 8, 247, 255],
            [0, 1, 2, 255], [0, 1, 2, 255], [0, 1, 2]):
        e = setup()
        for address, value in zip([0x6943, 0x6944, 0x695B, 0x6954, 0x6940, 0x67CC], [a, b, flag, stop, active, mode]):
            w(e, address, value)
        branch = adjustment(e); branches[branch] = branches.get(branch, 0) + 1
        counts['gates'] += 1
    for address in MAPS:
        for x in sample_points(address):
            e = setup(); f(e, 0x67E4, x)
            w(e, 0x6943 if address in MAPS[:2] else 0x6944, 1)
            w(e, 0x7247, int(address in [0xA3840, 0xA3858]))
            assert adjustment(e) == hex(address)
            counts['maps'] += 1
    for x in sample_points(0xA3900):
        e = setup(); protected(e, 0x2160, x); w(e, 0x6943, 1); w(e, 0x6940, 1)
        adjustment(e); counts['maps'] += 1
    # Values straddle both inclusive deadband endpoints in binary32 at the
    # measured input, including one representable step on either side.
    mapped = lookup1(0xA3900, Fraction(95))
    measurements = []
    for sign in [-1, 1]:
        bits = rtz_bits(mapped + sign * number(0xDB2A4))
        measurements += [exact_value(bits + offset) for offset in [-1, 0, 1]]
    measurements += [mapped, mapped - 100, mapped + 100]
    for measured, old in itertools.product(measurements, [-1000, -1, 0, Fraction(1, 3), 1000]):
        e = setup(); f(e, 0x67C8, measured); f(e, 0x67F4, q(old))
        w(e, 0x6943, 1); w(e, 0x6940, 255)
        adjustment(e); counts['boundary'] += 1
    for a, b, selector in itertools.product([0, 1, 2, 255], repeat=3):
        e = setup()
        for address, value in zip([0x67CC, 0x7247, 0x6956], [a, b, selector]): w(e, address, value)
        rates(e)
        # Stock down-rate calibrations DB228 and DB230 coincide. Observe the
        # real branch to prove selection without editing either ROM value.
        pc = 0x33BAC; e.pr = 0xF0000000; seen = set(); sp = e.r[15]
        for _ in range(200):
            if pc == 0xF0000000: break
            seen.add(pc); nxt, delay = e.instruction(pc)
            if delay:
                _, nested = e.instruction(pc + 2); assert not nested
            pc = nxt
        else: raise AssertionError('rate bound')
        assert e.r[15] == sp
        expected = 0x33BCC if a == 1 or b == 1 else 0x33BF0 if selector == 1 else 0x33BF6
        assert seen & {0x33BCC, 0x33BF0, 0x33BF6} == {expected}
        counts['rates'] += 1
    for c1, c2 in itertools.product([False, True], repeat=2):
        e = setup(); protected(e, 0x2160, 40)
        if c1: w(e, 0x2164, r(e, 0x2164, 2) ^ 1, 2)
        if c2: w(e, 0x2166, r(e, 0x2166, 2) ^ 2, 2)
        # Observe the actual helper return as well as downstream map output;
        # equal stock map values must not conceal checksum fallback mistakes.
        check = copy.deepcopy(e); check.fr[4] = rtz_bits(number(0xDB240))
        sp, mask = check.r[15], check.sr & 0xF0
        check.run(0x15246, 0xFFFF2160)
        assert (check.r[15], check.sr & 0xF0) == (sp, mask)
        assert exact_value(check.fr[0]) == (number(0xDB240) if c1 and c2 else 40)
        w(e, 0x6943, 1); w(e, 0x6940, 1); adjustment(e)
        counts['protection'] += 1
    for a, b in itertools.product([-100, -1, 0, Fraction(1, 3), 1, 100], repeat=2):
        e = setup(); e.fr[4] = rtz_bits(a); e.fr[5] = rtz_bits(b)
        want = abs(q(exact_value(e.fr[4]) - exact_value(e.fr[5])))
        run(e, 0x2578); assert exact_value(e.fr[0]) == want
        counts['distance'] += 1
    rng = random.Random(0x30DE2)
    for _ in range(400):
        e = setup()
        for a in [0x6943, 0x6944, 0x6954, 0x6940, 0x67CC, 0x7247]: w(e, a, rng.choice([0, 1, 2, 255]))
        w(e, 0x695B, rng.randrange(256))
        for a in [0x67E4, 0x67C8, 0x67F4]: f(e, a, Fraction(rng.randrange(-10000, 10000), 8))
        adjustment(e); counts['random'] += 1
    assert set(branches) == {'clear', 'increment', 'retain_raw_gate', *(hex(a) for a in MAPS)}
    return counts, branches


def caller_cases(include_gate=False):
    count = 0
    for gate, active, stop, mode in itertools.product([0, 1, 2], [0, 1], [0, 1], [0, 1, 2]):
        e = setup()
        for a, v in [(0x6943, gate), (0x6940, active), (0x6561, stop), (0x7247, mode)]: w(e, a, v)
        w(e, 0x7346, active)
        other = copy.deepcopy(e)
        if include_gate: active_gate(e)
        group(e); upstream.target(e)
        pc = 0x1B558 if include_gate else 0x1B55E; sp = other.r[15]; seen = []
        for _ in range(100000):
            if pc == 0x1B576: break
            if pc in [0x31E56, 0x30DBA, 0x30DE2, 0x33BAC, 0x30FB6]: seen.append(pc)
            nxt, delay = other.instruction(pc)
            if delay:
                _, nested = other.instruction(pc + 2); assert not nested
            pc = nxt
        else: raise AssertionError('caller bound')
        assert seen == ([0x31E56] if include_gate else []) + [0x30DBA, 0x30DE2, 0x33BAC, 0x30FB6] and other.r[15] == sp
        for a in OUTPUTS + [a for _, a in upstream.MAP1 + upstream.MAP2] + [0x67F0, 0x6904, 0x69A4, 0x67FC]:
            assert r(e, a, 4) == r(other, a, 4), hex(a)
        for a, size in [(0x6940, 1), (0x6954, 1), (0x9642, 2), (0x9611, 1)]: assert r(e, a, size) == r(other, a, size)
        count += 1
    return count


def retained():
    e = setup(); rows = []; mapped = lookup1(0xA3900, Fraction(95))
    for call in range(1, 41):
        w(e, 0x6943, 2 if 25 <= call <= 28 else 1)
        w(e, 0x6940, int(5 <= call <= 24 or call >= 33))
        w(e, 0x6561, int(29 <= call <= 32))
        w(e, 0x67CC, int(call >= 17))
        f(e, 0x67C8, mapped - (10 if call <= 12 else Fraction(1, 2) if call <= 16 else -10))
        branch = group(e); target_branch = upstream.target(e)
        rows.append(dict(call=call, branch=branch, target_branch=target_branch,
            adjustment=float(rf(e, 0x67F4)), target=float(rf(e, 0x67F0)),
            output=float(rf(e, 0x67FC)), rise=float(rf(e, 0x6908)), fall=float(rf(e, 0x690C))))
    assert all(row['branch'] == 'deadband' for row in rows[12:16])
    assert all(row['adjustment'] == rows[11]['adjustment'] for row in rows[12:16])
    assert all(row['branch'] == 'retain_raw_gate' for row in rows[24:28])
    assert all(row['adjustment'] == rows[23]['adjustment'] for row in rows[24:28])
    assert all(row['adjustment'] == 0 for row in rows[28:32])
    assert rows[-1]['adjustment'] < 0
    return rows


def prepare(e):
    upstream.prepare(e)
    for a in [0x6561, 0x65AA, 0x6940, 0x6956]: w(e, a, 0)
    f(e, 0x67C8, 100)


def step(e, call, stock_gate=False):
    # Raw entry inputs are fixtures; adjustment, rates, target and downstream
    # contributions are executed, with no output replacement after setup.
    f(e, 0x6DB4, 299 if call <= 20 else 560 if call <= 100 else 540 if call <= 180 else 250 if call <= 220 else 600)
    f(e, 0x67E4, 600 if call <= 100 else 1200 if call <= 220 else 2400)
    mapped = lookup1(0xA3900, Fraction(95))
    f(e, 0x67C8, mapped - (2 if call <= 160 else -2))
    w(e, 0x6943, int(call <= 240)); w(e, 0x6944, int(call > 240))
    w(e, 0x6940, int(41 <= call <= 200)); w(e, 0x6561, int(201 <= call <= 220))
    w(e, 0x67CC, int(121 <= call <= 240)); w(e, 0x695B, 1)
    w(e, 0x7002, 2 if 61 <= call <= 70 else 0)
    if call == 101: w(e, 0x966C, 96); w(e, 0x9611, 5); w(e, 0x9642, 30000, 2)
    if call == 141: w(e, 0x966C, 0)
    if stock_gate:
        w(e, 0x7346, int(41 <= call <= 200))
        active_gate(e)
    branch = group(e); target_branch = upstream.target(e)
    s = upstream.secondary
    s.gates.timer(e); s.gates.segment(e); s.group(e); s.inputs.publish(e)
    update, divisor = s.downstream.group(e); row = s.magnitude.integrated_step(e, call)
    row.update(active6940=r(e, 0x6940), adjustment_branch=branch, adjustment=float(rf(e, 0x67F4)),
        mapped67f8=float(rf(e, 0x67F8)), rise=float(rf(e, 0x6908)), fall=float(rf(e, 0x690C)),
        target_branch=target_branch, target=float(rf(e, 0x67F0)), candidate=float(rf(e, 0x69A4)),
        produced67fc=float(rf(e, 0x67FC)), target_mode=r(e, 0x9611),
        secondary684c=float(rf(e, 0x684C)), published6cc8=float(rf(e, 0x6CC8)),
        normalized8118=float(rf(e, 0x8118)), normalized_updated=update, normalized_divisor=float(divisor))
    return row


def main():
    counts, branches = direct(); counts['caller_four'] = caller_cases(); counts['caller_five'] = caller_cases(True); history = retained()
    print('Direct', counts, flush=True)
    rows, boundaries = upstream.secondary.prior.lifecycle(prepare=prepare, upstream=step,
        checkpoints={20, 40, 41, 60, 61, 70, 71, 100, 101, 120, 121, 140, 141, 160, 161, 200, 201, 220, 221, 240, 241, 320})
    by_call = {row['call']: row for row in rows}
    assert by_call[101]['produced67fc'] == by_call[140]['produced67fc'] == 14.6484375
    assert by_call[201]['adjustment'] == by_call[220]['adjustment'] == 0
    stock_rows, stock_boundaries = upstream.secondary.prior.lifecycle(prepare=prepare,
        upstream=lambda e, call: step(e, call, stock_gate=True),
        checkpoints={40, 41, 100, 101, 120, 121, 140, 141, 160, 161, 200, 201, 220, 221, 240, 241, 320})
    assert all(row['active6940'] == 0 and row['adjustment_branch'] not in ['increment', 'deadband'] for row in stock_rows)
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts, branches=branches, retained=history, serial_cycles=320,
        paired_can_updates=len(boundaries), can211_latch_updates=320, lifecycle=rows,
        stock_gate=dict(calibration_db0c0=ECU[0xDB0C0], serial_cycles=320,
            paired_can_updates=len(stock_boundaries), can211_latch_updates=320, lifecycle=stock_rows))
    (ROOT / 'control-target-adjustment-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Integrated conditional gate', 320, len(boundaries), 'stock gate', 320, len(stock_boundaries), flush=True)


if __name__ == '__main__': main()
