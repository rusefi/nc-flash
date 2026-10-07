"""Observe original20CBC entry/return inside native CMT0/capture task pairs.

The default short experiment stops external captures at20 and runs32 pairs.
No injected history/elapsed/hold/timer/phase/ack/fault values. Same task and
CAN fixtures as native CMT0 delivery; hardware cadence and wiring unproved.
"""
import probe_tcu_cmt0_delivery as clock
from verify_tcu_reference_hold import model,state
from verify_can201_byte6 import TCU
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate


class Observed(clock.Observed):
    def instruction(self,pc):
        if self.hold_pending and self.hold_pending[-1]['return_pc']==pc:
            row=self.hold_pending.pop()
            assert ram(self)==row.pop('expected_ram'),('20CBC actualreturn',hex(pc))
            row['after']=state(self);row['whole_application_ram_checked']=True
            self.hold_checks.append(row)
        if pc==0x20CBC:
            ref=SHRotate(TCU);ref.ram=dict(self.ram)
            row=dict(return_pc=self.pr,before=state(self),expected=model(ref),
                     expected_ram=ram(ref))
            self.hold_pending.append(row)
        return super().instruction(pc)


def fixture():
    t=clock.fixture();t.__class__=Observed
    t.hold_pending=[];t.hold_checks=[]
    return t


def before_task(t,call):
    assert not t.hold_pending
    t.hold_checks=[]
    clock.before_task(t,call)


def after_task(t,call):
    out=clock.after_task(t,call)
    assert not t.hold_pending
    out['hold_checks']=t.hold_checks
    if (call+1)%32==0:
        print(dict(completed_pairs=call+1,clock_prefixes=t.clock_number),flush=True)
    return out


def main(cycles=32,stop=20,filename='tcu-clock-hold-probe.json'):
    def configured():
        t=fixture();t.capture_enabled=lambda call,entry:call<stop
        return t
    clock.capture.cut.reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=cycles,timer=True,filename=filename,machine_factory=configured,
        before_task=before_task,after_task=after_task,scope=__doc__+f'\nCapturestop:{stop}; taskpairs:{cycles}.')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=32)
    parser.add_argument('--stop',type=int,default=20)
    parser.add_argument('--filename',default='tcu-clock-hold-probe.json')
    args=parser.parse_args();main(args.cycles,args.stop,args.filename)
