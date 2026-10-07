"""Original target-following countdown/latches and filtered contribution.

Stock ROM only; exact finite RTZ body/caller assertions, retained scenarios,
and explicitly scheduled ECU/TCU replay. No physical DSC/cadence proof.
"""
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import verify_control_target_adjustment as adjustment
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, run
from verify_throttle_candidate import protected
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent


def reference(e):
    bits = r(e, 0x2160, 4)
    check = ~((bits >> 16) + (bits & 65535)) & 65535
    valid = check in [r(e, 0x2164, 2), r(e, 0x2166, 2)]
    return (rf(e, 0x2160) if valid else number(0xDB240)), valid


def first_model(e):
    enabled = bool(r(e, 0x73C4) & 16)
    other = r(e, 0x6E64)
    permissive = r(e, 0x7346) == 0 or (other == 0 and r(e, 0x7010) == 0)
    reset = not enabled or permissive
    timer = ECU[0xDB0C3] if reset else max(0, r(e, 0x692A) - 1)
    mode = ECU[0xDB0BF]; value = r(e, 0x693E); branch = 'hold'
    clear = (reset and (mode == 0 or (permissive and mode == 1))) or (other == 0 and mode == 2)
    read_reference = False
    if clear: value, branch = 0, 'clear'
    elif timer:
        read_reference = True
        ref, _ = reference(e)
        # CMP/HS compares sign-extended byte loads as unsigned 32-bit values.
        source = r(e, 0x717C); threshold = ECU[0xDB0CD]
        sx32 = lambda byte: byte if byte < 128 else byte + 0xFFFFFF00
        if ref <= number(0xDB238) and r(e, 0x695B) & 8 and (
                not r(e, 0x734A) & 64 or sx32(source) >= sx32(threshold)):
            value, branch = 1, 'set'
    return timer, value, branch, read_reference


def first(e):
    timer, value, branch, read_ref = first_model(e)
    _, valid = reference(e)
    run(e, 0x31C36)
    assert r(e, 0x692A) == timer and r(e, 0x693E) == value, (timer, value, branch)
    if read_ref and not valid: assert r(e, 0x534C, 4) == 0xFFFF2160
    return branch


def filtered(e):
    cal = number(0xDB18C if r(e, 0x6956) else 0xDB188)
    weight = q(1 - q(1 - cal))
    value, old = rf(e, 0x6808), rf(e, 0x6828)
    want = q(value + q(weight * q(old - value)))
    if abs(q(value - want)) < number(0x3172C): want = value
    run(e, 0x31662)
    assert rf(e, 0x6828) == want, (rf(e, 0x6828), want)


def second_model(e):
    upper = q(rf(e, 0x6814) * number(0xDB28C))
    lower = q(upper - number(0xDB290))
    timer = ECU[0xDB0C4] if r(e, 0x695B) & 16 else max(0, r(e, 0x692B) - 1)
    value = r(e, 0x693F); current = rf(e, 0x6828); branch = 'hold'
    read_ref = not (current >= upper and timer == 0)
    if not read_ref: value, branch = 0, 'clear'
    elif reference(e)[0] >= number(0xDB23C) and current <= lower: value, branch = 1, 'set'
    return timer, value, branch, read_ref


def second(e):
    timer, value, branch, read_ref = second_model(e)
    _, valid = reference(e)
    run(e, 0x31D8C)
    assert r(e, 0x692B) == timer and r(e, 0x693F) == value, (timer, value, branch)
    if read_ref and not valid: assert r(e, 0x534C, 4) == 0xFFFF2160
    return branch


def group(e):
    a = first(e); filtered(e); b = second(e)
    return a, b


def setup():
    e = adjustment.setup()
    for a, v in [(0x73C4, 16), (0x6E64, 0), (0x7346, 1), (0x7010, 1),
                 (0x692A, 20), (0x692B, 100), (0x693E, 0), (0x693F, 0),
                 (0x734A, 0), (0x717C, 3), (0x695B, 8)]: w(e, a, v)
    f(e, 0x6808, 0); f(e, 0x6828, 0); f(e, 0x6814, 20)
    return e


def neighbors(value):
    bits = rtz_bits(value)
    return [exact_value(bits - 1), exact_value(bits), exact_value(bits + 1)]


