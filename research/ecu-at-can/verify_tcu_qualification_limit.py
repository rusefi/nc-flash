"""CAN215-derived qualification limit, history publication and original caller order.

Whole23544 executes, including fall-through2378A and all arithmetic helpers.
Explicit inputs/admission and bounded scheduling are not physical units/timing.
"""
import hashlib
import itertools
import json
import random

from sh_subset import signed
from verify_can201_byte6 import TCU,w,r
from verify_tcu_request_dispatch import curve
from verify_tcu_request_maps import lookup
from verify_tcu_transition_classification import pending_model
from verify_tcu_transition_progress import ObservedProgress,initialize_segment,SegmentEnd
from verify_tcu_phase_retirement import full_fixture
from verify_can215_feedback import sender,receive
from verify_tcu_request_admission import paired_snapshot

WORDS=[0x809C,0x80E8,0x80EE,0x80EA,0x80F6,0x8108,0x92E2,0x92E4,0x92E6,0x92F6,
       0x939C,0x939E,0x93F2,0x9394,0x933E,0x9398,0x93F0,0x93F6,0x80F8]
BYTES=[0x92CB,0x92D1,0x9310,0x9396,0x93F5,0x815A,0x8159,0x815B,0x93F4,
       0x93F8,0x939A,0x8089]
HISTORY_A=[0x93A0+2*i for i in range(15)]
HISTORY_B=[0x93BE+2*i for i in range(25)]
PREFIX_WORDS=[0x80F6,0x8108,0x939C,0x939E,0x93F2,0x9394,*HISTORY_A,*HISTORY_B]
PREFIX_BYTES=[0x9396,0x93F5]
TAIL_WORDS=[0x80F8,0x93F6,0x9398,0x93F0]
TAIL_BYTES=[0x815A,0x8159,0x815B,0x93F4,0x93F8,0x939A]


def div(a,b):
    return abs(a)//abs(b)*(-1 if (a<0)!=(b<0) else 1)


def clip(x,lo,hi):return max(lo,min(x,hi))


def snapshot(t):
    return {**{a:r(t,a,2) for a in [*WORDS,*HISTORY_A,*HISTORY_B]},
            **{a:r(t,a) for a in BYTES}}


def correction_model(d):
    x=d[0x80E8]
    value=(curve(0x7035C,x)>>2)-9600
    if d[0x92D1]&4:value-=(curve(0x7036F,x)>>2)-9600
    if d[0x92D1]&8:value-=(lookup(0x70382,x,d[0x92F6])>>2)-9600
    return value-16*d[0x9310]


def category(value,previous):
    axis=(value&65535)>>8
    bounds=TCU[0x70320:0x70327]
    index=6 if axis>=bounds[6] else next(i for i,v in enumerate(bounds) if axis<v)
    if index<previous and axis>=bounds[index]-TCU[0x76E8C]:index+=1
    return index


