"""Original release-overlay history producer and naturally incremented timer.

Independent signed arithmetic/history and timer-wheel models. Scheduling ratios
are explicit fixtures, not milliseconds or a full application-task simulation.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_extract import SHExtract
from sh_subset import signed
from verify_tcu_release_thresholds import TCU, w, r, model, state
from verify_tcu_ascending_release import quotient

ROOT = Path(__file__).resolve().parent


def filtered(old, current, divisor):
    old, current = signed(old, 16), signed(current, 16)
    divisor = max(128, signed(divisor, 16))
    delta = current - old
    change = quotient(delta * 128, divisor)
    if delta and change == 0:
        change = 1 if delta > 0 else -1
    return (old + change) & 65535


def history_model(t):
    old = [r(t, 0x9BE0 + 2*i, 2) for i in range(5)]
    current = r(t, 0x80EA, 2)
    newest = filtered(old[0], current, TCU[0x7730E] * 128)
    history = [newest] + old[:4]
    delta = max(0, signed(history[4], 16) - signed(newest, 16))
    if not r(t, 0x92C5) & 4 or signed(newest, 16) < signed(current, 16):
        history, delta = [current] * 5, 0
    # Saturating signed32 addition plus the opposite bias cancels modulo2^32.
    return history, min(delta, 32767)


def history(t):
    want, axis = history_model(t)
    sp = t.r[15]; t.run(0x45BA0, limit=200000)
    assert t.r[15] == sp
    assert [r(t, 0x9BE0+2*i, 2) for i in range(5)] == want
    assert r(t, 0x9B66, 2) == axis, (want, axis, r(t, 0x9B66, 2))
    return axis


def release(t):
    want = model(t); sp = t.r[15]
    t.run(0x45AA4, limit=200000)
    assert state(t) == want
    assert t.r[15] == sp


def direct():
    counts = dict(extract=0, filter=0, history=0)
    for source, dest, same, sr in itertools.product(
            [0, 0xFFFFFFFF, 0x01234567, 0x89ABCDEF, 0x80000000],
            [0, 0xFFFFFFFF, 0x01234567, 0x89ABCDEF, 0x80000000], [False, True], [0xF0, 0x3F1]):
        n, m = 7, 7 if same else 6
        isa = SHExtract((0x200D | n << 8 | m << 4).to_bytes(2, 'big'))
        isa.r[n] = dest; isa.r[m] = source; isa.sr = sr
        before = list(isa.r)
        joined = before[m].to_bytes(4, 'big') + before[n].to_bytes(4, 'big')
        assert isa.instruction(0) == (2, False)
        assert isa.r[n] == int.from_bytes(joined[2:6], 'big') and isa.sr == sr
        assert all(isa.r[i] == before[i] for i in range(16) if i != n)
        counts['extract'] += 1
    t = SHExtract(TCU)
    for old, current, divisor in itertools.product(
            [-32768, -100, -1, 0, 1, 100, 32767], repeat=3):
        t.r[5] = current; t.r[6] = divisor
        assert t.run(0x10FAC, old) & 65535 == filtered(old, current, divisor)
        counts['filter'] += 1
    # Include stock divisor and minimum-step behavior explicitly.
    for old, current in itertools.product([-32768, -4, -1, 0, 1, 4, 32767], repeat=2):
        t.r[5] = current; t.r[6] = 512
        assert t.run(0x10FAC, old) & 65535 == filtered(old, current, 512)
        counts['filter'] += 1
    rng = random.Random(0x45BA0)
    for flags, current, old in itertools.product([0, 1, 4, 5, 255],
            [-32768, -1, 0, 1, 32767], [-32768, -1, 0, 1, 32767]):
        w(t, 0x92C5, flags); w(t, 0x80EA, current, 2)
        for i in range(5): w(t, 0x9BE0+2*i, old, 2)
        history(t); counts['history'] += 1
    for _ in range(1000):
        w(t, 0x92C5, rng.choice([0, 4, 255])); w(t, 0x80EA, rng.randrange(65536), 2)
        for i in range(5): w(t, 0x9BE0+2*i, rng.randrange(65536), 2)
        history(t); counts['history'] += 1
    return counts


def saturation_cases():
    t = SHExtract(TCU)
    rows = []
    for current, tail in [(0, 32766), (0, 32767), (-1, 32767), (-32768, 32767)]:
        w(t, 0x92C5, 4); w(t, 0x80EA, current, 2)
        for i in range(5): w(t, 0x9BE0+2*i, current, 2)
        w(t, 0x9BE6, tail, 2)
        axis = history(t)
        assert axis == min(tail-current, 32767)
        rows.append(dict(current=current, shifted_tail=tail, axis=axis))
    return rows


def fixture(snapshot):
    t = SHExtract(TCU)
    t.ram = {int(a, 16): v for a, v in snapshot['ram'].items()}
    for a, v in [(0x8080, 6), (0x8081, 2), (0x9BEA, 2), (0x9BF0, 6),
                 (0x8084, 2), (0x9330, 0), (0x9338, 0), (0x92D3, 0),
                 (0x92C5, 0), (0x8088, 0), (0x9B64, 0), (0x9889, 0),
                 (0x9B40, 0), (0x92D1, 0), (0x9B3D, 0), (0x92D5, 1)]: w(t, a, v)
    for a, v in [(0x80EA, 3000), (0x9B3E, 6400), (0x9B66, 32768), (0x92F4, 768)]: w(t, a, v, 2)
    return t


def timed(snapshot, phase, interval, mode):
    t = fixture(snapshot); t.run(0x11004); w(t, 0x8494, phase, 4); w(t, 0x8009, 1)
    release(t); assert r(t, 0x9B64) & 3 == 1
    # First release must reset a naturally nonzero counter.
    for _ in range(16): t.run(0x12386)
    before = r(t, 0x815D); assert before > 0
    w(t, 0x92D5, 0); release(t)
    assert r(t, 0x815D) == 0 and r(t, 0x9B64) & 3 == 3
    expected_timer = 0; transitions = []; threshold_tick = None
    for tick in range(1, 2001):
        old_phase = r(t, 0x8494, 4)
        if old_phase in [1, 5, 9, 13]: expected_timer = min(255, expected_timer + 1)
        t.run(0x12386)
        assert r(t, 0x815D) == expected_timer
        assert r(t, 0x8494, 4) == (phase + tick) % 16
        if expected_timer >= 122 and threshold_tick is None: threshold_tick = tick
        if tick % interval: continue
        if mode == 'accepted_fall' and tick >= 20: w(t, 0x8081, 1)
        if mode == 'cancel_restart':
            w(t, 0x92D5, 1 if 20 <= tick < 40 else 0)
        flags, timer = r(t, 0x9B64) & 3, expected_timer
        first_release = flags == 1 and r(t, 0x92D5) == 0
        release(t)
        if first_release:
            expected_timer = 0; threshold_tick = None
        assert r(t, 0x815D) == expected_timer
        newflags = r(t, 0x9B64) & 3
        if flags != newflags or tick in [interval, 480, 484, 488]:
            transitions.append(dict(tick=tick, timer_before=timer, timer_after=expected_timer,
                                    flags_before=flags, flags_after=newflags))
        if newflags == 0:
            if mode == 'accepted_fall': assert tick >= 20 and expected_timer < 122
            else:
                assert expected_timer >= 122 and threshold_tick is not None
                assert tick == ((threshold_tick + interval - 1)//interval)*interval
            break
    else: raise AssertionError('release never completed')
    return dict(initial_phase=phase, service_interval=interval, mode=mode,
                timer_before_first_release=before, threshold_tick=threshold_tick,
                release_tick=tick, release_timer=expected_timer, transitions=transitions)


def retained_history(snapshot):
    t = fixture(snapshot); w(t, 0x92C5, 4)
    for i in range(5): w(t, 0x9BE0+2*i, 10000, 2)
    rows = []
    for value, special in [(10000, 4), (8000, 4), (6000, 4), (4000, 4),
                           (4000, 4), (4000, 4), (5000, 4), (8000, 4),
                           (6000, 0), (4000, 4), (3000, 4)]:
        w(t, 0x80EA, value, 2); w(t, 0x92C5, special)
        axis = history(t); release(t)
        rows.append(dict(measurement=value, special=special, axis=axis,
                         history=[r(t, 0x9BE0+2*i, 2) for i in range(5)],
                         overlay=state(t)))
    assert any(row['axis'] > 0 for row in rows)
    return rows


def main():
    raw = (ROOT/'tcu-fault-selection-snapshots.json').read_bytes()
    snapshots = json.loads(raw)
    result = dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                  snapshots_sha256=hashlib.sha256(raw).hexdigest(), direct=direct())
    result['saturation'] = saturation_cases()
    print('Direct:', result['direct'], flush=True)
    result['timed'] = [timed(snapshots['150'], phase, interval, mode)
                       for phase, interval, mode in itertools.product([0, 1, 15], [1, 3, 7],
                                                   ['expiry', 'accepted_fall', 'cancel_restart'])]
    result['history'] = retained_history(snapshots['150'])
    (ROOT/'tcu-overlay-lifecycle-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Timed:', len(result['timed']), 'history:', len(result['history']), flush=True)


if __name__ == '__main__': main()
