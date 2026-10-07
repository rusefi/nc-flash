"""Native CMT1/CMT0/capture/CAN prefixes joined to complete recovery tasks.

Original12374 initializes mode/primary phases; all8 prior direct11014 calls
use16CF4 through16D3E beforeRTE.100 CMT0 events/pair, capture/CAN inputs and
application/diagnostic order remain explicit fixtures, not measured cadence.
Actual20CBC hold inputs/wholeRAM returns are observed throughout.
"""
import probe_tcu_clock_hold as hold
from verify_tcu_cmt1_interrupt import Samples,execute_prefix
from verify_can201_byte6 import TCU,w
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate


class Observed(hold.Observed):
    def read(self,address,size):
        if self.cmt1_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.cmt1_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if self.cmt1_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.cmt1_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.cmt1_active and pc in [0x12386,0x12886,0x11014]:
            self.cmt1_entries.append(hex(pc))
        return super().instruction(pc)

    def primary_delivery(self):
        assert not(self.cmt1_active or self.cmt_active or self.capture_active)
        if getattr(self,'reset_primary_every_eight',True) and self.primary_number%8==0:
            self.primary_events=[]
        self.primary_number+=1;start=1000*self.primary_number
        status=getattr(self,'primary_status',128)
        self.cmt1_active=True
        try:event=execute_prefix(self,status,status,start,start+100)
        finally:self.cmt1_active=False
        assert event['active'] and event['mode']==(1 if self.primary_number==1 else 3)
        event.update(number=self.primary_number,accesses=self.cmt1_io.accesses,
                     independent_application_ram_checked=True,registers_and_mmio_checked=True)
        self.primary_events.append(event)


def fixture():
    t=hold.fixture();t.__class__=Observed
    t.cmt1_active=False;t.cmt1_io=Samples();t.cmt1_entries=[]
    t.primary_number=0;t.primary_events=[]
    ref=SHRotate(TCU);ref.ram=dict(t.ram);w(ref,0x8009,1)
    for a in [0x8494,0x8498,0x849C]:w(ref,a,0,4)
    # Explicit shared start-register sample preserves the preceding CMT0 bit.
    t.cmt1_io.samples={(0xFFFFF710,2):[1]}
    t.cmt1_active=True
    try:t.run(0x12374,limit=200000)
    finally:t.cmt1_active=False
    assert ram(t)==ram(ref)
    assert t.cmt1_io.accesses==[['write',0xFFFFF71C,2,1279],
                              ['read',0xFFFFF710,2,1],['write',0xFFFFF710,2,3]]
    assert all(not v for v in t.cmt1_io.samples.values())
    return t


def before_task(t,call):
    assert t.primary_number==8*call+1
    hold.before_task(t,call)
    assert t.primary_number==8*(call+1) and len(t.primary_events)==8


def after_task(t,call):
    out=hold.after_task(t,call)
    out['cmt1_interrupts']=t.primary_events
    return out


def main(cycles=320,filename='tcu-cmt1-delivery-probe.json'):
    hold.clock.capture.cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
        before_task=before_task,after_task=after_task,scope=__doc__)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=320)
    parser.add_argument('--filename',default='tcu-cmt1-delivery-probe.json')
    args=parser.parse_args();main(args.cycles,args.filename)