def direct():
    counts = dict(first_gates=0, first_boundaries=0, filter=0, second=0, protection=0)
    branches = {'first': set(), 'second': set()}
    for flags, a, b, c, timer, old in itertools.product([0, 16], [0, 1, 2, 255],
            [0, 1, 2, 255], [0, 1, 2, 255], [0, 1, 20, 255], [0, 1, 255]):
        e = setup()
        for address, value in zip([0x73C4, 0x7346, 0x6E64, 0x7010, 0x692A, 0x693E], [flags, a, b, c, timer, old]): w(e, address, value)
        branches['first'].add(first(e)); counts['first_gates'] += 1
    for ref, flag, extra, count, old in itertools.product(neighbors(number(0xDB238)),
            [0, 8], [0, 64], [0, 2, 3, 4, 127, 128, 255], [0, 1, 255]):
        e = setup(); protected(e, 0x2160, ref)
        for address, value in zip([0x695B, 0x734A, 0x717C, 0x693E], [flag, extra, count, old]): w(e, address, value)
        branches['first'].add(first(e)); counts['first_boundaries'] += 1
    for mode, value, old in itertools.product([0, 1, 2, 255], [-100, -1, 0, 1, 100],
            [-100, -1, 0, Fraction(1, 1024), Fraction(1, 512), 1, 100]):
        e = setup(); w(e, 0x6956, mode); f(e, 0x6808, value); f(e, 0x6828, old)
        filtered(e); counts['filter'] += 1
    for limit in [-20, 0, 20, 100]:
        upper = q(limit * number(0xDB28C)); lower = q(upper - number(0xDB290))
        samples = [q(upper + offset) for offset in [-1, 0, 1]] + [q(lower + offset) for offset in [-1, 0, 1]]
        for current, timer, flags, old, ref in itertools.product(samples, [0, 1, 2, 100], [0, 16],
                [0, 1, 255], neighbors(number(0xDB23C))):
            e = setup(); f(e, 0x6814, limit); f(e, 0x6828, current); protected(e, 0x2160, ref)
            for address, value in zip([0x692B, 0x695B, 0x693F], [timer, flags, old]): w(e, address, value)
            branches['second'].add(second(e)); counts['second'] += 1
    for c1, c2 in itertools.product([False, True], repeat=2):
        for fn, address, raw in [(first, 0x693E, 100), (second, 0x693F, 90)]:
            e = setup(); protected(e, 0x2160, raw)
            if c1: w(e, 0x2164, r(e, 0x2164, 2) ^ 1, 2)
            if c2: w(e, 0x2166, r(e, 0x2166, 2) ^ 2, 2)
            fn(e); assert r(e, address) == int(c1 and c2)
            counts['protection'] += 1
    assert branches == {'first': {'clear', 'set', 'hold'}, 'second': {'clear', 'set', 'hold'}}
    return counts


def caller_cases():
    count = 0
    for gate, mode, timer, history in itertools.product([0, 1, 2], [0, 1, 255], [0, 1, 20], [0, 1]):
        e = setup()
        for a, v in [(0x6943, gate), (0x6956, mode), (0x692A, timer), (0x692B, timer),
                     (0x693E, history), (0x693F, history)]: w(e, a, v)
        other = copy.deepcopy(e)
        adjustment.active_gate(e); adjustment.group(e); adjustment.upstream.target(e); group(e)
        pc = 0x1B558; sp = other.r[15]; seen = []
        ordered = [0x31E56, 0x30DBA, 0x30DE2, 0x33BAC, 0x30FB6, 0x31C36, 0x31662, 0x31D8C]
        for _ in range(100000):
            if pc == 0x1B588: break
            if pc in ordered: seen.append(pc)
            nxt, delay = other.instruction(pc)
            if delay:
                _, nested = other.instruction(pc + 2); assert not nested
            pc = nxt
        else: raise AssertionError('caller bound')
        assert seen == ordered and other.r[15] == sp
        for a in adjustment.OUTPUTS + [a for _, a in adjustment.upstream.MAP1 + adjustment.upstream.MAP2] + [0x67F0, 0x6904, 0x69A4, 0x67FC, 0x6828]:
            assert r(e, a, 4) == r(other, a, 4), hex(a)
        for a in [0x6940, 0x6954, 0x9611, 0x692A, 0x692B, 0x693E, 0x693F]: assert r(e, a) == r(other, a)
        assert r(e, 0x9642, 2) == r(other, 0x9642, 2)
        count += 1
    return count


