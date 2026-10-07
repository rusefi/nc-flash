"""Execute47240 class threshold overlays and retained operation tags.

Independent models check original bodies and descriptor preservation. Explicit
class/history fixtures are not naturally produced selector transitions.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import signed
from verify_tcu_paired_input import TCU, ECU, w, r
from verify_tcu_curve_sources import ObservedCurves, descriptors
from verify_tcu_transition_classification import proposal_model
from verify_tcu_qualification_limit import selection_then_limit

ROOT = Path(__file__).resolve().parent
CALIBRATIONS = [0x75138,0x75134,0x75130,0x7512C,0x7513C]
CLASSES = [0,1,2,3,4,5,6,128,255]


def state(t):
    return dict(**descriptors(t), calibration=[r(t,0x9C08+2*i,2) for i in range(5)],
                curves=[r(t,0x9C14+2*i,2) for i in range(30)], previous=r(t,0x9C12))


def expected(t):
    d=state(t)
    klass,old=signed(r(t,0x8080),8),signed(d['previous'],8)
    assert klass<=6 and old<=6
    offset=2 if r(t,0x916F)&4 else 0
    d['calibration']=[int.from_bytes(TCU[a+offset:a+offset+2],'big') for a in CALIBRATIONS]
    if klass>0:
        d['curves']=[x for v in d['calibration'] for x in [2,0,0,65535,v,v]]
        for i in range(klass-1,5):
            d['pointers'][i]=0x5DEAC
            d['pointers'][i+5]=0xFFFF9C14+12*i
            for j in [i,i+5]:
                d['operations'][j]=4;d['kinds'][j]=7
        if 0<old<klass:
            for i in range(old-1,klass-1):
                d['operations'][i]=4;d['kinds'][i]=7
    d['previous']=klass&255
    return d


class ReadAudit(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.cal_reads=[]
    def read(self,address,size):
        if size==2 and 0x7512C<=address<0x75140:
            self.cal_reads.append(address)
        return super().read(address,size)


def direct_cases():
    rng=random.Random(0x47240)
    t=ReadAudit();n=0
    fixtures=list(itertools.product(CLASSES,CLASSES,[0,4,251,255]))
    fixtures.extend((rng.choice(CLASSES),rng.choice(CLASSES),f) for f in range(256))
    for klass,old,flags in fixtures:
        for i in range(10):
            w(t,0x9AEC+4*i,0x70000+rng.randrange(65536),4)
            w(t,0x9B14+i,rng.randrange(256));w(t,0x9B32+i,rng.randrange(256))
        for a in [0x9B40,0x9AEA,0x9AEB,0x9C13]:w(t,a,rng.randrange(256))
        for i in range(35):w(t,0x9C08+2*i,rng.randrange(65536),2)
        w(t,0x8080,klass);w(t,0x9C12,old);w(t,0x916F,flags)
        want=expected(t);guard={a:r(t,a) for a in [0x8080,0x916F,0x9AEA,0x9AEB,0x9C13]}
        sp=t.r[15];t.cal_reads.clear();t.run(0x47240)
        assert state(t)==want,(klass,old,flags,state(t),want)
        assert {a:r(t,a) for a in guard}==guard
        assert t.cal_reads==[a+(2 if flags&4 else 0) for a in CALIBRATIONS]
        assert t.r[15]==sp;n+=1
    builder=0
    for values in itertools.product([0,1,32767,32768,65535],repeat=3):
        values=[values[0],values[1],values[2],values[1],values[0]]
        for i,v in enumerate(values):w(t,0x9C08+2*i,v,2)
        t.run(0x472A6)
        assert [r(t,0x9C14+2*i,2) for i in range(30)]==[x for v in values for x in [2,0,0,65535,v,v]]
        builder+=1
    return dict(whole_producer=n,arbitrary_word_curve_builder=builder)


class ObservedClass(ObservedCurves):
    def __init__(self):
        super().__init__();self.class_pending=None;self.class_checks=0;self.class_rows=[]
    def instruction(self,pc):
        if self.class_pending is not None and pc==self.class_pending[0]:
            _,want,before=self.class_pending
            assert state(self)==want,(before,state(self),want)
            self.class_rows.append(dict(before=before,after=want))
            self.class_checks+=1;self.class_pending=None
        if pc==0x47240:
            self.class_pending=(self.pr,expected(self),state(self))
        return super().instruction(pc)


def restore(snapshot):
    t=ObservedClass();t.ram={int(a,16):v for a,v in snapshot['ram'].items()}
    t.samples={int(a,16):v for a,v in snapshot['samples'].items()}
    return t


def retained(snapshot):
    rows=[]
    # Reset primary descriptors every4530C call, then execute all four producers.
    t=restore(snapshot)
    for a,v in [(0x916F,0),(0x9C7C,0),(0x9E88,0),(0x9B5C,0),(0x92D7,0),
                (0x9AE9,0),(0x92D1,0),(0x9B40,0),(0x9C12,0)]:w(t,a,v)
    w(t,0x9B3E,6400,2);w(t,0x80F2,0,2)
    for klass in [0,1,2,3,4,5,6,6,3,0,128,0]:
        w(t,0x8080,klass)
        old=r(t,0x9C12);t.curves.clear();t.stages.clear();sp=t.r[15]
        t.run(0x4530C,limit=1000000)
        assert t.r[15]==sp and t.class_pending is None
        assert len(t.curves)==10
        assert [r(t,0x9B1E+2*i,2) for i in range(10)]==[c['expected'] for c in t.curves]
        want=proposal_model(t)
        t.r[5]=0xFFFEC000;t.run(0x4508A,0xFFFEC004)
        assert (t.read(0xFFFEC004,1),t.read(0xFFFEC000,1))==want
        rows.append(dict(current=klass,previous=old,descriptors=descriptors(t),
                         thresholds=[r(t,0x9B1E+2*i,2) for i in range(10)],proposal=list(want),
                         stages=copy.deepcopy(t.stages)))
    assert t.class_checks==len(rows)
    return rows


def boundary_scans(snapshot):
    t=restore(snapshot)
    w(t,0x8080,1);w(t,0x9C12,0)
    t.run(0x4530C,limit=1000000)
    assert [r(t,0x9B1E+2*i,2) for i in range(5)]==[65535]*5
    rows=[]
    for old,measurement in itertools.product([0,1,4,5],[0,4003,4004,4005,65534,65535]):
        w(t,0x8084,old);w(t,0x80EA,measurement,2);w(t,0x9B3D,0)
        want=proposal_model(t)
        t.r[5]=0xFFFEC000;t.run(0x4508A,0xFFFEC004)
        assert (t.read(0xFFFEC004,1),t.read(0xFFFEC000,1))==want
        rows.append(dict(old=old,measurement=measurement,proposal=list(want)))
    assert next(x['proposal'] for x in rows if x['old']==1 and x['measurement']==65535)==[5,4]
    assert next(x['proposal'] for x in rows if x['old']==1 and x['measurement']==65534)==[1,0]
    return rows


def replays(snapshots):
    rows=[]
    previous=json.loads((ROOT/'tcu-fault-selection-verification.json').read_text())
    for call,klass,old in itertools.product([150,211],range(7),[0,1,3,6]):
        t=restore(snapshots[str(call)]);t.application_call=call
        w(t,0x8080,klass);w(t,0x9C12,old)
        sp=t.r[15];t.run(0x44CFE,limit=1000000)
        assert t.r[15]==sp and t.class_checks==1 and t.class_pending is None
        proposals=copy.deepcopy(t.proposal_rows)
        selection_then_limit(t)
        assert t.r[15]==sp
        if klass==0:
            old_stage=next(e for e in previous['events'] if e['call']==call and e['stage']=='before_scan')
            assert [r(t,0x9B1E+2*i,2) for i in range(10)]==old_stage['thresholds']
            assert t.creation_calls==[e['arguments'] for e in previous['events'] if e['call']==call and e['stage']=='319bc']
        rows.append(dict(snapshot_call=call,current=klass,previous=old,
                         threshold_stages=t.stages,proposals=proposals,proposed=r(t,0x8084),
                         accepted=r(t,0x8081),creations=t.creation_calls,
                         classifications=t.classification_rows))
    return rows


def main():
    path=ROOT/'tcu-fault-selection-snapshots.json';raw=path.read_bytes()
    prior=json.loads((ROOT/'tcu-fault-selection-verification.json').read_text())
    identity=dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(),ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                  snapshots_sha256=hashlib.sha256(raw).hexdigest())
    assert all(prior[k]==v for k,v in identity.items())
    snapshots=json.loads(raw)
    result=dict(scope=__doc__,**identity,direct=direct_cases())
    print('Direct:',result['direct'],flush=True)
    result['retained']=retained(snapshots['150'])
    print('Retained calls:',len(result['retained']),flush=True)
    result['boundary_scans']=boundary_scans(snapshots['150'])
    result['replays']=replays(snapshots)
    print('Full proposal/selection replays:',len(result['replays']),flush=True)
    (ROOT/'tcu-class-thresholds-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
