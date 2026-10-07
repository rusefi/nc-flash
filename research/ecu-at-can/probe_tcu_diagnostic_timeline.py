"""Original diagnostic ISR joins shared capture/timer/application timeline.

Diagnostic compare every500000phi, common epoch0 and zero service latency.
Tie order CMT0,CMT1,captureA,captureB,diagnostic,application. Previous pulse
trajectory/loss, CAN once/application and initialized diagnostic mode3 remain
explicit fixtures. No full boot, physical IRQ acceptance, bus or actuator proof.
"""
import probe_tcu_capture_timeline as capture
from probe_tcu_qualified_receive import diagnostic_state
from verify_tcu_diagnostic_timer import Samples,execute_prefix
from verify_tcu_base_publication import ram


class Observed(capture.Observed):
    def read(self,address,size):
        if self.diagnostic_active and (address&0xFFFFFFFF) >= 0xFFFFE000:
            return self.io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if self.diagnostic_active and (address&0xFFFFFFFF) >= 0xFFFFE000:
            return self.io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.diagnostic_active and pc in [0x1218E,0x1267C,0x12682,0x57002,0x56F80]:
            self.diagnostic_entries.append(hex(pc))
        return super().instruction(pc)

    def finish_diagnostic_interval(self):
        # Actual delivery occurred at its compare time in the merged timeline.
        assert not self.diag_pending
        self.suppressed_diagnostic_calls += 1

    def deliver_arrival(self,time,rank):
        if rank != 4:
            return super().deliver_arrival(time,rank)
        assert not(self.diagnostic_active or self.capture_active or self.application_active
                   or self.cmt_active or self.cmt1_active or self.diag_pending)
        self.diagnostic_number += 1
        n = self.diagnostic_number
        before = diagnostic_state(self)
        start = len(self.diag_boundaries)
        self.diagnostic_entries = []
        self.diagnostic_active = True
        try:
            compare = (15625*n)&65535
            event = execute_prefix(self,1,1,compare,compare,compare,n*1000,n*1000+100)
        finally:
            self.diagnostic_active = False
        assert not self.diag_pending
        event.update(number=n,peripheral_match_time=time,before=before,after=diagnostic_state(self),
                     entries=list(self.diagnostic_entries),boundaries=self.diag_boundaries[start:])
        self.diagnostic_events.append(event)
        return n


def fixture():
    t = capture.fixture()
    t.__class__ = Observed
    t.diagnostic_active = False
    t.io = Samples()
    t.diagnostic_entries = []
    t.diagnostic_events = []
    t.diagnostic_number = t.suppressed_diagnostic_calls = 0
    t.application_rank = 5
    t.timeline = capture.Timeline([(4,500000)])
    # Existing channels0/1/2 start sample and configured TIOR3A=1; original
    # initializer adds channel3. Common epoch remains an experiment assumption.
    t.io.samples = {(0xFFFFF401,1):[15,15],(0xFFFFF480,2):[0],
                    (0xFFFFF482,2):[0],(0xFFFFF4AB,1):[1,1,1,1]}
    before = ram(t)
    t.diagnostic_active = True
    try:
        t.run(0x167E4)
    finally:
        t.diagnostic_active = False
    assert ram(t) == before and all(not v for v in t.io.samples.values())
    assert len(t.io.accesses) == 18
    assert t.io.accesses[-1] == ['write',0xFFFFF401,1,31]
    return t


def before_task(t,call):
    t.diagnostic_events = []
    capture.before_task(t,call)


def after_task(t,call):
    out = capture.after_task(t,call)
    before = out.pop('before_diagnostic')
    after = out.pop('after_diagnostic')
    assert before == after
    assert t.suppressed_diagnostic_calls == call+1
    out.update(post_application_diagnostic_state=after,
        diagnostic_interrupts=t.diagnostic_events,
        diagnostic_schedule=dict(period=500000,epoch=0,total=t.diagnostic_number,
            suppressed_once_application_calls=t.suppressed_diagnostic_calls,
            zero_service_latency=True))
    return out


def main(cycles=8,filename='tcu-diagnostic-timeline-prefix8.json'):
    capture.task.main(cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
                      before_task=before_task,after_task=after_task,scope=__doc__)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--filename',default='tcu-diagnostic-timeline-prefix8.json')
    args = parser.parse_args()
    main(args.cycles,args.filename)
