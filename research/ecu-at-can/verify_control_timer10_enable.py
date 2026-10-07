"""Independent Timer10 latch and original7D0C enable-path whole-RAM checks."""
import itertools
import json
from pathlib import Path
from control_timer10_fixture import Timer10
from probe_control_timer_event2 import TimerEvent
from verify_control_contributions import ECU,w
from verify_control_raw_inputs import application,expected_write


def main():
    latches=0
    for status,value,read_first in itertools.product(range(16),range(16),[False,True]):
        io=Timer10(status)
        if read_first:assert io.read(0xFFFFF6E8,2)==status
        io.write(0xFFFFF6E8,value,2)
        assert io.status==(status&value if read_first else status)
        assert io.read(0xFFFFF6E8,2)==io.status
        latches+=1
    for enable in range(32):
        io=Timer10();io.write(0xFFFFF6EA,enable,2)
        assert io.read(0xFFFFF6EA,2)==enable;latches+=1
    rejects=0
    for a,v,n in [(0xFFFFF6E8,0,1),(0xFFFFF6EA,0,4),(0xFFFFF6E9,0,2),
                  (0xFFFFF6E8,16,2),(0xFFFFF6EA,32,2)]:
        io=Timer10(15,31)
        try:io.write(a,v,n)
        except ValueError:rejects+=1
        else:raise AssertionError('unsupported write accepted')
        assert (io.status,io.enable,io.accesses)==(15,31,[])
    cases=0
    for active,status,enable,index in itertools.product([0,1,255],range(16),[0,1,15,16,31],[0,1,127,255]):
        e=TimerEvent();e.r[15]=0xFFFED000;e.sr=0xF0;e.atu10=Timer10(status,enable)
        w(e,0x414C,active);w(e,0x4119,index);w(e,0x414B,253)
        want=application(e);saved=e.r[8:16].copy();gbr=e.gbr
        value=0 if ECU[0xDC3A9]==0x5A else ECU[0x1115D+2*index]&127
        if not active:
            expected_write(want,0x414B,value,1);expected_write(want,0x414C,1,1)
        e.run(0x7D0C)
        assert application(e)==want
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        assert e.atu10.status==(status if active else status&11)
        assert e.atu10.enable==(enable if active else enable|4)
        assert e.atu10.accesses==([] if active else [
            ['read',0xFFFFF6E8,2,status],['write',0xFFFFF6E8,2,11],
            ['read',0xFFFFF6E8,2,status&11],['read',0xFFFFF6EA,2,enable],
            ['write',0xFFFFF6EA,2,enable|4]])
        assert e.accesses==([] if active else [('write',0xFFFFF6D8,value,1),('write',0xFFFFF6C4,0,1)])
        cases+=1
    result=dict(status='PASS',scope=__doc__,latch_cases=latches,rejected_writes=rejects,
        original_enable_whole_ram_cases=cases,limits='No arriving timer/capture events or physical interrupt delivery; alltask startup not proved by this leaf.')
    Path(__file__).with_name('control-timer10-enable-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
