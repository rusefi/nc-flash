"""Original raw-input publishers feeding the ECU target calculation.

Independent finite RTZ and full application-RAM comparisons. Explicit call
order, RAM samples and cached D504 branch; no scheduler or sensor identity.
"""
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

import verify_control_target_source as target
from verify_control_contributions import ECU, w, r, f, rf, q, number, run
from sh_control_float import SHControlFloat
from verify_rtz_float import reference

ROOT = Path(__file__).resolve().parent


def setup():
    e = SHControlFloat(ECU)
    e.sr = 0xF0
    return e


def application(e):
    return {a: v for a, v in e.ram.items() if a >= 0xFFFF0000 and v}


def expected_write(memory, address, value, size):
    for i, byte in enumerate(value.to_bytes(size, 'big')):
        a = 0xFFFF0000 + address + i
        if byte:
            memory[a] = byte
        else:
            memory.pop(a, None)


def expected_float(memory, address, value, protected=False):
    bits = reference(value)
    expected_write(memory, address, bits, 4)
    if protected:
        check = ~((bits >> 16) + (bits & 65535)) & 65535
        for offset in [4, 6]:
            expected_write(memory, address + offset, check, 2)


def execute(e, entry, values):
    want = application(e)
    for address, value, protected in values:
        expected_float(want, address, value, protected)
    run(e, entry)
    actual = application(e)
    assert actual == want, (hex(entry), [(hex(a), actual.get(a, 0), want.get(a, 0))
        for a in actual.keys() | want.keys() if actual.get(a, 0) != want.get(a, 0)])


def first(e):
    fallback = r(e, 0x8EF8) != 0
    raw = rf(e, 0x40F4)
    a = number(0xB8144) if fallback else raw
    b = number(0xB8148) if fallback else raw
    c = b if fallback else max(a, number(0xB814C)) if r(e, 0x6565) == 1 else a
    values = [(0x6D20, a, True), (0x6D28, b, True), (0x6D38, c, True)]
    if r(e, 0x7016) == 0:
        values.append((0x6D30, a, True))
    execute(e, 0x39E7C, values)


def second(e):
    value = number(0xB8158) if r(e, 0x8F30) else rf(e, 0x40E0)
    values = [(0x6D40, value, True)]
    if r(e, 0x7016) == 0:
        values.append((0x6D48, value, False))
    execute(e, 0x39F48, values)


def selected(e):
    value = rf(e, 0x6D58)
    if r(e, 0x8EC6) == 1 or value > 65536:
        value = Fraction(0)
    history = [rf(e, 0x6D74 + 4*i) for i in range(6)]
    difference = q(q(abs(q(history[-1] - value)) * 20) / 3)
    values = [(0x6D5C, value, True), (0x6D68, difference, True)]
    values.extend((0x6D74 + 4*i, v, False) for i, v in enumerate([value] + history[:-1]))
    execute(e, 0x3A156, values)


def fallback_latch(e):
    want = application(e)
    addresses = [0x8F33, 0x8F34, 0x8F35, 0x8F36]
    if r(e, 0x9462) == 1 or r(e, 0x8F38) == 1:
        for address in addresses + [0x8F30]:
            expected_write(want, address, 0, 1)
    else:
        latches = [1 if r(e, 0x8F2C + i) == 0 else r(e, a)
                   for i, a in enumerate(addresses)]
        for address, value in zip(addresses, latches):
            expected_write(want, address, value, 1)
        if latches[2] == 1 or latches[3] == 1:
            expected_write(want, 0x8F30, 1, 1)
            expected_write(want, 0x8F37, 0, 1)
    run(e, 0x6D9E6)
    assert application(e) == want


def latch_cases():
    count = 0
    for mode, reset, inputs, old in itertools.product([0, 1, 2, 255], [0, 1, 2, 255],
            itertools.product([0, 2], repeat=4), [0, 1, 2, 255]):
        e = setup()
        for address, value in [(0x9462, mode), (0x8F38, reset),
                (0x8F30, old), (0x8F37, 255)]:
            w(e, address, value)
        for i in range(4):
            w(e, 0x8F2C + i, inputs[i]); w(e, 0x8F33 + i, old)
        fallback_latch(e); count += 1
    rng = random.Random(0x6D9E6)
    for _ in range(1024):
        e = setup()
        for address in [0x9462, 0x8F38, 0x8F30, 0x8F37] + list(range(0x8F2C, 0x8F30)) + list(range(0x8F33, 0x8F37)):
            w(e, address, rng.choice([0, 1, 2, 127, 128, 255]))
        fallback_latch(e); count += 1
    return count


