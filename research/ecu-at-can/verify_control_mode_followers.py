"""Original post-mode input producers and their retained minimum/countdown.

Stock finite RTZ execution, contiguous187-region caller and explicitly ordered
cross-task replay. Raw input identity, real task cadence and DSC actuation are
not inferred. No shared interpreter or existing verifier changes.
"""
import copy
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import verify_control_mode_feedback as prior
from verify_control_contributions import ECU,TCU,w,r,f,rf,q,number,run
from verify_control_input_gates import neighbors

ROOT=Path(__file__).resolve().parent
ENTRIES=[0x30B4A,0x30512,0x30522,0x30544,0x30702]
OUTPUTS=[(0x693C,1),(0x67D0,4),(0x67D4,4),(0x67D8,4),(0x6936,1)]


def mask(e):
    want=int(bool(r(e,0x695B)&0x1E))
    run(e,0x30B4A); assert r(e,0x693C)==want


def biased(e):
    want=q(rf(e,0x6CB4)+number(0xDB1D4))
    run(e,0x30512); assert rf(e,0x67D0)==want


def scaled(e):
    want=q(r(e,0x6CAC)*number(0x30604))
    run(e,0x30522); assert rf(e,0x67D4)==want


def initialize_minimum(e):
    want=r(e,0x67D0,4); run(e,0x3053A); assert r(e,0x67D8,4)==want


def minimum(e):
    want=min(rf(e,0x67D8),rf(e,0x67D0)) if r(e,0x70F0)==1 else rf(e,0x67D8)
    run(e,0x30544); assert rf(e,0x67D8)==want


def counter(e):
    decrement=(rf(e,0x67D4)>number(0xDB178) and rf(e,0x67D0)<number(0xDB17C)
        and r(e,0x91E5)!=1 and r(e,0x9462)!=1)
    want=max(0,r(e,0x6927)-1) if decrement else ECU[0xDB0B6]
    run(e,0x30764); assert r(e,0x6927)==want
    return decrement


def expired(e):
    want=int(r(e,0x6927)==0 and r(e,0x9462)==0)
    run(e,0x30702); assert r(e,0x6936)==want


def group(e):
    mask(e); biased(e); scaled(e); minimum(e); expired(e)


def direct():
    counts=dict(mask=0,biased=0,scaled=0,initialize=0,minimum=0,counter=0,expired=0)
    for flag in range(256):
        e=prior.setup(); w(e,0x695B,flag); mask(e); counts['mask']+=1
    values=[-1000,-10,-1,Fraction(-1,32),0,Fraction(1,32),1,8,10,1000]
    for value in values:
        e=prior.setup(); f(e,0x6CB4,value); biased(e); initialize_minimum(e)
        counts['biased']+=1; counts['initialize']+=1
    for raw in range(256):
        e=prior.setup(); w(e,0x6CAC,raw); scaled(e); counts['scaled']+=1
    for gate,value,old in itertools.product([0,1,2,255],values,values):
        e=prior.setup(); w(e,0x70F0,gate); f(e,0x67D0,value); f(e,0x67D8,old)
        minimum(e); counts['minimum']+=1
    for a,b,gate,raw,old in itertools.product([0,*neighbors(number(0xDB178)),30],
            [0,*neighbors(number(0xDB17C)),30],[0,1,2,255],[0,1,2,255],[0,1,200,255]):
        e=prior.setup(); f(e,0x67D4,a); f(e,0x67D0,b)
        w(e,0x91E5,gate); w(e,0x9462,raw); w(e,0x6927,old)
        counter(e); counts['counter']+=1
    for old,raw in itertools.product(range(256),[0,1,2,255]):
        e=prior.setup(); w(e,0x6927,old); w(e,0x9462,raw); expired(e); counts['expired']+=1
    return counts


