"""Native CAN startup, timed task interrupts and original mailbox receipts.

Extends the existing native readiness/capture/diagnostic event loop. No forced
task/receive mode, readiness, fault or history reset after admission. Explicit
external frames, reset/HCAN samples, timer epochs/ties and zero service latency.
"""
import hashlib
import json
from pathlib import Path

import verify_tcu_can_task_interrupt as interrupt
import verify_tcu_native_capture_startup as capture
import tcu_receive_fixture as rx
from verify_can201_byte6 import TCU, r

ROOT = Path(__file__).resolve().parent
END_PHI = capture.END_PHI


class Machine(interrupt.Machine):
    def read(self, address, size):
        if self.rx_registers is not None and 0xFFFFE400 <= address < 0xFFFFE600:
            # Within this guarded range the existing method returns before its
            # fallback super(); the finite mailbox sample owner stays this machine.
            return rx.ReceiveRegisters.read(self, address, size)
        return super().read(address, size)

    def write(self, address, value, size):
        if self.rx_registers is not None and 0xFFFFE400 <= address < 0xFFFFE600:
            return rx.ReceiveRegisters.write(self, address, value, size)
        return super().write(address, value, size)

    def instruction(self, pc):
        rx.observe_receive(self, pc)
        return super().instruction(pc)

    def initialize_extra(self):
        result = super().initialize_extra()
        self.can_timer_io.samples, self.expected_timer = interrupt.setup.timer_inputs(
            *[self.configuration[a] for a in [0xF401, 0xF480, 0xF482, 0xF4EB]])
        try:
            self.run(0x11FA0, limit=2000000)
            self.check_startup()
        finally:
            self.can_timer_active = False
        self.can_operational = True
        result['can_initialization'] = dict(task_mode=r(self,0x8003), receive_mode=r(self,0x8F6C),
                                            evidence=self.startup_evidence())
        return result

    def deliver_extra_event(self, kind, n, stamp):
        if kind == 'can_task':
            before = rx.receive_state(self)
            start = len(self.rx_boundaries)
            compare = (n*625)&65535
            event = interrupt.execute_prefix(self,1024,1024,compare,compare,compare,
                                               stamp,(stamp+50)&0xFFFFFFFF)
            assert not self.rx_pending
            event.update(before=before, after=rx.receive_state(self),
                         receive_boundaries=self.rx_boundaries[start:])
            return event
        if kind == 'receipt':
            before = rx.receive_state(self)
            frames = [(8,rx.phase.received.PAYLOAD201), (6,rx.phase.received.PAYLOAD215), (1,bytes(8))]
            rows = [rx.receipt(self,index,payload) for index,payload in frames]
            assert all(row['admitted'] for row in rows)
            return dict(before=before, after=rx.receive_state(self), frames=rows)
        return super().deliver_extra_event(kind,n,stamp)

    def observe_extra(self):
        return dict(**super().observe_extra(), can_task_mode=r(self,0x8003),
                    receive_state=rx.receive_state(self), receive_callbacks=self.rx_callbacks.copy())


def fixture(end_phi=END_PHI):
    t = capture.fixture(end_phi=end_phi)
    t.__class__ = Machine
    t.can_configuration = {}
    t.reset_samples = [8,0]
    t.can_timer_active = t.can_irq_active = t.can_operational = False
    t.can_timer_io = interrupt.setup.TimerSamples()
    t.can_irq_io = interrupt.Samples()
    t.can_entries, t.can_irq_entries = [],[]
    t.last_instruction = None
    t.rx_registers = None
    t.rx_accesses, t.rx_pending, t.rx_boundaries, t.rx_callbacks = [],[],[],[]
    t.additional_events += [(n*20000,0.9,'can_task',n) for n in range(1,end_phi//20000+1)]
    t.additional_events += [(n*81920,0.85,'receipt',n) for n in range(1,end_phi//81920+1)]
    return t


def main():
    scenarios = [capture.startup.native.run(period,epoch,machine_factory=fixture,end_phi=END_PHI)
                 for period,epoch in [(50000,7),(50000,0),(65536,0xFFFFFF00)]]
    for s in scenarios:
        if s['status'] != 'PASS':
            continue
        can = [r for r in s['rows'] if r['kind']=='can_task']
        receipts = [r for r in s['rows'] if r['kind']=='receipt']
        s['summary'].update(can_interrupts=len(can), received_frames=sum(len(r['event']['frames']) for r in receipts),
            can_admitted_phi=next(r['phi'] for r in can if r['event']['mode_before']==1 and r['event']['mode_after']==3),
            final_receive_state=s['rows'][-1]['receive_state'])
        assert len(can)==200 and len(receipts)==48
    result = dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),scenarios=scenarios,
        limits='CANperiod20000phi; commonzero timerstart epoch/latency fixtures. CAN201/215 fixtureencoded pluszero4EC once/application. Missingotherframes nothealthy. No physicalCAN/fullboot. TiesCMT0/diagnostic/CMT1/A/B/receipt/CANtask/application/foreground.')
    (ROOT/'tcu-native-can-timeline-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print([dict(status=s['status'], summary=s.get('summary'), error=s.get('error'), pc=s.get('pc')) for s in scenarios],flush=True)
    assert all(s['status']=='PASS' for s in scenarios)


if __name__ == '__main__':
    main()
