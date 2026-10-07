"""Original 30FB6/8BB20 target, branch priority, retained ramp and override.

Finite stock RTZ inputs; isolated original bodies and explicitly scheduled
paired replay. No task cadence, physical loop identity or DSC actuation claim.
"""
import copy
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path
import verify_control_secondary_path as secondary
from verify_control_contributions import ECU, TCU, w, r, f, rf, q, number, fixture, run
from verify_throttle_candidate import protected
from verify_model_sources import lookup1, lookup2, map2_info
from verify_control_sources import sample_points
from sh_exact_float import exact_value
from sh_rtz_float import rtz_bits

ROOT = Path(__file__).resolve().parent
MAP1 = [(0xA3810,0x67EC),(0xA3828,0x697C),(0xA381C,0x6980),(0xA3870,0x6984),(0xA3864,0x6988)]
MAP2 = [(0xA3948,0x698C),(0xA395C,0x6990),(0xA3970,0x6994)]


def descriptor(e,value):
    mode=r(e,0x9611) if r(e,0x966C)&0x60 else 0
    raw=r(e,0x9642,2); scale=number(0x8BC0C)
    if mode==0: raw=max(0,min(65535,int(q(q(value/scale)+Fraction(1,2)))))
    elif mode in [5,7]: value=q(raw*scale)
    return value,raw,mode


def helper(e,value):
    want,raw,mode=descriptor(e,value)
    e.fr[4]=rtz_bits(value);run(e,0x8BB20)
    assert exact_value(e.fr[0])==want
    assert r(e,0x9642,2)==raw and r(e,0x9611)==mode


def model(e):
    bits=r(e,0x2160,4); check=~((bits>>16)+(bits&65535))&65535
    valid=check in [r(e,0x2164,2),r(e,0x2166,2)]
    x=rf(e,0x2160) if valid else number(0xDB240); y=rf(e,0x67E4)
    vals={a:lookup1(m,y) for m,a in MAP1}
    vals.update({a:lookup2(m,x,y) for m,a in MAP2})
    a,b,mode,flags,other=[r(e,k) for k in [0x6943,0x6944,0x67CC,0x695B,0x7247]]
    special=mode==1 or other==1; base=vals[0x67EC]
    if flags&128 and a==b==0: target=q(base+vals[0x697C if special else 0x6980]); branch='bit7'
    elif a==1 or b==1 or flags&8: target=q(base+rf(e,0x67F4)); branch='gate_or_bit3'
    elif flags&16: target=q(base+vals[0x6984 if special else 0x6988]); branch='bit4'
    elif flags&4: target=q(base+vals[0x698C]); branch='bit2'
    elif flags&32: target=q(base+vals[0x6990]) if mode==other==0 else base; branch='bit5'
    elif flags&64: target=q(base+vals[0x6994]) if mode==other==0 else base; branch='bit6'
    elif flags&1: target=base; branch='bit0'
    else: target=rf(e,0x67F0); branch='retain'
    vals[0x67F0]=target; vals[0x6904]=min(target,number(0xDB21C))
    selected=vals[0x6904] if r(e,0x9376)==1 else target
    old=rf(e,0x67FC)
    value=max(q(old-rf(e,0x690C)),selected) if old>selected else min(q(old+rf(e,0x6908)),selected)
    vals[0x69A4]=value; output,raw,control=descriptor(e,value); vals[0x67FC]=output
    return vals,raw,control,branch,valid


def target(e):
    vals,raw,mode,branch,valid=model(e)
    run(e,0x30FB6)
    for a,v in vals.items(): assert rf(e,a)==v,(hex(a),rf(e,a),v,branch)
    assert r(e,0x9642,2)==raw and r(e,0x9611)==mode
    if not valid: assert r(e,0x534C,4)==0xFFFF2160
    return branch


def setup():
    e=fixture(); secondary.prepare(e)
    protected(e,0x2160,95)
    for a,v in [(0x67E4,1200),(0x67F0,7),(0x67F4,2),(0x67FC,8),(0x6908,Fraction(1,4)),(0x690C,Fraction(1,2))]: f(e,a,v)
    return e


