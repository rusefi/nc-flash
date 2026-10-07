"""Continue original scheduler/task17 startup using bounded CMT1 latches."""
import json
from pathlib import Path
from probe_control_scheduler_start import SchedulerStart,main as sequence
from control_cmt1_fixture import Cmt1


class SchedulerCmt(SchedulerStart):
    def __init__(self):
        super().__init__();self.cmt1=Cmt1()
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if address in self.cmt1.values:return self.cmt1.read(address,size)
        return super().read(address,size)
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address in self.cmt1.values:return self.cmt1.write(address,value,size)
        return super().write(address,value,size)


def main():
    e,result=sequence('control-scheduler-cmt-probe.json',SchedulerCmt)
    result.update(cmt1_accesses=e.cmt1.accesses,cmt1_values={hex(k):v for k,v in e.cmt1.values.items()})
    Path(__file__).with_name('control-scheduler-cmt-probe.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
