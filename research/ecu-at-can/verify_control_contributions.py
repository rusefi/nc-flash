"""Original baseline map/average and CAN211-latch-gated contribution.

Finite RTZ oracles and retained ECU/TCU integration. Task cadence and physical
signal identities remain unproved; no direct contribution-output injection
in the integrated lifecycle.
"""
import hashlib
import itertools
import json
from fractions import Fraction

import verify_control_baseline_source as chain
from verify_control_baseline_source import ECU,TCU,w,r,f,rf,q,number,fixture,run
from verify_model_sources import lookup1,lookup2,map2_info,axis
from verify_control_sources import sample_points
from verify_traction_flags import receive211,protected_byte


def average(e):
    count=r(e,0x80D8,2);total=rf(e,0x80D4);value=rf(e,0x80D0)
    if r(e,0x73C4)&0x80:
        count,total,value=65535,0,rf(e,0x6D20)
    elif count:
        count-=1;total=q(total+rf(e,0x6D20));value=q(total/(65535-count))
    run(e,0x590A0)
    assert [r(e,0x80D8,2),rf(e,0x80D4),rf(e,0x80D0)]==[count,total,value]


def baseline_map(e):
    want=lookup2(0xA365C,rf(e,0x6D38),rf(e,0x6D30))
    run(e,0x5904C);assert rf(e,0x80C8)==want


def baseline_extra(e):
    want=lookup1(0xA3650,rf(e,0x80D0)) if rf(e,0x6D30)<number(0xDA474) else 0
    run(e,0x59070);assert rf(e,0x80CC)==want==0


def baseline_sum(e):
    want=q(rf(e,0x80C8)+rf(e,0x80CC))
    run(e,0x5903C);assert rf(e,0x80C4)==want


def blend_maps(e):
    mode=r(e,0x7012)==1
    first=lookup1(0xA3670 if mode else 0xA367C,rf(e,0x6D28))
    second=lookup1(0xA3688 if mode else 0xA3694,rf(e,0x6D28))
    run(e,0x591A0);run(e,0x591D6)
    assert [rf(e,0x80E4),rf(e,0x80E8)]==[first,second]


def blend_weight(e):
    old=rf(e,0x80EC)
    want=min(1,q(old+number(0xDA5C0))) if r(e,0x7234)==1 else max(0,q(old-number(0xDA5C4)))
    run(e,0x5920C);assert rf(e,0x80EC)==want


def contribution(e):
    enabled=r(e,0x67AC)==1 and r(e,0x7978)==0
    if enabled:
        src,other=rf(e,0x80E8),rf(e,0x80E4)
        weight=q(1-q(1-rf(e,0x80EC)))
        blend=q(src+q(weight*q(other-src)))
        want=src if abs(q(src-blend))<number(0x59348) else blend
    else:want=0
    run(e,0x59154);assert rf(e,0x80DC)==want


def map_group(e):
    baseline_map(e);baseline_extra(e);baseline_sum(e)


def blend_group(e):
    blend_maps(e);blend_weight(e);contribution(e)


def correction(e):
    gate,previous=r(e,0x67AC),r(e,0x80F0)
    mode,special=r(e,0x7012)==1,r(e,0x6E3C)==1
    if gate==0:want=0
    elif previous==0:
        offset=(0 if special else 4) if mode else 8
        base=0xDA59C if r(e,0x7242)==1 else 0xDA5A8
        want=number(base+offset)
    else:
        address=(0xDA5B4 if special else 0xDA5B8) if mode else 0xDA5BC
        want=max(0,q(rf(e,0x80E0)-number(address)))
    run(e,0x59250)
    assert rf(e,0x80E0)==want and r(e,0x80F0)==gate


def latch_from_can(e,flags,count):
    old=r(e,0x7978)
    receive211(e,flags)
    # Other latch requests/edge state are held inactive in this fixture.
    w(e,0x7974,count,2)
    want=0 if count==0 else 1 if r(e,0x6A20)==1 else old
    run(e,0x4E80C)
    assert r(e,0x7978,2)==(want<<8)|(want^255)
    return want


