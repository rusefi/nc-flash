"""Original F28C/1062E timer callback drives acquisition and both event queues.

Each supplied CMT1 status sample executes the complete original timer callback,
then the scheduler drains to idle. No direct task7 enqueue or event2 injection.
All task stacks use explicit FFFED000 and admission maskF0. No hardware entry,
RTE interrupt delivery, absolute frequency or remote-controller proof.
"""
import hashlib
import json
from pathlib import Path

from probe_control_queued_event2 import QueuedEvent
from probe_control_task_dispatch import IdleBoundary
from verify_control_contributions import ECU,r,w
from verify_control_acquisition import REGISTERS
from verify_control_qualification_freshness import values
from control_timer10_fixture import Timer10
from control_sci4_fixture import Serial4

TIMER_TARGETS={int.from_bytes(ECU[a:a+4],'big') for a in range(0x1138C,0x113C4,4)}

class TimerEvent(QueuedEvent):
    WIDTHS={**QueuedEvent.WIDTHS,0xFFFFF75C:2}
    def __init__(self):
        super().__init__();self.cmt_active=False;self.cmt_samples=[];self.cmt_io=[]
        self.atu10=Timer10()
        self.sci4=Serial4(0xC0,[0]*4096)
        self.registers[0xFFFFF75C]=0
        self.timer_entries=[]
        self.timer_callbacks=[]
        self.sci0_rx.extend([0]*4096)
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if 0xFFFFF020<=address<=0xFFFFF026:return self.sci4.read(address,size)
        if address in [0xFFFFF6E8,0xFFFFF6EA]:return self.atu10.read(address,size)
        if self.cmt_active and address&0xFFFFFFFF==0xFFFFF718:
            if size!=2 or not self.cmt_samples:raise ValueError('CMT1 finite word sample exhausted')
            value=self.cmt_samples.pop(0);self.cmt_io.append(['read',0xFFFFF718,2,value]);return value
        return super().read(address,size)
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address==0xFFFFF75C:value &= 0x0380
        if 0xFFFFF020<=address<=0xFFFFF026:return self.sci4.write(address,value,size)
        if address in [0xFFFFF6E8,0xFFFFF6EA]:return self.atu10.write(address,value,size)
        if self.cmt_active and address&0xFFFFFFFF==0xFFFFF718:
            if size!=2:raise ValueError('CMT1 requires word write')
            self.cmt_io.append(['write',0xFFFFF718,2,value&65535]);return
        return super().write(address,value,size)
    def instruction(self,pc):
        if self.cmt_active and pc in TIMER_TARGETS:
            self.timer_callbacks.append(dict(target=pc,argument=self.r[4],return_pc=self.pr))
        if pc in [0xF28C,0x1062E,0xFA68,0xFBE8,0xDC2C,0xE5FC]:
            self.timer_entries.append(dict(stage=self.stage,pc=pc,pr=self.pr,
                argument=self.r[4],wheel=r(self,0x51E0,2),divider=r(self,0x51E2)))
        return super().instruction(pc)


def main(cycles=10,filename='control-timer-event2-prefix10.json',machine_type=TimerEvent,timer_delivery=None,scheduler_delivery=None):
    e=machine_type();e.r[15]=0xFFFED000;e.registers[0xFFFFF74E]=1
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),rows=[])
    try:
        for stage,entry in [('clear',0x10022),('filter',0xCA94),('initializer',0x1619A),
                            ('queues',0x38C4),('availability',0x3F40)]:
            e.stage=stage;e.run(entry,0xFFFF12B0 if entry in [0x38C4,0x3F40] else 0,limit=2000000)
        w(e,0x12BC,0xFFFED000,4);w(e,0x12C0,0xB0,4)
        e.adc_samples[REGISTERS[1]]=512<<6
        for cycle in range(cycles):
            e.stage=f'queued-event2-timer-{cycle}';e.r[15]=0xFFFED000;e.sr=0xF0
            e.adc_samples[REGISTERS[28]]=(0 if cycle<300 else 500)<<6
            e.cmt_samples=[0xC0];e.cmt_io=[];e.cmt_active=True
            starts=[len(v) for v in [e.timer_entries,e.queue_entries,e.rte_transfers,e.consume_checks,e.queue_callbacks]]
            try:
                if timer_delivery is None:e.run(0xF28C,limit=1000000)
                else:timer_delivery(e,cycle)
            finally:e.cmt_active=False
            assert not e.cmt_samples
            assert e.cmt_io==[['read',0xFFFFF718,2,0xC0],['write',0xFFFFF718,2,0x40]]
            queued=dict(wheel=r(e,0x51E0,2),divider=r(e,0x51E2),selected=r(e,0x12B6,2),
                queue2=r(e,0x45D8),queue3=r(e,0x45DB),pending=r(e,0x652D))
            try:
                if scheduler_delivery is None:e.run(0x3B8A,0xFFFF12B0,limit=2000000)
                else:scheduler_delivery(e,cycle)
            except IdleBoundary:pass
            else:raise AssertionError('timer tasks did not reach scheduler idle')
            assert not e.decode_pending and not e.qualification_pending and not e.consume_pending
            result['rows'].append(dict(cycle=cycle,queued=queued,fields=values(e),
                timer=e.timer_entries[starts[0]:],entries=e.queue_entries[starts[1]:],
                rte=e.rte_transfers[starts[2]:],consumed=e.consume_checks[starts[3]:],
                callbacks=e.queue_callbacks[starts[4]:],mmio=e.cmt_io.copy(),
                final=dict(queue2=r(e,0x45D8),queue3=r(e,0x45DB),pending=r(e,0x652D),
                    task3_available=r(e,0x11C3),task4_available=r(e,0x11CB),task7_available=r(e,0x11E3))))
            if cycle%20==19:print('timer tasks drained',cycle+1,flush=True)
        status='scheduler idle reached'
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
        status=type(exc).__name__+': '+str(exc)
    result.update(status=status,stage=e.stage,pc=e.pc,tail=e.tail,registers=e.r,
        timer10_accesses=e.atu10.accesses,
        sci4_accesses=e.sci4.accesses,sci4_transmitted=e.sci4.tx,sci4_remaining=len(e.sci4.rx),
        timer_callback_requests=e.timer_callbacks,
        timer_entries=e.timer_entries,queue_entries=e.queue_entries,
        activity=e.activity_checked,decode=e.decode_checked,qualification=e.qualification_checked)
    Path(__file__).with_name(filename).write_text(json.dumps(result,indent=2)+'\n')
    print(status,'timer rows',len(result['rows']),'pc',hex(e.pc),flush=True)
    return e,result


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=10)
    parser.add_argument('--filename',default='control-timer-event2-prefix10.json')
    args=parser.parse_args();main(args.cycles,args.filename)
