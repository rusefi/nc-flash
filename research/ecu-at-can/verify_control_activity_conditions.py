"""Independent original activity thresholds, stock admission and second hold.

Finite normal/zero float samples; stock calibration and explicit RAM fixtures.
No physical units, controller identity or elapsed-time claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
from fractions import Fraction
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r,w,f,rf,number
from verify_control_raw_inputs import application,expected_write
from verify_rtz_float import reference,value

ROOT=Path(__file__).resolve().parent
ENTRIES=[0x6F2C8,0x6F34C,0x74ED2]
IDS=[0x2F,0x30,0x2D,0x2E]


def expected(e,entry):
    want=application(e)
    if entry==0x6F2C8:
        for source,dest,high,width in [(0x6D40,0x8FE0,0xE0870,0xE0874),(0x6D20,0x8FDF,0xE0868,0xE086C)]:
            sample=rf(e,source);upper=number(high);lower=value(reference(upper-number(width)))
            flag=1 if sample>=upper else 0 if sample<lower else r(e,dest)
            expected_write(want,dest,flag,1)
    elif entry==0x6F34C:
        ids=IDS+([] if ECU[0xE0861] else [0x1F,0x20,0x2A,0x2B])
        flag=int(bool(r(e,0x735A)&128) and r(e,0x8FE0)==1 and r(e,0x8FDF)==1 and all(r(e,0x9935+i)!=0xC0 for i in ids) and r(e,0x9125)==1)
        expected_write(want,0x8FD8,flag,1)
    elif entry==0x74ED2:
        active=bool(r(e,0x735A)&128);counter=min(65535,r(e,0x9158,2)+int(active))
        first=int.from_bytes(ECU[0xE0CBE:0xE0CC0],'big');second=int.from_bytes(ECU[0xE0CC0:0xE0CC2],'big')
        expected_write(want,0x9158,counter,2)
        if r(e,0x915E)==1:
            expected_write(want,0x2444,0x00FF,2);expected_write(want,0x915E,0,1)
        elif active and counter>=first:expected_write(want,0x2444,0x01FE,2)
        expected_write(want,0x915C,int(active and counter<min(65535,first+second)),1)
    else:raise AssertionError(entry)
    return want


class Conditions(Hooks):
    def __init__(self):
        super().__init__();self.status_queries=[]
    def instruction(self,pc):
        if pc==0x9037C:self.status_queries.append((self.r[4]&65535,self.r[5]&255))
        return super().instruction(pc)


def check(e,entry):
    want=expected(e,entry);saved=e.r[8:16].copy();gbr=e.gbr
    e.run(entry)
    assert application(e)==want,(hex(entry),application(e),want)
    assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0 and not e.accesses


def main():
    counts=dict(thresholds=0,admission=0,status=0,second_hold=0)
    bits=[]
    for threshold in [-782,-777]:
        b=reference(Fraction(threshold));bits.extend([b-1,b,b+1])
    bits.extend([0,reference(Fraction(-1000)),reference(Fraction(1000))])
    for a,b,old_a,old_b in itertools.product(bits,bits,[0,1,2,255],[0,1,2,255]):
        e=Conditions();w(e,0x6D40,a,4);w(e,0x6D20,b,4);w(e,0x8FE0,old_a);w(e,0x8FDF,old_b)
        check(e,0x6F2C8);counts['thresholds']+=1
    for mode,a,b,c in itertools.product(range(256),[0,1,2],[0,1,2],[0,1,2]):
        e=Conditions()
        for address,val in [(0x735A,mode),(0x8FE0,a),(0x8FDF,b),(0x9125,c)]:w(e,address,val)
        check(e,0x6F34C)
        assert e.status_queries==([(i,0) for i in IDS] if mode&128 and a==b==1 else [])
        counts['admission']+=1
    for index,status in itertools.product(IDS,range(256)):
        e=Conditions();w(e,0x9935+index,status);before=application(e);saved=e.r[8:16].copy();e.r[5]=0
        assert e.run(0x9037C,index)==int(status==0xC0)
        assert application(e)==before and e.r[8:16]==saved
        counts['status']+=1
        e=Conditions()
        for address,val in [(0x735A,128),(0x8FE0,1),(0x8FDF,1),(0x9125,1),(0x9935+index,status)]:w(e,address,val)
        check(e,0x6F34C)
        expected_ids=IDS[:IDS.index(index)+1] if status==0xC0 else IDS
        assert e.status_queries==[(i,0) for i in expected_ids]
        counts['admission']+=1
    for states in itertools.product([0,0xC0],repeat=8):
        e=Conditions()
        for a,v in [(0x735A,128),(0x8FE0,1),(0x8FDF,1),(0x9125,1)]:w(e,a,v)
        for i,v in zip(IDS+[0x1F,0x20,0x2A,0x2B],states):w(e,0x9935+i,v)
        check(e,0x6F34C);counts['admission']+=1
    for mode,reset,old,pair in itertools.product(range(256),[0,1,2,255],[0,1,2,3,4,65534,65535],[0x00FF,0x01FE,0xA55A,0x0000]):
        e=Conditions()
        for a,v,size in [(0x735A,mode,1),(0x915E,reset,1),(0x9158,old,2),(0x2444,pair,2)]:w(e,a,v,size)
        check(e,0x74ED2);counts['second_hold']+=1
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,counts=counts,total=sum(counts.values()),calibration=dict(threshold=-777,width=5,optional_status_gate=ECU[0xE0861],first_count=1,additional_count=2))
    (ROOT/'control-activity-conditions-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(counts)

if __name__=='__main__':main()
