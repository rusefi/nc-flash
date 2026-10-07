"""Check entry-source versus newly published source in original4530C.

Saved synthetic RAM snapshots, explicit upstream overrides, and original
instructions. This is a call-order result, not a physical timing claim.
"""
import hashlib
import itertools
import json
from pathlib import Path

from verify_tcu_paired_input import ObservedPair, TCU, ECU, w, r
from verify_tcu_request_maps import interpolate
from verify_tcu_transition_classification import proposal_model

ROOT = Path(__file__).resolve().parent
PRODUCERS = [0x46FA0, 0x46200, 0x45AA4, 0x47240]


class ObservedAxis(ObservedPair):
    def __init__(self):
        super().__init__()
        self.lookups = []
        self.stages = []
        self.adjustments = []
        self.pending = []

    def instruction(self, pc):
        while self.pending and self.pending[-1][0] == pc:
            _, expected = self.pending.pop()
            assert self.r[0] & 65535 == expected
        if pc in PRODUCERS:
            self.stages.append(f'{pc:05x}')
        if pc == 0x108E6:
            p, x = self.r[5], self.r[4] & 65535
            n, shift = self.read(p, 2), self.read(p+2, 2)
            assert n in [2, 11] and shift == 0, (hex(p), n, shift)
            xs = [self.read(p+4+2*i, 2) for i in range(n)]
            ys = [self.read(p+4+2*n+2*i, 2) for i in range(n)]
            # Stock curves can contain repeated axes; endpoint and bracket
            # handling must follow the existing independent integer oracle.
            expected = interpolate(x, xs, ys)
            self.lookups.append(dict(pointer=f'{p:08x}', axis=x, expected=expected))
            self.pending.append((self.pr, expected))
        if pc in [0x44E14, 0x44F5A]:
            self.adjustments.append(f'{pc:05x}')
        return super().instruction(pc)


def restore(s):
    t = ObservedAxis()
    t.ram = {int(a, 16):v for a,v in s['ram'].items()}
    t.samples = {int(a, 16):v for a,v in s['samples'].items()}
    return t


def main():
    p = ROOT/'tcu-fault-selection-snapshots.json'
    prior = json.loads((ROOT/'tcu-fault-selection-verification.json').read_text())
    identity = dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                    ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                    snapshots_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    assert all(prior[k] == v for k,v in identity.items())
    snapshots = json.loads(p.read_text())
    assert int.from_bytes(TCU[0x7744E:0x77450], 'big') == 4
    assert [int.from_bytes(TCU[0x5DE90+4*i:0x5DE94+4*i], 'big') for i in range(4)] == PRODUCERS
    rows = []
    for flags, old, axes in itertools.product([0,1,2,4,8], [0,13,14], [(6400,39936),(14,70)]):
        t = restore(snapshots['150'])
        overrides = [(0x8080,0),(0x9C7C,flags),(0x9B40,old),(0x9E88,0),
                     (0x9B5C,0),(0x916F,0),(0x92D7,0),(0x9AE9,0),(0x92D1,0)]
        for a,v in overrides:
            w(t,a,v)
        w(t,0x9B3E,axes[0],2); w(t,0x941E,axes[1],2); w(t,0x80F2,0,2)
        for iteration in range(2):
            before = r(t,0x9B40)
            start, stage_start = len(t.lookups), len(t.stages)
            stack = t.r[15]
            t.run(0x4530C, limit=1000000)
            assert not t.pending and t.r[15] == stack
            calls = t.lookups[start:]
            expected_axis = axes[1] if before in [13,14] else axes[0]
            assert len(calls) == 10 and all(c['axis'] == expected_axis for c in calls)
            assert not t.adjustments
            thresholds = [r(t,0x9B1E+2*i,2) for i in range(10)]
            assert thresholds == [c['expected'] for c in calls]
            assert t.stages[stage_start:] == [f'{a:05x}' for a in PRODUCERS]
            after = {0:0,1:11,2:12,4:13,8:14}[flags]
            assert r(t,0x9B40) == after
            expected_pair = proposal_model(t)
            t.r[5] = 0xFFFEC000
            t.run(0x4508A, 0xFFFEC004)
            assert (t.read(0xFFFEC004,1),t.read(0xFFFEC000,1)) == expected_pair
            assert t.r[15] == stack and t.pending_proposal is None
            rows.append(dict(flags=flags, initial_source=old, iteration=iteration+1,
                             axis_inputs=axes, proposal=list(expected_pair),
                             source_before=before, source_after=after,
                             axis=expected_axis, thresholds=thresholds, lookups=calls))
    result = dict(scope=__doc__, **identity, entry_snapshot_call=150,
                  fixtures=dict(byte_overrides='Listed in script; source flags fixed between the two calls',
                                axis_pairs=[[6400,39936],[14,70]], word_80f2=0),
                  calls=len(rows), proposal_checks=len(rows), independent_lookup_checks=sum(len(x['lookups']) for x in rows),
                  rows=rows)
    (ROOT/'tcu-threshold-axis-history-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Axis-history calls:',len(rows),'Independent lookup checks:',result['independent_lookup_checks'])


if __name__ == '__main__':
    main()
