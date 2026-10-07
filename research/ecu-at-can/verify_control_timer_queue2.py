"""Independent original FBE8 producer and F6A0 consumer for stock queue2.

All valid counts0..30, endpoint ring indices and masks10/70/F0. Initialized
empty-queue task3 admission executes all callees; nonzero masks exclude inline
preemption. No scheduler/callback-body or hardware interrupt timing claim.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write
from verify_control_event2_activation import difference


def consumer_model(e,destination):
    want=application(e);queued=r(e,0x45D8);head=r(e,0x45D7)
    assert 0<=queued<=30 and 0<=head<30
    if queued:
        expected_write(want,0x45D7,(head+1)%30,1)
        expected_write(want,0x45D8,queued-1,1)
        for i in range(5):
            expected_write(want,destination-0xFFFF0000+i*4,r(e,0x476C+head*20+i*4,4),4)
    return want,0 if queued else 3


def main():
    counts=dict(producer=0,empty_admission=0,full_rejection=0,tail_wrap=0,consumer=0,empty_consumer=0)
    assert ECU[0x1136C:0x11374].hex()=='ffff476c00031e00'
    assert ECU[0x11344:0x1134C].hex()=='000200000000e5fc'
    assert ECU[0x4102]==2
    for seed,queued,tail,mask in itertools.product(range(8),range(31),[0,29],[0x10,0x70,0xF0]):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=mask;rng=random.Random(seed*10000+queued*100+tail)
        for a in range(e.r[15]-160,e.r[15]):e.write(a,rng.randrange(256),1)
        w(e,0x12B1,0);w(e,0x12C0,0xB0,4)
        e.run(0x38C4,0xFFFF12B0);e.run(0x3F40,0xFFFF12B0)
        for a in range(0x476C,0x49C4):w(e,a,rng.randrange(256))
        w(e,0x45D6,tail);w(e,0x45D7,tail);w(e,0x45D8,queued)
        want=application(e);saved=e.r[8:16].copy();gbr=e.gbr
        if queued<30:
            if queued==0:
                for a,value,size in [(0x11C3,1,1),(0x12A2,22,2),(0x12A4,22,2),
                    (0x12E0,4,1),(0x12B0,2,1),(0x12B6,3,2),(0x126C,3,2)]:
                    expected_write(want,a,value,size)
                counts['empty_admission']+=1
            words=[0xE5FC]+[e.read(e.r[15]-44+4*i,4) for i in range(1,5)]
            for i,value in enumerate(words):expected_write(want,0x476C+tail*20+4*i,value,4)
            expected_write(want,0x45D6,(tail+1)%30,1)
            expected_write(want,0x45D8,queued+1,1)
            counts['tail_wrap']+=int(tail==29)
        else:counts['full_rejection']+=1
        assert e.run(0xFBE8,0x5A000000+seed,limit=20000)==int(queued==30)
        assert application(e)==want,(seed,queued,tail,mask,difference(e,want))
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==mask
        assert not e.rte_transfers and 0xE5FC not in e.visited
        assert (0x35E0 in e.visited)==(queued==0)
        counts['producer']+=1
    for queued,head,mask in itertools.product(range(31),[0,29],[0x10,0x70,0xF0]):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=mask;rng=random.Random(queued*100+head)
        for a in range(0x476C,0x49C4):w(e,a,rng.randrange(256))
        for a in range(0x45A4,0x45B8):w(e,a,rng.randrange(256))
        w(e,0x45D6,17);w(e,0x45D7,head);w(e,0x45D8,queued)
        want,result=consumer_model(e,0xFFFF45A4);saved=e.r[8:16].copy();gbr=e.gbr
        e.r[5]=0xFFFF45A4
        assert e.run(0xF6A0,2,limit=20000)==result
        assert application(e)==want,(queued,head,mask,difference(e,want))
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==mask
        counts['consumer']+=1;counts['empty_consumer']+=int(queued==0)
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),counts=counts,
        descriptor='1136C: baseFFFF476C,task3,capacity30; row11344 selector2/zeroargs/E5FC',
        copied_words='Target E5FC plus four unused original caller-stack words; FBE8 argument is not copied.')
    Path(__file__).with_name('control-timer-queue2-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
