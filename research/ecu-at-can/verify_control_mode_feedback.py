"""Original30202 mode selection/history and31BE6/31C0E word countdowns.

Finite stock execution and explicitly ordered feedback replay. Task cadence,
intervening caller bodies and physical DSC identification remain unproved.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_control_target_source as source
from verify_control_contributions import ECU, TCU, w, r, f, rf, number, run

ROOT = Path(__file__).resolve().parent


def model(e):
    current, a, b, c, d = [r(e, x) for x in [0x6560, 0x693B, 0x6945, 0x69BB, 0x69B9]]
    selector = r(e, 0x6956, 2)
    if not r(e, 0x73C4) & 16: selector = 0x00FF
    elif r(e, 0x695B) & 16 and r(e, 0x69AD) == 1 and current == 0: selector = 0x01FE
    if a == b == 0 and rf(e, 0x6D5C) >= number(0xDB218): mode = 128
    elif a == 0 and r(e, 0x694B) == 1: mode = 64
    elif a == 0 and r(e, 0x6948) == 1: mode = 32
    elif c == a == 0 and b == 1 and r(e, 0x693E) == 1 and r(e, 0x6914, 2) > 0 and current == 1: mode = 16
    elif c == a == 0 and b == 1 and r(e, 0x693F) == 1 and r(e, 0x6916, 2) > 0: mode = 8
    elif c == 1 and a == d == 0 and b == 1: mode = 4
    elif c == 1 and a == 0 and d == b == 1: mode = 2
    else: mode = 1
    return mode, selector, current


def mode(e):
    want, selector, history = model(e)
    run(e, 0x30202)
    assert (r(e, 0x695B), r(e, 0x6956, 2), r(e, 0x69AD)) == (want, selector, history)
    return want


def timers(e):
    for entry, flag, address, cal in [(0x31BE6, 16, 0x6914, 0xDB0D2), (0x31C0E, 8, 0x6916, 0xDB0D4)]:
        want = max(0, r(e, address, 2) - 1) if r(e, 0x695B) & flag else int.from_bytes(ECU[cal:cal+2], 'big')
        run(e, entry); assert r(e, address, 2) == want


def setup():
    e = source.setup()
    for a, value in [(0x6560, 1), (0x693B, 0), (0x6945, 1), (0x69BB, 0), (0x69B9, 0),
                     (0x694B, 0), (0x6948, 0), (0x693E, 1), (0x693F, 1), (0x69AD, 1), (0x695B, 16), (0x73C4, 16)]: w(e, a, value)
    w(e, 0x6956, 0x029C, 2)  # Preserve deliberately noncomplementary pair if no writer runs.
    w(e, 0x6914, 38, 2); w(e, 0x6916, 375, 2)
    return e


def direct():
    counts = dict(priority=0, raw=0, selector=0, timers=0, random=0); modes = set()
    addresses = [0x6560, 0x693B, 0x6945, 0x69BB, 0x69B9, 0x694B, 0x6948, 0x693E, 0x693F]
    for values in itertools.product([0, 1], repeat=len(addresses)):
        for level in [19, 20]:
            e = setup()
            for a, v in zip(addresses, values): w(e, a, v)
            f(e, 0x6D5C, level); modes.add(mode(e)); counts['priority'] += 1
    for address, value, timer in itertools.product(addresses, [0, 1, 2, 127, 128, 255], [0, 1, 65535]):
        e = setup(); w(e, address, value); w(e, 0x6914, timer, 2); w(e, 0x6916, timer, 2)
        mode(e); counts['raw'] += 1
    for flags, enabled, previous, current, pair in itertools.product(range(256), [0, 16], [0, 1, 2], [0, 1, 2], [0x00FF, 0x029C]):
        e = setup()
        for a, v in [(0x695B, flags), (0x73C4, enabled), (0x69AD, previous), (0x6560, current)]: w(e, a, v)
        w(e, 0x6956, pair, 2); mode(e); counts['selector'] += 1
    for flag, a, b in itertools.product([0, 1, 8, 16, 24, 255], [0, 1, 38, 255, 256, 65535], [0, 1, 375, 255, 256, 65535]):
        e = setup(); w(e, 0x695B, flag); w(e, 0x6914, a, 2); w(e, 0x6916, b, 2)
        timers(e); counts['timers'] += 1
    rng = random.Random(0x30202)
    for _ in range(300):
        e = setup()
        for address in addresses + [0x695B, 0x69AD, 0x73C4]: w(e, address, rng.choice([0, 1, 2, 16, 255]))
        for address in [0x6914, 0x6916, 0x6956]: w(e, address, rng.randrange(65536), 2)
        mode(e); counts['random'] += 1
    assert modes == {1, 2, 4, 8, 16, 32, 64, 128}
    return counts


def caller_cases():
    count = 0
    for flags, a, current in itertools.product([0, 1, 8, 16, 24, 255], [0, 1, 2], [0, 1, 2]):
        for start, stop, ordered in [(0x18774, 0x1877A, [0x30202]), (0x1C9B4, 0x1C9C6, [0x30CE4, 0x31BE6, 0x31C0E])]:
            e = setup(); w(e, 0x695B, flags); w(e, 0x693B, a); w(e, 0x6560, current)
            other = copy.deepcopy(e)
            if start == 0x18774: mode(e)
            else: source.source(e); timers(e)
            pc = start; seen = []; sp = other.r[15]
            for _ in range(100000):
                if pc == stop: break
                if pc in ordered: seen.append(pc)
                nxt, delay = other.instruction(pc)
                if delay:
                    _, nested = other.instruction(pc + 2); assert not nested
                pc = nxt
            else: raise AssertionError('caller bound')
            assert seen == ordered and other.r[15] == sp
            for a in source.OUTPUTS: assert r(e, a, 4) == r(other, a, 4)
            for a, size in [(0x695B, 1), (0x6956, 2), (0x69AD, 1), (0x6914, 2), (0x6916, 2)]: assert r(e, a, size) == r(other, a, size)
            count += 1
    return count


def retained():
    e = setup(); rows = []
    for call in range(1, 451):
        w(e, 0x6560, 0 if call >= 21 else 1)
        w(e, 0x73C4, 0 if call == 31 else 16)
        timers(e); selected = mode(e)
        rows.append(dict(call=call, mode=selected, selector=r(e, 0x6956, 2), timer_a=r(e, 0x6914, 2), timer_b=r(e, 0x6916, 2)))
    assert rows[20]['selector'] == 0x01FE and rows[20]['mode'] == 8
    assert rows[30]['selector'] == 0x00FF
    assert any(row['mode'] == 1 and row['timer_b'] == 0 for row in rows)
    return rows


def prepare(e):
    source.prepare(e)
    w(e, 0x695B, 1); w(e, 0x6956, 0x00FF, 2); w(e, 0x69AD, 0)
    w(e, 0x6914, 0, 2); w(e, 0x6916, 0, 2)


def input_step(e, call):
    source.input_step(e, call)
    timers(e)  # Original source + two timers order from1C9B4..1C9C6.
    w(e, 0x6943, 0); w(e, 0x6944, 0)  # Let produced mode select target branches.
    if call == 25: w(e, 0x73C4, 0)  # Raw requalification, not a latch/count output fixture.


def mode_step(e, call):
    # Raw admissions only: retain previous latch outputs and produced timers.
    for a, v in [(0x6560, int(30 <= call <= 50)), (0x693B, 0), (0x6945, 1),
                 (0x69BB, 0), (0x69B9, 0), (0x694B, int(241 <= call <= 250)),
                 (0x6948, int(251 <= call <= 260))]: w(e, a, v)
    mode(e)


def step(e, call):
    old_mode = r(e, 0x695B)
    row = source.followers.step(e, call, input_producer=input_step, mode_producer=mode_step)
    row.update(entry_mode=old_mode, next_mode=r(e, 0x695B), selector_pair=r(e, 0x6956, 2),
        timer_mode16=r(e, 0x6914, 2), timer_mode8=r(e, 0x6916, 2), produced67e4=float(rf(e, 0x67E4)))
    return row


def main():
    counts = direct(); counts['caller'] = caller_cases(); history = retained()
    print('Direct', counts, flush=True)
    rows, boundaries = source.followers.adjustment.upstream.secondary.prior.lifecycle(prepare=prepare, upstream=step,
        checkpoints={1, 2, 3, 20, 29, 30, 31, 50, 51, 52, 60, 61, 100, 101, 160, 161, 180, 181, 200, 201, 220, 221, 240, 241, 250, 251, 260, 261, 320})
    by_call = {row['call']: row for row in rows}
    assert by_call[30]['next_mode'] == 16
    assert by_call[51]['selector_pair'] == 0x01FE and by_call[51]['next_mode'] == 8
    result = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts, retained=history, serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320, lifecycle=rows)
    (ROOT / 'control-mode-feedback-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Integrated', 320, len(boundaries), 'modes', sorted({row['next_mode'] for row in rows}), flush=True)


if __name__ == '__main__': main()
