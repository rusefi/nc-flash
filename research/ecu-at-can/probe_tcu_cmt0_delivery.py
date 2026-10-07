"""Original CMT0 prefixes joined to capture/receive/application/diagnostic tasks.

Original123B0 initializes mode/tick/countdown phases. Each prior direct11864
tick is replaced by16D6C through16DB6 beforeRTE; all128B6 helpers run. Explicit
100 CMT0 events and8 primary wheel calls per task pair, not measured cadence.
Same external capture intervals/absence and CAN receipts as capture delivery.
No injected age/cache/countdown/phase/ack/fault values or physical bus proof.
"""
import probe_tcu_capture_delivery as capture
from verify_tcu_cmt0_interrupt import Samples, execute_prefix
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate


def state(t):
    out={hex(a):r(t,a,n) for a,n in [(0x800A,1),(0x84D0,4),
          (0x84D4,1),(0x84D5,1),(0x84D6,1),(0x91AC,2)]}
    # Preserve every byte in the stock countdown ranges, including holes.
    out['countdown_8410_8491']=[r(t,a) for a in range(0x8410,0x8492)]
    return out


class Observed(capture.Observed):
    def read(self,address,size):
        if self.cmt_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.cmt_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if self.cmt_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.cmt_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.cmt_active and pc in [0x123C2,0x128B6,0x11864,0x1E506,0x11A64]:
            self.cmt_entries.append(hex(pc))
        return super().instruction(pc)

    def clock_delivery(self):
        assert not self.cmt_active and not self.capture_active
        if self.clock_count==0:self.clock_before=state(self)
        self.clock_number+=1;start=1000*self.clock_number
        self.cmt_active=True
        try:
            event=execute_prefix(self,128,128,start,start+100)
        finally:
            self.cmt_active=False
        assert event['active'] and event['tick']==self.clock_number
        assert event['mode']==(1 if self.clock_number==1 else 3)
        self.clock_count+=1
        if self.clock_count==1:self.clock_first=event
        self.clock_last=event;self.clock_after=state(self)


def fixture():
    t=capture.fixture();t.__class__=Observed
    t.cmt_active=False;t.cmt_io=Samples();t.cmt_entries=[]
    t.clock_number=0;t.clock_count=0
    ref=SHRotate(TCU);ref.ram=dict(t.ram)
    for a,v,n in [(0x800A,1,1),(0x84D0,0,4),(0x84D4,0,1),
                  (0x84D5,0,1),(0x84D6,0,1)]:w(ref,a,v,n)
    t.cmt_io.samples={(0xFFFFF710,2):[0]}
    t.cmt_active=True
    try:t.run(0x123B0,limit=200000)
    finally:t.cmt_active=False
    assert ram(t)==ram(ref)
    assert t.cmt_io.accesses==[['write',0xFFFFF716,2,624],
                              ['read',0xFFFFF710,2,0],['write',0xFFFFF710,2,1]]
    assert all(not v for v in t.cmt_io.samples.values())
    return t


def before_task(t,call):
    t.clock_count=0
    capture.before_task(t,call)
    assert t.clock_count==getattr(t,'expected_clock_count',100)


def after_task(t,call):
    out=capture.after_task(t,call)
    out['cmt0']=dict(count=t.clock_count,total=t.clock_number,
        first=t.clock_first,last=t.clock_last,before=t.clock_before,
        after=t.clock_after,after_tasks=state(t),
        differential_application_ram_checks=t.clock_count,
        registers_and_finite_ordered_mmio_checks=t.clock_count)
    return out


def main(cycles=320,filename='tcu-cmt0-delivery-probe.json'):
    capture.cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
        before_task=before_task,after_task=after_task,scope=__doc__)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=320)
    parser.add_argument('--filename',default='tcu-cmt0-delivery-probe.json')
    args=parser.parse_args();main(args.cycles,args.filename)