def lifecycle(prepare=None, upstream=None, checkpoints=()):
    """Retained paired pipeline; optional original producers run before59250.

    Default behavior and JSON are unchanged. Callbacks may provide additional
    checked evidence fields; they do not replace serial/CAN validation.
    """
    e=chain.setup_loop(numeric_fixtures=False);chain.initialize(e);chain.init_history(e)
    for a in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,a,0)
    protected_byte(e,0x722E,1);run(e,0x4E7F4)
    w(e,0x67AC,1);w(e,0x73C4,128);f(e,0x6D20,90);average(e);w(e,0x73C4,0)
    f(e,0x6D38,20);f(e,0x6D30,0);f(e,0x6D28,80)
    f(e,0x7020,150);f(e,0x6DB4,150);f(e,0x6CD4,0)
    map_group(e);chain.baseline(e);chain.initialize_records(e)
    f(e,0x6CB4,8);run(e,0x1DED8);w(e,0x722A,1);w(e,0x6536,1)
    w(e,0x5634,3);w(e,0x5635,1);w(e,0x8194,1);w(e,0x7346,1);w(e,0x7016,1)
    boundaries={1,2,10,11,12,20,21,22,30,31,32,40,41,50,51,60,61,80,81,100,101,120,140,160,180,181,190,191,200,201,220,240,260,280,300,320}
    if prepare is not None:prepare(e)
    rows=[];weight_max=False;weight_zero=False
    for call in range(1,321):
        flags=0x2000 if 11<=call<=20 or 41<=call<=50 else 0
        count=0 if 31<=call<=40 or 61<=call<=70 else 1
        latch=latch_from_can(e,flags,count)
        if call==81:w(e,0x7012,1)
        if call==101:f(e,0x6D38,80);f(e,0x6D30,20)
        if call==161:w(e,0x7012,2)
        if call==181:w(e,0x67AC,0)
        if call==191:w(e,0x67AC,1)
        w(e,0x7234,1 if call<=160 else 0)
        average(e);map_group(e)
        extra=upstream(e,call) if upstream is not None else {}
        correction(e);blend_group(e)
        weight_max |= rf(e,0x80EC)==1
        weight_zero |= call>160 and rf(e,0x80EC)==0
        chain.source_group(e);chain.group(e);chain.inputs(e);chain.ratio(e);chain.remainder(e)
        chain.input_map(e);chain.hysteresis(e);chain.input_select(e)
        chain.timer(e);chain.holdoff(e);chain.decay(e);chain.bounds(e);chain.source_map(e);chain.bounded(e);chain.coupling(e)
        row=chain.integrated(e,call,update_can=call in boundaries)
        assert latch==int(11<=call<=30 or 41<=call<=60)
        assert (rf(e,0x80DC)==0)==bool(latch or 181<=call<=190)
        if call in boundaries or call in checkpoints:
            row.update(can211_flags=flags,latch=latch,weight=float(rf(e,0x80EC)),
                       mapped=float(rf(e,0x80C4)),gated=float(rf(e,0x80DC)),
                       correction=float(rf(e,0x80E0)),contribution_enable=r(e,0x67AC),
                       baseline=float(rf(e,0x80BC)),current=float(rf(e,0x8048)),
                       average=float(rf(e,0x80D0)))
            row.update(extra)
            rows.append(row)
        chain.decay_step(e);chain.lower_source(e);chain.publish_records(e)
    assert weight_max and weight_zero
    return rows,boundaries


