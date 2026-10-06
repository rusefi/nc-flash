"""ECU current-input history group, original protected records and consumers.

Full local bodies in observed order, independent finite RTZ/state oracles.
History publication across tasks is explicitly scheduled, not a timing claim.
"""
import hashlib
import itertools
import json
import random
from fractions import Fraction
from verify_control_ratio_inputs import (ECU,TCU,w,r,f,rf,q,number,fixture,protected,checksum,
    setup_loop,initialize,integrated,protected_byte,init_history,ratio,remainder,
    input_map,hysteresis,input_select,timer,holdoff,decay,bounds,source_map,bounded,coupling,
    inputs,scaled)
from verify_model_sources import lookup1

CORRECTIONS=[0x80E0,0x8100,0x8140,0x8150,0x8230]
BASE_ADDITIONS=[0x80C4,0x80DC,0x80FC,0x8118,0x822C,0x80C0,
                0x8170,0x817C,0x8180,0x81C8,0x8204,0x81E4,0x8220,0x8238,0x8218]


def run(e,address):
    stack,mask=e.r[15],e.sr&0xF0;e.run(address)
    assert e.r[15]==stack and e.sr&0xF0==mask


def initialize_records(e):
    base=rf(e,0x80BC);run(e,0x58608)
    assert rf(e,0x8060)==rf(e,0x806C)==base
    for a in [0x804C,0x8070,0x8064]:assert rf(e,a)==0;checksum(e,a)


def baseline(e):
    divisor=rf(e,0x7020)
    old_base,old_component=rf(e,0x80BC),rf(e,0x80C0)
    if abs(divisor)<=number(0x58FD8):
        want,component=old_base,old_component
    else:
        component=max(rf(e,0x813C),q(q(rf(e,0x8098)*rf(e,0x6DB4))/divisor))
        values=[component if a==0x80C0 else rf(e,a) for a in BASE_ADDITIONS]
        want=values[0]
        for v in values[1:]:want=q(want+v)
        want=max(0,q(q(want-rf(e,0x81F8))-rf(e,0x8214)))
    run(e,0x58F10)
    assert rf(e,0x80BC)==want and rf(e,0x80C0)==component


def publish_records(e):
    a,b=rf(e,0x806C),rf(e,0x8060);run(e,0x5863A)
    assert rf(e,0x8070)==a and rf(e,0x8064)==b
    checksum(e,0x8070);checksum(e,0x8064)


def snapshot_records(e):
    assert e.sr&0xF0 # Avoid claiming the3894 zero-mask scheduler-resume path.
    a,b=(rf(e,0x80BC),)*2 if r(e,0x7016)==0 else (rf(e,0x8070),rf(e,0x8064))
    run(e,0x58652)
    assert [rf(e,x) for x in [0x8070,0x8064,0x8084,0x8088]]==[a,b,a,b]
    checksum(e,0x8070);checksum(e,0x8064)


def limits(e):
    previous,flag,count=r(e,0x8094),r(e,0x73B8),r(e,0x8080)
    want=ECU[0xD9F11] if previous==1 and flag==0 else max(0,count-1)
    run(e,0x586A6)
    assert (r(e,0x8080),r(e,0x8094))==(want,flag)
    old=rf(e,0x8078)
    if want==0 and r(e,0x7346)==1 and r(e,0x76B2)==1:
        value=min(q(old+number(0xD9F24)),max(old,number(0xD9F28)))
    else:value=max(q(old-number(0xD9F24)),lookup1(0xA35C8,rf(e,0x6DB4)))
    run(e,0x58730);assert rf(e,0x8078)==value
    old_map=rf(e,0x8090)
    mapped=lookup1(0xA35D4,rf(e,0x6DB4)) if r(e,0x7012)==1 else old_map
    cap=max(mapped,value) if r(e,0x7012)==1 else 0
    run(e,0x587A2)
    assert rf(e,0x807C)==cap and rf(e,0x8090)==mapped


def target_history(e):
    mode=r(e,0x7016);base,speed=rf(e,0x80BC),rf(e,0x6DB4)
    target=max(q(q(base*rf(e,0x7020))/speed),rf(e,0x807C)) if mode==1 and abs(speed)>number(0x5894C) else base
    run(e,0x587E4);assert rf(e,0x806C)==target
    if mode==1:
        alpha=q(1-number(0xD9F1C))
        blend=q(target+q(q(1-alpha)*q(rf(e,0x8088)-target)))
        filtered=target if abs(q(target-blend))<number(0x58968) else blend
    else:filtered=base
    run(e,0x58846);assert rf(e,0x8060)==filtered
    delta=max(0,q(target-filtered)) if mode==1 else 0
    run(e,0x58884);assert rf(e,0x805C)==delta
    amount=scaled(delta,speed) if mode==1 else 0
    run(e,0x588B8);assert rf(e,0x8058)==amount