def retained():
    rows = []; e = setup()
    for call in range(1, 131):
        # At1 reset counters;2..21 first counter expires without clearing its
        # latch. At22 permissive condition explicitly clears it. The second
        # latch stays set at expiry until its upper clear boundary is met.
        w(e, 0x73C4, 0 if call == 1 or call == 22 else 16)
        w(e, 0x695B, 24 if call == 1 else 8)
        f(e, 0x6828, 0 if call <= 110 else 20)
        a = first(e); b = second(e)
        rows.append(dict(call=call, first=a, second=b, timer_a=r(e, 0x692A), timer_b=r(e, 0x692B), latch_a=r(e, 0x693E), latch_b=r(e, 0x693F)))
    assert rows[1]['latch_a'] == 1 and rows[20]['timer_a'] == 0 and rows[20]['latch_a'] == 1
    assert rows[21]['latch_a'] == 0
    assert rows[100]['timer_b'] == 0 and rows[100]['latch_b'] == 1
    assert rows[110]['latch_b'] == 0
    return rows


def prepare(e):
    adjustment.prepare(e)
    for a, v in [(0x73C4, 16), (0x6E64, 0), (0x7346, 1), (0x7010, 1),
                 (0x692A, 20), (0x692B, 100), (0x693E, 0), (0x693F, 0), (0x717C, 3)]: w(e, a, v)
    f(e, 0x6828, 0)


def step(e, call, input_producer=None, mode_producer=None):
    f(e, 0x6DB4, 299 if call <= 20 else 560 if call <= 100 else 540 if call <= 180 else 250 if call <= 220 else 600)
    # Allow a separately verified upstream task producer to replace this raw
    # input fixture without duplicating the downstream replay pipeline.
    if input_producer is None:
        f(e, 0x67E4, 20 if call <= 100 else 40 if call <= 220 else 60)
    f(e, 0x67C8, 0)
    w(e, 0x6943, int(call <= 240)); w(e, 0x6944, int(call > 240))
    w(e, 0x6561, int(201 <= call <= 220)); w(e, 0x67CC, int(121 <= call <= 240))
    if mode_producer is None: w(e, 0x695B, 24 if call <= 10 else 8 if call <= 220 else 1)
    w(e, 0x73C4, 0 if call in [1, 221] else 16)
    if mode_producer is None: w(e, 0x6956, int(101 <= call <= 160))
    w(e, 0x7002, 2 if 61 <= call <= 70 else 0)
    if call == 101: w(e, 0x966C, 96); w(e, 0x9611, 5); w(e, 0x9642, 30000, 2)
    if call == 141: w(e, 0x966C, 0)
    if input_producer is not None: input_producer(e, call)
    adjustment.active_gate(e); adjustment.group(e); adjustment.upstream.target(e)
    a, b = group(e)  # Original contiguous task order; consumes prior6808/6814.
    consumed, limit = rf(e, 0x6808), rf(e, 0x6814)
    s = adjustment.upstream.secondary
    s.gates.timer(e)
    if mode_producer is not None: mode_producer(e, call)
    s.gates.segment(e); s.group(e); s.inputs.publish(e)
    update, divisor = s.downstream.group(e); row = s.magnitude.integrated_step(e, call)
    row.update(first_branch=a, second_branch=b, timer_a=r(e, 0x692A), timer_b=r(e, 0x692B),
        latch_a=r(e, 0x693E), latch_b=r(e, 0x693F), filtered6828=float(rf(e, 0x6828)),
        consumed6808=float(consumed), consumed6814=float(limit), adjustment=float(rf(e, 0x67F4)),
        produced67fc=float(rf(e, 0x67FC)), published6cc8=float(rf(e, 0x6CC8)),
        normalized8118=float(rf(e, 0x8118)))
    return row


def main():
    counts = direct(); counts['caller_eight'] = caller_cases(); history = retained()
    print('Direct', counts, flush=True)
    rows, boundaries = adjustment.upstream.secondary.prior.lifecycle(prepare=prepare, upstream=step,
        checkpoints={1, 2, 10, 11, 20, 21, 60, 61, 70, 71, 100, 101, 110, 120, 121, 140, 141, 160, 161, 200, 201, 220, 221, 240, 241, 320})
    assert any(row['adjustment'] < 0 for row in rows)
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts, retained=history, serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320, lifecycle=rows)
    (ROOT / 'control-target-followers-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Integrated', 320, len(boundaries), flush=True)


if __name__ == '__main__': main()
