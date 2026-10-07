"""Original raw-input enable/first qualifier and selective-acquisition integration.

Finite normal/zero binary32 inputs; explicit task ordering. No board identity,
real time, analog conversion, remote DSC/roof controller or physical proof.
"""
import copy
import hashlib
import itertools
import json
import random
from fractions import Fraction
from pathlib import Path

import verify_control_raw_provenance as second
import verify_control_raw_inputs as raw
import verify_control_acquisition_schedule as schedule
from verify_control_contributions import ECU,w,r,f,rf,q,number,run
from verify_spark_interaction import GATES

ROOT=Path(__file__).resolve().parent
LOW=int.from_bytes(ECU[0xE02BE:0xE02C0],'big')
HIGH=int.from_bytes(ECU[0xE02C0:0xE02C2],'big')
LONG,SHORT=ECU[0xE02BC:0xE02BE]


def enable(e):
    value=rf(e,0x6CB4); want=raw.application(e)
    raw.expected_float(want,0x9108,value)
    raw.expected_write(want,0x914B,int(number(0xE0CEC)<value<number(0xE0CF0)),1)
    second.compare(e,0x74DF8,want)


def qualify(e):
    want=raw.application(e);value=r(e,0x6C92,2);enabled=r(e,0x914B)==1
    for a,v in [(0x8EF9,int(value<LOW and enabled)),(0x8EFA,int(value>HIGH and enabled)),(0x8F00,0)]:
        raw.expected_write(want,a,v,1)
    if r(e,0x9462)==1:raw.expected_write(want,0x8EFF,0,1)
    elif LOW<=value<=HIGH:
        for a in [0x8EFF,0x8F00]:raw.expected_write(want,a,1,1)
    second.compare(e,0x6CD96,want)


def countdown(e):
    want=raw.application(e);reset=r(e,0x9462)==1 or r(e,0x8F00)==1
    for i in range(4):
        value=r(e,0x8EF4+i)
        if reset:value=LONG if i<2 else SHORT
        elif r(e,0x8EF9+i%2)==1:value=max(0,value-1)
        raw.expected_write(want,0x8EF4+i,value,1)
    second.compare(e,0x6CE24,want)


def latch(e):
    want=raw.application(e)
    if r(e,0x9462)==1 or r(e,0x8F00)==1:
        for a in list(range(0x8EFB,0x8EFF))+[0x8EF8]:raw.expected_write(want,a,0,1)
    else:
        values=[1 if r(e,0x8EF4+i)==0 else r(e,0x8EFB+i) for i in range(4)]
        for i,v in enumerate(values):raw.expected_write(want,0x8EFB+i,v,1)
        if values[2]==1 or values[3]==1:
            raw.expected_write(want,0x8EF8,1,1);raw.expected_write(want,0x8EFF,0,1)
    second.compare(e,0x6CF06,want)


def initialize(e):
    expected=copy.deepcopy(e);qualify(expected)
    for i in range(4):w(expected,0x8EF4+i,LONG if i<2 else SHORT)
    latch(expected);second.compare(e,0x6CD70,raw.application(expected))


def slice_check(e,start,stop,operations):
    expected=copy.deepcopy(e)
    for op in operations:op(expected)
    sp,mask=e.r[15],e.sr&0xF0
    schedule.execute_slice(e,start,stop)
    assert e.r[15]==sp and e.sr&0xF0==mask
    assert raw.application(e)==raw.application(expected)


def first_caller(e):slice_check(e,0x1B166,0x1B178,[qualify,countdown,latch])


def scales_caller(e):
    expected=copy.deepcopy(e)
    for channel in second.CHANNELS:second.scale(expected,channel)
    sp,mask=e.r[15],e.sr&0xF0
    schedule.execute_slice(e,0xE514,0xE520)
    assert e.r[15]==sp and e.sr&0xF0==mask
    assert raw.application(e)==raw.application(expected)


def admission(e):
    want=raw.application(e)
    # All other admission predicates remain explicit independent fixtures.
    admitted=all(r(e,a)==v for a,v in GATES.items())
    raw.expected_write(want,0x6E2F,int(admitted),1)
    second.compare(e,0x3AEEC,want)


