"""Execute stored adjustment initialization, accessors and producer49FE0.

Original stock instructions; independent integer/table model. Upstream inputs
and invocation order are explicit fixtures, not a hardware/scheduler model.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import signed
from verify_tcu_ascending_release import quotient
from verify_tcu_optional_thresholds import TCU, w, r, restore, configure, proposal_model, selection_then_limit

ROOT = Path(__file__).resolve().parent


def word(a):
    return signed(int.from_bytes(TCU[a:a+2], 'big'), 16)


def model(t):
    code = r(t, 0x9C9E, 2)
    group = code if code <= 2 else 0
    index = word(0x75EAA+2*group)
    delta = signed(r(t, 0x80EA, 2)-r(t, 0x9CA0, 2), 16)
    old = signed(r(t, 0x616A+2*index, 2), 16)
    admitted = TCU[0x75E7F+group]*64 <= delta < TCU[0x75E82+group]*64
    out = dict(group=group, index=index, delta=delta, old=old, admitted=admitted,
               new=old, divide=False, quotient=0, coefficient=None)
    if not admitted:
        return out
    measurement = signed(r(t, 0x9C9C, 2), 16)
    error = signed(measurement-TCU[0x75E85+group]*64, 16)
    if measurement >= TCU[0x75E88+group]*64 or r(t, 0x92D1)&1:
        coefficient = TCU[0x75E9B+group]
    elif not word(0x75E8C+2*group) <= error < word(0x75E92+2*group):
        coefficient = TCU[0x75E98+group]
    else:
        coefficient = None
    change = quotient(error*coefficient*16, word(0x70000+2*group)) if coefficient is not None else 0
    out.update(divide=coefficient is not None, quotient=change, coefficient=coefficient,
               new=max(word(0x75EA4+2*group), min(word(0x75E9E+2*group), old-change)))
    return out


def execute(t):
    want = model(t)
    before = [r(t, 0x616A+2*i, 2) for i in range(15)]
    expected = before.copy()
    if want['admitted']:
        expected[want['index']] = want['new'] & 65535
    saved = t.r[8:16].copy(); macl = t.macl; sr = t.sr & ~0x301
    t.visited.clear(); t.run(0x49FE0, limit=100000)
    assert [r(t, 0x616A+2*i, 2) for i in range(15)] == expected, want
    # Original software division changes the architectural M/Q/T bits.
    assert t.r[8:16] == saved and t.macl == macl and t.sr & ~0x301 == sr
    assert (0x24584 in t.visited) == (0x2456E in t.visited) == want['admitted']
    assert (0x10D0C in t.visited) == want['divide']
    assert (0x316A8 in t.visited) == (r(t, 0x9C9E, 2) <= 2)
    return want


def initialize(t, value=None):
    if value is None:
        t.run(0x15D04)
        value = int.from_bytes(TCU[0x5F222:0x5F224], 'big')
        assert r(t, 0xAD4E, 2) == value == 0
    else:
        w(t, 0xAD4E, value, 2)
    guards = [r(t, a, 2) for a in [0x6168, 0x6188]]
    w(t, 0x6168, 0x1234, 2); w(t, 0x6188, 0x5678, 2)
    for i in range(15): w(t, 0x616A+2*i, 0xA000+i, 2)
    sp = t.r[15]; t.run(0x137AC)
    assert t.r[15] == sp
    assert [r(t, 0x616A+2*i, 2) for i in range(15)] == [value & 65535]*15
    assert r(t, 0x6168, 2) == 0x1234 and r(t, 0x6188, 2) == 0x5678
    for address, value in zip([0x6168, 0x6188], guards): w(t, address, value, 2)


def direct():
    t = SHRotate(TCU); counts = dict(startup=0, initializer=0, accessors=0, producer_edges=0, producer_random=0)
    for sentinel in [0, 0xA5, 255]:
        for address in range(0xAD48, 0xB130): w(t, address, sentinel)
        sp = t.r[15]; t.run(0x15D04)
        assert t.r[15] == sp
        assert bytes(r(t, a) for a in range(0xAD4C, 0xB12C)) == TCU[0x5F220:0x5F600]
        assert all(r(t, a) == sentinel for a in [*range(0xAD48, 0xAD4C), *range(0xB12C, 0xB130)])
        counts['startup'] += 1
    assert [int.from_bytes(TCU[0x5D1C4+4*i:0x5D1C8+4*i], 'big') for i in range(15)] == [0xFFFFAD4E]*15
    for value in [0, 1, 32767, 32768, 65535]:
        initialize(t, value); counts['initializer'] += 1
    for setter, getter, index, value in itertools.product([0x24562, 0x2456E], [0x2457A, 0x24584],
            [0, 3, 6, 7, 8, 14, 0x10006], [0, 1, 32767, 32768, 65535]):
        before = [r(t, 0x616A+2*i, 2) for i in range(15)]
        t.r[5] = value
        assert t.run(setter, index) == 0
        before[index&65535] = value
        assert [r(t, 0x616A+2*i, 2) for i in range(15)] == before
        assert signed(t.run(getter, index), 32) == signed(value, 16)
        counts['accessors'] += 1
    for code in [0, 1, 2, 3, 10, 255, 65535]:
        group = code if code <= 2 else 0
        lo, hi = TCU[0x75E7F+group]*64, TCU[0x75E82+group]*64
        center, high = TCU[0x75E85+group]*64, TCU[0x75E88+group]*64
        a, b = word(0x75E8C+2*group), word(0x75E92+2*group)
        points = sorted(set([-32768, 32767, center, high-1, high, high+1,
                             center+a-1, center+a, center+a+1, center+b-1, center+b, center+b+1]))
        for flags, measurement, delta, old in itertools.product([0, 1, 2], points,
                [lo-1, lo, lo+1, hi-1, hi, -32768, 32767],
                [-32768, -513, -512, 0, word(0x75E9E+2*group), word(0x75E9E+2*group)+1, 32767]):
            for address, value in [(0x9C9E, code), (0x9C9C, measurement), (0x80EA, delta), (0x9CA0, 0)]:
                w(t, address, value, 2)
            w(t, 0x92D1, flags); w(t, 0x616A+2*word(0x75EAA+2*group), old, 2)
            execute(t); counts['producer_edges'] += 1
    rng = random.Random(0x49FE0)
    for _ in range(750):
        for address in [0x9C9E, 0x9C9C, 0x80EA, 0x9CA0]: w(t, address, rng.randrange(65536), 2)
        w(t, 0x9C9E, rng.choice([0, 1, 2, 3, 65535]), 2); w(t, 0x92D1, rng.randrange(256))
        for i in range(15): w(t, 0x616A+2*i, rng.randrange(65536), 2)
        execute(t); counts['producer_random'] += 1
    return counts


def retained():
    rows = []
    for group, flags, measurement in itertools.product(range(3), [0, 1], [15000, 15616, 17000]):
        t = SHRotate(TCU); initialize(t)
        for address, value in [(0x9C9E, group), (0x9C9C, measurement), (0x80EA, 640),
                               (0x9CA0, 640-TCU[0x75E7F+group]*64)]: w(t, address, value, 2)
        w(t, 0x92D1, flags)
        trace = [execute(t) for _ in range(64)]
        rows.append(dict(group=group, flags=flags, measurement=measurement, trace=trace))
    return rows


def replays(snapshots):
    rows = []
    for call, gate, measurement, full in itertools.product([150, 211], [0, 1], [15000, 15616, 17000], [False, True]):
        t = restore(snapshots[str(call)]); t.application_call = call
        configure(t, gate, 3, 0, 23040)
        # Execute stock startup and the initializer, then supply upstream
        # producer inputs. No adjustment or initializer-source injection.
        initialize(t)
        for group in range(3):
            for address, value in [(0x9C9E, group), (0x9C9C, measurement), (0x80EA, 640),
                    (0x9CA0, 640-TCU[0x75E7F+group]*64)]: w(t, address, value, 2)
            for _ in range(64): execute(t)
        produced = [signed(r(t, 0x6176+2*i, 2), 16) for i in range(3)]
        sp = t.r[15]
        if full:
            t.run(0x44CFE, limit=1000000); selection_then_limit(t)
            outcome = dict(proposed=r(t, 0x8084), accepted=r(t, 0x8081), creations=t.creation_calls)
        else:
            t.run(0x4530C, limit=1000000); pair = proposal_model(t)
            t.r[5] = 0xFFFEC000; t.run(0x4508A, 0xFFFEC004)
            assert [t.read(0xFFFEC004, 1), t.read(0xFFFEC000, 1)] == list(pair)
            outcome = dict(scan=list(pair))
        assert t.r[15] == sp and not t.optional_pending and len(t.threshold_rows) == 10
        rows.append(dict(call=call, gate=gate, measurement=measurement, full=full, produced=produced,
                         thresholds=t.threshold_rows, optional=t.optional_rows, **outcome))
    return rows


def main():
    raw = (ROOT/'tcu-fault-selection-snapshots.json').read_bytes()
    result = dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                  snapshots_sha256=hashlib.sha256(raw).hexdigest(), direct=direct())
    print('Direct', result['direct'], flush=True)
    result['retained'] = retained(); result['replays'] = replays(json.loads(raw))
    (ROOT/'tcu-stored-adjustments-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Retained', len(result['retained']), 'paired replays', len(result['replays']), flush=True)


if __name__ == '__main__': main()
