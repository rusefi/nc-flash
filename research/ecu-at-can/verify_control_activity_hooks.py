"""Independent original mode-flag edge callbacks and flag-producer checks.

Descriptor callbacks execute; no physical pin, event cadence or persistence claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent


def checked(e,entry,want):
    saved=e.r[8:16].copy();gbr=e.gbr
    e.run(entry)
    assert application(e)==want,(hex(entry),{hex(k):v for k,v in application(e).items() if want.get(k)!=v},{hex(k):v for k,v in want.items() if application(e).get(k)!=v})
    assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0


def main():
    counts=dict(mode_selection=0,flag_production=0,edge_callbacks=0,state_zero=0,state_six=0,retained_state_calls=0)
    for hold,stop,enabled,bits in itertools.product([0,1,2],[0,1,2],[0,1,255],[0,127,128,255]):
        e=Hooks()
        for a,v in [(0x735C,hold),(0x6604,stop),(0x6536,enabled),(0x73C4,bits)]:w(e,a,v)
        mode=128 if hold==0 or stop==1 else 64 if enabled==0 or bits&128 else 32
        want=application(e);expected_write(want,0x735A,mode,1);checked(e,0x42B36,want)
        counts['mode_selection']+=1
    for mode,hold,a,b,c in itertools.product(range(256),[0,1,2],[0,1,2],[0,1,2],[0,1,2]):
        e=Hooks()
        for address,value in [(0x735A,mode),(0x735C,hold),(0x82A8,a),(0xA433,b),(0x9149,c)]:w(e,address,value)
        flag=int(bool(mode&0x60) or hold==1 or bool(mode&0x80) and 1 in [a,b,c])
        want=application(e);expected_write(want,0x735B,flag,1);checked(e,0x42BCC,want)
        counts['flag_production']+=1
    for entry,current,old,counter in itertools.product([0x42C68,0x42CBE],range(256),[0,1,2,255],[0,255]):
        e=Hooks();w(e,0x735B,current);w(e,0x735E,old)
        w(e,0x660E,counter);w(e,0x660F,255-counter)
        pin=0xA55A if old&1 else 0;e.registers[0xFFFFF74E]=pin
        want=application(e);expected_write(want,0x735E,current,1)
        index=7 if old==0 and current==1 else 8 if old==1 and current==0 else None
        if index is not None:
            address=0x660E if index==7 else 0x660F
            expected_write(want,address,(r(e,address)+1)%256,1)
        checked(e,entry,want)
        assert [(d['bank'],d['index'],d['selector'],d['words'],d['target']) for d in e.descriptors]==([] if index is None else [(0,index,65535,0,0x1616C if index==7 else 0x16178)])
        assert e.registers[0xFFFFF74E]==(pin|8 if entry==0x42CBE and current==1 else pin)
        assert e.accesses==([('read',0xFFFFF74E,pin,2),('write',0xFFFFF74E,pin|8,2)] if entry==0x42CBE and current==1 else [])
        counts['edge_callbacks']+=1
    for a,b,c,d in itertools.product([0,1,255],repeat=4):
        e=Hooks()
        for address,value in zip([0x660E,0x660F,0x6610,0x6611],[a,b,c,d]):w(e,address,value)
        want=application(e);expected_write(want,0x99FC,1,1);expected_write(want,0x6610,(c+1)%256,1)
        checked(e,0x907F0,want)
        assert [(v['index'],v['target']) for v in e.descriptors]==[(9,0x16172)]
        counts['state_zero']+=1
    for a,b,c,d in itertools.product([0,1,127,128,255],[0,1,127,128,255],[0,255],[0,255]):
        e=Hooks();w(e,0x99FC,6);w(e,0x99FA,123,2)
        for address in [0x9A02,0x9A03,0x99FD,0x9A05]:w(e,address,0xA5)
        for address,value in zip([0x660E,0x660F,0x6610,0x6611],[a,b,c,d]):w(e,address,value)
        want=application(e)
        expected_write(want,0x99FA,0,2)
        for address in [0x9A02,0x9A03,0x99FD,0x9A05]:expected_write(want,address,0,1)
        expected_write(want,0x99FC,12 if a<=b else 1,1)
        if a<=b:expected_write(want,0x6611,(d+1)%256,1)
        checked(e,0x907F0,want)
        assert [(v['index'],v['target']) for v in e.descriptors]==([(10,0x1617E)] if a<=b else [])
        counts['state_six']+=1
        e.descriptors.clear();checked(e,0x907F0,want)
        assert not e.descriptors
        counts['retained_state_calls']+=1
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,counts=counts,total=sum(counts.values()))
    (ROOT/'control-activity-hooks-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts)

if __name__=='__main__':main()
