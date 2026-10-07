"""Original capture ISR prefixes joined to the complete320-pair recovery trace.

Same external capture intervals/absence, CAN receipts and task interleave as
probe_tcu_recovery_cut. Deliver timestamps through16C7C/16B44 with explicit
TSR0/ICR0A/ICR0B and two F6C0 profiling samples, stopping before RTE. No actual
interrupt delivery, hardware status side effects, clock rate or pin mapping.
"""
import probe_tcu_recovery_cut as cut
from verify_tcu_capture_interrupts import CaptureSamples, CHANNELS, execute_prefix


class Observed(cut.Observed):
    def read(self,address,size):
        if self.capture_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.capture_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if self.capture_active and (address & 0xFFFFFFFF)>=0xFFFFE000:
            return self.capture_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.capture_active and pc in [0x179A8,0x17A58]:
            self.capture_callbacks.append([pc,self.r[4]])
        return super().instruction(pc)

    def capture_delivery(self,entry,captured):
        assert not self.capture_active
        channel={0x179A8:'A',0x17A58:'B'}[entry]
        cfg=CHANNELS[channel]
        self.capture_number+=1
        start=1000*self.capture_number
        self.capture_active=True
        try:
            event=execute_prefix(self,channel,cfg['mask'],cfg['mask'],captured,start,start+100)
        finally:
            self.capture_active=False
        assert not self.source_pending
        event.update(differential_application_ram_checked=True,registers_checked=True)
        self.capture_events.append(event)


def fixture():
    t=cut.fixture();t.__class__=Observed
    t.capture_active=False;t.capture_io=CaptureSamples()
    t.capture_callbacks=[];t.capture_events=[];t.capture_number=0
    return t


def before_task(t,call):
    t.capture_events=[]
    cut.before_task(t,call)


def after_task(t,call):
    out=cut.after_task(t,call)
    out['capture_interrupts']=t.capture_events
    return out


def main(cycles=320,filename='tcu-capture-delivery-probe.json'):
    cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
        before_task=before_task,after_task=after_task,scope=__doc__)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=320)
    parser.add_argument('--filename',default='tcu-capture-delivery-probe.json')
    args=parser.parse_args();main(args.cycles,args.filename)