def prefix_model(d):
    for addresses,new in [(HISTORY_A,d[0x80F6]),(HISTORY_B,d[0x8108])]:
        values=[new,*[d[a] for a in addresses[:-1]]]
        for a,v in zip(addresses,values):d[a]=v
    numerator=(signed(d[0x80EE],16)<<15)&0xFFFFFFFF
    divisor=d[0x80E8]
    quotient=min(numerator//divisor,65535) if divisor else (65535 if numerator else 0)
    ratio=min((quotient*51200)>>15,51200)
    factor=curve(0x70331,ratio)>>1
    d[0x939C],d[0x93F2]=ratio,factor
    scaled=lambda a:clip(2*div(signed(d[a],16)*factor,12800),-6400,59135)
    first,second,third=scaled(0x92E4),scaled(0x92E6),scaled(0x92E2)
    d[0x80F6],d[0x8108]=(first>>1)&65535,(second>>1)&65535
    argument=(first+6400)&65535
    d[0x939E]=(third+6400)&65535
    d[0x9396]=category(argument,d[0x9396])
    d[0x93F5]=category(d[0x939E],d[0x93F5])
    correction=correction_model(d)
    # Firmware MULS.W truncates this returned32-bit correction to signed16.
    adjusted=clip(div(signed(correction,16)*factor,12800),-9600,59135)
    d[0x9394]=(adjusted>>1)&65535
    if d[0x92CB]&2:
        d[0x80F6]=d[0x8108]=d[0x9394]=32767
        d[0x939E]=65535
        d[0x9396]=d[0x93F5]=6
    return signed(argument,16),d[0x9396]


def slew(old,target,factor):
    factor=max(signed(factor,16),128)
    diff=(target&65535)-(old&65535)
    step=clip(div(diff*128,factor),-32768,32767)
    if diff and not step:step=1 if diff>0 else -1
    return signed(old,16)+step


def phase_for_code(t,code):
    head,count=r(t,0x96C4),r(t,0x96C5)
    for j in range(count):
        i=(head+j)%16
        if r(t,0x95DE+15*i)==code:return signed(r(t,0x95E1+15*i),8)
    return -1


def tail_model(d,argument,klass,pending,phase):
    result=signed(argument,16)
    retained=signed(d[0x9398],16)
    status=klass&255
    if not -1280<=signed(d[0x933E],16)<1280:d[0x815A]=0
    if d[0x93F4]==1:
        d[0x8159]=d[0x815A];d[0x815B]=255;d[0x93F0]=d[0x809C]
    if pending:
        code=d[0x8089];assert code<12
        descending=code>=5
        to=TCU[0x5D446+code]
        a,b=(TCU[0x76E8F],TCU[0x76E90]) if descending else (TCU[0x76E8D],TCU[0x76E8E])
        diff=signed(d[0x93F0]-d[0x809C],16)
        changed=diff>=1280 or diff<=-1280
        if changed:d[0x815B]=0;d[0x93F0]=d[0x809C]
        if d[0x8159]>=a and (d[0x93F4]==0 or d[0x93F8]&1) and d[0x815B]>=b and not changed:
            status=d[0x939A]
            if descending:result=slew(d[0x93F6],result,TCU[0x7032C+to]*128)
            if phase>=1:result=signed(d[0x93F6],16)
        if not descending:
            retained=result
            if TCU[0x70327+to-1]==1 and (argument&65535)>=(result&65535):retained=argument
    if d[0x92CB]&2:result=retained=65535;status=6
    d[0x80F8]=d[0x93F6]=result&65535;d[0x9398]=retained&65535
    d[0x939A]=status;d[0x93F4]=0;d[0x93F8]&=254


class ObservedLimit(ObservedProgress):
    def __init__(self):
        super().__init__()
        self.prefix_expected=self.tail_expected=None
        self.limit_checks=self.tail_checks=0
        self.order=[]
    def instruction(self,pc):
        if pc==0x48C08:self.order.append('selection')
        if pc==0x23544:
            d=snapshot(self);prefix_model(d);self.prefix_expected=d
            self.order.append('limit')
        if pc==0x2378A:
            if self.prefix_expected is not None:
                d=self.prefix_expected
                for a in PREFIX_WORDS+PREFIX_BYTES:
                    size=1 if a in PREFIX_BYTES else 2
                    assert r(self,a,size)==d[a],(hex(a),r(self,a,size),d[a])
                self.limit_checks+=1;self.prefix_expected=None
            d=snapshot(self)
            tail_model(d,self.r[4],self.r[5],pending_model(self),phase_for_code(self,d[0x8089]))
            self.tail_expected=d
        if pc==0x2399E:
            for a in TAIL_WORDS+TAIL_BYTES:
                size=1 if a in TAIL_BYTES else 2
                assert r(self,a,size)==self.tail_expected[a],(hex(a),r(self,a,size),self.tail_expected[a])
            self.tail_checks+=1;self.tail_expected=None
        return super().instruction(pc)


def selection_then_limit(t):
    sp=t.r[15];start=len(t.order);t.stop_before=0x1EAD2
    try:t.run(0x1EAC6,limit=1000000)
    except SegmentEnd:pass
    else:raise AssertionError('missing segment stop')
    finally:t.stop_before=None
    assert t.r[15]==sp and t.order[start:]==['selection','limit']


def can_inputs(t,primary):
    _,payload=sender(primary,0)
    receive(t,payload)
    w(t,0xA98C,1)  # Explicit healthy diagnostic admission, not a producer claim.
    t.run(0x516E6);t.run(0x216D8)
    assert r(t,0x92E2,2)==r(t,0x92E4,2)==primary*32
    return payload.hex(' ')


def direct_cases():
    t=ObservedLimit();rng=random.Random(0x23544)
    counts=dict(correction=0,slew=0,prefix=0,tail=0,capture=0)
    for x,flags,axis,byte in itertools.product([0,2048,5000,10000,32767,32768,65535],[0,4,8,12],[0,12800,65535],[0,17,255]):
        for a,v in [(0x80E8,x),(0x92F6,axis)]:w(t,a,v,2)
        w(t,0x92D1,flags);w(t,0x9310,byte)
        assert signed(t.run(0x23A44))==correction_model(snapshot(t))
        counts['correction']+=1
    for old,target,factor in itertools.product([0,1,32767,32768,65535],[0,1,32767,32768,65535],[0,127,128,129,256,32767,32768,65535]):
        t.r[5],t.r[6]=target,factor
        assert signed(t.run(0x239D2,old))==slew(old,target,factor)
        counts['slew']+=1
    for n in range(1800):
        for a in WORDS+HISTORY_A+HISTORY_B:w(t,a,rng.randrange(65536),2)
        for a in BYTES:w(t,a,rng.randrange(256))
        for a in [0x80E8,0x80EE,0x92E2,0x92E4,0x92E6]:
            w(t,a,rng.choice([0,1,1000,10000,32767,32768,65535]),2)
        w(t,0x8088,1)
        t.run(0x23544,limit=1000000)
        counts['prefix']+=1
    for code,phase,capture,timer,difference in itertools.product(range(12),[0,1,3],[0,1,2],[0,5,6,12,18,49,255],[-1281,-1280,-1279,0,1279,1280]):
        for a in WORDS:w(t,a,rng.randrange(65536),2)
        for a in BYTES:w(t,a,rng.randrange(256))
        w(t,0x8088,2);w(t,0x96C4,15);w(t,0x96C5,1)
        w(t,0x95DE+15*15,code);w(t,0x95E1+15*15,phase)
        w(t,0x95D4+15*15+1,0)
        w(t,0x8089,code);w(t,0x93F4,capture);w(t,0x8159,timer);w(t,0x815B,timer)
        w(t,0x93F0,10000+difference,2);w(t,0x809C,10000,2)
        t.r[5]=rng.randrange(7)
        t.run(0x2378A,rng.randrange(65536),limit=1000000)
        counts['tail']+=1
    for operation,source,flags in itertools.product([0,1,255,256,65535,65536],[0,12345,65535],[0,1,0xFE,0xFF]):
        w(t,0x939E,source,2);w(t,0x93F6,0x1234,2);w(t,0x93F8,flags)
        t.r[5]=operation;t.run(0x239B2)
        assert r(t,0x93F4)==1
        assert r(t,0x93F6,2)==(source if operation&65535==0 else 0x1234)
        assert r(t,0x93F8)==(flags|1 if operation&65535==0 else flags)
        counts['capture']+=1
    return counts


def can_classification_probe(primary, replacement=None):
    t=ObservedLimit();t.ram=dict(full_fixture().ram)
    w(t,0x606F,1);initialize_segment(t)
    for a,v in [(0x8080,6),(0x8084,2),(0x92D0,4),(0xA93A,1)]:w(t,a,v)
    for a,v in [(0x80EA,4672),(0x80E8,1000),(0x80EE,1000),(0x80F6,4224),(0x809C,20000),(0x809A,25000)]:w(t,a,v,2)
    for a in [0x921C,0x9220]:w(t,a,5000,4)
    t.run(0x48C08,limit=1000000)
    assert r(t,0x8081)==2
    # Explicit upstream reset gate, then 80 original progress services without
    # phase/timer service. This is a bounded scheduling/gate experiment.
    w(t,0x9315,1);t.run(0x32348)
    w(t,0x9315,0)
    for _ in range(80):t.run(0x32348)
    assert r(t,0x96C8,2)==8400
    payload=can_inputs(t,primary)
    t.run(0x23544,limit=1000000)
    published=r(t,0x939E,2)
    changed_payload=can_inputs(t,replacement) if replacement is not None else None
    # The changed CAN input, if any, has not yet reached23544. Original caller
    # classifies with the preceding939E, then publishes the changed limit.
    w(t,0x8084,1)
    for call in range(300):
        selection_then_limit(t)
        if r(t,0x8081)==1:break
        t.run(0x11014)
    else:raise AssertionError((primary,t.classification_rows,t.creation_calls))
    return dict(primary=primary,replacement=replacement,can215=payload,
                changed_can215=changed_payload,previous_limit=published,
                base92e2=r(t,0x92E2,2),limit939e=r(t,0x939E,2),
                limit9c52=r(t,0x9C52,2),candidate_delay_ticks=call,
                progress=[r(t,a,2) for a in [0x96C8,0x96CA,0x96CC]],
                accepted=r(t,0x8081),code=r(t,0x9C87),operation=r(t,0x9C88),
                creation_calls=t.creation_calls,retired_callbacks=t.retired,
                phase_codes=[r(t,0x95DE+15*((r(t,0x96C4)+i)%16)) for i in range(r(t,0x96C5))],
                classifications=t.classification_rows,group_calls=t.group_calls,
                order=t.order,limit_checks=t.limit_checks,tail_checks=t.tail_checks,
                **paired_snapshot(t))


def main():
    counts=direct_cases();print('Direct checks:',counts,flush=True)
    probes=[can_classification_probe(x) for x in [25,100]]
    assert [p['code'] for p in probes]==[6,0],probes
    lag=[can_classification_probe(a,b) for a,b in [(25,100),(100,25)]]
    assert [p['code'] for p in lag]==[6,0]
    assert [p['limit939e'] for p in lag]==[12736,7984]
    assert [p['limit9c52'] for p in lag]==[9600,12736]
    for p in probes+lag:
        assert p['candidate_delay_ticks']==0
        assert p['phase_codes']==([6] if p['code']==6 else [1,0])
        assert p['can216'].startswith('ff fe') and p['at_correction']==0
    from verify_can215_feedback import ECU
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                direct_cases=counts,total_direct_cases=sum(counts.values()),
                can_classification_probes=probes,publication_lag_probes=lag)
    path='research/ecu-at-can/tcu-qualification-limit-verification.json'
    with open(path,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