def direct():
    counts = dict(first=0, second=0, selected=0, initialize=0)
    values = [-100, 0, Fraction(1, 8), 80, 100, 65536]
    threshold = number(0xB814C)
    values += [q(threshold - 1), threshold, q(threshold + 1)]
    for value, fallback, flag, hold in itertools.product(values, [0, 1, 2, 255],
                                                       [0, 1, 2, 255], [0, 1, 2, 255]):
        e = setup()
        f(e, 0x40F4, value); f(e, 0x6D30, -23)
        w(e, 0x8EF8, fallback); w(e, 0x6565, flag); w(e, 0x7016, hold)
        first(e); counts['first'] += 1
    for value, fallback, hold in itertools.product(values, range(256), [0, 1, 2, 255]):
        e = setup()
        f(e, 0x40E0, value); f(e, 0x6D48, -23)
        w(e, 0x8F30, fallback); w(e, 0x7016, hold)
        second(e); counts['second'] += 1
    for value, invalid, oldest in itertools.product(
            [-100, -1, 0, Fraction(1, 8), 100, Fraction(16777215, 256), 65536,
             Fraction(8388609, 128), 65537], range(256), [-100, 0, 100]):
        e = setup()
        f(e, 0x6D58, value); w(e, 0x8EC6, invalid)
        for i, v in enumerate([1, 2, 3, 4, 5, oldest]):
            f(e, 0x6D74 + 4*i, v)
        selected(e); counts['selected'] += 1
    for mask in [0x10, 0x30, 0xF0]:
        e = setup(); e.sr = mask
        execute(e, 0x39E74, [(0x6D30, 0, True)])
        execute(e, 0x3A044, [(0x6D5C, 0, True), (0x6D68, 0, True)])
        counts['initialize'] += 2
    return counts


def decode(raw):
    return max(0, q(q(raw * number(0x3A228)) - 100))


def can_source(e, a, b, enabled, mt, invalid, cached, fallback):
    # Actual original unpack/validity/selection bodies, with independent inputs.
    w(e, 0x7353, enabled); w(e, 0x734A, 0x40 if mt else 0x80)
    w(e, 0x8EC6, invalid); w(e, 0x4564, 0)
    f(e, 0x452C, cached); f(e, 0x6E18, fallback)
    w(e, 0x6AF4, a, 2); w(e, 0x6AF6, b, 2)
    run(e, 0x35FA6); run(e, 0x35EBA)
    bad_a, bad_b = enabled == 1 and a == 65535, enabled == 1 and b == 65535
    assert (r(e, 0x6B01), r(e, 0x6B02)) == (bad_a, bad_b)
    value = Fraction(cached if mt else fallback)
    if enabled == 1 and not (bad_a and bad_b):
        value = decode(b) if bad_a else decode(a) if bad_b else q(q(decode(a) + decode(b))/2)
    if invalid == 1:
        value = Fraction(65537)
    run(e, 0x3A05E)
    assert rf(e, 0x6D58) == value and rf(e, 0x6D64) == cached
    assert 0xD504 in e.visited
    selected(e)


def retained():
    e = setup()
    f(e, 0x67E0, 7)
    rows = []
    for call in range(1, 321):
        hold = 0 if call <= 20 or call >= 301 else 2
        w(e, 0x7016, hold)
        w(e, 0x8EF8, 255 if 101 <= call <= 120 else 0)
        w(e, 0x9462, 1 if call == 201 else 0)
        for i in range(4):
            w(e, 0x8F2C + i, 0 if i == 2 and call == 181 else 2)
        fallback_latch(e)
        assert r(e, 0x8F30) == int(181 <= call <= 200)
        w(e, 0x6565, 1 if call <= 160 else 2)
        f(e, 0x40F4, 80 if call <= 160 else 100)
        f(e, 0x40E0, 10 if call <= 100 else 30 if call <= 220 else 50)
        first(e); second(e)
        a = [10000, 12345, 65535, 40000][(call // 20) % 4]
        b = [14567, 65535, 65535, 20000][(call // 20) % 4]
        enabled = 0 if 221 <= call <= 280 else 1
        mt = 241 <= call <= 260
        invalid = 1 if 141 <= call <= 150 else 2 if 151 <= call <= 160 else 0
        fallback = 65537 if 261 <= call <= 280 else 23
        can_source(e, a, b, enabled, mt, invalid, 17, fallback)
        branch = target.source(e)
        if call <= 8 or call % 20 in [0, 1] or call in [140, 141, 150, 151, 160, 161]:
            rows.append(dict(call=call, raw_words=[a, b], can4b0_enabled=enabled,
                mt=mt, invalid=invalid, hold=hold, branch=branch,
                values={hex(a): float(rf(e, a)) for a in
                    [0x6D20, 0x6D28, 0x6D30, 0x6D38, 0x6D40, 0x6D48, 0x6D58,
                     0x6D5C, 0x6D68, 0x695C, 0x6960, 0x67E0, 0x68FC, 0x67E4]},
                history=[float(rf(e, 0x6D74 + 4*i)) for i in range(6)]))
    return rows


def main():
    counts = direct()
    counts['fallback_latch'] = latch_cases()
    print('Direct', counts, flush=True)
    rows = retained()
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(),
        direct=counts, retained_cycles=320, retained=rows,
        calibrations={hex(a): float(number(a)) for a in [0xB8144, 0xB8148, 0xB814C, 0xB8158]},
        limits='Finite normal/zero samples; explicit scheduling. 40E0/40F4, upstream flag writers, '
               'live D504 peripheral branch, CAN sender identity, units, remote DSC, '
               'TCU/roof integration and physical validation remain open.')
    (ROOT / 'control-raw-inputs-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Retained', 320, flush=True)


if __name__ == '__main__':
    main()
