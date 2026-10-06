"""ECU retained source history: original ratio, hysteresis and decay bodies.

Finite RTZ/state oracles; selected caller groups, paired ROMs and synthetic
serial peer. Cross-task scheduling and upstream physical sources remain open.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from verify_control_sources import (ECU,TCU,w,r,f,rf,q,number,fixture,protected,
    checksum,setup_loop,initialize,integrated,protected_byte,input_map,input_select,
    bounds,source_map,bounded,coupling)


def ratio(e):
    a,b,c=[rf(e,x) for x in [0x802C,0x8038,0x803C]]
    eps=[number(x) for x in [0x58564,0x5856C,0x58574]]
    old=rf(e,0x8028)
    want=0 if abs(a)<=eps[0] else q(a/q(b*c)) if abs(b)>eps[1] and abs(c)>eps[2] else old
    delta=q(want-rf(e,0x801C))
    stack=e.r[15];e.run(0x58338)
    assert e.r[15]==stack and rf(e,0x8028)==want
    assert r(e,0x8197)==int(delta>=number(0xDAC58))
    assert r(e,0x8198)==int(delta<=0)
    return 'clear' if abs(a)<=eps[0] else 'update' if abs(b)>eps[1] and abs(c)>eps[2] else 'hold'


def remainder(e):
    want=max(0,q(q(rf(e,0x8028)-rf(e,0x801C))-q(rf(e,0x6C20)/number(0x58314))))
    stack=e.r[15];e.run(0x58280)
    assert e.r[15]==stack and rf(e,0x8018)==want


def hysteresis(e,valid=True):
    saved=rf(e,0x2310) if valid else number(0xD9E84)
    source=rf(e,0x8018);old=r(e,0x8023)
    want=0 if source>=q(saved+number(0xD9E78)) else 1 if source<=saved else old
    stack=e.r[15];e.run(0x582BC)
    assert e.r[15]==stack and r(e,0x8023)==want


def timer(e):
    reload=(r(e,0x8194)==0 or r(e,0x7012)==1 or r(e,0x7346)==0 or
            (r(e,0x8023)==0 and q(rf(e,0x7020)+number(0xD9E7C))>rf(e,0x6DB4)))
    want=int.from_bytes(ECU[0xD9E76:0xD9E78],'big') if reload else max(0,r(e,0x8020,2)-1)
    stack=e.r[15];e.run(0x58140)
    assert e.r[15]==stack and r(e,0x8020,2)==want


def holdoff(e):
    current,previous,hold=r(e,0x8020,2),r(e,0x8024,2),r(e,0x8022)
    want=ECU[0xD9E74] if current==0 and (previous!=0 or hold==0) else max(0,hold-1)
    stack=e.r[15];e.run(0x581B8)
    assert e.r[15]==stack and (r(e,0x8022),r(e,0x8024,2))==(want,current)


def decay(e,valid=True):
    raw=bytes(r(e,0x2310+j) for j in range(8))
    old=rf(e,0x2310) if valid else number(0xD9E84)
    admitted=r(e,0x8020,2)==0 and r(e,0x8022)==0
    step=number(0xD9E80);want=q(old-step) if old>step else 0
    stack,sr=e.r[15],e.sr;e.run(0x58102)
    assert e.r[15]==stack and e.sr&0xF0==sr&0xF0
    if admitted:
        assert rf(e,0x2310)==want;checksum(e,0x2310)
    else:assert bytes(r(e,0x2310+j) for j in range(8))==raw
    return admitted


def init_history(e):
    stack=e.r[15];e.run(0x58088);e.run(0x582B2)
    assert e.r[15]==stack and rf(e,0x2310)==number(0xD9E84)==0
    assert rf(e,0x801C)==number(0xD9E88)==Fraction(1363,2)
    checksum(e,0x2310)


def main():
    counts=dict(ratio=0,remainder=0,hysteresis=0,timer=0,holdoff=0,decay=0,initialization=0)
    values=lambda eps:[-2,-eps,q(-eps/2),0,q(eps/2),eps,2]
    for a,b,c in itertools.product(*(values(number(x)) for x in [0x58564,0x5856C,0x58574])):
        e=fixture();f(e,0x802C,a);f(e,0x8038,b);f(e,0x803C,c);f(e,0x8028,1234);f(e,0x801C,681.5)
        ratio(e);counts['ratio']+=1
    for source,offset,correction in itertools.product([-100,0,681.5,1000,30000],[-10,0,681.5,1000],[-60,0,1,60,12000]):
        e=fixture();f(e,0x8028,source);f(e,0x801C,offset);f(e,0x6C20,correction);remainder(e);counts['remainder']+=1
    for saved,delta,old,valid in itertools.product([0,100,2000],[-1,0,1,49,50,51],[0,1,2],[True,False]):
        e=fixture();protected(e,0x2310,saved);f(e,0x8018,saved+delta);w(e,0x8023,old)
        if not valid:w(e,0x2314,0,2);w(e,0x2316,0,2)
        hysteresis(e,valid);counts['hysteresis']+=1
    for a,b,c,latch,speed,count in itertools.product([0,1,2],[0,1,2],[0,1,2],[0,1,2],[99,100,101],[0,1,113,65535]):
        e=fixture()
        for address,value in [(0x8194,a),(0x7012,b),(0x7346,c),(0x8023,latch)]:w(e,address,value)
        f(e,0x7020,0);f(e,0x6DB4,speed);w(e,0x8020,count,2);timer(e);counts['timer']+=1
    for current,previous,hold in itertools.product([0,1,113,65535],[0,1,65535],[0,1,2,3,255]):
        e=fixture();w(e,0x8020,current,2);w(e,0x8024,previous,2);w(e,0x8022,hold);holdoff(e);counts['holdoff']+=1
    for saved,current,hold,valid in itertools.product([-1,0,number(0xD9E80),q(Fraction(1,10)),1,2000],[0,1,65535],[0,1,3],[True,False]):
        e=fixture();protected(e,0x2310,saved);w(e,0x8020,current,2);w(e,0x8022,hold)
        if not valid:w(e,0x2314,0,2);w(e,0x2316,0,2)
        decay(e,valid);counts['decay']+=1
    e=fixture();init_history(e);counts['initialization']+=1
    # Seed prior protected history explicitly after separately testing init.
    # Do not inject8018/8028/8020/8022/8023/8024 after setup.
    e=setup_loop(numeric_fixtures=False);initialize(e);init_history(e);protected(e,0x2310,1)
    for address in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,address,0)
    f(e,0x6CB4,8);e.run(0x1DED8);w(e,0x722A,1);w(e,0x6536,1)
    w(e,0x5634,3);w(e,0x5635,0);w(e,0x7012,0);w(e,0x7346,1)
    f(e,0x6D28,80);f(e,0x6D20,90);f(e,0x6C20,0);f(e,0x7020,0)
    f(e,0x802C,1363);f(e,0x8038,2);f(e,0x803C,1)
    boundaries={1,2,19,20,21,39,40,113,114,115,116,117,121,145,146,160,161,180,193,194,200,201,220}
    rows=[];writes=[]
    for call in range(1,221):
        if call==2:w(e,0x8194,1)
        if call==20:f(e,0x8038,0)
        if call==21:f(e,0x802C,0)
        if call==40:f(e,0x802C,1363);f(e,0x8038,2)
        if call==145:f(e,0x802C,3363)
        if call==161:f(e,0x802C,1363)
        if call==201:w(e,0x5635,1)
        # Relative order within each original caller group. Cross-group order
        # here is an explicit synthetic schedule, not proven production rate.
        ratio_branch=ratio(e);remainder(e);input_map(e);hysteresis(e);input_select(e)
        timer(e);holdoff(e)
        before=rf(e,0x2310);admitted=decay(e)
        if admitted:writes.append(dict(call=call,before=float(before),after=float(rf(e,0x2310))))
        bounds(e);source_map(e);bounded(e);coupling(e)
        row=integrated(e,call,update_can=call in boundaries)
        assert r(e,0x8020,2)==max(0,114-call)
        assert admitted==(call>=117 and (call-117)%4==0)
        if call==193:assert rf(e,0x2310)==0
        row.update(ratio_branch=ratio_branch,ratio=float(rf(e,0x8028)),remainder=float(rf(e,0x8018)),
                   retained=float(rf(e,0x2310)),selected_input=float(rf(e,0x8014)),
                   source_latch=r(e,0x8023),decay_timer=r(e,0x8020,2),decay_holdoff=r(e,0x8022),decay_write=admitted)
        if call in boundaries:rows.append(row)
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,serial_cycles=220,paired_can_updates=len(boundaries),lifecycle=rows,decay_writes=writes,
        limits='Explicitcross-task schedule,fixture ratio inputs/statuses,seeded valid prior2310 history; original local producers/timers. Physical source IDs,full initialization,ratio input provenance andvehicle timing/actuation remain open.'),indent=2))


if __name__=='__main__':main()
