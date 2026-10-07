"""Execute TCU record service and lookup/rate-limited output preparation.

Independent reference models, stock ROM, original nested helpers. Output
handoff18A44/hardware and physical signal identity remain outside this proof.
"""
import copy
import itertools
import json
import random
import hashlib
from pathlib import Path
import verify_tcu_base_publication as base
from verify_tcu_base_publication import TCU,w,r,s,ram,trunc,clamp,fixture,execute
from sh_subset import signed
ROOT=Path(__file__).resolve().parent

def word(a):return int.from_bytes(TCU[a:a+2],'big')
def bounds(i):return word(0x5FCAC+2*i),word(0x5FCA4+2*i)
def equal(t,ref):
    aa,bb=ram(t),ram(ref)
    assert aa==bb,{hex(a):(aa.get(a,0),bb.get(a,0)) for a in set(aa)|set(bb) if aa.get(a,0)!=bb.get(a,0)}

def initialize(t):
    ref=copy.deepcopy(t)
    for i in range(4):
        lo,hi=bounds(i)
        for a,v in [(0xA5D4,200),(0xA5E4,200),(0xA608,100),(0xA5F8,0x107),(0xA600,word(0x5FCB4+2*i)),(0xA63A,lo),(0xA642,hi),(0xA622,0),(0xA62A,lo),(0xA632,hi),(0xA64A,0)]:w(ref,a+2*i,v,2)
        w(ref,0xA654+4*i,0,4);w(ref,0xA5EC+i,0);w(ref,0xA61C+i,0)
    w(ref,0xA620,0);execute(t,0x52E54);equal(t,ref)

def service_model(t,i):
    j=2*i; tag=r(t,0xA5F8+j,2);lo,hi=bounds(i)
    accepted=not tag&0x8000 and bool(tag&255)
    if accepted:
        if tag&7:w(t,0xA622+j,clamp(s(t,0xA600+j),lo,hi),2)
        if tag&0x400:w(t,0xA632+j,r(t,0xA642+j,2),2)
        else:w(t,0xA642+j,hi,2);w(t,0xA632+j,hi,2)
        if tag&0x800:w(t,0xA62A+j,r(t,0xA63A+j,2),2)
        else:w(t,0xA63A+j,lo,2);w(t,0xA62A+j,lo,2)
        w(t,0xA5F8+j,tag&0xFF00,2)
        w(t,0xA64A+j,0 if tag&0x100 else r(t,0xA5DC+j,2),2)
        if not tag&0x1000:w(t,0xA654+4*i,0,4)
    raw=signed(trunc(s(t,0xA654+4*i,4),1000)+s(t,0xA622+j)+s(t,0xA64A+j),16)
    lo,hi=sorted([s(t,0xA62A+j),s(t,0xA632+j)])
    out=clamp(raw,lo,hi);w(t,0xA5DC+j,out,2)
    return dict(accepted=accepted,value=out,tag=r(t,0xA5F8+j,2))

def service(t,i):
    ref=copy.deepcopy(t);row=service_model(ref,i);execute(t,0x530C8,i);equal(t,ref);return row

def lookup(i,x):
    p=int.from_bytes(TCU[0x5FC94+4*i:0x5FC98+4*i],'big');x&=65535
    index,rem=divmod(x,50);a=word(p+2*index);b=word(p+2*index+2)
    return signed(a,16) if rem==0 or b==65535 else signed(a,16)+trunc((b-a)*rem,50)

def driver_model(t,i):
    j=2*i;feedback=r(t,0x8A34+j,2)
    if r(t,0xA5EC+i)==0 and (feedback^r(t,0xA608+j,2))&0x8000:w(t,0xA5EC+i,1)
    w(t,0xA608+j,feedback,2)
    old=r(t,0xA5D4+j,2);current=clamp(old,200,1000)
    if r(t,0xA61C+i):target=s(t,0xA614+j)
    else:
        target=lookup(i,s(t,0xA5DC+j));w(t,0xA5F0+j,target,2);target=signed(target,16)
    if r(t,0xAD3C):target=s(t,0xAD3E+j)
    delta=signed(target-current,16)
    # Original abs word return is sign-extended again by52FE0.
    if signed(abs(delta),16)>88:target=current+(88 if delta>0 else -88)
    w(t,0xA5E4+j,old,2);w(t,0xA5D4+j,clamp(target&65535,200,1000),2)
    test=r(t,0xA620)
    if r(t,0x809E,2)==0 and test:
        forced={1:1000,2:200,3:500}.get(test,100)
        w(t,0xA5D4+j,forced,2);w(t,0xA5E4+j,forced,2)
    return dict(value=r(t,0xA5D4+j,2),previous=r(t,0xA5E4+j,2),sticky=r(t,0xA5EC+i))

