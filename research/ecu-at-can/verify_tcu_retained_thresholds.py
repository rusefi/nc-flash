"""Execute46200 retained threshold overlay, hysteresis and admission.

Independent models cover original helpers and whole producer. Retained samples
and saved-state overrides are fixtures, not physical sensor/task evidence.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import signed
from verify_tcu_curve_sources import TCU,w,r,descriptors,curve
from verify_tcu_class_thresholds import ObservedClass
from verify_tcu_qualification_limit import selection_then_limit

ROOT=Path(__file__).resolve().parent
BYTE_INPUTS=[0x8080,0x9330,0x92C9,0x9B3C]
WORD_INPUTS=[0x9336,0x9390,0x9B3E,0x80EA]
OUT_BYTES=[0x9BF4,0x9BF5,0x9B40,0x9AEA]
OUT_WORDS=[0x9BF6,0x9BF8]
UP=[0x73FE4,0x73F84,0x73F24]
DOWN=[0x74014,0x73FB4,0x73F54]


def word(a):return int.from_bytes(TCU[a:a+2],'big',signed=True)


def fields(t):
    return {**{a:r(t,a) for a in BYTE_INPUTS+OUT_BYTES},
            **{a:r(t,a,2) for a in WORD_INPUTS+OUT_WORDS}}


def state(t):return dict(fields=fields(t),descriptors=descriptors(t))


def hysteresis(d):
    a,b=signed(d[0x9BF6],16),signed(d[0x9BF8],16)
    on=bool(d[0x9BF5]&8)
    if a>=word(0x77314) or (a>=word(0x77316) and b>=word(0x77318)):on=True
    if a<word(0x7731A) or (a<word(0x7731C) and b<word(0x7731E)):on=False
    d[0x9BF5]=(d[0x9BF5]&247)|(8 if on else 0)
    d[0x9AEA]=(d[0x9AEA]&251)|(4 if on else 0)
    if on:d[0x9B40]=6
    return on


def admitted(d):return d[0x8080] not in [0,1,2,255] and not d[0x9330]&1


def capture(d):
    d[0x9BF6]=word(0x77320)&65535 if d[0x92C9]&1 else d[0x9336]
    d[0x9BF8]=word(0x77322)&65535 if d[0x92C9]&2 else d[0x9390]


def predicate(t,index,d):
    axis=d[0x9B3E];measurement=signed(d[0x80EA],16);category=d[0x9B3C]
    if index==2:return int(measurement>=curve(t,DOWN[2],axis) or category<4)
    if index in [0,1]:
        for category_value,address in [(4,DOWN[2]),(3,DOWN[1]),(2,DOWN[0])][:3-index]:
            if category==category_value and measurement>=curve(t,address,axis):return 1
        return int(category<index+2)
    return 0


def model(t):
    result=state(t);d=result['fields'];desc=result['descriptors']
    latched=d[0x9BF5]&7
    on=hysteresis(d);admit=admitted(d)
    if admit:capture(d)
    if admit and on:
        for index in [2,1,0]:
            if not latched&(1<<index):
                policy=TCU[0x73F20+index]
                if policy==0 or (policy==1 and predicate(t,index,d)):latched|=1<<index
        d[0x9BF5]=(d[0x9BF5]&248)|latched
        for index in [2,1,0]:
            if latched&((1<<(index+1))-1):
                d[0x9BF4]|=1<<index
                slot=index+1
                desc['pointers'][slot]=UP[index]
                desc['pointers'][slot+5]=DOWN[index]
                for s in [slot,slot+5]:desc['operations'][s]=6;desc['kinds'][s]=5
    else:
        d[0x9BF4]&=248;d[0x9BF5]&=248
    desc['source']=d[0x9B40]
    return result


def check_fields(t,d):
    for a,v in d.items():assert r(t,a,2 if a in WORD_INPUTS+OUT_WORDS else 1)==v,(hex(a),v)


def direct():
    t=SHRotate(TCU);counts=dict(hysteresis=0,admission=0,capture=0,predicate=0,whole=0)
    for a,b,flags in itertools.product([0,14719,14720,14721,31999,32000,32001,32767,32768,65535],
                                      [0,12415,12416,13055,13056,65535],[0,7,8,15,255]):
        for x,v,n in [(0x9BF6,a,2),(0x9BF8,b,2),(0x9BF5,flags,1),(0x9AEA,0xA3,1),(0x9B40,13,1)]:w(t,x,v,n)
        d=fields(t);hysteresis(d);t.run(0x46580);check_fields(t,d);counts['hysteresis']+=1
    for klass,flags in itertools.product(range(256),[0,1,2,255]):
        w(t,0x8080,klass);w(t,0x9330,flags);want=int(admitted(fields(t)))
        assert t.run(0x46372)&255==want;counts['admission']+=1
    for a,b,fault in itertools.product([0,10240,32767,32768,65535],[0,10240,32767,32768,65535],[0,1,2,3,252,255]):
        w(t,0x9336,a,2);w(t,0x9390,b,2);w(t,0x92C9,fault)
        d=fields(t);capture(d);t.run(0x463CC);check_fields(t,d);counts['capture']+=1
    for axis,category in itertools.product([0,6400,39936,65535],[0,1,2,3,4,5,128,255]):
        thresholds=[curve(t,p,axis) for p in DOWN]
        measurements={0,32767,32768,65535,*[(v+offset)&65535 for v in thresholds for offset in [-1,0,1]]}
        for measurement,index in itertools.product(sorted(measurements),[0,1,2,3]):
            w(t,0x9B3E,axis,2);w(t,0x80EA,measurement,2);w(t,0x9B3C,category)
            want=predicate(t,index,fields(t));assert t.run(0x4643A,index)&255==want
            if index<3:assert t.run(0x46402,index)&255==want
            counts['predicate']+=1
    rng=random.Random(0x46200)
    fixtures=list(itertools.product(range(16),[0,3,6,255],[0,1,2,3]))
    fixtures.extend((rng.randrange(256),rng.randrange(256),rng.randrange(256)) for _ in range(512))
    for oldflags,klass,fault in fixtures:
        for a in BYTE_INPUTS+OUT_BYTES:w(t,a,rng.randrange(256))
        for a in WORD_INPUTS+OUT_WORDS:w(t,a,rng.choice([0,14719,14720,20000,31999,32000,32767,32768,65535]),2)
        for a,v in [(0x9BF5,oldflags),(0x8080,klass),(0x92C9,fault),(0x9330,rng.randrange(2)),(0x9B3C,rng.randrange(7))]:w(t,a,v)
        for i in range(10):
            w(t,0x9AEC+4*i,0x7404C+48*i,4);w(t,0x9B14+i,rng.randrange(256));w(t,0x9B32+i,rng.randrange(256))
        want=model(t);sp=t.r[15];t.run(0x46200,limit=100000)
        assert state(t)==want,(oldflags,klass,fault,state(t),want)
        assert t.r[15]==sp;counts['whole']+=1
    return counts


class ObservedRetained(ObservedClass):
    def __init__(self):
        super().__init__();self.overlay_pending=None;self.overlay_checks=0;self.overlay_rows=[]
    def instruction(self,pc):
        if self.overlay_pending is not None and pc==self.overlay_pending[0]:
            _,want,before=self.overlay_pending
            assert state(self)==want,(before,state(self),want)
            self.overlay_rows.append(dict(before=before,after=want))
            self.overlay_checks+=1;self.overlay_pending=None
        if pc==0x46200:self.overlay_pending=(self.pr,model(self),state(self))
        return super().instruction(pc)


def restore(snapshot):
    t=ObservedRetained();t.ram={int(a,16):v for a,v in snapshot['ram'].items()}
    t.samples={int(a,16):v for a,v in snapshot['samples'].items()};return t


def retained(snapshot):
    t=restore(snapshot)
    for a,v in [(0x8080,6),(0x9C12,6),(0x916F,0),(0x9C7C,0),(0x9E88,0),(0x9B5C,0),
                (0x92D7,0),(0x9AE9,0),(0x92D1,0),(0x9BF4,0),(0x9BF5,0),(0x9B3C,0)]:w(t,a,v)
    w(t,0x9BF6,0,2);w(t,0x9BF8,0,2);w(t,0x9B3E,6400,2);w(t,0x80F2,0,2)
    rows=[]
    for value,fault,gate in [(32000,0,0),(32000,0,0),(0,0,0),(0,0,0),
                            (32000,0,0),(32000,0,0),(32000,1,0),(32000,0,0),
                            (32000,0,0),(32000,0,1),(32000,0,0)]:
        w(t,0x9336,value,2);w(t,0x9390,16000,2);w(t,0x92C9,fault);w(t,0x9330,gate)
        t.curves.clear();t.stages.clear();sp=t.r[15]
        t.run(0x4530C,limit=1000000)
        assert t.r[15]==sp and t.overlay_pending is None
        assert len(t.curves)==10
        assert [r(t,0x9B1E+2*i,2) for i in range(10)]==[c['expected'] for c in t.curves]
        rows.append(dict(value=value,fault=fault,gate=gate,state=state(t),
                         overlay=t.overlay_rows[-1],stages=copy.deepcopy(t.stages),
                         thresholds=[r(t,0x9B1E+2*i,2) for i in range(10)]))
    assert t.overlay_checks==t.class_checks==len(rows)
    return rows


def replays(snapshots):
    rows=[]
    for call,klass,oldvalue,gate in itertools.product([150,211],[0,3,6],[0,32000],[0,1]):
        t=restore(snapshots[str(call)]);t.application_call=call
        for a,v,n in [(0x8080,klass,1),(0x9C12,klass,1),(0x9BF6,oldvalue,2),
                      (0x9BF8,16000,2),(0x9330,gate,1)]:w(t,a,v,n)
        sp=t.r[15];t.run(0x44CFE,limit=1000000);selection_then_limit(t)
        assert t.r[15]==sp and t.overlay_checks==t.class_checks==1
        rows.append(dict(call=call,klass=klass,previous_input=oldvalue,gate=gate,
                         state=state(t),stages=t.stages,proposals=t.proposal_rows,
                         proposed=r(t,0x8084),accepted=r(t,0x8081),creations=t.creation_calls))
    return rows


def main():
    raw=(ROOT/'tcu-fault-selection-snapshots.json').read_bytes()
    prior=json.loads((ROOT/'tcu-fault-selection-verification.json').read_text())
    assert hashlib.sha256(TCU).hexdigest()==prior['tcu_sha256']
    assert hashlib.sha256(raw).hexdigest()==prior['snapshots_sha256']
    snapshots=json.loads(raw)
    result=dict(scope=__doc__,tcu_sha256=prior['tcu_sha256'],snapshots_sha256=prior['snapshots_sha256'])
    result['direct']=direct();print('Direct:',result['direct'],flush=True)
    result['retained']=retained(snapshots['150']);print('Retained:',len(result['retained']),flush=True)
    result['replays']=replays(snapshots);print('Full replays:',len(result['replays']),flush=True)
    (ROOT/'tcu-retained-thresholds-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
