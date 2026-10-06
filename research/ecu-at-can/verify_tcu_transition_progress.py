"""Original transition progress initialization, rate selection and accumulation.

No physical progress units or scheduler cadence are inferred. Original startup
call order is executed as a bounded instruction segment, not a complete boot.
"""
import hashlib
import itertools
import json
import random

from sh_rotate import SHRotate
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_dispatch import curve
from verify_tcu_transition_classification import ObservedClassification
from verify_tcu_source_selection import sample
from verify_tcu_ascending_map import lifecycle
from verify_tcu_request_admission import paired_snapshot

PROGRESS = [0x96C8, 0x96CA, 0x96CC]
RATES = [0x970C, 0x9710, 0x9714]
BYTE_FIELDS = [0x8089,0x9315,0x95AE,0x95C9,0x9410,0x99DC,0x99C4,0x99B0,0x971A]
WORD_FIELDS = [0x80FA,0x80FE,0x9334,0x9718,0x9708,*PROGRESS]
OUTPUTS = [*PROGRESS,*RATES,0x971A,0x9718,0x9708]


def word(a):
    return int.from_bytes(TCU[a:a+2], 'big')


def inputs(t):
    return {**{a:r(t,a) for a in BYTE_FIELDS},
            **{a:r(t,a,2) for a in WORD_FIELDS},
            **{a:signed(r(t,a,4)) for a in RATES}}


def initial_model(accepted):
    return {0:[0,0,0],1:[25600,0,0],2:[25600,0,25600],
            3:[25600]*3,4:[25600]*3}.get(accepted & 255,[25600,25600,0])


def integrate(flag, old, rate):
    limit = signed(word(0x770C4),16) if (flag & 255)==1 else 25600
    return max(0,min(signed(old+rate),limit))


def request_group(code,operation):
    code,operation=code&255,operation&65535
    if code<5: return 65535 if operation==18 else 7
    if code<12: return 65535 if operation in [6,8,10,12,16,17] else 8
    return 65535


def helper(function,d):
    scale = signed(d[0x9718],16)
    constants={0x32A86:0x770CC,0x32AFC:0x770D0,0x32B1C:0x770CE,0x32C0C:0x770C6}
    if function in constants:
        return -((signed(word(constants[function]),16)*scale)>>6)
    curves={0x32A54:0x70B40,0x32AA6:0x70B49,0x32B3C:0x70B24,0x32BDA:0x70B34}
    if function in curves:
        axis=2*d[0x80FA if function==0x32BDA else 0x80FE]
        return ((curve(curves[function],axis)>>8)*scale)>>6
    assert function==0x32B6E
    axis=(((2*d[0x80FE])&65535)*TCU[0x770C8]+((2*d[0x80FA])&65535)*TCU[0x770C9])//100
    axis=min((axis+signed(word(0x770CA),16))&0xFFFFFFFF,65535)
    d[0x9708]=axis
    return -(((curve(0x70B2D,axis)>>8)*scale)>>6)


def rates_model(d):
    code=d[0x8089]
    def put(index,fn): d[RATES[index]]=helper(fn,d)
    if code==0:
        put(0,0x32A54)
    elif code==1:
        put(2,0x32B3C); put(0,0x32A54)
    elif code in [2,3]:
        put(1,0x32AA6)
    elif code==4:
        put(2,0x32C0C)
    elif code in [5,6,7,10]:
        if code==5: put(0,0x32A86)
        if code==5: put(2,0x32B6E)
        put(1,0x32B1C)
        if code!=10 and d[0x95AE]&1: put(1,0x32AFC)
        if code==6: put(2,0x32B6E)
        if code in [7,10]: put(2,0x32B3C)
    elif code==11:
        put(2,0x32B3C)
        if d[0x9410]&2:
            put(2,0x32BDA)
            if d[0x99DC]&1: d[0x971A]|=1
    elif code==9:
        put(2,0x32BDA)
        if (d[0x99C4]&4 and d[0x95C9]&2) or (d[0x99B0]&2 and not d[0x95C9]&2):
            d[0x971A]|=1


def progress_model(d):
    d[0x971A]&=254
    if d[0x9315]&3:
        for a in [*PROGRESS,*RATES]: d[a]=0
    else:
        d[0x9718]=curve(0x70B39,d[0x9334])>>8
        rates_model(d)
        for i,a in enumerate(PROGRESS):
            d[a]=integrate(d[0x971A]&1 if i==2 else 0,signed(d[a],16),d[RATES[i]])


