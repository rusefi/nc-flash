"""Original ratio inputs, shared environment values and paired command path.

Independent finite RTZ oracles; original lookup/helper bodies. Physical units,
complete cross-task scheduling and nonfinite exception behavior remain open.
"""
import hashlib
import itertools
import json
import struct
from fractions import Fraction
from verify_control_history import (ECU,TCU,w,r,f,rf,q,number,fixture,protected,checksum,
    setup_loop,initialize,integrated,protected_byte,init_history,ratio,remainder,
    input_map,hysteresis,input_select,timer,holdoff,decay,bounds,source_map,bounded,coupling)
from verify_model_sources import lookup1,axis

CONTRIBUTIONS=[0x80C4,0x80DC,0x80FC,0x8118,0x813C,0x822C]


def factor(e):
    summed=rf(e,CONTRIBUTIONS[0])
    for address in CONTRIBUTIONS[1:]:summed=q(summed+rf(e,address))
    mapped=lookup1(0xA261C,summed)
    correction=q(q(mapped*q(rf(e,0x6D40)+number(0x3A028)))/number(0x3A02C))
    assert ECU[0xC89A0]==0
    difference=q(rf(e,0x6DC4)-correction)
    want=lookup1(0xA35B0,difference)
    stack=e.r[15];e.visited.clear();e.run(0x5844E)
    assert e.r[15]==stack and {0x51286,0x39FB4,0x22F8}.issubset(e.visited)
    actual=[rf(e,a) for a in [0x7BB8,0x6D54,0x6D4C,0x8038]]
    assert actual==[summed,mapped,difference,want],(actual,[summed,mapped,difference,want])
    assert want==1;checksum(e,0x6D4C)


def environment(e):
    numerator=q(rf(e,0x6DC4)*number(0x585F8))
    denominator=q(q(rf(e,0x6D40)+number(0x58600))*number(0x58604))
    want=q(numerator/denominator)
    stack=e.r[15];e.run(0x58528)
    assert e.r[15]==stack and rf(e,0x803C)==want


def scaled(a,b):
    return q(q(q(q(q(a*b)/number(0x585A8))*number(0xCC028))*number(0xCA974))/2)


def numerators(e):
    current=scaled(rf(e,0x8048),rf(e,0x6DB4))
    baseline=scaled(rf(e,0x80BC),rf(e,0x7020))
    stack=e.r[15];e.run(0x583EE);e.run(0x58422)
    assert e.r[15]==stack and [rf(e,a) for a in [0x8030,0x8034]]==[current,baseline]


def select_numerator(e):
    lo=rf(e,0x8034);hi=q(lo+number(0xD9ECC));value=rf(e,0x8030)
    want=(lo if value<=lo else hi if value>=hi else value) if r(e,0x7016)==1 else lo
    stack=e.r[15];e.run(0x583B8)
    assert e.r[15]==stack and rf(e,0x802C)==want


def inputs(e):
    # 58528 is a separate caller group; its relative rate remains explicit.
    environment(e);factor(e);numerators(e);select_numerator(e)