def driver(t,i):
    ref=copy.deepcopy(t);row=driver_model(ref,i);execute(t,0x52EDC,i+1);equal(t,ref);return row

def main():
    rng=random.Random(0x530C8);counts={};t=fixture()
    for n in range(20):
        for a in range(0xA5D4,0xA664):w(t,a,rng.randrange(256))
        initialize(t)
    counts['initialization']=20
    count=0
    for i,hi,low in itertools.product(range(4),[0,0x100,0x400,0x800,0xC00,0x1000,0x1D00,0x8000,0xFFFF],range(256)):
        for a in [0xA600,0xA622,0xA62A,0xA632,0xA63A,0xA642,0xA64A,0xA5DC]:w(t,a+2*i,rng.randrange(65536),2)
        w(t,0xA654+4*i,rng.randrange(1<<32),4);w(t,0xA5F8+2*i,(hi&0xFF00)|low,2)
        service(t,i);count+=1
    counts['service']=count
    count=0
    for i in range(4):
        for x in range(bounds(i)[0],bounds(i)[1]+1,25):
            t.r[5]=int.from_bytes(TCU[0x5FC94+4*i:0x5FC98+4*i],'big');t.r[6]=50
            assert signed(execute(t,0x10700,x),32)==lookup(i,x),(i,x)
            count+=1
    counts['lookup']=count
    count=0
    for i,old,manual,diag,test in itertools.product(range(4),[0,199,200,201,500,912,999,1000,1001,32768,65535],[0,1],[0,1],[0,1,2,3,4,255]):
        w(t,0xA5D4+2*i,old,2);w(t,0xA5DC+2*i,rng.randrange(bounds(i)[0],bounds(i)[1]+1),2)
        w(t,0xA61C+i,manual);w(t,0xAD3C,diag);w(t,0xA620,test);w(t,0x809E,rng.choice([0,1]),2)
        w(t,0xA614+2*i,rng.randrange(65536),2);w(t,0xAD3E+2*i,rng.randrange(65536),2)
        w(t,0x8A34+2*i,rng.randrange(65536),2);w(t,0xA608+2*i,rng.randrange(65536),2);w(t,0xA5EC+i,rng.choice([0,1,255]))
        driver(t,i);count+=1
    counts['driver']=count
    # Critical wrapping/absolute-value and +/-88 rate boundaries.
    count=0
    for i,delta in itertools.product(range(4),[-32768,-32767,-89,-88,-87,0,87,88,89,32767]):
        w(t,0xA5D4+2*i,500,2);w(t,0xA61C+i,1);w(t,0xAD3C,0);w(t,0xA620,0);w(t,0xA614+2*i,500+delta,2)
        driver(t,i);count+=1
    counts['driver_edges']=count
    rows=[];t=base.bank_fixture();initialize(t);w(t,0x9856,4)
    for call in range(1,161):
        w(t,0x80EE,5500,2);w(t,0x98DC,0 if call<=80 else -1000,2)
        w(t,0x988A,int(call%30<15));w(t,0x993E,call*20,2);w(t,0x993C,300,2)
        w(t,0x9C58,int(60<=call<=65));w(t,0x8088,2 if 90<=call<=95 else 0)
        base.update(t);row=base.integrated(t);row['service']=service(t,1);row['driver']=driver(t,1);row['call']=call;rows.append(row)
    counts['integrated_retained']=160
    # Original adjacent service/driver call sequence; stop before18816 handoff.
    count=0
    for i in range(4):
        for value in [0,1000,5940,32767,65535]:
            t=fixture();initialize(t);w(t,0xA600+2*i,value,2)
            ref=copy.deepcopy(t);service(ref,i);driver(ref,i)
            t.r[13]=i;t.r[14]=i;sp=t.r[15];pc=0x12826
            for _ in range(20000):
                if pc==0x12836:break
                nxt,delay=t.instruction(pc)
                if delay:
                    _,nested=t.instruction(pc+2);assert not nested
                pc=nxt
            else:raise AssertionError('caller bound')
            assert t.r[15]==sp;equal(t,ref);count+=1
    counts['caller_slices']=count
    (ROOT/'tcu-output-service-verification.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,retained=rows,limits='Output preparation only;18816/18A44 hardware-facing handoff unexecuted. Explicit order/inputs; no physical units, cadence, CAN or actuator claim.'),indent=2)+'\n')
    print(json.dumps(counts))
if __name__=='__main__':main()