class SegmentEnd(Exception):
    pass


class ObservedProgress(ObservedClassification):
    def __init__(self):
        super().__init__()
        self.stop_before=None
        self.progress_checks=0
        self.pending_progress=None
        self.descending_entries=[]
        self.group_calls=[]
        self.pending_group=None

    def instruction(self,pc):
        if pc==self.stop_before: raise SegmentEnd
        if pc==0x4C880:
            code,operation=self.r[4]&255,self.r[5]&65535
            self.pending_group=(code,operation,request_group(code,operation))
        elif pc==0x4C8EA:
            code,operation,expected=self.pending_group
            assert self.r[0]==expected
            self.group_calls.append(dict(code=code,operation=operation,group=expected))
            self.pending_group=None
        if pc==0x32348:
            d=inputs(self); progress_model(d)
            self.pending_progress=d
        elif pc==0x323EA:
            d=self.pending_progress
            for a in OUTPUTS:
                size=4 if a in RATES else 1 if a==0x971A else 2
                assert r(self,a,size)==(d[a]&((1<<(8*size))-1)),(hex(a),r(self,a,size),d[a])
            self.progress_checks+=1
            self.pending_progress=None
        elif pc==0x4D010:
            self.descending_entries.append(dict(call=self.cycle,record=self.r[5]&65535,
                code=r(self,(self.r[5]&65535)+1),operation=r(self,(self.r[5]&65535)+8)))
        return super().instruction(pc)


def initialize_segment(t):
    # Original call48BC0 immediately followed by32140 at1E15C..1E166.
    sp=t.r[15]
    t.stop_before=0x1E168
    try:
        t.run(0x1E15C,limit=1000000)
    except SegmentEnd:
        pass
    else:
        raise AssertionError('startup segment failed to reach boundary')
    finally:
        t.stop_before=None
    assert t.r[15]==sp
    assert [r(t,a,2) for a in PROGRESS]==initial_model(r(t,0x8081))


def direct_cases():
    t=SHRotate(TCU); rng=random.Random(0x32348)
    counts=dict(initial=0,integrator=0,helpers=0,rates=0,progress=0,startup_segment=0,request_group=0)
    for code,operation in itertools.product(range(256),[0,1,5,6,7,8,9,10,11,12,13,16,17,18,19,255,0x106,0x108,0x112,65535,65536,65544]):
        t.r[5]=operation
        assert t.run(0x4C880,code)==request_group(code,operation)
        counts['request_group']+=1
    for accepted in range(256):
        w(t,0x8081,accepted)
        t.run(0x32140)
        assert [r(t,a,2) for a in PROGRESS]==initial_model(accepted)
        counts['initial']+=1
    for flag,old,rate in itertools.product([0,1,2,255,256,257],[-32768,-1,0,3839,3840,25599,25600,32767,0x7FFFFFFF],[-0x80000000,-256,-1,0,1,256,0x7FFFFFFF]):
        t.r[5],t.r[6]=old&0xFFFFFFFF,rate&0xFFFFFFFF
        assert t.run(0x32C2C,flag)==integrate(flag,old,rate)
        counts['integrator']+=1
    functions=[0x32A54,0x32A86,0x32AA6,0x32AFC,0x32B1C,0x32B3C,0x32B6E,0x32BDA,0x32C0C]
    for fn,scale,x,y in itertools.product(functions,[0,1,63,64,128,32767,32768,65535],[0,3328,12800,32767,32768,65535],[0,12800,65535]):
        for a,v in [(0x9718,scale),(0x80FE,x),(0x80FA,y),(0x9708,0xA5A5)]:w(t,a,v,2)
        d=inputs(t); expected=helper(fn,d)
        assert t.run(fn)&0xFFFFFFFF==expected&0xFFFFFFFF,(hex(fn),d,expected)
        assert r(t,0x9708,2)==d[0x9708]
        counts['helpers']+=1
    for code,bits in itertools.product(range(256),range(64)):
        for a in BYTE_FIELDS: w(t,a,rng.randrange(256))
        for a in WORD_FIELDS: w(t,a,rng.randrange(65536),2)
        for a in RATES: w(t,a,rng.getrandbits(32),4)
        w(t,0x8089,code)
        for i,(a,mask) in enumerate([(0x95AE,1),(0x95C9,2),(0x9410,2),(0x99DC,1),(0x99C4,4),(0x99B0,2)]):
            w(t,a,(r(t,a)&~mask)|(mask if bits&(1<<i) else 0))
        d=inputs(t); rates_model(d)
        t.run(0x328FC)
        for a in [*RATES,0x971A,0x9708]:
            size=4 if a in RATES else 1 if a==0x971A else 2
            assert r(t,a,size)==d[a]&((1<<(8*size))-1),(code,bits,hex(a),r(t,a,size),d[a])
        counts['rates']+=1
    t=ObservedProgress()
    for code,flags,trial in itertools.product([*range(12),255],range(8),range(8)):
        for a in BYTE_FIELDS: w(t,a,rng.randrange(256))
        for a in WORD_FIELDS: w(t,a,rng.choice([0,128,3840,12800,25599,25600,32768,65535]),2)
        for a in RATES: w(t,a,rng.choice([-1000,0,1000,0x7FFFFFFF]),4)
        w(t,0x8089,code); w(t,0x9315,flags|0xA0)
        t.run(0x32348)
        counts['progress']+=1
    for accepted in [0,1,2,3,4,5,255]:
        w(t,0x606F,accepted)
        initialize_segment(t)
        assert r(t,0x8081)==accepted
        counts['startup_segment']+=1
    return counts


