"""Whole-RAM oracle for mode0 scheduler queue initialization and priority3.

Original38C4,391A,3988 execute. Only task7 requests, up to six entries, with
wraparound; no overflow/other-priority/interrupt or physical cadence claim.
"""
import json,random
from pathlib import Path
from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import w,r
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent


def compare(e,want,entry,argument=0xFFFF12B0,expected_mask=None):
    sp=e.r[15];gbr=e.gbr;sr=e.sr&0xF0
    value=e.run(entry,argument)
    assert application(e)==want,(hex(entry),{hex(a):(want.get(a,0),application(e).get(a,0)) for a in set(want)|set(application(e)) if want.get(a,0)!=application(e).get(a,0)})
    assert e.r[15]==sp and e.gbr==gbr and e.sr&0xF0==(sr if expected_mask is None else expected_mask)
    return value


def main():
    counts=dict(initialize=0,enqueue=0,consume=0)
    for seed in range(32):
        e=TaskDispatch();e.sr=0xF0;rng=random.Random(seed)
        for a in range(0x11A0,0x1300):w(e,a,rng.randrange(256))
        w(e,0x12B1,0);w(e,0x12C0,0xB0,4)
        want=application(e)
        for a,v,n in [(0x12B0,255,1),(0x12B6,65535,2),(0x12D0,0x4204,4),(0x12D4,0xFFFF1240,4)]:expected_write(want,a,v,n)
        for a in range(0x12E0,0x12F0):expected_write(want,a,0,1)
        for a in range(0x129A,0x12AB,4):expected_write(want,a,65535,2)
        compare(e,want,0x38C4);counts['initialize']+=1
        # Four passes: drain single request, fill/drain all six, then retain
        # one while wrapping tail with four further enqueue/dequeue pairs.
        operations=['enqueue','consume']+['enqueue']*6+['consume']*5
        operations+=['enqueue','consume']*4+['consume']
        queue=[];head=tail=None
        for operation in operations:
            want=application(e)
            if operation=='enqueue':
                first=not queue
                if first:
                    head=tail=32
                    for a,v,n in [(0x12A6,head,2),(0x12A8,tail,2),(0x12E0,8,1),(0x12B0,3,1),(0x12B6,7,2)]:expected_write(want,a,v,n)
                else:
                    tail=32 if tail==37 else tail+1;expected_write(want,0x12A8,tail,2)
                expected_write(want,0x1240+2*tail,7,2);queue.append(7)
                e.r[5]=7;e.r[6]=3
                assert compare(e,want,0x391A)==int(first)
                counts['enqueue']+=1
            else:
                assert queue;queue.pop(0)
                if not queue:
                    for a,v,n in [(0x12A6,65535,2),(0x12E0,0,1),(0x12B0,255,1),(0x12B6,65535,2)]:expected_write(want,a,v,n)
                else:
                    head=32 if head==37 else head+1;expected_write(want,0x12A6,head,2)
                    expected_write(want,0x12B6,7,2)
                e.r[5]=3
                assert compare(e,want,0x3988,expected_mask=0xB0 if not queue else None)==1
                counts['consume']+=1
        assert not queue and r(e,0x12B6,2)==65535
    result=dict(scope=__doc__,status='PASS',counts=counts)
    (ROOT/'control-task-queue-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
