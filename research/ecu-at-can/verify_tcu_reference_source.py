"""Original reference acquisition, policy and both-capture shift lifecycles.

Synthetic timestamps, ages and call order; original firmware helpers execute.
No sensor wiring, physical units, peripheral interrupts or full task emulation.
"""
import hashlib
import itertools
import json
import random

from sh_rotate import SHRotate
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_measurement import clamp, div, wire
from verify_tcu_reference_error import COEFFICIENTS
from verify_tcu_phase_retirement import full_fixture, RetirementTCU, GROUPS
from verify_tcu_request_admission import periodic, paired_snapshot

RESET = 14*4096


def udiv(a, b):
    a, b = a & 0xFFFFFFFF, b & 0xFFFFFFFF
    return a//b if b else 0xFFFFFFFF if a else 0


def samples(t):
    return [signed(r(t, 0x91CC+4*i, 4), 32) for i in range(18)]


def seed(t, values, head=0):
    for i, value in enumerate(values):
        w(t, 0x91CC+4*i, value, 4)
    w(t, 0x91B4, head)


def normalized(total, count):
    period = div(clamp(total*18), count)
    return clamp(div(153600000, period), 0, 32767), period


def branch_model(g, regs):
    """Predict selected209B4 outputs at its post-gate20AAC boundary."""
    flags=r(g,0x91A6)
    fallback=bool(r(g,0x9194)&1 or flags&16)
    if fallback:
        branch='fallback'; period=-1
        kind=signed(regs[6],8)
        index=6 if kind==-1 else regs[10]&255
        if regs[5]&255==1: index=g.read(regs[15],1)
        result=0 if kind==0 else clamp(div(signed(regs[9]<<12,32),COEFFICIENTS[index]),-32768,32767)
        result=clamp(result,0,32767); reference=result
    elif flags&1:
        branch='hold';result=r(g,0x80EA,2);reference=r(g,0x80EC,2);period=r(g,0x9198,4)
    elif r(g,0x810D)>=14 or r(g,0x9195)>=14:
        branch='stale';result=reference=0;period=-1
        flags|=4
    else:
        branch='history';flags&=~4
        values=samples(g); idx=r(g,0x91B4)
        total=0; kept=0; kept_sum=0
        threshold=signed(r(g,0x9238,4),32)
        for i in range(18):
            total=signed(total+values[(idx-i)%18],32)
            if total<threshold or kept<5:
                kept+=1;kept_sum=total
        result,period=normalized(total,18)
        reference=result if r(g,0x92C6)&16 else normalized(kept_sum,kept)[0]
    return dict(branch=branch, result=result, reference=reference, period=period, flags=flags)


class Observed(SHRotate):
    """Read-only observation after original gate producers, never skip opcodes."""
    def instruction(self, pc):
        if pc == 0x20AAC:
            self.gate_state = (dict(self.ram), list(self.r))
        return super().instruction(pc)


