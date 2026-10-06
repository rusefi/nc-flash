"""CAN calculation -> candidate throttle angle -> outgoing word buffer.

Physical naming corroborated by saved romdrop XML, not an actuator bench test.
Original bodies, stock ROM, explicit calls and synthetic protected RAM records.
"""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from sh_control_float import SHControlFloat
from verify_traction_flags import ECU, TCU, f, rf, w, r
from verify_model_sources import rounded as q, number
from verify_numeric_arbitration import paired
from verify_control_conversion import publish


def protected(e, address, value):
    f(e, 0xBFF0, value)
    e.fr[4] = r(e, 0xBFF0, 4)
    e.run(0x15522, 0xFFFF0000+address)
    assert rf(e, address) == value
    checksum(e, address)


def checksum(e, address):
    bits = r(e, address, 4)
    want = ~((bits >> 16)+(bits & 65535)) & 65535
    assert r(e, address+4, 2) == r(e, address+6, 2) == want


def setup():
    e = SHControlFloat(ECU)
    e.sr = 0xF0
    for a,v in [(0x2114, 10.5), (0x211C, 11), (0x2124, 100), (0x212C, 12)]:
        protected(e, a, v)
    return e


def local_consumers(e):
    value, flag, old = rf(e, 0x72FC), r(e, 0xA3A4), r(e, 0x7344)
    e.run(0x39B04)
    want = number(0xBACB0) if flag == 1 else max(0, min(number(0x39CA8), value))
    assert rf(e, 0x6CD4) == want
    checksum(e, 0x6CD4)
    e.run(0x4268E)
    lo,hi = q(number(0xBB254)-number(0xBB258)),number(0xBB254)
    assert r(e, 0x7344) == (0 if value > hi else 1 if value <= lo else old)


def angle(e):
    want = max(0, min(number(0xBAEA4), q(q(rf(e, 0x72FC)+rf(e, 0x6D00))*number(0xBACA8))))
    e.run(0x255C8)
    assert rf(e, 0x569C) == want
    return want


def selected(e):
    closed, cap = rf(e, 0x2114), rf(e, 0x2124)
    if r(e, 0x566C) == 1:
        v, branch = q(rf(e, 0x565C)+closed), '566c'
    elif r(e, 0x566E) == 1:
        v, branch = rf(e, 0x5520), '566e'
    elif r(e, 0x5670) == 1:
        v, branch = q(rf(e, 0x5620)+closed), '5670'
    elif r(e, 0x5672) == 1:
        v, branch = rf(e, 0x5650), '5672'
    else:
        v, branch = q(rf(e, 0x569C)+closed), 'normal'
    want = 0 if v <= 0 else cap if v >= cap else v
    e.run(0x25682)
    assert rf(e, 0x56A0) == want, (branch, rf(e, 0x56A0), want)
    checksum(e, 0x56A0)
    return branch


def pack(e):
    unit = number(0x22750)
    def quantize(v, scale=unit):
        return max(0, min(65535, int(q(q(v/scale)+Fraction(1,2)))))
    numeric = {4:quantize(rf(e,0x56A0)), 6:quantize(rf(e,0x56A0)),
               8:quantize(rf(e,0x2114)),10:quantize(rf(e,0x211C)),
               12:quantize(rf(e,0x212C)),14:quantize(rf(e,0x6DB4),number(0x22780)),
               20:r(e,0x5588,2),22:r(e,0x558A,2)}
    disabled = r(e,0x9462) != 0
    aggregate = int(r(e,0x522A)==1 or r(e,0x5324)==1)
    flags17 = sum(int(r(e,a)==1)<<i for i,a in enumerate(
        [0x722A,0x5676,0x5677,0x6646,0x522A,0x2138,0x566E,0x567E]))
    flags18 = int(r(e,0x6645)==1)
    flags18 |= int(not disabled and r(e,0x5678)==1)<<1
    flags18 |= int(not disabled and not r(e,0x562A) and not r(e,0x562F) and r(e,0x5679)==1)<<2
    flags18 |= aggregate<<3
    before = [r(e,0x5592+i) for i in [0,1,2,3,*range(24,38)]]
    high = r(e,0x55A4) & 0xF0
    e.run(0x2256C)
    assert all(r(e,0x5592+i,2)==v for i,v in numeric.items())
    assert r(e,0x55A2)==(0 if disabled else r(e,0x5640))
    assert r(e,0x55A3)==flags17 and r(e,0x55A4)==high|flags18
    assert r(e,0x55A5)==r(e,0x5586) and r(e,0x5530)==aggregate
    assert [r(e,0x5592+i) for i in [0,1,2,3,*range(24,38)]]==before
    # Execute actual C1F6 per-word writer, same19 words as static224DE loop.
    # Admission, startC00A, serial hardware and remote recipient are not modeled.
    for i in range(19):
        e.r[5] = r(e,0x5592+2*i,2)
        e.run(0xC1F6,i)
    payload=bytes(r(e,0x5592+i) for i in range(38))
    assert payload==bytes(r(e,0x437A+i) for i in range(38))
    return numeric[4]


