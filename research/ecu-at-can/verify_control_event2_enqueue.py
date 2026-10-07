"""Independent whole-RAM proof of event2 enqueue with nonempty/full queue3.

Original215C6/1826E/2BC8C/DAE8/F5A0 execute without skipped callees. Queue
count1/99/100 and tail0/99 are explicit states. Empty-queue task activation,
callback dispatch, native producer scheduling and physical traction remain separate.
OriginalF6A0 consumer is checked separately across all valid counts0..100.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write


def consumer_model(e,destination):
    """Independent stock queue3 F6A0 effects, including all five copied words."""
    want=application(e);queued=r(e,0x45DB);head=r(e,0x45DA)
    assert 0<=queued<=100 and 0<=head<100
    if queued:
        expected_write(want,0x45DA,(head+1)%100,1)
        expected_write(want,0x45DB,queued-1,1)
        for i in range(5):
            expected_write(want,destination-0xFFFF0000+i*4,r(e,0x49C4+head*20+i*4,4),4)
    return want,0 if queued else 3


def main():
    counts=dict(admitted=0,producer_limited=0,queue_full=0,tail_wrapped=0)
    for pending,queued,tail in itertools.product(range(256),[1,99,100],[0,99]):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=0xF0
        rng=random.Random(pending*1000+queued*10+tail)
        # Preserve the caller's unused three descriptor argument words too.
        for a in range(e.r[15]-160,e.r[15]):e.write(a,rng.randrange(256),1)
        for a in [0x6520,0x6524,0x6528,0x535C]:w(e,a,rng.randrange(1<<32),4)
        for a in range(0x49C4,0x49C4+2000):w(e,a,rng.randrange(256))
        w(e,0x652C,57);w(e,0x652D,pending)
        w(e,0x45D9,tail);w(e,0x45DA,37);w(e,0x45DB,queued)
        want=application(e);saved=e.r[8:16].copy();gbr=e.gbr
        if pending<10:
            expected_write(want,0x652D,pending+1,1)
            expected_write(want,0x6520,2,4)
            if queued<100:
                words=[0x2BCE6,2]+[e.read(e.r[15]-36+4*i,4) for i in range(2,5)]
                for i,value in enumerate(words):expected_write(want,0x49C4+tail*20+4*i,value,4)
                expected_write(want,0x45D9,(tail+1)%100,1)
                expected_write(want,0x45DB,queued+1,1)
                counts['admitted']+=1;counts['tail_wrapped']+=int(tail==99)
            else:counts['queue_full']+=1
        else:counts['producer_limited']+=1
        result=e.run(0x215C6,limit=20000)
        assert application(e)==want,(pending,queued,tail)
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        assert (0xF5A0 in e.visited)==(pending<10)
        assert 0x2BCE6 not in e.visited and 0x35E0 not in e.visited
        assert result==int(pending<10 and queued==100)
    consumed=empty=0
    for queued,head,mask in itertools.product(range(101),[0,99],[0,0x70,0xF0]):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=mask
        rng=random.Random(queued*1000+head*10+mask)
        for a in range(0x49C4,0x49C4+2000):w(e,a,rng.randrange(256))
        for a in range(0x45B8,0x45CC):w(e,a,rng.randrange(256))
        w(e,0x45D9,53);w(e,0x45DA,head);w(e,0x45DB,queued)
        want,expected_result=consumer_model(e,0xFFFF45B8)
        saved=e.r[8:16].copy();gbr=e.gbr
        if queued:
            consumed+=1
        else:empty+=1
        e.r[5]=0xFFFF45B8
        result=e.run(0xF6A0,3,limit=20000)
        assert application(e)==want,(queued,head,mask)
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==mask
        assert result==expected_result
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        cases=sum(counts[k] for k in ['admitted','producer_limited','queue_full']),counts=counts,
        consume_cases=consumed+empty,consumed=consumed,empty_rejections=empty,
        descriptor_words='Target,event2,three preserved unused caller-stack words; all five copied.')
    Path(__file__).with_name('control-event2-enqueue-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
