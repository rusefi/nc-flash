"""Observe original proposal stages during produced CAN fault/recovery.

Snapshots preserve entry RAM for bounded replay. Instrumentation is read-only;
counterfactual replay inputs, when used, are explicitly identified.
"""
import json
import hashlib
import itertools
import sys
from pathlib import Path
from verify_tcu_paired_input import ObservedPair,w,r
from verify_tcu_input_faults import retained_profile
from verify_tcu_paired_input import TCU,ECU
from verify_tcu_qualification_limit import selection_then_limit
from sh_subset import signed

CALLS={149,150,151,210,211,212}
PAIR_STAGES={0x4508A,0x495C0,0x452DC,0x44664,0x466B8,0x4662C,
             0x46DB6,0x46D34,0x46DE4,0x46CC8,0x46D30,0x46A34,0x46B00,0x45160}
POINTS={0x44D52:'before_scan',0x44D5A:'after_scan',0x44D60:'after4A5DE',
        0x44D6A:'after_source',0x44D74:'after_pipeline',0x44DA4:'after45160'}
BYTES=[0x8080,0x8081,0x8083,0x8084,0x8085,0x8086,0x8089,0x92D5,0x9B40,0x9B3D,0x9C50,0x9C54,0x9316]
WORDS=[0x8098,0x809A,0x809C,0x80EA,0x80F8,0x939E,0x96C8,0x96CA,0x96CC]


def fields(t):
    return {**{f'{a:04x}':r(t,a) for a in BYTES},**{f'{a:04x}':r(t,a,2) for a in WORDS}}


class ObservedDecision(ObservedPair):
    def __init__(self):
        super().__init__();self.events=[];self.snapshots={};self.returns=[]
    def instruction(self,pc):
        call=self.application_call
        if call in CALLS:
            if pc==0x44CFE:
                self.snapshots[str(call)]={'ram':{f'{a:08x}':v for a,v in self.ram.items()},
                    'samples':{f'{a:08x}':v for a,v in self.samples.items()},'fields':fields(self)}
            while self.returns and self.returns[-1][0]==pc:
                _,fn,p,q=self.returns.pop()
                self.events.append(dict(call=call,stage=f'{fn:05x}',event='return',
                    pair=[self.read(p,1),self.read(q,1)],fields=fields(self)))
            if pc in PAIR_STAGES:
                p,q=self.r[4],self.r[5]
                self.events.append(dict(call=call,stage=f'{pc:05x}',event='entry',
                    pair=[self.read(p,1),self.read(q,1)],fields=fields(self)))
                self.returns.append((self.pr,pc,p,q))
            if pc in POINTS:
                self.events.append(dict(call=call,stage=POINTS[pc],event='point',
                    pair=[self.read(self.r[15],1),self.read(self.r[15]+4,1)],fields=fields(self),
                    thresholds=[r(self,0x9B1E+2*i,2) for i in range(10)],
                    operations=[r(self,0x9B14+i) for i in range(10)]))
            if pc==0x4744C:
                self.events.append(dict(call=call,stage='4744c',event='entry',
                    pair=[self.r[5]&255,self.r[4]&255],fields=fields(self)))
            if pc==0x319BC:
                self.events.append(dict(call=call,stage='319bc',event='creation',
                    arguments=[self.r[i]&255 for i in [4,5,6]],fields=fields(self)))
        return super().instruction(pc)


def axis_cases():
    threshold=int.from_bytes(TCU[0x772F8:0x772FA],'big',signed=True)
    assert threshold==25600
    count=0;t=ObservedPair()
    for comparison,local,c5,d5,d3 in itertools.product(
            [0,3200,16384,19968,25600,32767,32768,65535],
            [0,threshold-1,threshold,threshold+1,32767,32768,65535],
            [0,2,255],[0,8,128,136,255],[0,64,255]):
        for a,v in [(0x809C,comparison),(0x8098,local)]:w(t,a,v,2)
        for a,v in [(0x92C5,c5),(0x92D5,d5),(0x92D3,d3)]:w(t,a,v)
        expected=65535 if signed(local,16)>threshold and c5&2 and not d5&128 and not d3&64 else (comparison*2)&65535
        t.run(0x44FCE)
        assert r(t,0x9B3E,2)==expected
        count+=1
    return count


def replays(snapshots):
    results=[]
    for call in [150,211]:
        for fault,comparison,primary,local in itertools.product([0,136],[3200,19968],[24960,25600],[0,19968]):
            s=snapshots[str(call)];t=ObservedDecision()
            t.ram={int(a,16):v for a,v in s['ram'].items()}
            t.samples={int(a,16):v for a,v in s['samples'].items()}
            t.application_call=call
            for a,v,n in [(0x92D5,fault,1),(0x809C,comparison,2),(0x809A,primary,2),(0x8098,local,2)]:w(t,a,v,n)
            sp=t.r[15];t.run(0x44CFE,limit=1000000);selection_then_limit(t)
            assert t.r[15]==sp and not t.returns
            assert r(t,0x9B3E,2)==comparison*2
            assert r(t,0x8084)==(4 if comparison==3200 else 1)
            expected=([[1,1,0]] if comparison==3200 else []) if call==150 else ([] if comparison==3200 else [[6,8,0]])
            assert t.creation_calls==expected
            before=next(e for e in t.events if e['stage']=='before_scan')
            after=next(e for e in t.events if e['stage']=='after_scan')
            results.append(dict(snapshot_call=call,explicit_overrides=dict(flags=fault,comparison=comparison,primary=primary,local=local),
                axis=r(t,0x9B3E,2),thresholds=before['thresholds'],scan_pair=after['pair'],
                proposed=r(t,0x8084),accepted=r(t,0x8081),creations=t.creation_calls,
                classification=t.classification_rows))
    return results


def main():
    root=Path('research/ecu-at-can')
    snapshot_path=root/'tcu-fault-selection-snapshots.json'
    result_path=root/'tcu-fault-selection-verification.json'
    if '--replay-only' in sys.argv:
        result=json.loads(result_path.read_text())
        snapshots=json.loads(snapshot_path.read_text())
    else:
        t=ObservedDecision();profile=retained_profile(t=t)
        previous=json.loads((root/'tcu-input-faults-verification.json').read_text())['retained_profile']
        assert json.loads(json.dumps(profile))==previous
        assert not t.returns
        snapshots=t.snapshots
        snapshot_path.write_text(json.dumps(snapshots,indent=2)+'\n')
        result=dict(scope=__doc__,profile_regression='Identical to saved fault profile',events=t.events)
    identities=dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(),ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                    snapshots_sha256=hashlib.sha256(snapshot_path.read_bytes()).hexdigest())
    for key,value in identities.items():
        if key in result:assert result[key]==value
    result.update(identities)
    result['axis_cases']=axis_cases();result['counterfactual_replays']=replays(snapshots)
    result_path.write_text(json.dumps(result,indent=2)+'\n')
    print('Axis cases:',result['axis_cases'],'Counterfactual replays:',len(result['counterfactual_replays']),flush=True)


if __name__=='__main__':main()
