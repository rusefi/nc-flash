"""Execute45AA4 active/release overlay with independent state/curve models.

Explicit RAM/timer samples and saved-state replays; no physical units or
scheduler period asserted. Original helper bodies execute without stubs.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import signed
from verify_tcu_curve_sources import TCU,w,r,descriptors
from verify_tcu_request_maps import interpolate
from verify_tcu_transition_classification import pending_model
from verify_tcu_retained_thresholds import ObservedRetained
from verify_tcu_qualification_limit import selection_then_limit

ROOT=Path(__file__).resolve().parent
BYTES=[0x8080,0x8081,0x8084,0x8088,0x8089,0x9330,0x9338,0x92D5,0x92D3,0x92C5,
       0x92D1,0x9889,0x9B40,0x9B3D,0x9B64,0x815D,0x9BEA,0x9BF0,0x9BF1]
WORDS=[0x80EA,0x9B3E,0x9B66,0x92F4,0x92F0,0x9BEC,0x9BEE]


def word(a):return int.from_bytes(TCU[a:a+2],'big',signed=True)


def fields(t):return {**{a:r(t,a) for a in BYTES},**{a:r(t,a,2) for a in WORDS}}


def state(t):
    return dict(fields=fields(t),descriptors=descriptors(t),
                curves=[[r(t,0x9B68+12*i+2*j,2) for j in range(6)] for i in range(10)])


def curve(t,p,x):
    count,shift=t.read(p,2),t.read(p+2,2)
    assert count in [2,3,4,11] and shift==0,(hex(p),count,shift)
    return interpolate(x&65535,[t.read(p+4+2*i,2) for i in range(count)],
                       [t.read(p+4+2*count+2*i,2) for i in range(count)])


def admit(d):
    return int(d[0x8080] not in [0,1,255] and signed(d[0x80EA],16)>=word(0x7730C)
               and not d[0x9330]&1 and d[0x9B40] not in [11,12,13,14])


def enter(t,d):
    fault=bool(d[0x92D5]&128);special=bool(d[0x92C5]&4)
    blocked=pending_model(t) and d[0x8089] in range(5)
    return int((not fault and not d[0x92D3]&64 and d[0x92D5]&1 and d[0x9338]==0
                and (signed(d[0x80EA],16)<word(0x77310) or special) and not blocked)
               or (fault and special))


def leave(d):
    fault=bool(d[0x92D5]&128);other=bool(d[0x92D3]&64);special=bool(d[0x92C5]&4)
    return int((not fault and not other and ((not special and not d[0x92D5]&1)
                                              or d[0x9338]!=0)) or (fault and not special))


def history(d,active,release):
    accepted,old=d[0x8081],d[0x9BEA]
    keep=active!=0 and signed(d[0x8080],8)<=signed(d[0x9BF0],8) and accepted<=old
    keep=keep and (accepted>=old or (release!=1 and d[0x9B3D]==5))
    if not keep:d[0x9BF1]&=254;d[0x9BEE]=0
    if active==1 and accepted<old and release==0 and d[0x9B3D]==5:
        d[0x9BF1]|=1;d[0x9BEE]=d[0x9BEC]


def lower(t,index,flag,x,y,d):
    result=curve(t,0x73C3A+20*index,y)
    if not d[0x9889]&32:result+=curve(t,0x73D02+20*index,x)
    else:
        result+=curve(t,0x73E6A+20*index,x)
        if flag==1:result+=curve(t,0x73ECE+16*index,d[0x92F0]*2)
    if d[0x9B40]==1:
        result=curve(t,0x73C9E+20*index,y)+curve(t,0x73D66+20*index,x)
    return result


def build(t,result,release):
    d=result['fields'];desc=result['descriptors'];curves=result['curves']
    for i in range(10):curves[i][:4]=[2,0,0,65535]
    for i in range(5):
        if release==1:upper=65535
        else:
            down=lower(t,i,int(bool(d[0x92D1]&8)),d[0x9B66],d[0x92F4]*2,d)&65535
            base=signed(d[0x9BEE] if d[0x9BF1]&1 else down,16)+word(0x77312)
            minimum=curve(t,(0x73E1A if d[0x9B40]==1 else 0x73DCA)+16*i,d[0x9B3E])
            upper=max(base&65535,minimum);curves[i+5][4:]=[down,down]
        curves[i][4:]=[upper,upper]
    for i in range(5 if release==1 else 10):
        desc['pointers'][i]=0xFFFF9B68+12*i;desc['operations'][i]=5;desc['kinds'][i]=6


def model(t):
    result=state(t);d=result['fields'];active=d[0x9B64]&1;release=(d[0x9B64]>>1)&1
    if d[0x8081]>=d[0x9BEA]:d[0x9BEC]=d[0x80EA]
    if not admit(d):active=release=0
    elif not active:
        if enter(t,d):active=1;release=0
    elif leave(d):
        if not release:release=1;d[0x815D]=0
        if d[0x815D]>=TCU[0x73C34+d[0x8084]] or d[0x8081]<d[0x9BEA]:active=release=0
    else:release=0
    d[0x9B64]=(d[0x9B64]&252)|active|(release<<1)
    history(d,active,release)
    if active:build(t,result,release)
    d[0x9BEA]=d[0x8081];d[0x9BF0]=d[0x8080]
    return result


def seed(t,rng):
    for a in BYTES:w(t,a,rng.randrange(256))
    for a in WORDS:w(t,a,rng.choice([0,255,256,6330,6331,32767,32768,65535]),2)
    for a in [0x8081,0x9BEA,0x8084]:w(t,a,rng.randrange(6))
    w(t,0x96C4,0);w(t,0x96C5,1);w(t,0x95D4+13,0)
    for i in range(10):
        w(t,0x9AEC+4*i,0x7404C+48*i,4);w(t,0x9B14+i,160+i);w(t,0x9B32+i,180+i)
        for j in range(6):w(t,0x9B68+12*i+2*j,rng.randrange(65536),2)


def direct():
    t=SHRotate(TCU);rng=random.Random(0x45AA4);counts=dict(admission=0,predicates=0,history=0,lower=0,builder=0,whole=0)
    for cls,source,meas,gate in itertools.product([0,1,2,6,127,128,255],[0,1,6,10,11,12,13,14,15],
                                                [0,255,256,257,32767,32768,65535],[0,1,2]):
        for a,v,n in [(0x8080,cls,1),(0x9B40,source,1),(0x80EA,meas,2),(0x9330,gate,1)]:w(t,a,v,n)
        assert t.run(0x45CE4)==admit(fields(t));counts['admission']+=1
    for flags,other,special,gate,pending,code,meas in itertools.product([0,1,128,129],[0,64],[0,4],[0,1],[0,2],[0,4,5,255],[6330,6331,6332]):
        for a,v,n in [(0x92D5,flags,1),(0x92D3,other,1),(0x92C5,special,1),(0x9338,gate,1),
                      (0x8088,pending,1),(0x8089,code,1),(0x80EA,meas,2),(0x96C4,0,1),(0x95D4+13,0,1)]:w(t,a,v,n)
        d=fields(t);assert t.run(0x45D30)==enter(t,d);assert t.run(0x45DD0)==leave(d)
        assert t.run(0x4617C)==int(bool(flags&128 and special&4))
        assert t.run(0x461A6)==int(bool(flags&128 and not special&4));counts['predicates']+=1
    for active,release,cls,oldcls,accepted,old,op in itertools.product([0,1],[0,1],[0,3,255],[0,3,255],[1,2],[1,2],[0,5]):
        seed(t,rng)
        for a,v in [(0x8080,cls),(0x9BF0,oldcls),(0x8081,accepted),(0x9BEA,old),(0x9B3D,op)]:w(t,a,v)
        d=fields(t);history(d,active,release);sp=t.r[15];t.r[5]=release;t.run(0x46030,active,limit=100000)
        assert fields(t)==d,(active,release,cls,oldcls,accepted,old,op,fields(t),d)
        assert t.r[15]==sp;counts['history']+=1
    for index,source,mode,flag,x,y in itertools.product(range(5),[0,1,6],[0,32],[0,1],[0,8,31,64,32768,65535],[0,1280,1536,2048,65535]):
        w(t,0x9B40,source);w(t,0x9889,mode);w(t,0x92F0,1536,2)
        d=fields(t);want=lower(t,index,flag,x,y,d);t.r[5]=flag;t.r[6]=signed(x,16)&0xFFFFFFFF;t.r[7]=signed(y,16)&0xFFFFFFFF
        assert t.run(0x460E0,index,limit=100000)==want,(index,source,mode,flag,x,y,want,t.r[0]);counts['lower']+=1
    for release,source,mode,flag,latch in itertools.product([0,1,2],[0,1,6],[0,32],[0,8],[0,1]):
        seed(t,rng)
        for a,v in [(0x9B40,source),(0x9889,mode),(0x92D1,flag),(0x9BF1,latch)]:w(t,a,v)
        want=state(t);build(t,want,release);sp=t.r[15];t.run(0x45E70,release,limit=100000)
        assert state(t)==want,(release,source,mode,flag,latch,state(t),want);assert t.r[15]==sp;counts['builder']+=1
    cases=list(itertools.product(range(4),[0,1,2,6,255],[0,1,128,129],[0,4],[0,1],[0,121,122,255]))
    for flags,cls,fault,special,gate,timer in cases:
        seed(t,rng)
        for a,v in [(0x9B64,flags),(0x8080,cls),(0x92D5,fault),(0x92C5,special),(0x9330,gate),
                    (0x815D,timer),(0x9B40,rng.choice([0,1,6,11])),(0x92D3,rng.choice([0,64])),
                    (0x9338,rng.randrange(2))]:w(t,a,v)
        w(t,0x80EA,rng.choice([255,256,6330,6331,65535]),2)
        want=model(t);sp=t.r[15];t.run(0x45AA4,limit=200000)
        assert state(t)==want,(flags,cls,fault,special,gate,timer,state(t),want)
        assert t.r[15]==sp;counts['whole']+=1
    return counts


class ObservedRelease(ObservedRetained):
    def __init__(self):
        super().__init__();self.release_pending=None;self.release_checks=0;self.release_rows=[]
    def instruction(self,pc):
        if self.release_pending is not None and pc==self.release_pending[0]:
            _,want,before=self.release_pending;assert state(self)==want,(before,state(self),want)
            self.release_rows.append(dict(before=before,after=want));self.release_checks+=1;self.release_pending=None
        if pc==0x45AA4:self.release_pending=(self.pr,model(self),state(self))
        return super().instruction(pc)


def restore(snapshot):
    t=ObservedRelease();t.ram={int(a,16):v for a,v in snapshot['ram'].items()}
    t.samples={int(a,16):v for a,v in snapshot['samples'].items()};return t


def retained(snapshot):
    t=restore(snapshot)
    for a,v in [(0x8080,6),(0x9C12,6),(0x8081,2),(0x9BEA,2),(0x9BF0,6),(0x8084,2),
                (0x916F,0),(0x9C7C,0),(0x9E88,0),(0x9B5C,0),(0x92D7,0),(0x9AE9,0),
                (0x92D1,0),(0x9BF5,0),(0x9330,0),(0x9338,0),(0x92D3,0),(0x92C5,0),
                (0x8088,0),(0x9B64,0),(0x9889,0)]:w(t,a,v)
    for a,v in [(0x9BF6,0),(0x9336,0),(0x80EA,3000),(0x9B3E,6400),(0x80F2,0),(0x9B66,31),(0x92F4,768)]:w(t,a,v,2)
    rows=[]
    for faults,special,timer,accepted,operation in [(1,0,50,2,0),(0,0,50,2,0),(0,0,121,2,0),
        (0,0,122,2,0),(1,0,0,2,0),(1,0,0,1,5),(0,0,20,0,5),(128,4,0,0,5),
        (128,0,0,0,5),(129,4,0,0,5)]:
        for a,v in [(0x92D5,faults),(0x92C5,special),(0x815D,timer),(0x8081,accepted),(0x9B3D,operation)]:w(t,a,v)
        t.curves.clear();t.stages.clear();t.run(0x4530C,limit=1000000)
        assert len(t.curves)==10
        assert [r(t,0x9B1E+2*i,2) for i in range(10)]==[x['expected'] for x in t.curves]
        rows.append(dict(input=dict(faults=faults,special=special,timer=timer,accepted=accepted,operation=operation),
                         overlay=t.release_rows[-1],thresholds=[r(t,0x9B1E+2*i,2) for i in range(10)],stages=copy.deepcopy(t.stages)))
    assert t.release_checks==t.overlay_checks==t.class_checks==len(rows)
    return rows


def replays(snapshots):
    rows=[]
    for call,cls,flags,special in itertools.product([150,211],[0,3,6],[0,1,3],[0,4]):
        t=restore(snapshots[str(call)]);t.application_call=call
        for a,v in [(0x8080,cls),(0x9C12,cls),(0x9B64,flags),(0x92C5,special)]:w(t,a,v)
        sp=t.r[15];t.run(0x44CFE,limit=1000000);selection_then_limit(t)
        assert t.r[15]==sp and t.release_checks==t.overlay_checks==t.class_checks==1
        rows.append(dict(call=call,cls=cls,oldflags=flags,special=special,state=state(t),
                         stages=t.stages,proposed=r(t,0x8084),accepted=r(t,0x8081),creations=t.creation_calls))
    return rows


def main():
    raw=(ROOT/'tcu-fault-selection-snapshots.json').read_bytes();prior=json.loads((ROOT/'tcu-fault-selection-verification.json').read_text())
    assert hashlib.sha256(TCU).hexdigest()==prior['tcu_sha256'];assert hashlib.sha256(raw).hexdigest()==prior['snapshots_sha256']
    snapshots=json.loads(raw);result=dict(scope=__doc__,tcu_sha256=prior['tcu_sha256'],snapshots_sha256=prior['snapshots_sha256'])
    result['direct']=direct();print('Direct:',result['direct'],flush=True)
    result['retained']=retained(snapshots['150']);print('Retained:',len(result['retained']),flush=True)
    result['replays']=replays(snapshots);print('Full replays:',len(result['replays']),flush=True)
    (ROOT/'tcu-release-thresholds-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
