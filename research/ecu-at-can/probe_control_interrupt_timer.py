"""Original idle IRQ wrapper/epilogue replaces direct timer call/explicit dispatch.

Explicit exception frame PC3D0C/SR0, entrySRF0 and native ROM idle stack.
Originalidle handler33F0 reaches3D10 directly; task context stackFFFED000 is
still the prior fixture. No VBR/INTC acceptance or clock/remote-device proof.
"""
import json
from pathlib import Path
from sh_control_interrupt import ControlInterrupt,execute_to
from probe_control_timer_event2 import main as sequence
from probe_control_task_dispatch import IdleBoundary
from verify_control_contributions import r


def timer(e,cycle):
    if cycle==0:
        try:e.run(0x3B8A,0xFFFF12B0)
        except IdleBoundary:pass
        else:raise AssertionError('initial idle not reached')
        e.irq_trace=[]
    assert r(e,0x12B8,4)==0x80000000 and r(e,0x12B6,2)==65535
    e.r[15]=e.read(0x4078,4)-8;e.sr=0xF0
    e.write(e.r[15],0x3D0C,4);e.write(e.r[15]+4,0,4)
    start=len(e.rte_transfers);e.irq_active=True
    assert execute_to(e,0x2F78,{0x32D8},1000000)==0x32D8
    assert r(e,0x12B8,4)==0x80000001
    e.irq_trace.append(dict(cycle=cycle,after_callback_stack=e.r[15],nesting=r(e,0x12B8,4),
        selected=r(e,0x12B6,2),rte_start=start))


def scheduler(e,cycle):
    assert execute_to(e,0x32D8,{0x3D0C},2000000)==0x3D0C
    assert r(e,0x12B8,4)==0x80000000 and e.r[15]==e.read(0x4078,4) and e.sr==0
    assert not e.queue2_pending
    e.irq_active=False
    e.irq_trace[-1].update(after_idle_stack=e.r[15],final_nesting=r(e,0x12B8,4),
        queue2_checks=len(e.queue2_checks))
    raise IdleBoundary


def main(cycles=10,filename='control-interrupt-timer-prefix10.json'):
    e,result=sequence(cycles,filename,ControlInterrupt,timer,scheduler)
    result.update(interrupt_scope=__doc__,interrupts=getattr(e,'irq_trace',[]),
        queue2_checks=e.queue2_checks,queue2_callbacks=e.queue2_callbacks)
    Path(__file__).with_name(filename).write_text(json.dumps(result,indent=2)+'\n')
    print('Interrupt cycles',len(result['interrupts']),'queue2 checks',len(e.queue2_checks),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=10)
    parser.add_argument('--filename',default='control-interrupt-timer-prefix10.json')
    args=parser.parse_args();main(args.cycles,args.filename)
