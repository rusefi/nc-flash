"""Original magnitude-selected baseline and activation holdoff group.

72B4/72BC producer identity remains open. Original initialization and consumers
execute; synthetic input changes are not CAN producer attribution.
"""
import hashlib
import itertools
import json
from fractions import Fraction

import verify_control_contributions as prior
from verify_control_contributions import ECU,TCU,w,r,f,rf,q,number,fixture,run
from verify_control_input_history import checksum
from verify_model_sources import lookup1,axis
from verify_control_sources import sample_points


def initialize(e):
    run(e,0x41A34)
    for a in [0x72B4,0x72BC]:assert rf(e,a)==0;checksum(e,a)
    assert r(e,0x72C4)==0


def first(e):
    if r(e,0x7242)!=1:want=0
    else:
        high=abs(rf(e,0x72B4))>=number(0xD99A4)
        base=(0xDA6D8 if high else 0xDA6E0) if r(e,0x67AC)==1 else (0xDA6E8 if high else 0xDA6F0)
        want=number(base+(0 if r(e,0x7012)==1 else 4))
    run(e,0x59504);assert rf(e,0x810C)==want


def second(e):
    value=abs(rf(e,0x72BC))
    want=next((number(v) for threshold,v in [(0xDA6D4,0xDA70C),(0xDA6D0,0xDA708),(0xDA6CC,0xDA704)] if value>number(threshold)),0)
    run(e,0x595D0);assert rf(e,0x8108)==want


def factors(e):
    width=q(number(0xDA710)-number(0xDA714))
    assert abs(width)>number(0x59700)
    value=q(q(rf(e,0x6D5C)-number(0xDA714))/width)
    a=max(number(0xDA718),min(1,value));b=max(number(0xDA71C),min(1,value))
    run(e,0x59626)
    assert [rf(e,0x80F4),rf(e,0x80F8)]==[a,b] and b==1


def curve_factor(e):
    want=lookup1(0xA36A0,rf(e,0x6D28))
    run(e,0x593C4);assert rf(e,0x8110)==want


def combine(e):
    want=q(q(rf(e,0x80F4)*rf(e,0x8110))*max(rf(e,0x8108),rf(e,0x810C)))
    run(e,0x593DE);assert rf(e,0x80FC)==want


def pulse(e):
    gate,previous,count=r(e,0x7242),r(e,0x8114),r(e,0x8104)
    if gate==0:want=0;branch='clear'
    elif previous==0 and count==0:
        scale=number(0xDA700) if r(e,0x8040)==1 else 1
        want=q(q(q(rf(e,0x80F8)*number(0xDA6F8))*rf(e,0x8110))*scale);branch='pulse'
    else:want=max(0,q(rf(e,0x8100)-number(0xDA6FC)));branch='decay'
    timer=ECU[0xDA6C8] if gate==1 and previous==0 else max(0,count-1)
    run(e,0x59402)
    assert [rf(e,0x8100),r(e,0x8104),r(e,0x8114)]==[want,timer,gate]
    return branch


def group(e):
    first(e);second(e);factors(e);curve_factor(e)
    branch=pulse(e);combine(e)
    return branch


def integrated_step(e,call):
    gate=0 if call==2 or 4<=call<=16 or call in [40,42] or 61<=call<=80 else 2 if call==41 else 1
    w(e,0x7242,gate)
    if call==61:f(e,0x72BC,201)
    if call==81:f(e,0x6D5C,7);w(e,0x8040,1)
    if call==101:f(e,0x72B4,-9999)
    if call==121:f(e,0x6D28,20)
    if call==141:f(e,0x6D28,60)
    if call==161:f(e,0x6D28,80);f(e,0x6D5C,0);w(e,0x8040,0)
    old=r(e,0x8104);branch=group(e)
    if call in [1,17,41,43,81]:assert branch=='pulse'
    if call==3:assert branch=='decay' and rf(e,0x8100)==0 and old==11 and r(e,0x8104)==12
    if call==41:assert r(e,0x8104)==0
    return dict(magnitude_gate=gate,magnitude_branch=branch,magnitude_holdoff=r(e,0x8104),
                magnitude_inputs=[float(rf(e,a)) for a in [0x72B4,0x72BC]],
                magnitude_choices=[float(rf(e,a)) for a in [0x810C,0x8108]],
                magnitude_factors=[float(rf(e,a)) for a in [0x80F4,0x80F8,0x8110]],
                magnitude_baseline=float(rf(e,0x80FC)),magnitude_correction=float(rf(e,0x8100)))


def main():
    counts=dict(initializers=0,first=0,second=0,factors=0,curve=0,combine=0,pulse=0)
    for mask,value in itertools.product([0x10,0x30,0xF0],[-1,0,7]):
        e=fixture();e.sr=mask;f(e,0x72B4,value);f(e,0x72BC,value);w(e,0x72C4,255)
        initialize(e);counts['initializers']+=1
    for gate,enabled,mode,value in itertools.product([0,1,2,255],[0,1,2],[0,1,2],[-10000,-9999,-9998,0,9998,9999,10000]):
        e=fixture();w(e,0x7242,gate);w(e,0x67AC,enabled);w(e,0x7012,mode);f(e,0x72B4,value)
        first(e);counts['first']+=1
    for value in [-201,-200,-199,-101,-100,-99,-51,-50,-49,0,49,50,51,99,100,101,199,200,201]:
        e=fixture();f(e,0x72BC,value);second(e);counts['second']+=1
    for value in sorted(set([Fraction(x,8)+delta for x in [0,28,56] for delta in [Fraction(-1,8),0,Fraction(1,8)]]+[-10,10])):
        e=fixture();f(e,0x6D5C,value);factors(e);counts['factors']+=1
    for value in sample_points(0xA36A0):
        e=fixture();f(e,0x6D28,value);curve_factor(e);counts['curve']+=1
    for values in itertools.product([-1,0,Fraction(1,2)],repeat=4):
        e=fixture()
        for a,v in zip([0x80F4,0x8110,0x8108,0x810C],values):f(e,a,v)
        combine(e);counts['combine']+=1
    for gate,previous,count,flag,factor,old in itertools.product([0,1,2,255],[0,1,2,255],[0,1,11,12,255],[0,1,2],[-1,0,1],[-1,0,1]):
        e=fixture()
        for a,v in [(0x7242,gate),(0x8114,previous),(0x8104,count),(0x8040,flag)]:w(e,a,v)
        f(e,0x80F8,1);f(e,0x8110,factor);f(e,0x8100,old)
        pulse(e);counts['pulse']+=1
    rows,boundaries=prior.lifecycle(prepare=initialize,upstream=integrated_step,
                                  checkpoints={3,4,16,17,18,39,42,43,121,141,161})
    a=0xA36A0;n=int.from_bytes(ECU[a:a+2],'big');xp=int.from_bytes(ECU[a+4:a+8],'big');vp=int.from_bytes(ECU[a+8:a+12],'big')
    constants={hex(a):float(number(a)) for a in [0xD99A4,*range(0xDA6CC,0xDA720,4)]}
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,
        constants=constants,countdown_reload=ECU[0xDA6C8],map=dict(axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n)))),
        lifecycle=rows,limits='Original six local bodies plus41A34 protected initialization;72B4/72BC later changes are explicit fixtures, no CAN producer established. Other input/status values, cross-task schedule, serial peer and remaining contributions remain fixtures. Original CAN211 latch and paired TCU packer/ECU decoder path retained; physical attribution unproved.'),indent=2))


if __name__=='__main__':main()
