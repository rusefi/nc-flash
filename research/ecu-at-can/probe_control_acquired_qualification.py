"""Explicit acquisition-request then event2 interleave with changing ADC input.

120 software request pairs, no physical cadence ratio. Actual391A/3B8A/RTE/
E26C/3CB8 idle lifecycle then original2BCE6 event2. ADC28 low60/recovery60;
no internal application inputs or qualification flags are fabricated.
"""
import json
from pathlib import Path
from probe_control_task_dispatch import Observed,main as sequence
from verify_control_periodic_raw_decode import expected
from verify_control_raw_inputs import application
from verify_control_qualification_freshness import values
from verify_control_acquisition import REGISTERS
from verify_control_contributions import r


class AcquiredQualification(Observed):
    def __init__(self):
        super().__init__()
        # Extend the inherited explicit all-zero research sample stream from
        # 256 to1024 bytes. No physical serial peer behavior is inferred.
        self.sci0_status=0xC0
        self.sci0_rx.extend([0]*(1024-len(self.sci0_rx)))
        self.decode_pending=None;self.decode_checked=[];self.event_returns=[]
    def instruction(self,pc):
        if self.decode_pending is not None and pc==self.decode_pending['return']:
            item=self.decode_pending;self.decode_pending=None
            assert application(self)==item.pop('expected')
            item['after']={hex(a):r(self,a,n) for a,n in [(0x6C92,2),(0x6CAE,1),(0x6C98,2)]}
            self.decode_checked.append(item)
        if pc==0x39926:
            assert self.decode_pending is None
            self.decode_pending=dict(stage=self.stage,return_=self.pr,expected=expected(self),
                raw=[r(self,a,2) for a in [0x4040,0x4042,0x4046]])
            self.decode_pending['return']=self.decode_pending.pop('return_')
        return super().instruction(pc)


def before(e,cycle):
    e.adc_samples[REGISTERS[28]]=(0 if cycle<60 else 500)<<6


def after(e,cycle):
    e.stage=f'event2-{cycle}';e.write(0xFFFFD800,2,4)
    # This independently delivered callback uses the same explicit synthetic
    # caller stack as prior event2 tests; real task7 stack remains in RAM.
    sp=e.r[15];e.r[15]=0xFFFED000
    e.run(0x2BCE6,0xFFFFD800,limit=1000000)
    assert e.r[15]==0xFFFED000 and not e.decode_pending and not e.qualification_pending
    e.r[15]=sp
    e.event_returns.append(dict(cycle=cycle,fields=values(e)))
    if cycle%20==19:print('paired returns',cycle+1,flush=True)


def main():
    name='control-acquired-qualification-probe.json'
    e,row=sequence(queued=True,cycles=120,filename=name,machine_type=AcquiredQualification,
                   before_cycle=before,after_cycle=after)
    row.update(scope=__doc__,sci0_status_fixture=0xC0,sci0_input_samples=1024,sci0_remaining=len(e.sci0_rx),activity=e.activity_checked,decode=e.decode_checked,events=e.event_returns,qualification=e.qualification_checked)
    for item in e.qualification_checked:
        if item['entry']==0x6CFD8:assert item['reports']==item['selected']
    Path(__file__).with_name(name).write_text(json.dumps(row,indent=2)+'\n')
    print(row['status'],'event returns',len(e.event_returns),'decoded',len(e.decode_checked),flush=True)


if __name__=='__main__':main()
