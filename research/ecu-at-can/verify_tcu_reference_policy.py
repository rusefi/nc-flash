"""Original cached-source/discrepancy policy, alternate value and recovery.

Synthetic timestamps, phase states, ages and call schedules. Original helpers
execute without stubs. Physical units, real task timing and hardware unproved.
"""
import hashlib
import itertools
import json
import random

from sh_rotate import SHRotate
from sh_subset import signed
from verify_can201_byte6 import TCU,w,r
from verify_tcu_measurement import clamp,div,wire
from verify_tcu_reference_source import samples,normalized
from verify_tcu_reference_error import COEFFICIENTS,error


def convert(value,index):
    return clamp(div(signed(value,16)*4096,COEFFICIENTS[index]),-32768,32767)


def discrepancy(t,active,raw=None):
    raw=signed(r(t,0x91A2,2),16) if raw is None else raw
    old=[signed(r(t,0x91B8+2*i,2),16) for i in range(6)]
    cached=signed(r(t,0x91C4,2),16) if active else signed(r(t,0x80EE,2),16) if r(t,0x810C)<5 else 0
    index=r(t,0x91C9) if active else r(t,0x8081)
    selected=index if active else 6 if r(t,0x8080)==255 else index
    value=convert(cached,selected)
    latch=bool(r(t,0x91A6)&16)
    count=r(t,0x91C6)
    if old[0]-raw>=998:latch,count=True,0
    difference=value-raw
    count=0 if difference>=128 and difference>=div(value*5,100) else min(255,count+1)
    if not (r(t,0x9194)&1 or r(t,0x92C6)&16) and count>=7:latch=False
    return {'flags':(r(t,0x91A6)&~16)|16*int(latch),'count':count,
            'cache':cached&65535,'index':index,'history':[(x&65535) for x in old[1:]+[raw]],
            'converted':value}


def alternate(t,active):
    refresh=not active and r(t,0x8196)*4>=37
    cached=signed(r(t,0x80EE,2),16) if refresh else signed(r(t,0x91B6,2),16)
    if refresh and r(t,0x810C)>=5:cached=0
    index=r(t,0x8081) if refresh else r(t,0x91C8)
    selected=6 if refresh and r(t,0x8080)==255 else index
    if r(t,0x9194)&1 or r(t,0x91A6)&16:
        result=signed(r(t,0x80EA,2),16)
    elif r(t,0x8080)==0:result=0
    else:result=convert(cached,selected)
    return clamp(result,0,32767),cached&65535,index


def phase(t,active):
    w(t,0x8088,2 if active else 1)
    w(t,0x96C4,0);w(t,0x96C5,1 if active else 0)
    w(t,0x95D4+13,1)


