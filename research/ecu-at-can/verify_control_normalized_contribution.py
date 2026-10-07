"""Original seven-body group producing8118, with finite RTZ/state models.

Physical input identities, scheduler periods, remote DSC and actuator effects
remain unproved. Integration supplies explicit upstream samples, not outputs.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import verify_control_contributions as prior
import verify_control_magnitude as magnitude
from verify_control_contributions import ECU,TCU,w,r,f,rf,q,number,fixture,run
from verify_model_sources import lookup1,axis
from verify_control_sources import sample_points

ROOT=Path(__file__).resolve().parent


def filtered(e):
    value,old=rf(e,0x684C),rf(e,0x8120)
    factor=q(1-q(1-number(0xDA774)))
    want=q(value+q(factor*q(old-value)))
    if abs(q(value-want))<number(0x59880):want=value
    run(e,0x597B6);assert rf(e,0x8120)==want


def hysteresis(e):
    value=rf(e,0x8120);want=r(e,0x812A)
    if value<q(number(0xDA764)-number(0xDA768)):want=0
    elif value>number(0xDA764):want=1
    run(e,0x597E2);assert r(e,0x812A)==want


def countdown(e):
    want=ECU[0xDA760] if r(e,0x8134)==0 and r(e,0x812A)==1 else max(0,r(e,0x8128)-1)
    oldflag=r(e,0x812A)
    run(e,0x5980E);assert [r(e,0x8128),r(e,0x8134)]==[want,oldflag]


def first(e):
    want=lookup1(0xA36C4,rf(e,0x8120)) if r(e,0x8128)>0 else max(0,q(rf(e,0x811C)-number(0xDA778)))
    run(e,0x598B4);assert rf(e,0x811C)==want


def second_gate(e):
    value=rf(e,0x6818);threshold=lookup1(0xA36E8,rf(e,0x8120));want=r(e,0x812B)
    if value<number(0xDA77C):want=0
    elif value>=threshold:want=1
    run(e,0x598EA);assert r(e,0x812B)==want


def second(e):
    mode=r(e,0x7012)==1;value=lookup1(0xA36D0 if mode else 0xA36DC,rf(e,0x8120))
    count=r(e,0x8129);old=rf(e,0x8124);flag=r(e,0x812B)
    if r(e,0x8135)==0 and flag==1:want=value;count=ECU[0xDA761]
    else:
        count=max(0,count-1)
        want=max(0,q(old-number(0xDA76C if mode else 0xDA770))) if count==0 else old
    run(e,0x59924)
    assert [rf(e,0x8130),rf(e,0x8124),r(e,0x8129),r(e,0x8135)]==[value,want,count,flag]


def normalized(e):
    mapped=lookup1(0xA36AC if r(e,0x7012)==1 else 0xA36B8,rf(e,0x6CC8))
    denominator=q(q(q(q(number(0xCC028)*number(0xCA974))/2)*rf(e,0x7020))/60)
    update=abs(denominator)>number(0x5985C)
    want=q(q(mapped+max(rf(e,0x811C),rf(e,0x8124)))/denominator) if update else rf(e,0x8118)
    run(e,0x59720)
    assert [rf(e,0x812C),rf(e,0x8118)]==[mapped,want]
    return update,denominator


def group(e):
    filtered(e);hysteresis(e);countdown(e);first(e);second_gate(e);second(e)
    return normalized(e)


def direct():
    counts=dict(filter=0,hysteresis=0,countdown=0,first=0,gate=0,second=0,normalized=0)
    for old,value in itertools.product([-10,0,Fraction(1,1024),10,100],repeat=2):
        e=fixture();f(e,0x8120,old);f(e,0x684C,value);filtered(e);counts['filter']+=1
    points=sorted({number(0xDA764)+d for d in [-number(0xDA768)-1,-number(0xDA768),-number(0xDA768)+1,0,1]})
    for value,old in itertools.product(points,[0,1,2,255]):
        e=fixture();f(e,0x8120,value);w(e,0x812A,old);hysteresis(e);counts['hysteresis']+=1
    for flag,old,count in itertools.product([0,1,2,255],[0,1,2,255],[0,1,2,ECU[0xDA760],255]):
        e=fixture();w(e,0x812A,flag);w(e,0x8134,old);w(e,0x8128,count);countdown(e);counts['countdown']+=1
    for value,count,old in itertools.product(sample_points(0xA36C4),[0,1,255],[-1,0,1]):
        e=fixture();f(e,0x8120,value);w(e,0x8128,count);f(e,0x811C,old);first(e);counts['first']+=1
    for value,old in itertools.product(sample_points(0xA36E8),[0,1,2,255]):
        threshold=lookup1(0xA36E8,value)
        for sample in sorted({number(0xDA77C)+d for d in [-1,0,1]}|{threshold+d for d in [-1,0,1]}):
            e=fixture();f(e,0x8120,value);w(e,0x812B,old);f(e,0x6818,sample);second_gate(e);counts['gate']+=1
    for mode,flag,oldflag,count,old in itertools.product([0,1,2],[0,1,2],[0,1,2],[0,1,2,255],[-1,0,1]):
        e=fixture();w(e,0x7012,mode);w(e,0x812B,flag);w(e,0x8135,oldflag);w(e,0x8129,count)
        f(e,0x8124,old);f(e,0x8120,75);second(e);counts['second']+=1
    # The nearest binary32 samples around the stock denominator deadband.
    boundary=number(0x5985C)*60/q(q(number(0xCC028)*number(0xCA974))/2)
    from sh_rtz_float import rtz_bits
    from sh_exact_float import exact_value
    b=rtz_bits(boundary)
    near=[exact_value(b+d) for d in [-2,-1,0,1,2]]
    divisors=[-150,-1,0,1,150,*near,*[-v for v in near]]
    for mode,value,divisor,pair in itertools.product([0,1,2],sample_points(0xA36AC),divisors,[(0,0),(1,2),(2,1),(-2,-1)]):
        e=fixture();w(e,0x7012,mode);f(e,0x6CC8,value);f(e,0x7020,divisor)
        f(e,0x811C,pair[0]);f(e,0x8124,pair[1]);f(e,0x8118,7)
        normalized(e);counts['normalized']+=1
    return counts



def caller_cases():
    import copy
    outputs=[(a,4) for a in [0x8118,0x811C,0x8120,0x8124,0x812C,0x8130]]
    outputs += [(a,1) for a in [0x8128,0x8129,0x812A,0x812B,0x8134,0x8135]]
    functions=[0x597B6,0x597E2,0x5980E,0x598B4,0x598EA,0x59924,0x59720]
    count=0
    for mode,value,oldflag in itertools.product([0,1,2],[0,100],[0,1]):
        e=fixture();prepare(e);w(e,0x7012,mode);w(e,0x8134,oldflag)
        for a,v in [(0x684C,value),(0x6818,value),(0x6CC8,80),(0x7020,150),(0x8120,75)]:f(e,a,v)
        other=copy.deepcopy(e);group(e);pc=0x1A598;sp=other.r[15];seen=[]
        for _ in range(100000):
            if pc==0x1A5C2:break
            if pc in functions:seen.append(pc)
            nxt,delay=other.instruction(pc)
            if delay:
                _,nested=other.instruction(pc+2);assert not nested
            pc=nxt
        else:raise AssertionError('caller instruction bound')
        assert seen==functions and other.r[15]==sp
        assert [r(other,a,n) for a,n in outputs]==[r(e,a,n) for a,n in outputs]
        count+=1
    return count


def prepare(e):
    magnitude.initialize(e)
    # Start local histories at explicit zero, not a claim about boot ownership.
    for a in [0x8118,0x811C,0x8120,0x8124,0x812C,0x8130]:f(e,a,0)
    for a in [0x8128,0x8129,0x812A,0x812B,0x8134,0x8135]:w(e,a,0)


def step(e,call):
    f(e,0x684C,0 if call<=20 or 141<=call<=220 else 100)
    f(e,0x6818,0 if call<=40 or 121<=call<=180 else 100)
    f(e,0x6CC8,0 if call<=10 else 80 if call<=160 else 160)
    update,divisor=group(e)
    row=magnitude.integrated_step(e,call)
    row.update(normalized_updated=update,normalized_divisor=float(divisor),
               normalized_contribution=float(rf(e,0x8118)),
               normalization_parts=[float(rf(e,a)) for a in [0x8120,0x811C,0x8124,0x812C]],
               normalization_flags=[r(e,a) for a in [0x8128,0x8129,0x812A,0x812B,0x8134,0x8135]])
    return row


def main():
    counts=direct();counts['caller_segment']=caller_cases();print('Direct:',counts,flush=True)
    rows,boundaries=prior.lifecycle(prepare=prepare,upstream=step,checkpoints={10,11,20,21,40,41,120,121,140,141,160,161,180,181,220,221})
    print('Retained:',320,'paired:',len(boundaries),flush=True)
    tables={}
    for a in range(0xA36AC,0xA36E9,12):
        n=int.from_bytes(ECU[a:a+2],'big');xp=int.from_bytes(ECU[a+4:a+8],'big');vp=int.from_bytes(ECU[a+8:a+12],'big')
        tables[hex(a)]=dict(axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n))))
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                direct=counts,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,
                constants={hex(a):float(number(a)) for a in [0xCC028,0xCA974,0x5985C,0x59880,*range(0xDA764,0xDA780,4)]},
                timer_reloads=list(ECU[0xDA760:0xDA762]),tables=tables,lifecycle=rows)
    (ROOT/'control-normalized-contribution-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
