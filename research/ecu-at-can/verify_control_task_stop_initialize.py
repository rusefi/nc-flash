"""Independent original977A2 RAM-initializer oracle for the new GBR path."""
import hashlib
import itertools
import json
from pathlib import Path
from verify_control_task_stop_retained import Observed
from verify_control_raw_inputs import application,expected_write
from verify_control_contributions import ECU


def main():
    count=0
    for old,gbr in itertools.product([0,0x55,0xAA,255],[0,0xFFFF8000,0xFFFF2B8C,0xFFFFFFFF]):
        e=Observed();e.gbr=gbr
        for address in range(0x2B88,0x2CDC):e.write(0xFFFF0000+address,old,1)
        e.r[8:15]=[0xABC00000+i for i in range(7)]
        preserved=e.r[8:16].copy();want=application(e)
        for address in range(0x2B90,0x2CD0):expected_write(want,address,0,1)
        for address in [0x2B8C,0x2B8E,0x2CD4]:expected_write(want,address,0xA55A,2)
        for address in [0x2CD0,0x2CD2]:expected_write(want,address,0x00FF,2)
        e.run(0x977A2)
        assert application(e)==want and e.r[8:16]==preserved and e.gbr==gbr
        assert e.sr&0xF0==0xF0 and not e.accesses
        count+=1
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),original_initializer_cases=count,
                scope=__doc__,cleared_bytes=320,protected_words={'A55A':[0x2B8C,0x2B8E,0x2CD4],'00FF':[0x2CD0,0x2CD2]})
    Path(__file__).with_name('control-task-stop-initialize-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(count,'original977A2 full-RAM/register/GBR cases passed')


if __name__=='__main__':main()
