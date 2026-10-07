"""Check actual queue2 consumer returns in the retained timer/scheduler fixture."""
import json
from pathlib import Path
from probe_control_timer_event2 import TimerEvent,main as sequence
from verify_control_timer_queue2 import consumer_model
from verify_control_contributions import r
from verify_control_raw_inputs import application


class Queue2Timer(TimerEvent):
    def __init__(self):
        super().__init__();self.queue2_pending=None;self.queue2_checks=[];self.queue2_callbacks=[]
    def instruction(self,pc):
        if self.queue2_pending is not None and pc==self.queue2_pending['return_pc']:
            item=self.queue2_pending;self.queue2_pending=None
            assert application(self)==item.pop('expected') and self.r[0]==item['result']
            self.queue2_checks.append(item)
        if pc==0xF6A0 and self.r[4]==2 and self.stage.startswith('queued-event2-timer-'):
            assert self.queue2_pending is None
            want,result=consumer_model(self,self.r[5])
            self.queue2_pending=dict(stage=self.stage,return_pc=self.pr,expected=want,
                result=result,count=r(self,0x45D8),head=r(self,0x45D7))
        if pc==0xDC66:
            self.queue2_callbacks.append(dict(stage=self.stage,target=self.r[2],
                words=[r(self,0x45A4+i*4,4) for i in range(5)]))
        return super().instruction(pc)


def main():
    root=Path(__file__).resolve().parent
    e,result=sequence(10,'control-timer-queue2-prefix10.json',Queue2Timer)
    assert result['status']=='scheduler idle reached' and len(result['rows'])==10
    assert result==json.loads((root/'control-timer-event2-prefix10.json').read_text())
    assert not e.queue2_pending
    assert len(e.queue2_checks)==len(e.queue2_callbacks)==2
    assert all(v['return_pc']==0xDC50 and v['result']==0 and v['count']==1 for v in e.queue2_checks)
    assert all(v['target']==0xE5FC for v in e.queue2_callbacks)
    result.update(queue2_scope=__doc__,queue2_checks=e.queue2_checks,queue2_callbacks=e.queue2_callbacks,
        exact_previous_timer_prefix=True)
    (root/'control-timer-queue2-prefix10.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS two actualqueue2wholeRAM returns; exactprevious10-cycle record')


if __name__=='__main__':main()