def direct():
    counts=dict(enable=0,qualify=0,countdown=0,latch=0,initialize=0,adc_enable=0)
    for value,old in itertools.product([-1,0,8-Fraction(1,2097152),8,8+Fraction(1,1048576),20,
            200-Fraction(1,65536),200,200+Fraction(1,65536),65536],[0,1,2,255]):
        e=raw.setup();f(e,0x6CB4,value);w(e,0x914B,old);enable(e);counts['enable']+=1
    for value,enabled,mode in itertools.product(list(range(1024))+[65535], [0,1,2,255],[0,1,2,255]):
        e=raw.setup();w(e,0x6C92,value,2);w(e,0x914B,enabled);w(e,0x9462,mode)
        w(e,0x8EFF,255);w(e,0x8F00,255);qualify(e);counts['qualify']+=1
    rng=random.Random(0x6CE24)
    for _ in range(2048):
        e=raw.setup()
        for a in [0x9462,0x8F00,0x8EF9,0x8EFA]:w(e,a,rng.choice([0,1,2,255]))
        for a in range(0x8EF4,0x8EF8):w(e,a,rng.choice([0,1,2,3,49,50,127,128,255]))
        for a in [0x8EF8]+list(range(0x8EFB,0x8F00)):w(e,a,rng.choice([0,1,2,255]))
        countdown(e);latch(e);counts['countdown']+=1;counts['latch']+=1
    for value,mode in itertools.product([0,LOW,HIGH,1023,65535],[0,1,2,255]):
        e=raw.setup()
        for a in range(0x8EF4,0x8F01):w(e,a,255)
        w(e,0x6C92,value,2);w(e,0x9462,mode);w(e,0x914B,1);initialize(e);counts['initialize']+=1
    e=second.acquisition.setup()
    for count in range(1024):
        w(e,0x400A,count<<6,2);second.acquisition.scale(e)
        second.acquisition.publish(e,True);enable(e)
        assert r(e,0x914B)==int(count>=410)
        counts['adc_enable']+=1
    return counts


def retained():
    e=schedule.setup();rows=[]
    for a,v in GATES.items():w(e,a,v)
    w(e,0x6C92,500,2);w(e,0x6CAE,128)
    initialize(e);second.initialize(e);f(e,0x67E0,7);f(e,0x6D5C,23)
    for call in range(1,321):
        # Explicit sample changes expose third-bank retention and publication phase.
        adc1=300 if 41<=call<=64 or 145<=call<=170 else 600
        adc28=0 if call<=80 else LOW if call<=112 else 1023 if call<=224 else HIGH
        adc29=512 if call<=112 else 1023 if call<=224 else second.HIGH*4
        values=[0]*32;values[1]=adc1<<6;values[28]=adc28<<6;values[29]=adc29<<6
        schedule.schedule(e,values,True)
        second.acquisition.decode(e)
        second.acquisition.publish(e,call==1)
        slice_check(e,0x1B14E,0x1B154,[enable])
        scales_caller(e);first_caller(e);second.caller(e)
        raw.first(e);raw.second(e);raw.target.source(e);admission(e)
        rows.append(dict(call=call,supplied=[adc1,adc28,adc29],
            copied=[schedule.REGISTERS.index(a) for a in e.adc_reads],
            count28=r(e,0x6C92,2),byte29=r(e,0x6CAE),source6cb4=float(rf(e,0x6CB4)),
            enabled=r(e,0x914B),first_counters=[r(e,0x8EF4+i) for i in range(4)],
            second_counters=[r(e,0x8F2C+i) for i in range(4)],
            fallback=[r(e,0x8EF8),r(e,0x8F30)],spark_admitted=r(e,0x6E2F),
            published=[float(rf(e,0x6D20)),float(rf(e,0x6D40))],target=float(rf(e,0x67E4))))
    by={row['call']:row for row in rows}
    assert by[5]['fallback']==[1,1] and by[5]['spark_admitted']==0
    assert by[17]['fallback']==[1,0] and by[17]['byte29']==128
    assert by[80]['count28']==0 and by[81]['count28']==LOW
    assert by[112]['count28']==LOW and by[113]['count28']==1023
    assert by[224]['count28']==1023 and by[225]['count28']==HIGH
    assert by[40]['enabled']==1 and by[41]['enabled']==0
    assert by[64]['enabled']==0 and by[65]['enabled']==1
    assert by[81]['fallback']==[0,0] and by[81]['spark_admitted']==1
    assert by[115]['fallback']==[1,1] and by[115]['spark_admitted']==0
    assert by[225]['fallback']==[0,0] and by[225]['spark_admitted']==1
    assert by[145]['first_counters']==by[170]['first_counters']
    assert by[170]['fallback']==[1,1]  # Disabling qualification does not clear latched faults.
    return rows


def main():
    counts=direct();print(counts,flush=True);rows=retained()
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),counts=counts,
        calibration=dict(first_low=LOW,first_high=HIGH,long=LONG,short=SHORT,
                         enable_low=float(number(0xE0CEC)),enable_high=float(number(0xE0CF0))),
        retained_cycles=len(rows),retained=rows,
        limits='Explicit cross-task call order; intervening1B154/15A/160/178 routines omitted. Real task cadence, ADC conversion/interrupts, board identities, CAN211/21A sender/units, DSC/roof internals and physical integration unproved.')
    (ROOT/'control-raw-enable-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Retained',len(rows),flush=True)


if __name__=='__main__':main()
