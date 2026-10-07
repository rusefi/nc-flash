"""Independent task-availability initialization and empty event2 queue admission.

Mode0..3 initialization and mask10/70/F0 admissions only. Nonzero masks keep
35E0 from inline context switching; separate retained dispatch executes tasks.
"""
import itertools
import json
import random
from pathlib import Path

from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write


def difference(e,want):
    actual=application(e)
    return {hex(a):[want.get(a,0),actual.get(a,0)] for a in set(want)|set(actual)
        if want.get(a,0)!=actual.get(a,0)}


def main():
    initialized=admitted=0
    for mode,seed in itertools.product(range(4),range(32)):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=0xF0;rng=random.Random(seed)
        for a in range(0x11A8,0x1240):w(e,a,rng.randrange(256))
        w(e,0x12B1,mode);want=application(e);saved=e.r[8:16].copy()
        # All19 stock mode-mask words are1; modes1..3 preserve descriptors.
        assert int.from_bytes(ECU[0x407C:0x407E],'big')==19
        for index in range(19):
            assert int.from_bytes(ECU[0x4080+4*index:0x4084+4*index],'big')==1
            if mode==0:
                entry=0x40D0+index*16
                address=int.from_bytes(ECU[entry+4:entry+8],'big')-0xFFFF0000
                for offset,value in [(0,0),(2,255),(3,ECU[entry+12])]:
                    expected_write(want,address+offset,value,1)
        e.run(0x3F40,0xFFFF12B0)
        assert application(e)==want,difference(e,want)
        assert e.r[8:16]==saved and e.sr&0xF0==0xF0
        initialized+=1
    for seed,mask,tail in itertools.product(range(32),[0x10,0x70,0xF0],[0,99]):
        e=TaskDispatch();e.r[15]=0xFFFED000;e.sr=mask;rng=random.Random(seed)
        for a in range(e.r[15]-160,e.r[15]):e.write(a,rng.randrange(256),1)
        w(e,0x12B1,0);w(e,0x12C0,0xB0,4)
        e.run(0x38C4,0xFFFF12B0);e.run(0x3F40,0xFFFF12B0)
        w(e,0x45D9,tail);w(e,0x45DA,tail);w(e,0x45DB,0)
        w(e,0x652D,seed%10);w(e,0x535C,rng.randrange(1<<32),4)
        want=application(e);saved=e.r[8:16].copy();gbr=e.gbr
        for a,value,size in [(0x652D,seed%10+1,1),(0x6520,2,4),(0x11CB,1,1),
                            (0x129E,2,2),(0x12A0,2,2),(0x12E0,2,1),
                            (0x12B0,1,1),(0x12B6,4,2),(0x1244,4,2),
                            (0x45D9,(tail+1)%100,1),(0x45DB,1,1)]:
            expected_write(want,a,value,size)
        words=[0x2BCE6,2]+[e.read(e.r[15]-36+4*i,4) for i in range(2,5)]
        for i,value in enumerate(words):expected_write(want,0x49C4+tail*20+i*4,value,4)
        assert e.run(0x215C6,limit=20000)==0
        assert application(e)==want,difference(e,want)
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==mask
        assert {0x35E0,0x391A,0xF5A0}.issubset(e.visited)
        assert not e.rte_transfers and 0x2BCE6 not in e.visited
        admitted+=1
    result=dict(status='PASS',scope=__doc__,initialization_cases=initialized,
        empty_queue_admissions=admitted,task_index=4,priority=1,stock_availability=2)
    Path(__file__).with_name('control-event2-activation-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
