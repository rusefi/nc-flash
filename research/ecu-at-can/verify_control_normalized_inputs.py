"""Execute seven upstream numeric bodies feeding the normalized contribution.

Finite RTZ models, protected-write checks and explicit retained scheduling.
Intervening production caller steps, physical units and DSC identity stay open.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import verify_control_contributions as prior
import verify_control_magnitude as magnitude
import verify_control_normalized_contribution as downstream
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_control_input_history import checksum

ROOT = Path(__file__).resolve().parent


def clamp(value, low, high):
    return low if value < low else high if value > high else value


def error(e):
    target = q(rf(e, 0x6CB4) + number(0xDB1D4))
    want = clamp(q(rf(e, 0x67FC) - target), number(0x31474), number(0x31470))
    run(e, 0x3127E)
    assert [rf(e, a) for a in [0x6964, 0x6800]] == [target, want]


def difference(e):
    current = rf(e, 0x6800)
    want = clamp(q(current - rf(e, 0x6970)), number(0x31474), number(0x31470))
    run(e, 0x312AA)
    assert [rf(e, a) for a in [0x6804, 0x6970]] == [want, current]


def term(e, index):
    shared = r(e, 0x6958) == 0 or r(e, 0x67CC) == 1 or r(e, 0x7247) == 1
    gain = number((0xDB190 if shared else 0xDB19C) + 4 * index)
    if shared:
        upper = number(0xDB1BC + 4 * index) if r(e, 0x6939) == 1 else number(0x316E4)
    else:
        upper = number(0xDB1C8 + 4 * index)
    source = rf(e, 0x6804 if index == 2 else 0x6800)
    want = clamp(q(source * gain), number(0x316F0), upper)
    address = [0x6818, 0x6820, 0x6824][index]
    if index == 1:
        want = clamp(q(rf(e, address) + want), 0, rf(e, 0x6814))
    run(e, [0x3153A, 0x31598, 0x31606][index])
    assert rf(e, address) == want, (index, shared, gain, source, upper, want, rf(e, address))
    if index == 0:
        checksum(e, address)


def summed(e):
    if r(e, 0x7002) != 0:
        want = 0
    else:
        value = q(q(rf(e, 0x6818) + rf(e, 0x6820)) + rf(e, 0x6824))
        want = clamp(value, 0, rf(e, 0x680C))
    run(e, 0x312D4)
    assert rf(e, 0x6808) == want


def publish(e):
    bits = r(e, 0x6808, 4)
    run(e, 0x399B0)
    assert r(e, 0x6CC8, 4) == bits
    checksum(e, 0x6CC8)


def group(e):
    error(e)
    difference(e)
    for index in range(3):
        term(e, index)
    summed(e)
    publish(e)


def direct():
    counts = dict(error=0, difference=0, terms=0, sum=0, publish=0)
    for target, measured in itertools.product([-100, 0, Fraction(1, 8), 8, 100], repeat=2):
        e = fixture()
        f(e, 0x6CB4, target); f(e, 0x67FC, measured)
        error(e); counts['error'] += 1
    for value, old in itertools.product([-3, Fraction(-5, 2), -1, 0, 1, Fraction(5, 2), 3], repeat=2):
        e = fixture()
        f(e, 0x6800, value); f(e, 0x6970, old)
        difference(e); counts['difference'] += 1
    for flags, value, old in itertools.product(itertools.product([0, 1, 2], repeat=4),
                                             [-100, -10, -1, 0, Fraction(1, 1024), 1, 10, 100],
                                             [0, Fraction(1, 2), 1]):
        e = fixture()
        for a, v in zip([0x6958, 0x67CC, 0x7247, 0x6939], flags): w(e, a, v)
        f(e, 0x6800, value); f(e, 0x6804, value)
        f(e, 0x6820, old); f(e, 0x6814, 1)
        for index in range(3): term(e, index); counts['terms'] += 1
    # Include cancellation-sensitive ordering and raw nonboolean inhibit values.
    vectors = list(itertools.product([-1, 0, 1], repeat=3))
    vectors += [(2**24, 1, -2**24), (2**24, -2**24, 1)]
    for values, limit, inhibit in itertools.product(vectors, [0, Fraction(1, 2), 10], [0, 1, 2, 255]):
        e = fixture()
        for a, v in zip([0x6818, 0x6820, 0x6824], values): f(e, a, v)
        f(e, 0x680C, limit); w(e, 0x7002, inhibit)
        summed(e); counts['sum'] += 1
    for mask, value in itertools.product([0x10, 0x30, 0xF0], [-100, 0, Fraction(1, 8), 100]):
        e = fixture(); e.sr = mask; f(e, 0x6808, value)
        publish(e); counts['publish'] += 1
    return counts


def prepare(e):
    downstream.prepare(e)
    for a, value in [(0x6970, 0), (0x6820, 0), (0x6814, 50), (0x680C, 80)]: f(e, a, value)
    for a, value in [(0x6958, 0), (0x67CC, 0), (0x7247, 0), (0x6939, 1), (0x7002, 0)]: w(e, a, value)


def step(e, call):
    # Input and limit sources remain explicit; no 6818 or 6CC8 output injection.
    f(e, 0x67FC, 8 if call <= 20 else 10 if call <= 100 else 6 if call <= 180 else 11)
    f(e, 0x684C, 0 if call <= 20 or 141 <= call <= 220 else 100)
    w(e, 0x7002, 2 if 121 <= call <= 140 else 0)
    group(e)
    update, divisor = downstream.group(e)
    row = magnitude.integrated_step(e, call)
    row.update(upstream_input=float(rf(e, 0x67FC)), upstream_target=float(rf(e, 0x6964)),
               upstream_error=float(rf(e, 0x6800)), upstream_difference=float(rf(e, 0x6804)),
               upstream_terms=[float(rf(e, a)) for a in [0x6818, 0x6820, 0x6824]],
               upstream_inhibit=r(e, 0x7002), published6cc8=float(rf(e, 0x6CC8)),
               normalized_contribution=float(rf(e, 0x8118)), normalized_updated=update,
               normalized_divisor=float(divisor))
    return row


def main():
    counts = direct()
    print('Direct:', counts, flush=True)
    rows, boundaries = prior.lifecycle(prepare=prepare, upstream=step,
                                      checkpoints={19, 20, 21, 22, 99, 100, 101, 102, 120, 121, 140, 141, 180, 181})
    assert all(row['upstream_terms'][2] == 0 for row in rows)
    assert all(row['published6cc8'] == 0 for row in rows if 121 <= row['call'] <= 140)
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                  tcu_sha256=hashlib.sha256(TCU).hexdigest(), direct=counts,
                  serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320,
                  lifecycle=rows)
    (ROOT / 'control-normalized-inputs-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Retained:', 320, 'paired:', len(boundaries), flush=True)


if __name__ == '__main__': main()