def main():
    counts=dict(average=0,average_retained=0,map=0,extra=0,sum=0,
                blend_maps=0,blend_weight=0,contribution=0,correction=0)
    for flags,count,total,value in itertools.product([0,1,128,255],[0,1,2,32768,65534,65535],[-100,0,100],[0,90]):
        e=fixture();w(e,0x73C4,flags);w(e,0x80D8,count,2)
        f(e,0x80D4,total);f(e,0x80D0,7);f(e,0x6D20,value)
        average(e);counts['average']+=1
    e=fixture();w(e,0x73C4,128);f(e,0x6D20,90);average(e)
    w(e,0x73C4,0)
    for i in range(512):
        f(e,0x6D20,80 if i%2 else 100);average(e);counts['average_retained']+=1
    assert r(e,0x80D8,2)==65535-512 and rf(e,0x80D0)==90
    xs,ys,_=map2_info(0xA365C)
    points=lambda a:[a[0]-1,a[-1]+1]+a+[q((x+y)/2) for x,y in zip(a,a[1:])]
    for x,y in itertools.product(points(xs),points(ys)):
        e=fixture();f(e,0x6D38,x);f(e,0x6D30,y);baseline_map(e);counts['map']+=1
    for x,y in itertools.product([-201,-200,Fraction(-1599,8),0],sample_points(0xA3650)):
        e=fixture();f(e,0x6D30,x);f(e,0x80D0,y);baseline_extra(e);counts['extra']+=1
    for a,b in itertools.product([-1,0,Fraction(1,8),1,2**24],repeat=2):
        e=fixture();f(e,0x80C8,a);f(e,0x80CC,b);baseline_sum(e);counts['sum']+=1
    for mode,x in itertools.product([0,1,2,255],sample_points(0xA3670)):
        e=fixture();w(e,0x7012,mode);f(e,0x6D28,x);blend_maps(e);counts['blend_maps']+=1
    for flag,value in itertools.product([0,1,2,255],[-1,0,number(0xDA5C4),Fraction(1,2),q(1-number(0xDA5C0)),1,2]):
        e=fixture();w(e,0x7234,flag);f(e,0x80EC,value);blend_weight(e);counts['blend_weight']+=1
    for gate,latch,weight,a,b in itertools.product([0,1,2],[0,1,2],[0,Fraction(1,2),1],[-1,0,Fraction(1,8)],[-1,0,Fraction(1,16)]):
        e=fixture();w(e,0x67AC,gate);protected_byte(e,0x7978,latch)
        f(e,0x80EC,weight);f(e,0x80E4,a);f(e,0x80E8,b)
        contribution(e);counts['contribution']+=1
    for gate,previous,mode,special,flag,old in itertools.product([0,1,2,255],[0,1,2],[0,1,2],[0,1,2],[0,1,2],[0,Fraction(1,32),1]):
        e=fixture()
        for a,v in [(0x67AC,gate),(0x80F0,previous),(0x7012,mode),(0x6E3C,special),(0x7242,flag)]:w(e,a,v)
        f(e,0x80E0,old);correction(e);counts['correction']+=1
    rows,boundaries=lifecycle()
    tables={}
    for a in [0xA3650,0xA3670,0xA367C,0xA3688,0xA3694]:
        n=int.from_bytes(ECU[a:a+2],'big');xp=int.from_bytes(ECU[a+4:a+8],'big');vp=int.from_bytes(ECU[a+8:a+12],'big')
        tables[hex(a)]=dict(axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n))))
    xs,ys,vp=map2_info(0xA365C)
    tables['0xa365c']=dict(x=list(map(float,xs)),y=list(map(float,ys)),values=list(map(float,axis(vp,len(xs)*len(ys)))))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,
        tables=tables,lifecycle=rows,
        limits='Original nine bodies, original CAN211 normalize/latch; source inputs and latch admission count remain fixtures. Cross-task schedule, serial peer and other baseline contributions remain fixtures. Paired helper resetsA3A4 and CAN211 fields; latch is updated explicitly before local contribution group. Physical sender/units/actuation unproved.'),indent=2))


if __name__=='__main__':main()
