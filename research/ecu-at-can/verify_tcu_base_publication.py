"""Independent stock 3AC70 formula -> allocated class application -> output.

Original helpers execute; no observed return feeds the reference formula.
Application inputs and cross-task order are fixtures, not hardware evidence.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
from sh_subset import signed
from verify_tcu_class_application import bank_fixture, lower_model, select
from verify_tcu_class_adjustments import fixture, execute, TCU, w, r, clamp, consumer_model, update
from verify_tcu_request_maps import lookup, table
from verify_tcu_request_dispatch import curve
from verify_tcu_ascending_release import quotient
from verify_tcu_transition_classification import pending_model

ROOT = Path(__file__).resolve().parent

def trunc(n, d): return abs(n)//d * (-1 if n < 0 else 1)
def s(t, a, n=2): return signed(r(t, a, n), n*8)
def ram(t): return {a:v for a,v in t.ram.items() if a>=0xFFFF0000 and v}

def base_model(t):
    x=s(t,0x80EE); z=s(t,0x993E)
    if r(t,0x988A)==1:
        cap=min(s(t,0x993C),1535)
        ratio=clamp(quotient((z-cap)*256,signed(1536-cap,16)),0,256)
        y=max(0,s(t,0x92E4))
        a=lookup(0x71B8C,y,x)>>2; b=lookup(0x71BB8,y,x)>>2
        deduction=lookup(0x71BAB,x,s(t,0x80FE)*2)>>2 if pending_model(t) else 0
        out=a-((a-b)*ratio>>8)-deduction
        return out,dict(mode=1,ratio=ratio,a=a,b=b,deduction=deduction)
    weight=2294 if s(t,0x9940,4)>=0 else 655
    bank=0 if r(t,0x92D1)&4 or (r(t,0x92EE,2)>>7)<9 else 1
    a=curve(0x71BD7+13*bank,x)>>2
    product=signed(z+128,16)*weight
    delta=trunc(product*20,65536)
    bonus=lookup(0x71BF1,x,s(t,0x92F6))>>2 if r(t,0x92D1)&8 else 0
    out=max(0,a+delta+bonus)
    return out,dict(mode=0,weight=weight,bank=bank,a=a,delta=delta,bonus=bonus)

def check_base(t):
    expected,row=base_model(t); before=ram(t)
    actual=signed(execute(t,0x3AC70),32)
    assert actual==expected,(actual,expected,row)
    assert ram(t)==before
    assert (0x3ACAE in t.visited)==(r(t,0x988A)==1)
    assert (0x3AD32 in t.visited)==(r(t,0x988A)==1 and bool(pending_model(t)))
    assert (0x3AE2E in t.visited)==(r(t,0x988A)!=1 and bool(r(t,0x92D1)&8))
    return dict(value=actual,**row)

def publication(t):
    # Stock slot1 is disabled before reduction, regardless of supplied value.
    assert TCU[0x5CCE4:0x5CCE6]==bytes([1,0])
    ref=copy.deepcopy(t); w(ref,0x910A,32767,2)
    value=0 if r(t,0x9C58)&1 or r(t,0x9108,2)==32767 else s(t,0x9108)
    value=clamp(value,0,15232); scaled=value*100>>8
    for a,v in [(0x8100,value),(0x80AC,scaled),(0xA5FA,0x107),(0xA602,scaled)]:w(ref,a,v,2)
    execute(t,0x1F2AA)
    assert ram(t)==ram(ref),(value,scaled)
    assert {0x53070,0x5307E} <= t.visited
    return dict(value=value,scaled=scaled,slot0=r(t,0x9108,2),slot1=r(t,0x910A,2))

def integrated(t):
    ref=copy.deepcopy(t); base,detail=base_model(t)
    lower=lower_model(t); dynamic=consumer_model(t)
    value=min(15206,max(lower,signed(base,16)+dynamic+(s(t,0x98DC)>>1)))
    w(ref,0x9854,lower,2); w(ref,0x98B6+4*r(t,0x9856),value,2)
    assert signed(execute(t,0x36704),32)==value
    assert ram(t)==ram(ref)
    row=dict(base=base,detail=detail,applied=value,**select(t))
    row['output']=publication(t)
    return row

def seed(t,rng):
    for a in [0x80EE,0x80FE,0x92E4,0x92EE,0x92F6,0x993C,0x993E,0x98DC]:w(t,a,rng.randrange(65536),2)
    w(t,0x9940,rng.randrange(1<<32),4);w(t,0x92D1,rng.randrange(256))
    w(t,0x988A,rng.choice([0,1,2,255])); w(t,0x8088,rng.choice([0,2]))
    w(t,0x96C4,0);w(t,0x96C5,0);w(t,0x95E1,rng.choice([0,1,2,3]))

def main():
    assert TCU[0x77240:0x7724B]==bytes.fromhex('0600008008f6028f000009')
    counts={};rng=random.Random(0x3AC701F2AA);t=fixture();samples=[]
    # Grid helpers are independently modeled at all knots, midpoints and extrema.
    count=0
    for a in [0x71B8C,0x71BAB,0x71BB8,0x71BF1]:
        xs,ys,_=table(a)
        xx=sorted({0,65535,*xs,*[(p+q)//2 for p,q in zip(xs,xs[1:])]})
        yy=sorted({0,65535,*ys,*[(p+q)//2 for p,q in zip(ys,ys[1:])]})
        for x,y in itertools.product(xx,yy):
            t.r[5]=y;t.r[6]=a
            assert execute(t,0x1078A,x)==lookup(a,x,y)
            count+=1
    counts['grids']=count
    count=0
    for a in [0x71BD7,0x71BE4]:
        n=TCU[a];xs=[v*256 for v in TCU[a+1:a+1+n]]
        for x in sorted({0,65535,*xs,*[(p+q)//2 for p,q in zip(xs,xs[1:])]}):
            t.r[5]=a
            assert execute(t,0x10764,x)==curve(a,x)
            count+=1
    counts['curves']=count
    counts['base']=0
    for mode,z,cap,active in itertools.product([0,1,2,255],[-32768,-1536,-129,-128,-1,0,1,1535,1536,32767],[-32768,-31233,-31232,-31231,0,1535,1536,32767],[0,2]):
        seed(t,rng);w(t,0x988A,mode);w(t,0x993E,z,2);w(t,0x993C,cap,2);w(t,0x8088,active);w(t,0x95E1,0)
        row=check_base(t);counts['base']+=1
        if len(samples)<12:samples.append(row)
    for _ in range(1000):seed(t,rng);check_base(t);counts['base']+=1
    # Generic reducer is last-nonsentinel, with signed values, not max or min.
    count=0
    for values,default in itertools.product(itertools.product([0,100,200,32767,32768,65535],repeat=2),[-99,0,123]):
        for i,v in enumerate(values):w(t,0xB800+2*i,v,2)
        t.r[5]=2;t.r[6]=default&0xFFFFFFFF
        expected=next((signed(v,16) for v in reversed(values) if v!=32767),default)
        assert signed(execute(t,0x30686,0xFFFFB800),32)==expected
        count+=1
    counts['reducer']=count
    counts['publication']=0
    for value,other,bits in itertools.product([-32768,-1,0,1,101,102,15206,15231,15232,15233,32766,32767],[0,100,32767,65535],[0,1,2,255]):
        w(t,0x9108,value,2);w(t,0x910A,other,2);w(t,0x9C58,bits)
        publication(t);counts['publication']+=1
    rows=[]
    for _ in range(320):
        t=bank_fixture();seed(t,rng)
        for i in range(3):w(t,0x616A+2*i,rng.randrange(65536),2)
        w(t,0x9856,rng.choice([4,5,6,7]));w(t,0x9C58,rng.choice([0,1,2,255]));w(t,0x910A,12345,2)
        row=integrated(t)
        if len(rows)<16:rows.append(row)
    counts['integrated']=320
    # Original call instructions only; enclosing periodic task/cadence unproved.
    counts['caller_slices']=0
    for value,bits in itertools.product([0,1,15206,32767,65535],[0,1,2,255]):
        t=fixture();w(t,0x9108,value,2);w(t,0x910A,12345,2);w(t,0x9C58,bits)
        ref=copy.deepcopy(t);publication(ref);sp=t.r[15];pc=0x1EC10
        for _ in range(10000):
            if pc==0x1EC16:break
            nxt,delay=t.instruction(pc)
            if delay:
                _,nested=t.instruction(pc+2);assert not nested
            pc=nxt
        else:raise AssertionError('caller bound')
        assert t.r[15]==sp and ram(t)==ram(ref)
        counts['caller_slices']+=1
    t=bank_fixture();w(t,0x9856,4);retained=[]
    for call in range(1,161):
        w(t,0x80EE,5500,2);w(t,0x98DC,0 if call<=80 else -1000,2)
        w(t,0x988A,int(call%30<15));w(t,0x993E,call*20,2);w(t,0x993C,300,2)
        w(t,0x9C58,int(60<=call<=65));w(t,0x8088,2 if 90<=call<=95 else 0)
        update(t);row=integrated(t);row['call']=call;retained.append(row)
    counts['retained']=160
    out=dict(rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,samples=samples,integrated_samples=rows,retained=retained,
             limits='Raw inputs and explicit call order; no physical signal/actuator, hardware, CAN connection, or stock adjustment-admission claim.')
    (ROOT/'tcu-base-publication-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(counts))

if __name__=='__main__':main()
