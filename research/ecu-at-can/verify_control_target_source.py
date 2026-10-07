"""Original 30CE4/33C02/33C2A production of the target-map input67E4.

Stock calibrations, finite RTZ values and two original caller sites. Combined
replay explicitly orders separate task regions; no scheduler/physical claim.
"""
import copy
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
import verify_control_target_followers as followers
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, run
from verify_control_sources import sample_points
from verify_model_sources import lookup1
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent
OUTPUTS = [0x695C, 0x6960, 0x67E0, 0x68FC, 0x67E4]


def filter_value(value, old, coefficient, epsilon):
    retention = q(1 - q(1 - coefficient))
    result = q(value + q(retention * q(old - value)))
    return value if abs(q(value - result)) < epsilon else result


def extra_model(e):
    return q(max(0, q(rf(e, 0x6D20) - number(0xDB154))) * number(0xDB158))


def extra(e):
    want = extra_model(e)
    run(e, 0x33C02); assert rf(e, 0x6960) == want


def correction_model(value, old):
    filtered = filter_value(value, old, number(0xDB148), number(0x33CA4))
    return max(number(0xDB14C), min(number(0xDB150), filtered))


def correction(e):
    want = correction_model(rf(e, 0x695C), rf(e, 0x67E0))
    run(e, 0x33C2A); assert rf(e, 0x67E0) == want, (rf(e, 0x67E0), want)


def model(e):
    vals = {a: rf(e, a) for a in OUTPUTS}
    if r(e, 0x8F30):
        vals[0x68FC] = vals[0x67E4] = number(0xDB15C)
        return vals, 'fallback'
    vals[0x695C] = lookup1(0xA3804, rf(e, 0x6D5C))
    vals[0x6960] = extra_model(e)
    vals[0x67E0] = correction_model(vals[0x695C], rf(e, 0x67E0))
    vals[0x68FC] = q(q(rf(e, 0x6D40) + vals[0x67E0]) + vals[0x6960])
    if ECU[0xDB0C1] == 1 and rf(e, 0x6D20) > number(0xDB214) and r(e, 0x6920, 2) == 0:
        vals[0x67E4] = filter_value(vals[0x68FC], vals[0x67E4], number(0xDB210), number(0x30F20))
        branch = 'final_filter'
    else:
        vals[0x67E4] = vals[0x68FC]; branch = 'copy'
    return vals, branch


def source(e):
    want, branch = model(e)
    run(e, 0x30CE4)
    for a, v in want.items(): assert rf(e, a) == v, (hex(a), rf(e, a), v, branch)
    assert branch != 'final_filter'  # Stock DB0C1=0; do not claim this branch ran.
    return branch


def setup():
    e = followers.setup()
    for a, v in [(0x6D20, 80), (0x6D40, 10), (0x6D5C, 30), (0x67E0, 7),
                 (0x695C, 11), (0x6960, 3), (0x68FC, 23), (0x67E4, 40)]: f(e, a, v)
    w(e, 0x8F30, 0); w(e, 0x6920, 0, 2)
    return e


def direct():
    counts = dict(extra=0, correction=0, maps=0, gates=0, random=0)
    bits = rtz_bits(number(0xDB154))
    values = [exact_value(bits + d) for d in [-2, -1, 0, 1, 2]] + [-100, 0, 80, 90, 100, 1000]
    for value in values:
        e = setup(); f(e, 0x6D20, value); extra(e); counts['extra'] += 1
    for value, old in itertools.product([-100, 0, 7, 10, 16, 100],
            [-100, 0, 7, Fraction(14337, 2048), 10, 16, Fraction(32769, 2048), 100]):
        e = setup(); f(e, 0x695C, value); f(e, 0x67E0, old)
        correction(e); counts['correction'] += 1
    for axis, value, base, old in itertools.product(sample_points(0xA3804), [80, 100], [-10, 10, 50], [0, 7, 16, 30]):
        e = setup(); f(e, 0x6D5C, axis); f(e, 0x6D20, value); f(e, 0x6D40, base); f(e, 0x67E0, old)
        source(e); counts['maps'] += 1
    for inhibit, count, value in itertools.product([0, 1, 2, 127, 128, 255], [0, 1, 255, 256, 65535], [79, 80, 81, 100]):
        e = setup(); w(e, 0x8F30, inhibit); w(e, 0x6920, count, 2); f(e, 0x6D20, value)
        branch = source(e)
        assert branch == ('fallback' if inhibit else 'copy')
        counts['gates'] += 1
    rng = random.Random(0x30CE4)
    for _ in range(400):
        e = setup()
        for a in [0x6D20, 0x6D40, 0x6D5C, *OUTPUTS]: f(e, a, Fraction(rng.randrange(-8000, 8000), 8))
        w(e, 0x8F30, rng.choice([0, 0, 1, 2, 255])); w(e, 0x6920, rng.randrange(65536), 2)
        source(e); counts['random'] += 1
    return counts


