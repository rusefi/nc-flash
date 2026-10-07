"""Native CMT delivery at configured relative frequency with explicit timing.

Both counters begin at zero at supplied common epoch0. Peripheral-clock match
times are20000*n and40960*n; CMT0 is delivered first on ties.100 CMT0 matches
precede each application/diagnostic pair. Task/CAN/capture timing and zero
initial offset remain fixtures; hardware admission/nesting is not simulated.
"""
import probe_tcu_cmt1_delivery as primary


class Observed(primary.Observed):
    def primary_delivery(self):
        # Supersede the old eight-per-pair wheel requests. Actual events below
        # go through the same original ISR/model implementation as before.
        self.supplied_primary_requests += 1

    def clock_delivery(self):
        target = 20000*(self.clock_number+1)
        while 40960*(self.primary_number+1) < target:
            self.deliver_primary_match()
        super().clock_delivery()
        self.clock_order.append([target,0,self.clock_number])
        if 40960*(self.primary_number+1) == target:
            self.deliver_primary_match()

    def deliver_primary_match(self):
        primary.Observed.primary_delivery(self)
        timestamp = 40960*self.primary_number
        self.primary_events[-1]['peripheral_match_time'] = timestamp
        self.clock_order.append([timestamp,1,self.primary_number])


def fixture():
    t = primary.fixture()
    t.__class__ = Observed
    t.reset_primary_every_eight = False
    t.primary_status = 0xC1  # configured CMIE/CKS plus supplied compare flag
    t.supplied_primary_requests = 0
    t.clock_order = []
    return t


def before_task(t,call):
    assert t.supplied_primary_requests == call*8+1
    t.primary_events = []
    t.clock_order = []
    primary.hold.before_task(t,call)
    assert t.supplied_primary_requests == (call+1)*8
    assert t.clock_number == (call+1)*100
    assert t.primary_number == t.clock_number*20000//40960
    assert t.clock_order == sorted(t.clock_order)


def after_task(t,call):
    out = primary.hold.after_task(t,call)
    out['cmt1_interrupts'] = t.primary_events
    out['clock_order'] = t.clock_order
    out['clock_schedule'] = dict(peripheral_time=t.clock_number*20000,
        cmt0_total=t.clock_number,cmt1_total=t.primary_number,
        superseded_primary_requests=t.supplied_primary_requests,
        initial_offset=0,cmt0_before_cmt1_on_ties=True)
    return out


def main(cycles=8,filename='tcu-clock-ratio-prefix8.json'):
    primary.hold.clock.capture.cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
        before_task=before_task,after_task=after_task,scope=__doc__)


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--filename',default='tcu-clock-ratio-prefix8.json')
    args=parser.parse_args();main(args.cycles,args.filename)