def coefficient(e):
    mapped=lookup1(0xA35BC,rf(e,0x6D28))
    old=rf(e,0x8054)
    if r(e,0x7346)==0 or ECU[0xD9F10]!=0 or r(e,0x7016)==0:value=0
    elif number(0xD9F18)==0:value=old
    else:
        raw=q(q(q(rf(e,0x8058)-mapped)*number(0xD9F14))/number(0xD9F18))
        value=max(0,min(number(0xD9F14),raw))
        if r(e,0x7010)==1 or r(e,0x7EEE)>0:value=q(value*number(0xD9F20))
    run(e,0x5898C)
    assert rf(e,0x808C)==mapped and rf(e,0x8054)==value
    assert 0<=value<=number(0xD9F14)<q(1-number(0x58B38))


def unmix(e):
    old=bytes(r(e,0x804C+i) for i in range(8));a=rf(e,0x8054);den=q(1-a)
    admitted=abs(den)>number(0x58B38)
    want=q(q(rf(e,0x806C)-q(a*rf(e,0x8084)))/den) if admitted else rf(e,0x804C)
    run(e,0x58A34);assert rf(e,0x804C)==want
    if admitted:checksum(e,0x804C)
    else:assert bytes(r(e,0x804C+i) for i in range(8))==old


def current(e):
    speed=rf(e,0x6DB4);mode=r(e,0x7016)
    if mode==0:want=rf(e,0x80BC);branch='baseline'
    elif abs(speed)<=number(0x58B54):want=rf(e,0x8048);branch='hold'
    else:
        total=rf(e,CORRECTIONS[0])
        for a in CORRECTIONS[1:]:total=q(total+rf(e,a))
        want=q(rf(e,0x804C)+q(q(total*rf(e,0x7020))/speed));branch='corrected'
    run(e,0x58A7A);assert rf(e,0x8048)==want
    return branch


def group(e):
    baseline(e);snapshot_records(e);limits(e);target_history(e);coefficient(e);unmix(e)
    return current(e)