def main():
    counts=dict(factor=0,environment=0,numerator_pairs=0,numerator_selection=0)
    for values,t,p in itertools.product(itertools.product([0,Fraction(1,8)],repeat=6),[-30,20,100],[0,50,100]):
        e=fixture()
        for address,value in zip(CONTRIBUTIONS,values):f(e,address,value)
        f(e,0x6D40,t);f(e,0x6DC4,p);factor(e);counts['factor']+=1
    # Cancellation-sensitive order, signed values and table endpoint clamps.
    for values in [[2**24,1,-2**24,0,0,0],[2**24,-2**24,1,0,0,0],[-1,0,0,0,0,0],[1,0,0,0,0,0]]:
        e=fixture()
        for address,value in zip(CONTRIBUTIONS,values):f(e,address,value)
        f(e,0x6D40,20);f(e,0x6DC4,100);factor(e);counts['factor']+=1
    for p,t in itertools.product([-1,0,Fraction(1,1024),1,50,100,200],[-300,-272,-30,0,20,100]):
        e=fixture();f(e,0x6DC4,p);f(e,0x6D40,t);environment(e);counts['environment']+=1
    for a,b in itertools.product([-1,0,Fraction(1,8),1,5,100,2000],repeat=2):
        e=fixture();f(e,0x8048,a);f(e,0x6DB4,b);f(e,0x80BC,b);f(e,0x7020,a)
        numerators(e);counts['numerator_pairs']+=1
    for mode,baseline,value in itertools.product([0,1,2,255],[0,5,10],[-1,0,4,5,6,14.5,15,20]):
        e=fixture();w(e,0x7016,mode);f(e,0x8034,baseline);f(e,0x8030,value)
        select_numerator(e);counts['numerator_selection']+=1
    rejection=[]
    for p in [0,100]:
        e=fixture();f(e,0x6DC4,p);f(e,0x6D40,-273);f(e,0x803C,7)
        try:e.run(0x58528)
        except ValueError as exc:
            assert str(exc)=='RTZ division by zero unsupported',str(exc)
            assert rf(e,0x803C)==7
            rejection.append(dict(input=p,error=str(exc)))
        else:raise AssertionError('Unsupported exception arithmetic must stop')
    e=setup_loop(numeric_fixtures=False);initialize(e);init_history(e);protected(e,0x2310,1)
    for address in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,address,0)
    f(e,0x6CB4,8);e.run(0x1DED8);w(e,0x722A,1);w(e,0x6536,1)
    w(e,0x5634,3);w(e,0x5635,1);w(e,0x8194,1);w(e,0x7346,1)
    f(e,0x6D28,80);f(e,0x6D20,90);f(e,0x6C20,0);f(e,0x7020,150)
    f(e,0x80BC,Fraction(1,2));f(e,0x8048,Fraction(1,2))
    f(e,0x80C4,Fraction(1,8))
    boundaries={1,2,10,11,20,25,26,40,41,60,61,64,65,66,80,81,100,101,120,121,140}
    rows=[]
    for call in range(1,141):
        if call==11:f(e,0x6D40,100)
        if call==21:f(e,0x6DC4,0)  # hold CAN models; ratio sees produced zero denominator
        if call==25:f(e,0x6DC4,100)
        if call==41:f(e,0x80BC,0)
        if call==61:f(e,0x80BC,Fraction(1,2));f(e,0x80C4,1)
        if call==81:w(e,0x7016,1);f(e,0x8048,10)
        if call==101:w(e,0x7016,2);w(e,0x5635,0)
        if call==121:w(e,0x5635,1);f(e,0x6D40,20)
        inputs(e);branch=ratio(e);remainder(e);input_map(e);hysteresis(e);input_select(e)
        timer(e);holdoff(e);decay(e);bounds(e);source_map(e);bounded(e);coupling(e)
        row=integrated(e,call,update_can=call in boundaries)
        assert branch==('hold' if 21<=call<25 else 'clear' if 41<=call<61 else 'update'),(call,branch)
        row.update(ratio_branch=branch,environment=[float(rf(e,a)) for a in [0x6DC4,0x6D40]],
          ratio_inputs=[float(rf(e,a)) for a in [0x802C,0x8038,0x803C]],
          numerator_pair=[float(rf(e,a)) for a in [0x8030,0x8034]],
          ratio=float(rf(e,0x8028)),remainder=float(rf(e,0x8018)),
          mapped_difference=float(rf(e,0x6D4C)),sum=float(rf(e,0x7BB8)),
          retained=float(rf(e,0x2310)),decay_timer=r(e,0x8020,2))
        if call in boundaries or call in [21,22,24]:rows.append(row)
    tables={}
    for a in [0xA261C,0xA35B0]:
        n,kind,pad,xp,vp=struct.unpack_from('>HBBII',ECU,a)
        tables[hex(a)]=dict(axis_address=hex(xp),values_address=hex(vp),kind=kind,
            axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n))))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,expected_model_rejections=rejection,serial_cycles=140,paired_can_updates=len(boundaries),
        tables=tables,lifecycle=rows,
        limits='Finite normal/zero arithmetic; no FPSCR exception emulation. Synthetic cross-task schedule and serial peer. 8048/80BC/contributions/environment/statuses remain fixtures. CAN model updates deliberately held during6DC4zero; physical units/outputs unproved.'),indent=2))


if __name__=='__main__':main()
