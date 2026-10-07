"""Independent originalDD56..70E4 boundary, configuring timer4/5/9 ports."""
import itertools,json,random
from pathlib import Path
from probe_control_scheduler_ports import SchedulerPorts,REGISTERS
from sh_control_interrupt import execute_to
from verify_control_raw_inputs import application


def main():
    count=0
    for seed,mask in itertools.product(range(64),[0x10,0x70,0xF0]):
        e=SchedulerPorts();rng=random.Random(seed);e.r[15]=0xFFFED000;e.sr=mask
        for a,(size,_) in REGISTERS.items():e.registers[a]=rng.randrange(1<<(size*8))
        e.registers[0xFFFFF69C]&=0x33
        expected=e.registers.copy();accesses=[];memory=application(e)
        def rmw(a,and_mask,or_mask):
            value=expected[a];accesses.append(['read',a,1,value])
            expected[a]=(value&and_mask)|or_mask;accesses.append(['write',a,1,expected[a]])
        def zero(a):
            expected[a]=0;accesses.append(['write',a,REGISTERS[a][0],0])
        rmw(0xFFFFF4CB,0xF8,5);zero(0xFFFFF4C2)
        rmw(0xFFFFF69C,0xFC,1);zero(0xFFFFF694)
        rmw(0xFFFFF4EA,0xF8,6);zero(0xFFFFF4E6)
        rmw(0xFFFFF4EA,0x8F,0x60);zero(0xFFFFF4E8)
        rmw(0xFFFFF4CA,0xF8,6);zero(0xFFFFF4C6)
        rmw(0xFFFFF4CA,0x8F,0x60);zero(0xFFFFF4C8)
        assert execute_to(e,0xDD56,{0x70E4})==0x70E4
        assert application(e)==memory and e.registers==expected and e.timer_port_accesses==accesses
        assert e.r[15]==0xFFFED000 and e.sr&0xF0==mask
        count+=1
    rejected=0
    for a,size,value in [(0xFFFFF4CB,2,0),(0xFFFFF4C2,1,0),(0xFFFFF69C,1,4)]:
        e=SchedulerPorts();before=e.registers.copy()
        try:e.write(a,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('unsupported timer write accepted')
        assert e.registers==before and not e.timer_port_accesses
    result=dict(status='PASS',scope=__doc__,original_cases=count,rejected_writes=rejected,
        accesses_per_case=len(accesses),limits='Stopsbefore70E4body; no physicalcapture/compare/countereffects, masksnonzero.')
    Path(__file__).with_name('control-startup-ports-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