def direct():
    counts=dict(helper=0,priority=0,maps=0,ramp=0,protection=0,random=0); branches={}
    scale=number(0x8BC0C)
    values=[-10,0,Fraction(1,3),10,32,1000]+[q(scale*(n+Fraction(1,2))) for n in [0,1,32767,65534,65535]]
    for mask,mode,raw,value in itertools.product([0,16,32,64,96,255],[0,1,4,5,6,7,8,255],[0,1,32768,65535],values):
        e=fixture();w(e,0x966C,mask);w(e,0x9611,mode);w(e,0x9642,raw,2);helper(e,q(value));counts['helper']+=1
    for flags,a,b in itertools.product(range(256),[0,1,2],[0,1,2]):
        e=setup();w(e,0x695B,flags);w(e,0x6943,a);w(e,0x6944,b)
        branch=target(e);branches[branch]=branches.get(branch,0)+1;counts['priority']+=1
    for flags,a,b in itertools.product([0,1,4,8,16,32,64,128,255],[0,1,2,255],[0,1,2,255]):
        e=setup();w(e,0x695B,flags);w(e,0x67CC,a);w(e,0x7247,b);target(e);counts['priority']+=1
    ys=set().union(*(set(sample_points(m)) for m,a in MAP1))
    xs=set()
    for m,a in MAP2:
        xx,yy,_=map2_info(m)
        for source,dest in [(xx,xs),(yy,ys)]:
            dest.update(source);dest.update([source[0]-1,source[-1]+1]);dest.update(q((a+b)/2) for a,b in zip(source,source[1:]))
    for x,y in itertools.product(sorted(xs),sorted(ys)):
        e=setup();protected(e,0x2160,x);f(e,0x67E4,y);w(e,0x695B,4);target(e);counts['maps']+=1
    for old,inc,dec,cap in itertools.product([-10,0,7,14,20],[0,Fraction(1,4),10,-1],[0,Fraction(1,2),10,-1],[0,1,2,255]):
        e=setup();f(e,0x67FC,old);f(e,0x6908,inc);f(e,0x690C,dec);w(e,0x9376,cap);target(e);counts['ramp']+=1
    for c1,c2 in itertools.product([False,True],repeat=2):
        e=setup();protected(e,0x2160,40) # Distinguish admitted value from fallback95.
        if c1:w(e,0x2164,r(e,0x2164,2)^1,2)
        if c2:w(e,0x2166,r(e,0x2166,2)^2,2)
        e.fr[4]=rtz_bits(number(0xDB240));sp,mask=e.r[15],e.sr&0xF0
        e.run(0x15246,0xFFFF2160)
        assert (e.r[15],e.sr&0xF0)==(sp,mask)
        assert exact_value(e.fr[0])==(number(0xDB240) if c1 and c2 else 40)
        w(e,0x695B,4);target(e);counts['protection']+=1
    rng=random.Random(0x30FB6)
    for _ in range(500):
        e=setup()
        for a in [0x6943,0x6944,0x67CC,0x7247,0x9376]:w(e,a,rng.choice([0,1,2,255]))
        w(e,0x695B,rng.randrange(256));w(e,0x966C,rng.choice([0,32,64,96]));w(e,0x9611,rng.choice([0,5,7,255]));w(e,0x9642,rng.randrange(65536),2)
        for a in [0x67E4,0x67F0,0x67F4,0x67FC,0x6908,0x690C]:f(e,a,Fraction(rng.randrange(-100,1000),8))
        target(e);counts['random']+=1
    assert set(branches)=={'bit7','gate_or_bit3','bit4','bit2','bit5','bit6','bit0','retain'}
    return counts,branches


