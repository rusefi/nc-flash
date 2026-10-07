"""CAN215 byte6 through the original paired transition-input caller.

Original ECU encoder, TCU receive callback, selection/history and paired
caller execute. Source6CD4, summary92D5, scheduling and peripheral samples
remain fixtures; no physical units, sender sensor or complete task claim.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import random

from sh_exact_float import exact_bits
from sh_subset import signed
from verify_can215_feedback import sender, receive
from verify_tcu_comparison_input import (
    ECU, TCU, w, r, ObservedComparison, word_magnitude, ecu_payload,
    receive as receive201,
)
from verify_tcu_qualification_lifecycle import retained

HISTORY = [0x9346 + 2*i for i in range(4)]
WORDS = [0x880C, 0x809A, 0x933A, 0x933E, 0xA500, *HISTORY]
BYTES = [0x880E, 0x92D5, 0x938C, 0x82C4, 0x8198, 0x933D, 0x933C, 0x9344, 0xA502]
OUTPUT_WORDS = [a for a in WORDS if a != 0x880C]
OUTPUT_BYTES = [a for a in BYTES if a not in [0x880E, 0x92D5]]


def snap(t):
    return {**{a:r(t,a,2) for a in WORDS}, **{a:r(t,a) for a in BYTES}}


def selection(d):
    fault = bool(d[0x92D5] & 128)
    if fault and not d[0x938C] & 1:
        d[0x82C4] = 0
    d[0x938C] = (d[0x938C] & 254) | int(fault)
    # Both stock fault branches return25600, separated by timer threshold31.
    return 25600 if fault else min(25600, d[0x880C]*256//10)


def producer_model(d):
    value = selection(d)
    history = [d[0x809A], *[d[a] for a in HISTORY[:3]]]
    d.update(zip(HISTORY, history))
    d[0x809A] = d[0x933A] = value
    d[0xA500] = value*10//256
    d[0xA502] = 4 if d[0x92D5]&128 else (1 if d[0x880E]==2 else 2)
    bounds = [128*x for x in TCU[0x5CD1C:0x5CD29]]
    category = next((i for i,v in enumerate(bounds) if value<v),12)
    if category<signed(d[0x933D],8) and value>=signed(bounds[category]-640,16):
        category += 1
    d[0x933D] = category
    d[0x933C] = category//2 if category<10 else category-5
    short = value-signed(history[0],16)
    long = value-signed(history[3],16)
    if word_magnitude(short)>=25600:
        d[0x8198] = 0
        if word_magnitude(long)>=2560:
            d[0x9344] |= 1
    if word_magnitude(long)<2560 and d[0x8198]>=6:
        d[0x9344] &= 254
    d[0x933E] = 0 if d[0x9344]&1 else long&65535


def packet(primary, source, invalid=0, mode=0x80):
    e,_ = sender(primary,0,mode=mode)
    w(e,0x6CD4,exact_bits(source),4)
    w(e,0xA3A4,invalid)
    # Reexecute the complete producer and packer after supplying the real input.
    e.run(0x369D6);e.run(0x36A28)
    return bytes(r(e,0x6B50+i) for i in range(8))


class ObservedPair(ObservedComparison):
    def __init__(self):
        super().__init__()
        self.primary_expected = None
        self.primary_checks = 0
        self.primary_rows = []

    def instruction(self,pc):
        if pc==0x22F46:
            self.primary_expected = snap(self)
            producer_model(self.primary_expected)
        elif pc==0x230E4:
            for a in OUTPUT_WORDS+OUTPUT_BYTES:
                size = 1 if a in OUTPUT_BYTES else 2
                assert r(self,a,size)==self.primary_expected[a], (
                    hex(a),r(self,a,size),self.primary_expected[a])
            self.primary_checks += 1
            self.primary_expected = None
        result = super().instruction(pc)
        if pc==0x2399E and self.application_call in [0,1,99,100,109,110,111,113,114,130,162,163,170,171,173,174,320]:
            self.primary_rows.append(dict(call=self.application_call,
                raw=r(self,0x8F32),value=r(self,0x880C,2),validity=r(self,0x880E),
                primary=r(self,0x809A,2),change=signed(r(self,0x933E,2),16),
                flags=r(self,0x9344),timer815a=r(self,0x815A),
                limit=r(self,0x939E,2),live_input=r(self,0x80F8,2)))
        return result


def direct_cases():
    assert TCU[0x5C80E:0x5C812].hex()=='050a0000'
    assert TCU[0x5C59C:0x5C5A0].hex()=='010a0000'
    assert TCU[0x76DFA:0x76E02].hex()=='640002800a006400'
    assert TCU[0x76E0A:0x76E0E].hex()=='1fff6400'
    counts = dict(encoder=0,receive=0,selection=0,paired_producer=0)
    values = [Fraction(n,4) for n in [-4,-1,0,1,2,3,4,389,390,391,399,400,401,509,510,511,512,800]]
    for value,invalid,mode in itertools.product(values,[0,1,2,255],[0,0x40,0x80,0xC0]):
        payload = packet(25,value,invalid,mode)
        expected = 255 if invalid==1 else min(200,max(0,int(value*2+Fraction(1,2))))
        assert payload[6]==(0xA5 if mode==0 else expected)
        counts['encoder'] += 1
    t = ObservedPair()
    t.run(0x170D4)
    assert r(t,0x880C,2)==r(t,0x880E)==0
    for raw,old in itertools.product(range(256),[0,975,65535]):
        w(t,0x880C,old,2)
        receive(t,bytes.fromhex('0219021e0200')+bytes([raw,0]))
        assert r(t,0x880C,2)==(old if raw==255 else raw*5)
        assert r(t,0x880E)==(1 if raw==255 else 2)
        counts['receive'] += 1
    for flags,oldflag,timer,value in itertools.product(range(256),[0,0xA5],[0,30,31,127,128,255],[0,975,1000,1270,65535]):
        for a,v in [(0x92D5,flags),(0x938C,oldflag),(0x82C4,timer)]:w(t,a,v)
        w(t,0x880C,value,2)
        d=snap(t);expected=selection(d)
        assert t.run(0x23406)==expected
        assert r(t,0x938C)==d[0x938C] and r(t,0x82C4)==d[0x82C4]
        counts['selection'] += 1
    rng=random.Random(0x22F3C)
    for n in range(1800):
        for a in WORDS:w(t,a,rng.randrange(65536),2)
        for a in BYTES:w(t,a,rng.randrange(256))
        w(t,0x880C,rng.choice([0,5,35,70,975,1000,1270,65535]),2)
        w(t,0x92D5,rng.choice([0,8,128,136]))
        w(t,0x89B0,rng.choice([0,780,1000,1270]),2)
        w(t,0x8088,1);w(t,0x96C5,0)
        sp=t.r[15]
        t.run(0x22F3C,limit=1000000)
        assert t.r[15]==sp
        counts['paired_producer'] += 1
    assert t.primary_checks==t.comparison_checks==counts['paired_producer']
    return counts


def paired_lifecycle(change=False):
    t=ObservedPair();payload201=ecu_payload(78,78,0)
    packets={}
    def update(t,call):
        t.application_call=call
        if call==0:
            receive201(t,payload201)
            for i in range(7):w(t,0x8F0D+i,0)
        primary=100 if 100<=call<170 else 25
        source=60 if change and 110<=call<170 else Fraction(195,2)
        key=(primary,source)
        if key not in packets:packets[key]=packet(primary,source)
        receive(t,packets[key])
        w(t,0xA98C,1)
        t.run(0x516E6);t.run(0x216D8)
        t.run(0x1ADD0,limit=1000000)
        t.run(0x22F3C,limit=1000000)
    trace=retained(25,changes={100:100,170:25},t=t,comparison_update=update)
    assert t.primary_checks==t.comparison_checks==t.input_source_checks==321
    rows={x['call']:x for x in t.primary_rows}
    assert rows[0]['primary']==24960
    if change:
        assert rows[110]['primary']==15360 and rows[110]['change']==-9600
        assert rows[110]['timer815a']==0
        assert rows[114]['change']==0
        assert rows[170]['change']==9600 and rows[174]['change']==0
    return dict(changed_byte6=change,packets=[dict(primary=p,source=str(s),payload=b.hex(' '))
                for (p,s),b in packets.items()],primary_rows=t.primary_rows,
                primary_checks=t.primary_checks,comparison_checks=t.comparison_checks,
                source_checks=t.input_source_checks,trace=trace)


def main():
    counts=direct_cases();print('Direct cases:',counts,flush=True)
    profiles=[]
    for change in [False,True]:
        profiles.append(paired_lifecycle(change));print('Profile:',change,flush=True)
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                tcu_sha256=hashlib.sha256(TCU).hexdigest(),direct_cases=counts,
                total_direct_cases=sum(counts.values()),profiles=profiles)
    path='research/ecu-at-can/tcu-paired-input-verification.json'
    with open(path,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
