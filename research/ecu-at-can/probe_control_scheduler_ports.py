"""Task17 continuation with documented timer4/5/9 configuration latches.

SH7058 table11.3/PDFzero254,257; TIOR4/5 allbitsR/W (PDF294), TCR9Cmask33
(PDF283). No counters, capture edges, compare outputs or physical pins.
"""
import json
from pathlib import Path
from probe_control_scheduler_adc import SchedulerAdc
from probe_control_scheduler_start import main as sequence

REGISTERS={0xFFFF0000+a:(size,initial) for a,size,initial in [
    (0xF4CB,1,0),(0xF4C2,2,65535),(0xF69C,1,0),(0xF694,1,255),
    (0xF4EA,1,0),(0xF4E6,2,65535),(0xF4E8,2,65535),
    (0xF4CA,1,0),(0xF4C6,2,65535),(0xF4C8,2,65535)]}


class SchedulerPorts(SchedulerAdc):
    WIDTHS={**SchedulerAdc.WIDTHS,**{a:size for a,(size,_) in REGISTERS.items()}}
    def __init__(self):
        super().__init__();self.timer_port_accesses=[]
        for a,(_,initial) in REGISTERS.items():self.registers[a]=initial
    def read(self,a,size):
        a &= 0xFFFFFFFF
        value=super().read(a,size)
        if a in REGISTERS:self.timer_port_accesses.append(['read',a,size,value])
        return value
    def write(self,a,value,size):
        a &= 0xFFFFFFFF
        if a==0xFFFFF69C and value&0xCC:raise ValueError('reserved TCR9C bits')
        super().write(a,value,size)
        if a in REGISTERS:self.timer_port_accesses.append(['write',a,size,value&((1<<(size*8))-1)])


def main():
    e,result=sequence('control-scheduler-ports-probe.json',SchedulerPorts)
    result.update(timer_ports_scope=__doc__,timer_port_accesses=e.timer_port_accesses,
        adc_poll_samples=e.poll_accesses,cmt1_accesses=e.cmt1.accesses)
    Path(__file__).with_name('control-scheduler-ports-probe.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