def caller_cases():
    count=0
    for flag,mode,mask in itertools.product([0,1,4,8,16,32,64,128,255],[0,5,7],[0,96]):
        e=setup();w(e,0x695B,flag);w(e,0x9611,mode);w(e,0x966C,mask);w(e,0x9642,30000,2)
        other=copy.deepcopy(e);target(e);pc=0x1B570;sp=other.r[15];seen=[]
        for _ in range(100000):
            if pc==0x1B576:break
            if pc==0x30FB6:seen.append(pc)
            nxt,delay=other.instruction(pc)
            if delay:
                _,nested=other.instruction(pc+2);assert not nested
            pc=nxt
        else:raise AssertionError('caller bound')
        assert seen==[0x30FB6] and other.r[15]==sp
        for address in [a for _,a in MAP1+MAP2]+[0x67F0,0x6904,0x69A4,0x67FC]:assert r(e,address,4)==r(other,address,4)
        assert r(e,0x9642,2)==r(other,0x9642,2) and r(e,0x9611)==r(other,0x9611)
        count+=1
    return count


def retained():
    rows=[];e=setup();f(e,0x67FC,0);f(e,0x67F0,2)
    for call in range(1,33):
        if call==9:f(e,0x67F0,6)
        if call==17:w(e,0x966C,32);w(e,0x9611,5);w(e,0x9642,30000,2)
        if call==25:w(e,0x966C,0)
        branch=target(e)
        rows.append(dict(call=call,branch=branch,target=float(rf(e,0x67F0)),candidate=float(rf(e,0x69A4)),value=float(rf(e,0x67FC)),mode=r(e,0x9611)))
    assert rows[7]['value']==2 and rows[15]['value']==4
    assert rows[16]['value']==14.6484375 and rows[23]['value']==14.6484375
    assert rows[24]['value']==14.1484375 and rows[24]['mode']==0
    return rows


def prepare(e):
    secondary.prepare(e);protected(e,0x2160,95)
    for a,v in [(0x67E4,1200),(0x67F0,7),(0x67F4,2),(0x67FC,0),(0x6908,Fraction(1,4)),(0x690C,Fraction(1,2))]:f(e,a,v)
    for a in [0x6943,0x6944,0x67CC,0x7247,0x9376,0x9611]:w(e,a,0)


def step(e,call):
    f(e,0x6DB4,299 if call<=20 else 560 if call<=100 else 540 if call<=180 else 250 if call<=220 else 600)
    f(e,0x67E4,600 if call<=100 else 1200 if call<=220 else 2400)
    w(e,0x695B,1 if call<=80 else 4 if call<=160 else 32 if call<=240 else 0)
    w(e,0x7002,2 if 61<=call<=70 else 0)
    if call==101:w(e,0x966C,96);w(e,0x9611,5);w(e,0x9642,30000,2)
    if call==141:w(e,0x966C,0)
    branch=target(e) # Explicit cross-task scheduling, not an original contiguous caller.
    secondary.gates.timer(e);secondary.gates.segment(e);secondary.group(e);secondary.inputs.publish(e)
    update,divisor=secondary.downstream.group(e);row=secondary.magnitude.integrated_step(e,call)
    row.update(target_branch=branch,target=float(rf(e,0x67F0)),candidate=float(rf(e,0x69A4)),
               produced67fc=float(rf(e,0x67FC)),target_mode=r(e,0x9611),
               secondary684c=float(rf(e,0x684C)),published6cc8=float(rf(e,0x6CC8)),
               normalized8118=float(rf(e,0x8118)),normalized_updated=update,normalized_divisor=float(divisor))
    return row


def integrated():
    rows,boundaries=secondary.prior.lifecycle(prepare=prepare,upstream=step,checkpoints={20,21,60,61,70,71,80,81,100,101,120,140,141,160,161,220,221,240,241,320})
    by_call={row['call']:row for row in rows}
    for call in [101,120,140]:assert by_call[call]['produced67fc']==14.6484375 and by_call[call]['target_mode']==5
    assert by_call[141]['target_mode']==0
    return rows,boundaries


def main():
    counts,branches=direct();counts['caller']=caller_cases();history=retained()
    print('Direct',counts,flush=True)
    rows,boundaries=integrated()
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,branches=branches,
                retained=history,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,lifecycle=rows)
    (ROOT/'control-upstream-target-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Integrated',320,len(boundaries),flush=True)

if __name__=='__main__':main()