def callers():
    count=0
    for mode,raw,old,gate in itertools.product([0,1,8,16,255],[0,128,255],[0,1],[0,1]):
        e=prior.setup(); w(e,0x695B,mode); w(e,0x6CAC,raw); w(e,0x6927,old); w(e,0x70F0,gate)
        f(e,0x67D8,20); other=copy.deepcopy(e)
        prior.source.followers.adjustment.upstream.secondary.gates.timer(e)
        prior.mode(e); group(e)
        ordered=[0x3181C,0x30202]+ENTRIES; pc=0x1876E; seen=[]; sp=other.r[15]
        for _ in range(100000):
            if pc==0x18798: break
            if pc in ordered: seen.append(pc)
            nxt,delay=other.instruction(pc)
            if delay:
                _,nested=other.instruction(pc+2); assert not nested
            pc=nxt
        else: raise AssertionError('caller bound')
        assert seen==ordered and other.r[15]==sp
        for a,n in OUTPUTS+[(0x6910,2),(0x695B,1),(0x6956,2),(0x69AD,1)]:
            assert r(e,a,n)==r(other,a,n),(hex(a),r(e,a,n),r(other,a,n))
        count+=1
    return count


def retained():
    e=prior.setup(); w(e,0x6CAC,255); w(e,0x9462,0); w(e,0x91E5,0); w(e,0x6927,200)
    w(e,0x70F0,1); f(e,0x6CB4,8); biased(e); scaled(e); initialize_minimum(e)
    rows=[]
    for call in range(1,241):
        w(e,0x9462,1 if call==205 else 2 if call==210 else 0)
        if call==30: f(e,0x6CB4,5)
        if call==40: f(e,0x6CB4,8)
        decrement=counter(e); group(e)
        rows.append(dict(call=call,counter=r(e,0x6927),expired=r(e,0x6936),
            minimum=float(rf(e,0x67D8)),input=float(rf(e,0x67D0)),decrement=decrement))
    assert rows[198]['counter']==1 and rows[199]['expired']==1
    assert rows[204]['counter']==200 and rows[204]['expired']==0
    assert rows[209]['counter']==195 and rows[209]['expired']==0
    assert rows[29]['minimum']==rows[39]['minimum']<rows[39]['input']
    return rows


def prepare(e):
    prior.prepare(e)
    w(e,0x6CAC,0); w(e,0x70F0,0); w(e,0x9462,0); w(e,0x91E5,0); w(e,0x6927,200)
    biased(e); initialize_minimum(e)


def input_step(e,call):
    prior.input_step(e,call)
    #30764 has a different caller at19E10; this order is explicit, not proven
    #scheduler ordering. It consumes the previous produced67D0/67D4 values.
    counter(e)


def mode_step(e,call):
    prior.mode_step(e,call)
    w(e,0x6CAC,0 if call<=100 else 120 if call<=160 else 255)
    w(e,0x70F0,1 if 40<=call<=60 else 2)
    w(e,0x9462,1 if 201<=call<=210 else 0)
    group(e)


def step(e,call):
    old=r(e,0x695B)
    row=prior.source.followers.step(e,call,input_producer=input_step,mode_producer=mode_step)
    row.update(entry_mode=old,next_mode=r(e,0x695B),selector_pair=r(e,0x6956,2),
        mode_mask=r(e,0x693C),biased67d0=float(rf(e,0x67D0)),scaled67d4=float(rf(e,0x67D4)),
        retained67d8=float(rf(e,0x67D8)),counter6927=r(e,0x6927),expired6936=r(e,0x6936),
        upper6939=r(e,0x6939),inhibit6937=r(e,0x6937))
    return row


def main():
    counts=direct(); counts['caller']=callers(); history=retained()
    print('Verified direct/caller',counts,flush=True)
    rows,boundaries=prior.source.followers.adjustment.upstream.secondary.prior.lifecycle(prepare=prepare,upstream=step,
        checkpoints={1,30,40,50,51,60,61,100,101,160,161,200,201,210,211,240,241,250,251,260,261,320})
    assert any(row['scaled67d4']>float(number(0xDB170)) and row['inhibit6937']==1 for row in rows)
    out=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts,retained=history,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,lifecycle=rows)
    (ROOT/'control-mode-followers-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Integrated',320,len(boundaries),'inhibits',sorted({r['inhibit6937'] for r in rows}),flush=True)


if __name__=='__main__': main()