def check_policy(t,active):
    assert bool(t.run(0x31720))==active
    expected=discrepancy(t,active)
    t.run(0x20FAC,limit=100000)
    assert [r(t,a,n) for a,n in [(0x91A6,1),(0x91C6,1),(0x91C4,2),(0x91C9,1)]]==[expected[k] for k in ['flags','count','cache','index']]
    assert [r(t,0x91B8+2*i,2) for i in range(6)]==expected['history']
    expected_alt=alternate(t,active)
    actual=t.run(0x20EAA,limit=100000)
    assert (actual,r(t,0x91B6,2),r(t,0x91C8))==expected_alt
    return expected,expected_alt


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rng=random.Random(0x20FAC)
    cases=0
    for active,age,kind,index,cached_index in itertools.product([False,True],
            [0,4,5,127,128,255],[0,1,255],range(7),range(7)):
        t=SHRotate(TCU);phase(t,active)
        for a,v,n in [(0x810C,age,1),(0x8080,kind,1),(0x8081,index,1),
                      (0x91C9,cached_index,1),(0x91C8,cached_index,1),
                      (0x8196,rng.choice([0,9,10,255]),1),
                      (0x80EE,rng.choice([0,1,1000,10000,32767,32768,65535]),2),
                      (0x91C4,rng.choice([0,1,1000,30000,32768,65535]),2),
                      (0x91B6,rng.choice([0,1,1000,30000,32768,65535]),2),
                      (0x80EA,rng.choice([0,1,9999,32767,32768,65535]),2),
                      (0x91A2,rng.randrange(65536),2),(0x91A6,rng.randrange(256),1),
                      (0x91C6,rng.choice([0,5,6,7,127,128,254,255]),1),
                      (0x9194,rng.randrange(256),1),(0x92C6,rng.randrange(256),1)]:w(t,a,v,n)
        for i in range(6):w(t,0x91B8+2*i,rng.randrange(65536),2)
        check_policy(t,active);cases+=1

    # Exact discrepancy, drop and clear-counter boundaries with identity index3.
    boundaries=0
    for raw,converted,drop,count,blocked,latch in itertools.product(
            [0,10000],[127,128,129,10525,10526,10527], [997,998], [5,6,7,255],
            [0,1,16,17],[0,16]):
        t=SHRotate(TCU);phase(t,False)
        for a,v,n in [(0x8080,1,1),(0x8081,3,1),(0x80EE,converted,2),
                      (0x91A2,raw,2),(0x91B8,raw+drop,2),(0x91C6,count,1),
                      (0x9194,blocked&1,1),(0x92C6,blocked&16,1),(0x91A6,latch,1)]:w(t,a,v,n)
        check_policy(t,False);boundaries+=1

    # Direct alternate-source boundaries independently of discrepancy mutation.
    alt_cases=0
    for active,timer,age,kind,blocked in itertools.product([False,True],
            [0,9,10,255],[4,5,128],[0,1,255],[0,1,16]):
        t=SHRotate(TCU);phase(t,active)
        for a,v,n in [(0x8196,timer,1),(0x810C,age,1),(0x8080,kind,1),
                      (0x8081,2,1),(0x91C8,4,1),(0x91B6,5000,2),
                      (0x80EE,10000,2),(0x80EA,7777,2),(0x9194,blocked&1,1),
                      (0x91A6,blocked&16,1)]:w(t,a,v,n)
        expected=alternate(t,active)
        assert (t.run(0x20EAA,limit=100000),r(t,0x91B6,2),r(t,0x91C8))==expected
        alt_cases+=1

    elapsed_cases=0
    for value,sr in itertools.product([0,1,65534,65535],[0,1,0xF0,0xF1]):
        t=SHRotate(TCU);t.sr=sr;w(t,0x91AC,value,2)
        t.run(0x2094E)
        assert r(t,0x91AC,2)==min(65535,value+1) and t.sr&~1==sr&~1
        elapsed_cases+=1

    scheduler_cases=0
    for mode,value in itertools.product(range(256),[0,65534,65535]):
        t=SHRotate(TCU);w(t,0x800A,mode);w(t,0x91AC,value,2)
        t.run(0x128B6,limit=100000)
        assert r(t,0x91AC,2)==(min(65535,value+1) if mode==3 else value)
        assert r(t,0x84D0,4)==int(mode==3)
        scheduler_cases+=1
    t=SHRotate(TCU);t.run(0x20658);w(t,0x91AC,65535,2)
    t.run(0x179A8,12160,limit=100000)
    assert r(t,0x91AC,2)==0

    # Original timer wheel -> source timers, with original clear conditions.
    t=SHRotate(TCU);t.run(0x12880)
    wheel=[]
    for tick in range(80):
        t.run(0x11014)
        expected=[(tick+2)//2,(tick+3)//4,(tick+5)//8]
        assert [r(t,a) for a in [0x810C,0x8158,0x8196]]==expected
        if tick in [0,1,3,71,75,79]:wheel.append({'calls':tick+1,'age810C':expected[0],'hold8158':expected[1],'settle8196':expected[2]})

    # A capture-driven deceleration triggers and clears bit4 while active phase
    # retains old measured/index caches. No direct80EA/80EC/80EE/9218 writes.
    lifecycles=[]
    for initial_interval,initial_raw,should_latch in [(9480,9001,False),(6400,13333,True)]:
        t=SHRotate(TCU);t.run(0x20658);t.run(0x211C4)
        w(t,0x8080,1);w(t,0x8081,3)
        def capture(interval):
            w(t,0x810D,0);w(t,0x810C,0)
            t.run(0x179A8,(r(t,0x88FC,4)+interval)&0xFFFFFFFF)
            t.run(0x17A58,(r(t,0x890C,4)+12800)&0xFFFFFFFF)
            t.run(0x2124C,limit=100000)
        for _ in range(32):capture(initial_interval);t.run(0x2086C,limit=200000)
        assert r(t,0x80EA,2)==r(t,0x80EC,2)==initial_raw and r(t,0x80EE,2)==5000
        assert r(t,0x91A6)&16==0 and r(t,0x91C4,2)==5000
        phase(t,True)
        t.run(0x2117C);t.run(0x30B20);t.run(0x30B28,9)
        rows=[]
        for tick in range(36):
            capture(12160)
            raw=normalized(sum(samples(t)),18)[0]
            expected=discrepancy(t,True,raw)
            # Capture cleared91AC; no hold/fault-summary gate is enabled in this fixture.
            assert r(t,0x91AC,2)==0 and r(t,0x9194)&1==0
            t.run(0x2086C,limit=200000)
            assert r(t,0x91A2,2)==raw and r(t,0x91A6)==expected['flags']
            assert r(t,0x91C6)==expected['count'] and r(t,0x91C4,2)==5000
            assert r(t,0x8196)==0
            if expected['flags']&16:assert r(t,0x80EA,2)==r(t,0x80EC,2)==5000
            else:assert r(t,0x80EA,2)==raw
            assert r(t,0x91A4,2)==5000
            previous=signed(r(t,0x95C0,2),16)
            t.run(0x2117C);t.run(0x30B9E)
            expected_error=error(5000,r(t,0x9228,4))
            assert signed(r(t,0x80D8,2),16)==(previous+expected_error)//2
            rows.append({'call':tick+1,'raw':raw,'source80EA':r(t,0x80EA,2),
                         'source80EC':r(t,0x80EC,2),'flags':r(t,0x91A6),'counter':r(t,0x91C6),
                         'reference':r(t,0x9228,4),'error':signed(r(t,0x80D8,2),16),
                         'can216_byte4':wire(t)})
        assert any(row['flags']&16 for row in rows)==should_latch
        assert rows[-1]['flags']&16==0 and rows[-1]['source80EA']==rows[-1]['source80EC']==7017
        lifecycles.append({"initial_interval":initial_interval,"initial_raw":initial_raw,"latched":should_latch,"checkpoints":rows})
    print(json.dumps({'scope':__doc__.strip(),'tcu_sha256':hashlib.sha256(TCU).hexdigest(),
                      'cached_policy_cases':cases,'threshold_cases':boundaries,
                      'alternate_source_cases':alt_cases,'elapsed_counter_cases':elapsed_cases,
                      'elapsed_scheduler_mode_cases':scheduler_cases,
                      'timer_wheel_calls':80,'timer_checkpoints':wheel,
                      'capture_policy_lifecycles':lifecycles,'paired_measurement_can216_ecu_checks':sum(len(x['checkpoints']) for x in lifecycles)},indent=2))


if __name__=='__main__':main()