def main():
    assert ECU[0xBAEA0]==1 and ECU[0xBB20C]==ECU[0xBACBE]==0
    local=0
    for value,flag,old in itertools.product([-20,0,Fraction(1,4),Fraction(3,8),Fraction(1,2),Fraction(5,8),40,100,120],[0,1,2],[0,1,2]):
        e=setup();f(e,0x72FC,value);w(e,0xA3A4,flag);w(e,0x7344,old)
        local_consumers(e);local+=1
    angles=0
    for value,offset,raw in itertools.product([-100,0,Fraction(1,4),40,100,200],[-20,0,20],[0,512,65535]):
        e=setup();f(e,0x72FC,value);f(e,0x6D00,offset);w(e,0x6A54,raw,2)
        angle(e);angles+=1
    selection=0
    for flags,closed,cap in itertools.product(itertools.product([0,1,2],repeat=4),[-10,10.5],[20,100]):
        e=setup();protected(e,0x2114,closed);protected(e,0x2124,cap)
        for a,v in [(0x569C,40),(0x565C,5),(0x5520,30),(0x5620,-20),(0x5650,80)]:f(e,a,v)
        for a,v in zip([0x566C,0x566E,0x5670,0x5672],flags):w(e,a,v)
        selected(e);selection+=1
    packing=0
    for mask,disabled in itertools.product(range(256),[0,1,2]):
        e=setup();protected(e,0x56A0,Fraction(mask,4));f(e,0x6DB4,2000+mask)
        for i,a in enumerate([0x722A,0x5676,0x5677,0x6646,0x522A,0x2138,0x566E,0x567E]):w(e,a,(mask>>i)&1)
        for i,a in enumerate([0x6645,0x5678,0x5679,0x562A,0x562F,0x5324]):w(e,a,(mask>>i)&1)
        #2138 uses15146 checksum-protected byte reader: valid value/complement.
        w(e,0x2139,255-r(e,0x2138))
        w(e,0x9462,disabled);w(e,0x5640,0xA5);w(e,0x55A4,0xF0)
        w(e,0x5586,0x7A);w(e,0x5588,0x1234,2);w(e,0x558A,0xABCD,2)
        pack(e);packing+=1
    # Same ECU retained across traction activation, local substitution, overrides
    # and return. Each step rebuilds actualTCU216/218 then follows originalcalls.
    history=[]
    e=setup()
    for a,v in [(0x6DC4,100),(0x6D40,20),(0x71D8,3),(0x71D0,4),(0x71C4,32),
                (0x7154,Fraction(1,2)),(0x6DB4,2000),(0x7E0C,40),(0x72F8,50),(0x6D00,0)]:f(e,a,v)
    for active,alternate,override in [(0,0,0),(1,0,0),(1,1,0),(1,0,1),(1,0,2),(0,0,0)]:
        _,e=paired(3200,1600,10040,10060,active,e=e)
        w(e,0x718C,active)
        e.run(0xA477E,limit=100000)
        # Earlier verifier independentlymodels the map stage; here all producer
        # outputs remain original, and checks start at publication/downstream.
        publish(e,alternate)
        local_consumers(e);angle(e)
        w(e,0x566E,override);f(e,0x5520,30)
        branch=selected(e);word=pack(e)
        history.append(dict(active=active,substitute=alternate,override=override,
           selected=float(rf(e,0x72FC)),angle=float(rf(e,0x569C)),
           branch=branch,final=float(rf(e,0x56A0)),outgoing_word=word))
    source=Path(__file__).with_name('sources')/'lffeee.xml'
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
       definition_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),local_cases=local,
       angle_cases=angles,selection_cases=selection,packing_cases=packing,history=history,
       limits='Explicit call scheduling and synthetic local/protected records. Definition-supported throttle candidate; no serial transfer, remote processor, pins or physical actuation proof.'),indent=2))


if __name__=='__main__':main()
