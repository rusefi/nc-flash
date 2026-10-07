"""Original class0..2 stored adjustment update, spreading and consumers.

Stock integer/software arithmetic, full original bodies, retained records and
one caller slice. Raw measurements/error are fixtures; no persistence claim.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_tcu_stored_adjustments as stored
from verify_tcu_stored_adjustments import TCU, w, r, word, initialize
from sh_extract import SHExtract
from verify_tcu_request_maps import interpolate
from sh_subset import signed

ROOT = Path(__file__).resolve().parent
FLAG_BASE = 0x6165
WEIGHTS = {0: [(1, 109), (2, 90)], 1: [(0, 147), (2, 109)], 2: [(0, 166), (1, 147)]}


def clamp(x, lo=-80, hi=80): return max(lo, min(hi, x))


def classify(raw):
    value = signed(raw, 16) >> 7
    return 127 if value < 24 or value > 48 else 0 if value < 32 else 1 if value < 40 else 2


def slots(t): return [signed(r(t, 0x616A + 2*i, 2), 16) for i in range(15)]


def flags(t): return [r(t, FLAG_BASE + i) for i in range(3)]


def multiply(value, weight):
    product = signed(value, 32) * weight
    out = abs(product) // 128 * (-1 if product < 0 else 1)
    return clamp(out, -2147483648, 2147483647)


def spread_model(old, oldflags, group, value):
    group &= 255
    group = group if group in [0, 1] else 2
    out, seen = old.copy(), oldflags.copy()
    seen[group] = 1
    for target, weight in WEIGHTS[group]:
        if oldflags[target] == 0:
            out[target] = signed(multiply(value, weight), 16)
    return out, seen


def execute(t, address, argument=0):
    saved = t.r[8:16].copy(); macl = t.macl; sr = t.sr & ~0x301
    t.visited.clear(); result = t.run(address, argument, limit=300000)
    assert t.r[8:16] == saved and t.macl == macl and t.sr & ~0x301 == sr
    return result


def spread(t, group, value):
    want, seen = spread_model(slots(t), flags(t), group, value)
    t.r[5] = value & 0xFFFFFFFF
    execute(t, 0x36E90, group)
    assert slots(t) == want and flags(t) == seen, (group, value, slots(t), want)


def model(t):
    group = classify(r(t, 0x80EE, 2)); error = signed(r(t, 0x98DC, 2), 16)
    out, seen = slots(t), flags(t)
    delta = 1 if error > -527 else -1 if error < -701 else 0
    active = group != 127 and delta != 0
    if active:
        out[group] = clamp(out[group] + delta)
        out, seen = spread_model(out, seen, group, out[group])
        error = clamp(error - delta * 24, -30464, 30464)
    return out, seen, error, group, active


def update(t):
    want, seen, error, group, active = model(t)
    execute(t, 0x36D1A)
    assert slots(t) == want and flags(t) == seen
    assert signed(r(t, 0x98DC, 2), 16) == error
    assert (0x36E90 in t.visited) == (0x39F94 in t.visited) == active
    return group, active


def consumer_model(t):
    values = [(((value + 136) >> 1) & 255) * 256 for value in slots(t)[:3]]
    encoded = interpolate((r(t, 0x80EE, 2) * 2) & 65535, [28*256, 36*256, 44*256], values)
    return clamp(((encoded & 65535) >> 7) - 136) * 16


def consumers(t):
    before = slots(t); seen = flags(t)
    expected = consumer_model(t)
    actual = signed(execute(t, 0x36A74), 32)
    assert actual == expected, (before[:3], r(t, 0x80EE, 2), actual, expected)
    fixed = signed(execute(t, 0x36A0A), 32)
    assert fixed == clamp(before[2] * 16, -32768, 32767)
    assert slots(t) == before and flags(t) == seen
    return actual, fixed


def fixture():
    t = SHExtract(TCU); initialize(t)
    for a in range(FLAG_BASE, FLAG_BASE+3): w(t, a, 0)
    w(t, 0x80EE, 5500, 2); w(t, 0x98DC, 0, 2)
    return t


def direct():
    counts = dict(classify=0, spread=0, updater=0, accessors=0, uniform=0, consumer=0)
    t = fixture()
    samples = sorted({(x+d) & 65535 for x in range(0, 65536, 128) for d in [-1, 0, 1]})
    for raw in samples:
        w(t, 0x80EE, raw, 2)
        assert signed(execute(t, 0x36DBC), 32) == classify(raw)
        counts['classify'] += 1
    for group, value, flagvalues in itertools.product([0, 1, 2, 3, 255, 256, 257],
            [-2147483648, -32769, -80, -1, 0, 1, 80, 32768, 2147483647],
            list(itertools.product([0, 1, 255], repeat=3))):
        t = fixture()
        for i, value0 in enumerate([11, -22, 33]): w(t, 0x616A+2*i, value0, 2)
        for i, flag in enumerate(flagvalues): w(t, FLAG_BASE+i, flag)
        spread(t, group, value); counts['spread'] += 1
    for raw, error, old, flagvalues in itertools.product([3000, 3500, 4500, 5500, 6300, 65535],
            [-32768, -702, -701, -614, -527, -526, 32767], [-32768, -81, -80, 0, 80, 81, 32767],
            [(0, 0, 0), (1, 0, 1), (255, 255, 255)]):
        t = fixture(); w(t, 0x80EE, raw, 2); w(t, 0x98DC, error, 2)
        for i in range(3): w(t, 0x616A+2*i, old, 2); w(t, FLAG_BASE+i, flagvalues[i])
        update(t); counts['updater'] += 1
    for group, value in itertools.product(range(3), [-2147483648, -32769, -81, -80, -1, 0, 80, 81, 32768, 2147483647]):
        t = fixture(); before = slots(t); t.r[5] = group
        execute(t, 0x36E16, value); before[group] = clamp(value)
        assert slots(t) == before and flags(t) == [0, 0, 0]
        assert signed(execute(t, 0x36DFE, group), 32) == before[group]
        counts['accessors'] += 1
    for old, delta in itertools.product([-32768, -81, -80, -1, 0, 80, 81, 32767], [-32768, -81, -1, 0, 1, 81, 32767, 65536]):
        t = fixture()
        for i in range(3): w(t, 0x616A+2*i, old+i, 2)
        before = slots(t); want = before.copy()
        want[:3] = [clamp(v + signed(delta, 16)) for v in before[:3]]
        execute(t, 0x36B26, delta); assert slots(t) == want and flags(t) == [0, 0, 0]
        counts['uniform'] += 1
    rng = random.Random(0x36D1A)
    for _ in range(300):
        t = fixture()
        for i in range(3): w(t, 0x616A+2*i, rng.randrange(65536), 2)
        w(t, 0x80EE, rng.randrange(65536), 2)
        consumers(t); counts['consumer'] += 1
    return counts


def caller(t):
    expected = copy.deepcopy(t)
    counter = (r(t, 0x985D) + 1) & 255
    admitted = r(t, 0x985C) == 2 and counter == TCU[0x7713C]
    if admitted: update(expected)
    if admitted or r(t, 0x985C) != 2: counter = 0
    w(expected, 0x985D, counter)
    pc = 0x369C4; sp = t.r[15]; seen = []
    for _ in range(300000):
        if pc == 0x369E6: break
        if pc == 0x36D1A: seen.append(pc)
        nxt, delay = t.instruction(pc)
        if delay:
            _, nested = t.instruction(pc+2); assert not nested
        pc = nxt
    else: raise AssertionError('caller bound')
    assert t.r[15] == sp and bool(seen) == admitted
    assert slots(t) == slots(expected) and flags(t) == flags(expected)
    assert r(t, 0x98DC, 2) == r(expected, 0x98DC, 2) and r(t, 0x985D) == counter
    return admitted


def caller_cases():
    count = 0
    for state, counter, raw, error in itertools.product([0, 1, 2, 255], [0, 13, 14, 15, 254, 255], [3500, 5500], [-1000, 0]):
        t = fixture()
        for a, v, size in [(0x985C,state,1),(0x985D,counter,1),(0x80EE,raw,2),(0x98DC,error,2)]: w(t,a,v,size)
        caller(t); count += 1
    return count


def retained():
    t = fixture(); rows = []
    for call in range(1, 101):
        raw = 5500 if call <= 85 or call >= 91 else 3500
        error = 0 if call <= 90 else -1000
        w(t, 0x80EE, raw, 2); w(t, 0x98DC, error, 2)
        group, active = update(t); dynamic, fixed = consumers(t)
        rows.append(dict(call=call, group=group, active=active, slots=slots(t)[:3], flags=flags(t),
            error=signed(r(t,0x98DC,2),16), dynamic=dynamic, fixed=fixed))
    assert rows[79]['slots'] == [103, 91, 80] and rows[79]['flags'] == [0, 0, 1]
    assert rows[85]['slots'][0] == 80 and rows[85]['flags'] == [1, 0, 1]
    assert rows[-1]['slots'][0] == 80 and rows[-1]['slots'][2] == 70
    assert rows[79]['dynamic'] == 1280
    # Execute repeated real caller slices, letting its own byte counter run.
    t = fixture(); w(t,0x985C,2); w(t,0x985D,0); scheduled=[]
    for call in range(1, 46):
        w(t,0x98DC,0,2)
        if caller(t): scheduled.append(dict(call=call, slots=slots(t)[:3], flags=flags(t)))
        consumers(t)
    assert [row['call'] for row in scheduled] == [15,30,45]
    return rows, scheduled


def main():
    counts = direct(); counts['caller'] = caller_cases(); history, scheduled = retained()
    result = dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(), counts=counts,
        retained=history, scheduled=scheduled, scope_limit='RAM/cache storage; raw80EE/98DC and985C admission are explicit fixtures, no physical cadence/persistence proof.')
    (ROOT/'tcu-class-adjustments-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Verified',counts,'retained',len(history),'caller updates',[r['call'] for r in scheduled],flush=True)


if __name__ == '__main__': main()
