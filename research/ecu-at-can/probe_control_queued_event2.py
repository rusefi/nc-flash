"""Original event2 producer, empty-queue activation and task4 callback dispatch.

Reuse initialized acquisition fixture and supplied task7/event2 interleave.
Original3F40 initializes task availability; original215C6 queues event2 through
35E0/391A, then3B8A/RTE entersDC80 and calls2BCE6. Explicit maskF0 prevents
inline preemption. Event task uses synthetic stackFFFED000 so existing full
application-RAM oracles remain distinct from temporary stack storage. No native
producer frequency, interrupt entry, physical inputs or remote DSC claim.
"""
import json
from pathlib import Path

from probe_control_acquired_qualification import AcquiredQualification,before
from probe_control_task_dispatch import main as sequence,IdleBoundary
from verify_control_contributions import r,w
from verify_control_qualification_freshness import values
from verify_control_event2_enqueue import consumer_model
from verify_control_raw_inputs import application


class QueuedEvent(AcquiredQualification):
    def __init__(self):
        super().__init__();self.event_queue_trace=[];self.queue_entries=[]
        self.consume_pending=None;self.consume_checks=[];self.queue_callbacks=[]
    def instruction(self,pc):
        if self.consume_pending is not None and pc==self.consume_pending['return_pc']:
            item=self.consume_pending;self.consume_pending=None
            assert application(self)==item.pop('expected')
            assert self.r[0]==item['result']
            self.consume_checks.append(item)
        if pc==0xF6A0 and self.r[4]==3 and self.stage.startswith('queued-event2-'):
            assert self.consume_pending is None
            want,result=consumer_model(self,self.r[5])
            self.consume_pending=dict(stage=self.stage,return_pc=self.pr,expected=want,
                result=result,count=r(self,0x45DB),head=r(self,0x45DA))
        if pc==0xDCBA:
            self.queue_callbacks.append(dict(stage=self.stage,target=self.r[2],
                words=[r(self,0x45B8+i*4,4) for i in range(5)]))
        if pc in [0x215C6,0x1826E,0x2BC8C,0xDAE8,0xF5A0,0x35E0,0x391A,
                  0xDC80,0xF6A0,0x2BCE6,0x3CB8]:
            self.queue_entries.append(dict(pc=pc,pr=self.pr,argument=self.r[4],
                pending=r(self,0x652D),count=r(self,0x45DB),task=r(self,0x12B6,2)))
        return super().instruction(pc)


def prepare(e,cycle):
    if cycle==0:
        e.run(0x3F40,0xFFFF12B0)
        assert r(e,0x11CB)==2
    before(e,cycle)


def after(e,cycle):
    e.stage=f'queued-event2-{cycle}'
    saved_stack=e.r[15];saved_context_stack=r(e,0x12BC,4)
    e.r[15]=0xFFFED000;e.sr=0xF0
    w(e,0x12BC,0xFFFED000,4)
    start=len(e.queue_entries);rte_start=len(e.rte_transfers)
    consume_start=len(e.consume_checks);callback_start=len(e.queue_callbacks)
    assert r(e,0x45DB)==0
    e.run(0x215C6,limit=1000000)
    admission=dict(pending=r(e,0x652D),count=r(e,0x45DB),task=r(e,0x12B6,2),
        availability=r(e,0x11CB),priority=r(e,0x12B0))
    assert admission==dict(pending=1,count=1,task=4,availability=1,priority=1)
    try:e.run(0x3B8A,0xFFFF12B0,limit=1000000)
    except IdleBoundary:pass
    else:raise AssertionError('task4 did not reach scheduler idle')
    assert not e.decode_pending and not e.qualification_pending and not e.consume_pending
    assert r(e,0x45DB)==0 and r(e,0x652D)==0 and r(e,0x11CB)==2
    e.event_queue_trace.append(dict(cycle=cycle,admission=admission,
        entries=e.queue_entries[start:],rte=e.rte_transfers[rte_start:],
        consumed=e.consume_checks[consume_start:],callbacks=e.queue_callbacks[callback_start:],
        fields=values(e),head=r(e,0x45DA),tail=r(e,0x45D9)))
    e.r[15]=saved_stack;w(e,0x12BC,saved_context_stack,4)
    if cycle%20==19:print('queued event returns',cycle+1,flush=True)


def main(cycles=8,filename='control-queued-event2-prefix8.json'):
    e,row=sequence(queued=True,cycles=cycles,filename=filename,machine_type=QueuedEvent,
        before_cycle=prepare,after_cycle=after)
    row.update(scope=__doc__,event_queue=e.event_queue_trace,decode=e.decode_checked,
        qualification=e.qualification_checked,activity=e.activity_checked,
        queue_entries=e.queue_entries,callbacks=e.queue_callbacks)
    Path(__file__).with_name(filename).write_text(json.dumps(row,indent=2)+'\n')
    print(row['status'],'queued events',len(e.event_queue_trace),flush=True)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--filename',default='control-queued-event2-prefix8.json')
    args=parser.parse_args();main(args.cycles,args.filename)