def main():
    assert hashlib.sha256(TCU).hexdigest() == '8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    assert TCU[0x77444:0x77446] == bytes([18, 3])
    assert TCU[0x76E46:0x76E49] == bytes([14, 37, 5])
    assert int.from_bytes(TCU[0x76E44:0x76E46], 'big') == 360
    assert [int.from_bytes(TCU[a:a+n], 'big') for a,n in [(0x76E30,2),(0x76E34,4),(0x76E38,2),(0x76E3A,2),(0x76E3C,1),(0x76E3E,2),(0x76E40,4),(0x76E4E,2),(0x76E50,2),(0x76E52,2),(0x76E54,1)]] == [7680,91643,538,128,244,2560,91643,998,128,1280,7]
    t = SHRotate(TCU)
    t.run(0x20658)
    assert samples(t) == [RESET]*18 and r(t, 0x91B4) == 0
    assert all(r(t,a) == 255 for a in [0x810D,0x8196,0x9195])
    assert r(t,0x9198,4) == r(t,0x919C,4) == 0xFFFFFFFF

    ingestion = 0
    for old, incoming, flags, kind, axis in itertools.product(
            [1000,6000], [0,499,500,2101,2102,10000,RESET+1,0xFFFFFFFF],
            [0,2,4,8,10], [0,1], [7679,7680]):
        seed(t,[old]*18,17)
        for a,v,n in [(0x88F8,incoming,4),(0x91A6,flags,1),(0x8080,kind,1),
                      (0x80E8,axis,2),(0x810D,7,1),(0x91AA,2,1),(0x91AC,321,2)]:
            w(t,a,v,n)
        t.run(0x20678)
        assert r(t,0x9195) == 7
        if kind == 0 and axis >= 7680 and flags & 4:
            assert samples(t) == [old]*18 and r(t,0x91B4) == 17
            assert r(t,0x810D) == 7 and r(t,0x91AC,2) == 321
            assert r(t,0x91AA) == 2 and r(t,0x91A6) == flags
        else:
            value = min(incoming,RESET)
            total = old*18
            expected_flags = flags & ~2 if flags & 2 and total <= 91643 else flags
            ratio = udiv(value*256,old)
            spike = total <= 91643 and (ratio > 538 or ratio < 128)
            if spike and not flags & 8:
                value = old
                expected_flags |= 8
            else:
                expected_flags &= ~8
            assert samples(t) == [value]+[old]*17
            assert r(t,0x91B4) == 0 and r(t,0x91A6) == expected_flags
            assert r(t,0x810D) == r(t,0x91AA) == r(t,0x91AC,2) == 0
        ingestion += 1

    sums = 0
    values = [i*1001-500 for i in range(18)]
    for head, angle in itertools.product(range(18), [-360,0,19,20,60,180,359,360,720]):
        seed(t,values,head)
        expected = signed(sum(values[(head-i)%18] for i in range(max(0,div(angle*18,360)))),32)
        t.macl=0x87654321
        assert signed(t.run(0x207DE,angle),32) == expected and t.macl==0x87654321
        sums += 1

    timestamps=0
    for previous,delta,counter in itertools.product([0,1,0xFFFFFFF0],
            [0,1,9,10,12160,RESET*10+1,0xFFFFFFFF],[0,65534,65535]):
        seed(t,[RESET]*18,17)
        for a,v,n in [(0x88FC,previous,4),(0x91A6,0,1),(0x8080,1,1),
                      (0x810D,7,1),(0x8900,123,2)]:w(t,a,v,n)
        for a in [0x88F0,0x88F2,0x88F4]:w(t,a,counter,2)
        current=(previous+delta)&0xFFFFFFFF
        t.run(0x179A8,current,limit=100000)
        assert r(t,0x88FC,4)==current and r(t,0x88F8,4)==delta//10
        assert samples(t)==[min(RESET,delta//10)]+[RESET]*17
        assert r(t,0x8900,2)==0 and r(t,0x9195)==7 and r(t,0x810D)==0
        assert all(r(t,a,2)==min(65535,counter+1) for a in [0x88F0,0x88F2,0x88F4])
        timestamps+=1

    raw_cases=0
    for age,prior in itertools.product([0,13,14,127,128,255],repeat=2):
        seed(t,[1000]*18)
        w(t,0x810D,age);w(t,0x9195,prior)
        assert t.run(0x20DF8,limit=100000)==(8533 if age<14 and prior<14 else 0)
        raw_cases+=1

    gate_cases = 0
    for period, elapsed, timer, flags, fault, recovery in itertools.product(
            [1000,6000], [0,2,3,65535], [0,243,244,255], [0,2,0xF8], [0,2], [0,1]):
        seed(t,[period]*18)
        for a,v,n in [(0x91AC,elapsed,2),(0x8158,timer,1),(0x91A6,flags,1),
                      (0x92C6,fault,1),(0xAC87,recovery,1),(0x9194,0xFE,1),
                      (0x809A,3000,2),(0x8080,1,1),(0x8081,1,1)]:
            w(t,a,v,n)
        held = period*18<=91643 and udiv(elapsed<<16,period>>2)>538
        expected_timer = timer if held else 0
        expected_flags = (flags|1) if held else (flags&~1)
        if expected_timer>=244:
            expected_flags |= 6
        expected_summary = 0xFE | bool(expected_flags&2 or fault&2 or recovery)
        t.run(0x20CBC,limit=100000)
        assert r(t,0x91A6)==expected_flags and r(t,0x8158)==expected_timer
        assert r(t,0x9194)==expected_summary
        assert samples(t)==([RESET]*18 if expected_timer>=244 else [period]*18)
        gate_cases += 1
    for axis,kind,index in itertools.product([2559,2560,32768],[0,1,255],[0,1]):
        seed(t,[6000]*18)
        for a,v,n in [(0x91A6,2,1),(0x809A,axis,2),(0x8080,kind,1),(0x8081,index,1),(0xAC87,0,1),(0x92C6,0,1)]:
            w(t,a,v,n)
        t.run(0x20CBC)
        expected=0 if signed(axis,16)<2560 and kind!=0 and index==0 else 2
        assert r(t,0x91A6)==expected and r(t,0x9194)&1==bool(expected)
        gate_cases+=1

    anomaly = 0
    # Full20FAC with inactive phase: saved sample/index update from measured input.
    for raw,old_delta,measured,counter,prior_flag,blocked in itertools.product(
            [1000,8000], [997,998], [0,1000,1200,10000], [0,6,7,254,255], [0,16], [0,1,16]):
        for a,v,n in [(0x91A2,raw,2),(0x91B8,raw+old_delta,2),(0x80EE,measured,2),
                      (0x91C6,counter,1),(0x91A6,prior_flag,1),(0x9194,blocked&1,1),
                      (0x92C6,blocked&16,1),(0x810C,0,1),(0x8080,1,1),(0x8081,3,1),(0x8088,0,1)]:
            w(t,a,v,n)
        for i in range(1,6): w(t,0x91B8+2*i,100+i,2)
        latch = bool(prior_flag)
        c=counter
        if old_delta>=998: latch,c=True,0
        diff=measured-raw
        c=0 if diff>=128 and diff>=div(measured*5,100) else min(255,c+1)
        if not blocked and c>=7: latch=False
        t.run(0x20FAC,limit=100000)
        assert r(t,0x91A6)==16*int(latch) and r(t,0x91C6)==c
        assert r(t,0x91C4,2)==measured and r(t,0x91C9)==3
        assert [r(t,0x91B8+2*i,2) for i in range(6)]==[101,102,103,104,105,raw]
        anomaly+=1

    # Branch oracle observes the gate producers' outputs before209B4 arithmetic.
    # Those gates are separately verified above, not mocked for this test.
    rng=random.Random(0x209B4)
    branch_counts={}
    differences=[]
    for case in range(900):
        t=Observed(TCU)
        entries=[rng.randrange(100,10000) for _ in range(18)]
        head=case%18
        seed(t,entries,head)
        for a,v,n in [(0x91A6,rng.choice([0,1,2,4,16]),1),(0x9194,0x80,1),
                      (0x92C6,rng.choice([0,0,0,2,16]),1),(0xAC87,case%7==0,1),
                      (0x91AC,rng.choice([0,0,0,20]),2),(0x8158,rng.choice([0,244]),1),
                      (0x809A,3000,2),(0x8080,rng.choice([0,1,255]),1),
                      (0x8081,case%7,1),(0x91C7,(case+1)%7,1),(0x91C9,3,1),
                      (0x810D,rng.choice([0,0,0,13,14,255]),1),(0x9195,0,1),
                      (0x810C,rng.choice([0,4,5,255]),1),(0x8196,rng.choice([0,9,10,255]),1),
                      (0x80EE,7000,2),(0x91A8,5000,2),(0x9238,rng.choice([0,10000,30000,72000,2147483647]),4),
                      (0x80EA,1234,2),(0x80EC,2345,2),(0x9198,56789,4),
                      (0x8088,2 if case%3==0 else 0,1)]: w(t,a,v,n)
        t.macl=0x12345678
        whole_caller=bool(case%2)
        actual=t.run(0x2086C if whole_caller else 0x209B4,limit=200000)
        if whole_caller: actual=r(t,0x80EA,2)
        memory,regs=t.gate_state
        g=SHRotate(TCU);g.ram=memory
        predicted=branch_model(g,regs)
        branch,result,reference,period,flags=[predicted[k] for k in ['branch','result','reference','period','flags']]
        assert actual==result and r(t,0x80EC,2)==reference,(case,branch,actual,result,r(t,0x80EC,2),reference)
        assert r(t,0x9198,4)==period&0xFFFFFFFF and r(t,0x91A6)==flags
        assert r(t,0x9194)&2==2*bool(flags&4) and t.macl==0x12345678
        branch_counts[branch]=branch_counts.get(branch,0)+1
        if reference!=result and len(differences)<4:
            differences.append({'case':case,'branch':branch,'returned':result,'reference80EC':reference})
    assert set(branch_counts)=={'fallback','hold','stale','history'} and differences

    # Both capture callbacks feed the complete source producers. No direct
    #80EA/80EC/80EE/9218/80D8 writes occur in these shift lifecycle fixtures.
    base=full_fixture()
    lifecycles=[];paired_checks=0
    for old,head in [(3,0),(3,15),(5,0)]:
        t=RetirementTCU();t.ram=dict(base.ram)
        t.run(0x20658);t.run(0x211C4)
        def acquire(reference_interval,measured_interval):
            w(t,0x810D,0);w(t,0x810C,0)
            t.run(0x179A8,(r(t,0x88FC,4)+reference_interval)&0xFFFFFFFF)
            t.run(0x17A58,(r(t,0x890C,4)+measured_interval)&0xFFFFFFFF)
            t.run(0x2124C,limit=100000)
            t.run(0x2086C,limit=200000)
            t.run(0x2117C)
        # Constant reference capture1216 produces7017 after settling. Normal
        # ring ingestion may reject an initial sharp change for one capture.
        initial=5890 if old==3 else 10660
        final=6490 if old==3 else 12790
        for _ in range(32): acquire(12160,initial)
        assert r(t,0x80EC,2)==r(t,0x80EA,2)==7017
        refs=[signed(r(t,0x9218+4*i,4),32) for i in range(7)]
        w(t,0x96C4,head);w(t,0x606F,old);t.run(0x48BC0)
        for a,v,n in [(0x8080,6,1),(0x8084,old-1,1),(0x92D0,4,1),(0xA93A,1,1),
                      (0x80F6,4224,2),(0x809C,20000,2)]:w(t,a,v,n)
        t.run(0x48C08,limit=1000000)
        record=r(t,0xA2BC,4)&65535;phase=0x95D4+15*head
        rows=[];last=None;numeric=[]
        for call in range(401):
            if call:
                t.run(0x11014)
                acquire(12160,initial if call<80 else final)
                t.run(0x30B9E)
                t.run(0x31524,2,limit=1000000)
                periodic(t)
            else:t.run(0x4C7AC);t.run(0x1FB8C)
            state=(r(t,phase+13),r(t,record),r(t,0x96C5))
            numeric.append(r(t,0x915A,2))
            if state!=last or call in [79,80,102,103,104]:
                rows.append({'call':call,'phase':state[0],'request':state[1],'active_count':state[2],
                             'source80EA':r(t,0x80EA,2),'source80EC':r(t,0x80EC,2),
                             'measured80EE':r(t,0x80EE,2),'error':signed(r(t,0x80D8,2),16),
                             'measurement_can_byte4':wire(t),**paired_snapshot(t)})
                paired_checks+=1;last=state
            if not state[2]:break
        assert call<400 and r(t,0x8088)==1 and r(t,0xA2BA)==0
        assert r(t,0x915A,2)==0x7FFF
        assert {group for index,group in t.acks if index==head}==set(GROUPS)
        if old==3:assert any(value not in [0,0x7FFF] for value in numeric)
        lifecycles.append({'old':old,'code':old+4,'head':head,'references':refs,
                           'retired_at':call,'numeric_requests':sorted(set(numeric)), 'checkpoints':rows})

    print(json.dumps({'scope':__doc__.strip(),'tcu_sha256':hashlib.sha256(TCU).hexdigest(),
                      'ingestion_cases':ingestion,'history_sum_cases':sums,'gate_cases':gate_cases,
                      'timestamp_cases':timestamps,'raw_age_cases':raw_cases,
                      'anomaly_cases':anomaly,'producer_branch_cases':branch_counts,
                      'different_reference_examples':differences,'full_caller_cases':450,
                      'both_capture_lifecycles':lifecycles,'paired_can216_ecu_checks':paired_checks},indent=2))


if __name__=='__main__': main()