def retained_trace(enabled=0):
    t=ObservedProgress(); rows=[]; last=None; source_rows=[]
    def upstream(t,call):
        if call==1:
            t.run(0x17230);t.run(0x17D54)
            w(t,0x921C,6500,4)
        sample(t,enabled)
        # One explicitly scheduled original progress task per application cycle.
        t.run(0x32348,limit=1000000)
        t.run(0x44CFE,limit=1000000);t.run(0x48C08,limit=1000000)
        if call in [1,2,80,81,100,150,200,320]:
            source_rows.append(dict(call=call,accepted=r(t,0x8081),code=r(t,0x9C87),
                operation=r(t,0x9C88),progress=[r(t,a,2) for a in PROGRESS],
                rates=[signed(r(t,a,4)) for a in RATES],flags=r(t,0x9C54),gate=r(t,0x9315)))
    def observe(t,call,subcall):
        nonlocal last
        head,count=r(t,0x96C4),r(t,0x96C5)
        state=dict(head=head,count=count,records=[dict(index=i,code=r(t,0x95DE+15*i),phase=r(t,0x95E1+15*i))
                         for i in [(head+j)%16 for j in range(count)]],source915a=r(t,0x915A,2))
        if state!=last:
            rows.append(dict(call=call,subcall=subcall,**state,**paired_snapshot(t)))
            last=state
    trace=lifecycle(25000,t=t,calls=320,samples={80:6500},prepare=initialize_segment,
                    upstream=upstream,observe=observe,require_ascending=False)
    assert rows[0]['records'][0]['code']==6 and rows[-1]['count']==0
    assert t.creation_calls[:2]==[[1,0,0],[6,8,0]]
    assert [code for _,code in t.retired]==[1]*3+[6]*3
    assert t.progress_checks==320 and t.pending_progress is None
    assert t.group_calls[:2]==[dict(code=1,operation=0,group=7),dict(code=6,operation=8,group=65535)]
    assert not t.descending_entries
    assert all(x['tcu_source915a']==32767 and x['at_correction']==0 for x in rows)
    return dict(input25=enabled,source_rows=source_rows,checkpoints=rows,
                ascending_trace=trace,classification_rows=t.classification_rows,
                progress_checks=t.progress_checks,classification_checks=t.classification_checks,
                descending_entries=t.descending_entries,group_calls=t.group_calls,
                acks=t.acks,retired=t.retired)


def main():
    counts=direct_cases()
    print('Direct checks:',counts,flush=True)
    traces=[retained_trace(x) for x in [0,1]]
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),direct_cases=counts,
                retained_traces=traces,
                limits='Startup segment and progress body execute; surrounding scheduler/peripherals and source units remain fixtures.939E production remains outside these traces.')
    path='research/ecu-at-can/tcu-transition-progress-verification.json'
    with open(path,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
