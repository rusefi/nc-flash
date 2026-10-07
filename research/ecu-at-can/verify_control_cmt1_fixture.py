"""Independent bounded CMT1 latch/clear/reserved-access checks."""
import itertools,json
from pathlib import Path
from control_cmt1_fixture import Cmt1


def main():
    cases=0
    controls=[0,1,2,3,64,65,66,67]
    for old,flag,read_first,new,write_flag in itertools.product(controls,[False,True],[False,True],controls,[False,True]):
        c=Cmt1();c.values[0xFFFFF718]=old+128*flag
        if read_first:assert c.read(0xFFFFF718,2)==old+128*flag
        c.write(0xFFFFF718,new+128*write_flag,2)
        expected_flag=flag and not (read_first and not write_flag)
        assert c.values=={0xFFFFF710:0,0xFFFFF718:new+128*expected_flag,0xFFFFF71A:0,0xFFFFF71C:65535}
        assert c.read(0xFFFFF718,2)==new+128*expected_flag
        cases+=1
    for address in [0xFFFFF710,0xFFFFF71A,0xFFFFF71C]:
        for value in (range(4) if address==0xFFFFF710 else [0,1,2499,32768,65535]):
            c=Cmt1();before=c.values.copy();before[address]=value
            c.write(address,value,2);assert c.values==before and c.read(address,2)==value
            cases+=1
    rejected=0
    for address,size,value in [(0xFFFFF710,1,0),(0xFFFFF712,2,0),(0xFFFFF71A,4,0),(0xFFFFF710,2,4),(0xFFFFF718,2,4),(0xFFFFF718,2,256)]:
        c=Cmt1();before=c.values.copy()
        try:c.write(address,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('unsupported CMT write accepted')
        assert c.values==before and not c.accesses and not c.seen_flag
    result=dict(status='PASS',scope=__doc__,cases=cases,rejected_writes=rejected,
        limits='No matches/timebase or hardware interrupt events; word-only subset.')
    Path(__file__).with_name('control-cmt1-fixture-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
