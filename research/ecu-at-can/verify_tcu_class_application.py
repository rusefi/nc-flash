"""Stock uniform-update admission and complete stored-adjustment application.

Application math is independently modeled around an observed original 3AC70
return. That base producer executes without stubs but is NOT independently
modeled here. This is composition evidence, not proof of base signal meaning.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
from verify_tcu_class_adjustments import (fixture, execute, slots, flags, TCU,
    w, r, clamp, consumer_model, update)
from sh_subset import signed

ROOT=Path(__file__).resolve().parent


def uniform_fixture():
    t=fixture()
    for a,v,n in [(0x9889,1,1),(0x8080,6,1),(0x8081,4,1),(0x80EE,4000,2),(0x9870,1,1)]: w(t,a,v,n)
    return t


def uniform():
    assert TCU[0x7713A:0x7713C] == b'\0\0'
    t=uniform_fixture()
    for value in range(65536):
        w(t,0x985A,value,2)
        assert execute(t,0x36948)==0
        assert 0x36984 in t.visited and 0x36988 not in t.visited
        assert r(t,0x985A,2)==value
    full=0
    for state,mode,old in itertools.product([0,1,2,3,255],[0,1,2,3,4,5,6,255],[-32768,-81,-80,0,79,80,32767]):
        t=uniform_fixture(); w(t,0x9858,state); w(t,0x9870,mode)
        for i in range(3): w(t,0x616A+2*i,old,2); w(t,0x6165+i,[0,1,255][i])
        before=slots(t); seen=flags(t)
        execute(t,0x36800)
        want=0 if state in [2,3] or state==1 and mode in [2,3,4,5,6] else state
        assert r(t,0x9858)==want
        if state==3: before[:3]=[clamp(v+11) for v in before[:3]]
        assert slots(t)==before and flags(t)==seen
        assert (0x36B26 in t.visited)==(state==3)
        full+=1
    helpers=0
    for state,bits in itertools.product([0,1,2,3,255],[0,1,63,64,65,255]):
        t=uniform_fixture(); w(t,0x9858,state); w(t,0x9889,bits)
        execute(t,0x36848)
        assert r(t,0x9858)==(2 if state!=0 and bits&64 else 0)
        helpers+=1
    for state in [0,1,2,3,255]:
        t=uniform_fixture(); w(t,0x9858,state); execute(t,0x36838)
        assert r(t,0x9858)==(1 if state==0 else state)
        helpers+=1
    for mode,value in itertools.product([0,1,255],[0,1,32767,32768,65534,65535]):
        t=uniform_fixture(); w(t,0x9870,mode); w(t,0x985A,value,2)
        execute(t,0x3686E)
        active=mode!=0 and value<65535
        assert r(t,0x985A,2)==value+active
        assert r(t,0x6170,2)==(value+1 if active else 0)
        # Original getter imports cached slot3, independently of local word985A.
        execute(t,0x367F0)
        assert r(t,0x985A,2)==r(t,0x6170,2)
        helpers+=1
    rows=[]; t=uniform_fixture()
    for call in range(1,41):
        execute(t,0x36838); w(t,0x9889,65); execute(t,0x36848)
        assert r(t,0x9858)==2
        execute(t,0x36800)
        assert r(t,0x9858)==0 and 0x36B26 not in t.visited
        execute(t,0x3686E)
        assert slots(t)[:3]==[0]*3 and r(t,0x985A,2)==call and slots(t)[3]==call
        rows.append(dict(call=call,state=r(t,0x9858),count=call,slots=slots(t)[:4]))
    return dict(exhaustive=65536,full=full,helpers=helpers),rows


def bank_fixture():
    t=fixture()
    assert r(t,0xAE18,4)==0x0304FFFF
    execute(t,0x39BE2)
    handles=[execute(t,0x39BF2,priority) for priority in [1,2,3,2]]
    assert handles==[4,5,6,7]
    for head,members in [(0,[4]),(1,[5,7]),(2,[6]),(3,[])]:
        chain=[head]+members
        for pos,index in enumerate(chain):
            assert r(t,0x98B4+4*index)==chain[pos-1]
            assert r(t,0x98B5+4*index)==chain[(pos+1)%len(chain)]
    return t


def tail_model(t,value):
    value=signed(value,16); out=r(t,0x98AE,2)
    first=bool(r(t,0x9924)&1)
    if first and value>=13133: out=2
    if (first or r(t,0x9889)&16 or r(t,0x9860)&1) and 102<=value<13133: out=1
    if value<102: out=0
    return out


def tail_cases():
    count=0
    for value,old,first,second,third in itertools.product(
            [-32768,-1,0,101,102,103,13132,13133,13134,32767],
            [0,1,2,255,65535],[0,1],[0,16],[0,1]):
        t=fixture()
        for a,v,n in [(0x98B2,value,2),(0x98AE,old,2),(0x9924,first,1),(0x9889,second,1),(0x9860,third,1)]: w(t,a,v,n)
        want=tail_model(t,value); execute(t,0x39B56)
        assert r(t,0x98AE,2)==want
        count+=1
    return count


def select(t):
    # These fixtures use original allocation order: p3:[6],p2:[5,7],p1:[4].
    old_flags=r(t,0x98AC); old_selected=r(t,0x98D4,2); old_index=r(t,0x98D6)
    permissive=r(t,0x800E)>=60 and signed(r(t,0x933C),8)<4 and r(t,0x8081)==5
    forced=permissive and bool(r(t,0x92C8)&64)
    if forced:
        value=15232 if r(t,0x92C8)&16 else 0
        index=old_index
    else:
        for index in [6,5,7,4]:
            value=r(t,0x98B6+4*index,2)
            if value!=65535: break
    expected_flags=(old_flags & ~0x11) | (not permissive) | (16 if forced else 0)
    links=[r(t,0x98B4+4*i,2) for i in range(8)]
    ref=copy.deepcopy(t)
    w(ref,0x98AE,tail_model(t,value),2)
    w(ref,0x98B2,value,2); w(ref,0x9108,32767 if value==65535 else value,2)
    w(ref,0x98AC,expected_flags)
    if not forced: w(ref,0x98D4,value,2); w(ref,0x98D6,index)
    execute(t,0x39C90)
    assert r(t,0x98B2,2)==value and r(t,0x9108,2)==(32767 if value==65535 else value)
    assert r(t,0x98AC)==expected_flags
    assert r(t,0x98D6)==index and r(t,0x98D4,2)==(old_selected if forced else value)
    assert [r(t,0x98B4+4*i,2) for i in range(8)]==links
    assert r(t,0x98AE,2)==r(ref,0x98AE,2) and 0x39B56 in t.visited
    keys={a for a in set(t.ram)|set(ref.ram) if a>=0xFFFF0000}
    assert all(t.ram.get(a,0)==ref.ram.get(a,0) for a in keys)
    return dict(published=r(t,0x9108,2),selected_index=index,forced=forced)


def selection_cases():
    count=0
    candidates=[[65535]*4,[100,200,300,400],[100,65535,65535,400],[65535,200,65535,400]]
    for values,byte0,byte1,gear,bits in itertools.product(candidates,[59,60,255],[3,4,255],[4,5],[0,16,64,80]):
        t=bank_fixture()
        for index,value in zip([4,5,6,7],values):
            t.r[5]=value; execute(t,0x39C0A,index)
        for a,v in [(0x800E,byte0),(0x933C,byte1),(0x8081,gear),(0x92C8,bits),(0x98AC,0xAA)]: w(t,a,v)
        select(t); count+=1
    return count


def lower_model(t):
    fixed=clamp(slots(t)[2]*16,-32768,32767)
    return clamp(4019+fixed,0,15232)


def application(t):
    # Reference only the nested base return. The rest of the arithmetic,
    # storage address, word truncation and allowed RAM effects are independent.
    ref=copy.deepcopy(t)
    base=signed(execute(ref,0x3AC70),16)
    base_branches=[pc for pc in [0x3ACAE,0x3AD4E] if pc in ref.visited]
    lower=lower_model(ref); dynamic=consumer_model(ref)
    value=min(15206,max(lower,base+dynamic+(signed(r(ref,0x98DC,2),16)>>1)))
    index=r(ref,0x9856)
    w(ref,0x9854,lower,2); w(ref,0x98B6+4*index,value,2)
    before=slots(t); seen=flags(t)
    actual=signed(execute(t,0x36704),32)
    assert actual==value,(actual,value,base,dynamic,lower)
    assert r(t,0x9854,2)==lower and r(t,0x98B6+4*index,2)==value
    assert slots(t)==before and flags(t)==seen
    # Ignore synthetic stack bytes; compare ALL application RAM bytes written
    # or supplied in either execution, with implicit zero bytes normalized.
    keys={a for a in set(t.ram)|set(ref.ram) if a>=0xFFFF0000}
    assert all(t.ram.get(a,0)==ref.ram.get(a,0) for a in keys)
    assert all(pc in t.visited for pc in [0x3AC70,0x36A74,0x3676E,0x36A0A,0x39C0A,0x30518])
    return dict(base=base,dynamic=dynamic,lower=lower,value=value,index=index,base_branches=base_branches)


def application_cases():
    lower_cases=0
    t=fixture()
    for value in [-32768,-2049,-2048,-952,-252,-251,-1,0,1,79,80,81,700,701,2047,2048,32767]:
        w(t,0x616E,value,2)
        assert signed(execute(t,0x3676E),32)==lower_model(t)
        lower_cases+=1
    rng=random.Random(0x36704); branches=set(); count=0; samples=[]
    for mode in [0,1,2,255]:
        for _ in range(75):
            t=bank_fixture(); w(t,0x988A,mode)
            for a in [0x80EE,0x80FE,0x92E4,0x92F6,0x993C,0x993E,0x98DC]: w(t,a,rng.randrange(65536),2)
            for i in range(3): w(t,0x616A+2*i,rng.randrange(65536),2)
            w(t,0x92D1,rng.randrange(16)); w(t,0x9856,rng.choice([4,5,6,7]))
            row=application(t); row.update(select(t)); branches.update(row['base_branches']); count+=1
            if len(samples)<8: samples.append(row)
    assert branches=={0x3ACAE,0x3AD4E}
    # Directly produced conditional updates flow into original application.
    t=bank_fixture(); w(t,0x9856,4); rows=[]
    for call in range(1,101):
        w(t,0x80EE,5500,2); w(t,0x98DC,0 if call<=80 else -1000,2)
        update(t)
        row=application(t); row.update(select(t)); row.update(call=call,slots=slots(t)[:3]); rows.append(row)
    assert rows[79]['slots']==[103,91,80]
    return dict(lower=lower_cases,full=count),samples,rows


def main():
    uniform_counts,uniform_rows=uniform()
    print('Uniform checks passed',uniform_counts,flush=True)
    application_counts,samples,rows=application_cases()
    application_counts['selection']=selection_cases()
    application_counts['tail']=tail_cases()
    out=dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(),uniform_counts=uniform_counts,
        uniform_retained=uniform_rows,application_counts=application_counts,
        application_samples=samples,application_retained=rows,scope_limit=__doc__)
    (ROOT/'tcu-class-application-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Application checks passed',application_counts,'retained',len(rows),flush=True)


if __name__=='__main__': main()
