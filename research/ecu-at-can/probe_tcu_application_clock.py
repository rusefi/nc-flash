"""Retained tasks through native application ISR at configured relative periods.

Common epoch0 and zero dispatch latency are explicit fixtures. Application
compares every81920 peripheral clocks; CMT0 every20000, CMT1 every40960.
Timer prefixes precede application on ties. CAN and captures remain once per
task pair, with previous timestamp/payload fixtures; diagnostic task follows
each application. Not a complete vehicle clock/interrupt model.
"""
import probe_tcu_cmt1_delivery as primary
from probe_tcu_cmt0_delivery import Observed as ClockMachine
from verify_tcu_application_interrupt import Samples,ADDRESSES,execute_prefix
from verify_tcu_base_publication import ram


class Observed(primary.Observed):
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if self.application_active and address in ADDRESSES:
            return self.application_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if self.application_active and address in ADDRESSES:
            return self.application_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.application_active and pc in [0x1220A,0x126DA,0x126EC,0x1E5F6]:
            self.application_entries.append(hex(pc))
        return super().instruction(pc)

    def primary_delivery(self):
        self.supplied_primary_requests += 1

    def clock_delivery(self):
        self.supplied_clock_requests += 1
        if self.supplied_clock_requests%100 != 1:
            return
        target=(self.application_number+1)*81920
        while min(20000*(self.clock_number+1),40960*(self.primary_number+1)) <= target:
            a,b=20000*(self.clock_number+1),40960*(self.primary_number+1)
            if a<=b:
                ClockMachine.clock_delivery(self)
                self.clock_order.append([a,0,self.clock_number])
            else:
                primary.Observed.primary_delivery(self)
                self.primary_events[-1]['peripheral_match_time']=b
                self.clock_order.append([b,1,self.primary_number])

    def application_delivery(self):
        assert not(self.application_active or self.cmt_active or self.cmt1_active or self.capture_active)
        self.application_number += 1
        compare=(2560*self.application_number)&65535
        self.application_active=True
        try:
            self.application_event=execute_prefix(self,1,1,compare,compare,compare,
                self.application_number*1000,self.application_number*1000+100)
        finally:
            self.application_active=False
        assert self.application_event['armed'] and self.application_event['mode_after']==3
        self.clock_order.append([81920*self.application_number,2,self.application_number])


def fixture():
    t=primary.fixture();t.__class__=Observed
    t.application_active=False;t.application_io=Samples();t.application_entries=[]
    t.application_number=0;t.application_event=None
    t.supplied_clock_requests=t.supplied_primary_requests=0
    t.reset_primary_every_eight=False;t.primary_status=0xC1;t.clock_order=[]
    # Explicit shared ATU start-register sample: other channels0..2 started.
    t.application_io.samples={(0xFFFFF401,1):[7,7]}
    before=ram(t);t.application_active=True
    try:t.run(0x16A3C)
    finally:t.application_active=False
    assert ram(t)==before
    assert t.application_io.accesses==[['read',0xFFFFF401,1,7],['write',0xFFFFF401,1,7],
        ['write',0xFFFFF442,2,0],['write',0xFFFFF454,2,2560],
        ['read',0xFFFFF401,1,7],['write',0xFFFFF401,1,15]]
    return t


def before_task(t,call):
    assert t.application_number==call and t.supplied_primary_requests==call*8+1
    t.expected_clock_count=((call+1)*81920)//20000-(call*81920)//20000
    t.clock_order=[];t.primary_events=[]
    primary.hold.before_task(t,call)
    assert t.supplied_primary_requests==(call+1)*8
    assert t.supplied_clock_requests==(call+1)*100
    assert t.clock_number==((call+1)*81920)//20000
    assert t.primary_number==2*(call+1)


def after_task(t,call):
    out=primary.hold.after_task(t,call)
    assert t.clock_order==sorted(t.clock_order)
    out.update(application_interrupt=t.application_event,cmt1_interrupts=t.primary_events,
        clock_order=t.clock_order,clock_schedule=dict(peripheral_time=(call+1)*81920,
            cmt0_total=t.clock_number,cmt1_total=t.primary_number,application_total=t.application_number,
            initial_offset=0,zero_compare_latency=True))
    return out


def main(cycles=8,filename='tcu-application-clock-prefix8.json'):
    primary.hold.clock.capture.cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
        before_task=before_task,after_task=after_task,scope=__doc__)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--filename',default='tcu-application-clock-prefix8.json')
    args=parser.parse_args();main(args.cycles,args.filename)
