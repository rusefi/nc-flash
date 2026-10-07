"""Execute stock threshold-bank production and observe saved-state dispatch.

Direct cases use explicit RAM inputs. Replays restore earlier fault-profile
RAM; observations do not replace instructions or inject producer outputs.
This does not establish physical signal identity or complete task scheduling.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from verify_tcu_paired_input import ObservedPair, TCU, w, r
from verify_tcu_request_maps import interpolate

ROOT = Path(__file__).resolve().parent
INPUTS = [0x8080, 0x8081, 0x916F, 0x92D0, 0x9C7C, 0x9E88,
          0x9B5C, 0x92D7, 0x92CA, 0xA534, 0x9F29]
OUTPUTS = [0x9AEA, 0x9AEB, 0x9B40]
DISPATCH = [0x46FA0, 0x46200, 0x45AA4, 0x47240]
BANKS = [0x7404C, 0x7422C, 0x7440C, 0x745EC, 0x747CC,
         0x749AC, 0x74B8C, 0x74D6C, 0x74F4C]


def descriptors(t):
    return dict(pointers=[r(t, 0x9AEC+4*i, 4) for i in range(10)],
                operations=[r(t, 0x9B14+i) for i in range(10)],
                kinds=[r(t, 0x9B32+i) for i in range(10)],
                source=r(t, 0x9B40))


def copy_bytes(t):
    return bytes(r(t, 0x9CA8+i) for i in range(480))


def expected_bank(d):
    base, source, kind = 0x7404C, 0, 0
    for bit in range(4):
        if d[0x9C7C] & (1 << bit):
            base, source, kind = 0x745EC+480*bit, 11+bit, 8+bit
    dynamic = bool(d[0x9E88] & 1)
    if dynamic:
        base, source, kind = 0xFFFF9CA8, 1, 1
    fixed = bool((d[0x916F] & 1 and not d[0x92D0] & 8 and TCU[0x77340] == 1)
                 or d[0x9B5C] & 1)
    if fixed:
        base, source, kind = 0x7440C, 3, 2
    special = bool(d[0x92D7] & 1 and not d[0x92CA] & 128 and d[0x8080] == 6)
    highest = special and d[0xA534] == 1
    if special:
        base, source, kind = 0x74D6C, 15, 12
    if highest:
        base, source, kind = 0x74F4C, 16, 13
    flags = 1 | ((d[0x9C7C] & 15) << 1) | (int(dynamic) << 5)
    flags |= (int(special) << 6) | (int(highest) << 7)
    return (dict(pointers=[base+48*i for i in range(10)],
                 operations=[source]*10, kinds=[kind]*10, source=source),
            (d[0x9AEA] & 254) | int(fixed), flags, dynamic)


def producer_cases():
    assert TCU[0x77340] == 0
    rng = random.Random(0x46FA0)
    cases = []
    for bits, dynamic, fixed, cls, blocked, special, extra in itertools.product(
            range(16), range(2), range(2), [0, 6, 255], range(2), range(2), [0, 1, 2]):
        d = {a: rng.randrange(256) for a in INPUTS+OUTPUTS}
        d.update({0x9C7C: bits, 0x9E88: dynamic, 0x9B5C: fixed,
                  0x8080: cls, 0x92CA: blocked*128, 0x92D7: special,
                  0xA534: extra, 0x8081: rng.randrange(7)})
        cases.append(d)
    cases.extend({a: rng.randrange(256) for a in INPUTS+OUTPUTS} for _ in range(256))
    copies = held = 0
    sources = set()
    t = SHRotate(TCU)
    for d in cases:
        for a, value in d.items():
            w(t, a, value)
        for i in range(10):
            w(t, 0x9AEC+4*i, 0xFFFFA000+48*i, 4)
            w(t, 0x9B14+i, 160+i)
            w(t, 0x9B32+i, 180+i)
        for i in range(480):
            w(t, 0x9CA8+i, i & 255)
        before, oldcopy = descriptors(t), copy_bytes(t)
        stack = t.r[15]
        t.run(0x46FA0, limit=100000)
        assert t.r[15] == stack
        if d[0x8080] == 255:
            assert descriptors(t) == before and copy_bytes(t) == oldcopy
            assert all(r(t, a) == d[a] for a in OUTPUTS)
            held += 1
            continue
        expected, flag_a, flag_b, dynamic = expected_bank(d)
        assert descriptors(t) == expected, d
        assert (r(t, 0x9AEA), r(t, 0x9AEB)) == (flag_a, flag_b), d
        sources.add(expected['source'])
        if dynamic:
            records = []
            for i in range(10):
                row = i+5 if i < 5 and d[0x9F29] & 2 and d[0x8081] == i else i
                address = 0x7422C+48*row
                records.append(TCU[address:address+48])
            assert copy_bytes(t) == b''.join(records), d
            copies += 1
        else:
            assert copy_bytes(t) == oldcopy
    return dict(cases=len(cases), early_holds=held, dynamic_copies=copies,
                observed_sources=sorted(sources), stock_77340=TCU[0x77340])


def curve(t, pointer, axis):
    count, shift = t.read(pointer, 2), t.read(pointer+2, 2)
    assert count in (2, 11) and shift == 0, (hex(pointer), count, shift)
    axes = [t.read(pointer+4+2*i, 2) for i in range(count)]
    values = [t.read(pointer+4+2*count+2*i, 2) for i in range(count)]
    return interpolate(axis & 65535, axes, values)


def interpolation_cases():
    count = 0
    t = SHRotate(TCU)
    for base in BANKS:
        for row in range(10):
            pointer = base+48*row
            axes = [t.read(pointer+4+2*i, 2) for i in range(11)]
            values = {0, 65535}
            values.update(max(0, min(65535, x+delta)) for x in axes for delta in [-1, 0, 1])
            values.update((a+b)//2 for a, b in zip(axes, axes[1:]))
            for axis in sorted(values):
                t.r[5] = pointer
                expected = curve(t, pointer, axis)
                t.run(0x108E6, axis)
                assert t.r[0] & 65535 == expected, (hex(pointer), axis, t.r[0], expected)
                count += 1
    return count


class ObservedCurves(ObservedPair):
    def __init__(self):
        super().__init__()
        self.stages = []
        self.curves = []
        self.pending_stage = None
        self.pending_curve = None

    def instruction(self, pc):
        if pc == 0x45366 and self.pending_stage is not None:
            self.stages.append(dict(function=f'{self.pending_stage:05x}', **descriptors(self)))
            self.pending_stage = None
        if pc in DISPATCH and self.pr == 0x45366:
            self.pending_stage = pc
        if pc == 0x108E6 and self.pr == 0x453D8:
            pointer, axis = self.r[5] & 0xFFFFFFFF, self.r[4] & 65535
            self.pending_curve = dict(pointer=pointer, axis=axis, expected=curve(self, pointer, axis))
        if pc == 0x453D8 and self.pending_curve is not None:
            assert self.r[0] & 65535 == self.pending_curve['expected']
            self.curves.append(self.pending_curve)
            self.pending_curve = None
        return super().instruction(pc)


def restore(snapshot):
    t = ObservedCurves()
    t.ram = {int(a, 16): v for a, v in snapshot['ram'].items()}
    t.samples = {int(a, 16): v for a, v in snapshot['samples'].items()}
    return t


def replays(snapshots):
    assert int.from_bytes(TCU[0x7744E:0x77450], 'big') == 4
    assert [int.from_bytes(TCU[0x5DE90+4*i:0x5DE94+4*i], 'big') for i in range(4)] == DISPATCH
    rows = []
    for call in [149, 150, 211]:
        t = restore(snapshots[str(call)])
        t.application_call = call
        t.run(0x44CFE, limit=1000000)
        assert [s['function'] for s in t.stages] == [f'{f:05x}' for f in DISPATCH]
        expected = dict(pointers=[0x7404C+48*i for i in range(10)],
                        operations=[0]*10, kinds=[0]*10, source=0)
        assert all({k:s[k] for k in expected} == expected for s in t.stages)
        assert len(t.curves) == 10
        assert [c['expected'] for c in t.curves] == [r(t, 0x9B1E+2*i, 2) for i in range(10)]
        rows.append(dict(call=call, stages=t.stages, curves=t.curves))
    return rows


def retained_switch(snapshot):
    t = restore(snapshot)
    # Explicit bank-control and two distinguishable axis inputs; keep the
    # remainder of the saved producer/admission state intact across calls.
    w(t, 0x9B40, 0)
    w(t, 0x9B3E, 6400, 2)
    w(t, 0x941E, 39936, 2)
    rows = []
    for mask, source, axis in [(4, 13, 6400), (4, 13, 39936), (0, 0, 39936), (0, 0, 6400)]:
        w(t, 0x9C7C, mask)
        t.stages.clear()
        t.curves.clear()
        t.run(0x4530C, limit=1000000)
        assert r(t, 0x9B40) == source
        assert len(t.curves) == 10 and all(c['axis'] == axis for c in t.curves)
        base = 0x749AC if source == 13 else 0x7404C
        assert [c['pointer'] for c in t.curves] == [base+48*i for i in range(10)]
        rows.append(dict(explicit_9c7c=mask, source=source, axis=axis,
                         curves=list(t.curves), thresholds=[r(t, 0x9B1E+2*i, 2) for i in range(10)]))
    return rows


def main():
    snapshot_path = ROOT/'tcu-fault-selection-snapshots.json'
    raw = snapshot_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '16d58c0427de7905b52531ef943cc01b311d1aeeda511eebf33d525362bda943'
    snapshots = json.loads(raw)
    result = dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                  snapshots_sha256=hashlib.sha256(raw).hexdigest())
    result['producer'] = producer_cases()
    print('Producer:', result['producer'], flush=True)
    result['interpolation_cases'] = interpolation_cases()
    print('Interpolation:', result['interpolation_cases'], flush=True)
    result['saved_state_replays'] = replays(snapshots)
    result['retained_bank_switch'] = retained_switch(snapshots['150'])
    (ROOT/'tcu-curve-sources-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Saved-state replays: 3; retained bank-switch calls: 4', flush=True)


if __name__ == '__main__':
    main()