def caller_cases():
    count = 0
    for start, stop in [(0x16A70, 0x16A76), (0x1C9B4, 0x1C9BA)]:
        for inhibit, value, axis in itertools.product([0, 1, 2], [80, 100], [0, 30, 90]):
            e = setup(); w(e, 0x8F30, inhibit); f(e, 0x6D20, value); f(e, 0x6D5C, axis)
            other = copy.deepcopy(e); source(e); pc = start; seen = []; sp = other.r[15]
            for _ in range(100000):
                if pc == stop: break
                if pc in [0x30CE4, 0x33C02, 0x33C2A]: seen.append(pc)
                nxt, delay = other.instruction(pc)
                if delay:
                    _, nested = other.instruction(pc + 2); assert not nested
                pc = nxt
            else: raise AssertionError('caller bound')
            assert seen == ([0x30CE4] if inhibit else [0x30CE4, 0x33C02, 0x33C2A])
            assert other.r[15] == sp
            for a in OUTPUTS: assert r(e, a, 4) == r(other, a, 4), hex(a)
            count += 1
    return count


def retained():
    e = setup(); rows = []
    for call in range(1, 81):
        f(e, 0x6D5C, 90 if call <= 40 else 0)
        f(e, 0x6D20, 80 if call <= 20 else 100)
        w(e, 0x8F30, 2 if 31 <= call <= 40 else 0)
        branch = source(e)
        row = dict(call=call, branch=branch, mapped=float(rf(e, 0x695C)),
            correction=float(rf(e, 0x67E0)), extra=float(rf(e, 0x6960)),
            combined=float(rf(e, 0x68FC)), produced67e4=float(rf(e, 0x67E4)))
        rows.append(row)
    for row in rows[30:40]:
        assert row['produced67e4'] == 66.25
        assert all(row[k] == rows[29][k] for k in ['mapped', 'correction', 'extra'])
    assert rows[20]['extra'] > 0 and rows[19]['extra'] == 0
    assert rows[40]['correction'] < rows[29]['correction']
    return rows


def prepare(e):
    followers.prepare(e)
    f(e, 0x67E0, 7); f(e, 0x6D40, 10); f(e, 0x6D5C, 30)
    w(e, 0x8F30, 0); w(e, 0x6920, 0, 2)


def input_step(e, call):
    # Raw upstream variables remain fixtures; this executed source replaces
    # the67E4 fixture before the target/follower/downstream sequence.
    f(e, 0x6D40, 10 if call <= 100 else 30 if call <= 220 else 50)
    f(e, 0x6D5C, 30 if call <= 160 else 90)
    f(e, 0x6D20, 80 if call <= 160 else 100)
    w(e, 0x8F30, 2 if 181 <= call <= 200 else 0)
    source(e)


def step(e, call):
    row = followers.step(e, call, input_producer=input_step)
    row.update(source_branch='fallback' if r(e, 0x8F30) else 'copy',
        produced67e4=float(rf(e, 0x67E4)), combined68fc=float(rf(e, 0x68FC)),
        correction67e0=float(rf(e, 0x67E0)), mapped695c=float(rf(e, 0x695C)), extra6960=float(rf(e, 0x6960)))
    return row


def main():
    counts = direct(); counts['caller'] = caller_cases(); history = retained()
    print('Direct', counts, flush=True)
    rows, boundaries = followers.adjustment.upstream.secondary.prior.lifecycle(prepare=prepare, upstream=step,
        checkpoints={20, 21, 60, 61, 70, 71, 100, 101, 120, 121, 140, 141, 160, 161, 180, 181, 200, 201, 220, 221, 240, 241, 320})
    by_call = {row['call']: row for row in rows}
    assert by_call[181]['produced67e4'] == by_call[200]['produced67e4'] == 66.25
    assert by_call[160]['extra6960'] == 0 and by_call[161]['extra6960'] > 0
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts, retained=history, serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320, lifecycle=rows)
    (ROOT / 'control-target-source-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Integrated', 320, len(boundaries), flush=True)


if __name__ == '__main__': main()