def main():
    counts=dict(baseline=0,snapshots=0,limits=0,targets=0,coefficients=0,unmix=0,current=0,initializers=0)
    for divisor,speed,term,source in itertools.product(
            [-1,-number(0x58FD8),0,number(0x58FD8),1,150],[0,150,1500],[-1,0,Fraction(1,2)],[-1,0,1]):
        e=fixture();f(e,0x7020,divisor);f(e,0x6DB4,speed);f(e,0x8098,source)
        f(e,0x80BC,7);f(e,0x80C0,8)
        for a in BASE_ADDITIONS:
            if a!=0x80C0:f(e,a,term)
        f(e,0x81F8,Fraction(1,8));f(e,0x8214,Fraction(1,4));baseline(e);counts['baseline']+=1
    for mode,base,mask in itertools.product([0,1,2,255],[-1,0,Fraction(1,2),2],[0x10,0x30,0xF0]):
        e=fixture();e.sr=mask;f(e,0x80BC,base);initialize_records(e);counts['initializers']+=1
        f(e,0x806C,3);f(e,0x8060,4);publish_records(e)
        w(e,0x7016,mode);snapshot_records(e);counts['snapshots']+=1
    rng=random.Random(0x58A7A)
    for i in range(600):
        e=fixture()
        for a in [0x8094,0x73B8,0x7346,0x76B2,0x7012]:w(e,a,rng.choice([0,1,2,255]))
        w(e,0x8080,rng.choice([0,1,2,255]));f(e,0x8078,rng.choice([-1,0,Fraction(1,8),1]))
        f(e,0x8090,3);f(e,0x6DB4,rng.choice([0,500,1000,1200,3000,7500,9000]))
        limits(e);counts['limits']+=1
    for mode,speed,base in itertools.product([0,1,2,255],[-150,-1,-number(0x5894C),0,number(0x5894C),1,150,1500],[-1,0,Fraction(1,2),2]):
        e=fixture();w(e,0x7016,mode);f(e,0x6DB4,speed);f(e,0x80BC,base)
        f(e,0x7020,150);f(e,0x807C,Fraction(1,8));f(e,0x8088,1)
        target_history(e);counts['targets']+=1
    for mode,enabled,amount,flag,extra in itertools.product([0,1,2],[0,1,2],[-1,0,Fraction(1,8),Fraction(1,4),1],[0,1,2],[0,1,2]):
        e=fixture();w(e,0x7016,mode);w(e,0x7346,enabled);w(e,0x7010,flag);w(e,0x7EEE,extra)
        f(e,0x8058,amount);f(e,0x6D28,80);coefficient(e);counts['coefficients']+=1
    for a,target,prior in itertools.product([0,Fraction(1,2),number(0xD9F14),q(1-number(0x58B38)),1,q(1+number(0x58B38)),2],[-1,0,1,4],[-1,0,2]):
        e=fixture();f(e,0x8054,a);f(e,0x806C,target);f(e,0x8084,prior);protected(e,0x804C,7)
        unmix(e);counts['unmix']+=1
    for mode,speed,base in itertools.product([0,1,2,255],[-2,-number(0x58B54),0,number(0x58B54),1,150],[0,Fraction(1,2),2]):
        e=fixture();w(e,0x7016,mode);f(e,0x6DB4,speed);f(e,0x80BC,base)
        f(e,0x8048,9);protected(e,0x804C,3);f(e,0x7020,150)
        for a,v in zip(CORRECTIONS,[Fraction(1,8),Fraction(1,4),-1,2,Fraction(1,2)]):f(e,a,v)
        current(e);counts['current']+=1
    e=setup_loop(numeric_fixtures=False);initialize(e);init_history(e)
    for a in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,a,0)
    f(e,0x7020,150);f(e,0x80C4,Fraction(1,2));baseline(e);initialize_records(e)
    f(e,0x6CB4,8);e.run(0x1DED8);w(e,0x722A,1);w(e,0x6536,1)
    w(e,0x5634,3);w(e,0x5635,1);w(e,0x8194,1);w(e,0x7346,1)
    f(e,0x6D28,80);f(e,0x6D20,90);f(e,0x6C20,0);f(e,0x7020,150)
    f(e,0x80E0,Fraction(1,8))
    boundaries={1,2,10,11,20,21,40,41,42,60,61,62,80,81,100,101,110,115,116,120,140}
    rows=[]
    for call in range(1,141):
        if call==11:w(e,0x7016,1)
        if call==21:f(e,0x6DB4,1500)
        if call==41:f(e,0x6DB4,150)
        if call==61:w(e,0x7016,2)
        if call==81:w(e,0x7016,0)
        if call==101:w(e,0x7016,1);w(e,0x7010,1);f(e,0x6DB4,50)
        if call==111:f(e,0x6DB4,0)
        if call==115:f(e,0x6DB4,50)
        branch=group(e);inputs(e);ratio(e);remainder(e);input_map(e);hysteresis(e);input_select(e)
        timer(e);holdoff(e);decay(e);bounds(e);source_map(e);bounded(e);coupling(e)
        row=integrated(e,call,update_can=call in boundaries)
        row.update(input_mode=r(e,0x7016),current_branch=branch,current_input=float(rf(e,0x8048)),
            baseline=float(rf(e,0x80BC)),baseline_component=float(rf(e,0x80C0)),
            target=float(rf(e,0x806C)),filtered=float(rf(e,0x8060)),
            coefficient=float(rf(e,0x8054)),protected_base=float(rf(e,0x804C)),
            prior_target=float(rf(e,0x8084)),prior_filtered=float(rf(e,0x8088)),
            numerator_pair=[float(rf(e,a)) for a in [0x8030,0x8034]],numerator=float(rf(e,0x802C)))
        assert branch==('baseline' if call<=10 or 81<=call<101 else 'hold' if 111<=call<115 else 'corrected')
        if 61<=call<81:assert rf(e,0x802C)==rf(e,0x8034)
        if call in boundaries or call in [111,112,114]:rows.append(row)
        # Original publisher is in another task (1D710); this chosen cadence
        # is explicit and does not establish production scheduling frequency.
        publish_records(e)
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,serial_cycles=140,paired_can_updates=len(boundaries),lifecycle=rows,
        limits='Original local group58F10..58A7A andpublisher5863A; upstream baseline contributions/corrections/statuses remain fixtures. Publisher once per cycle is synthetic schedule. Nonzero SR mask only;3894 scheduler-resume path,fulltask/hardware andphysicalunits remain open. CAN updatesheldduring6DB4zero.'),indent=2))


if __name__=='__main__':main()
