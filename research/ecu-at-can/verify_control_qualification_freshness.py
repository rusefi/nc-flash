"""Observe qualification-to-report freshness after executed startup.

Uses the shared RAM-test/filter/application/40-event pipeline. Original ROM
callees execute. Cache oracles apply only where downstream admission is off;
other paths are retained as observations, never silently treated as verified.
"""
import json
from pathlib import Path
from verify_control_initialized_activity import InitializedActivity
from verify_control_clear_startup import run_sequence
from verify_control_qualification_report import expected, reports
from verify_control_raw_inputs import application
from verify_control_contributions import r

FIELDS = {0x8EF4:1,0x8EF5:1,0x8EF6:1,0x8EF7:1,0x8EF8:1,0x8EF9:1,
          0x8EFA:1,0x8EFB:1,0x8EFC:1,0x8EFD:1,0x8EFE:1,0x8EFF:1,
          0x8F00:1,0x6C92:2,0x914B:1,0x99D5:1,0x99D8:2,0x9462:1,
          0x9A28:1,0x973D:1,0x973E:1}


def values(e):
    return {hex(a):r(e,a,n) for a,n in FIELDS.items()}


class Observed(InitializedActivity):
    def __init__(self):
        super().__init__()
        self.qualification_pending=[]
        self.qualification_checked=[]
        self.qualification_writes=[]

    def instruction(self, pc):
        while self.qualification_pending and pc==self.qualification_pending[-1]['return']:
            item=self.qualification_pending.pop()
            want=item.pop('expected')
            if want is not None:
                assert application(self)==want, (self.stage,hex(item['entry']))
                assert item['reports']==item['selected']
            item['after']=values(self)
            self.qualification_checked.append(item)
        if pc in [0x6CD96,0x6CE24,0x6CF06,0x6CFD8]:
            want=None;selected=None
            if pc==0x6CFD8:
                selected=reports(self)
                if not selected or r(self,0x99D5)!=1 or not(r(self,0x99D8,2)&0x8000):
                    want,selected=expected(self)
            self.qualification_pending.append(dict(entry=pc,stage=self.stage,return_=self.pr,
                before=values(self),expected=want,selected=selected,reports=[],cache_oracle=want is not None))
            self.qualification_pending[-1]['return']=self.qualification_pending[-1].pop('return_')
        if pc==0x8FAC8 and self.qualification_pending and self.qualification_pending[-1]['entry']==0x6CFD8:
            self.qualification_pending[-1]['reports'].append((self.r[4],self.r[5]))
        return super().instruction(pc)

    def write(self,address,value,size):
        result=super().write(address,value,size)
        if self.stage.startswith('event2-') and 0xFFFF8EF4<=address<0xFFFF8F01:
            self.qualification_writes.append(dict(stage=self.stage,pc=self.instruction_pc,address=address,value=value,size=size))
        return result


def main():
    filename='control-qualification-freshness-verification.json'
    e,row=run_sequence(entry=0x10022,filename=filename,scope=__doc__,
                       samples=[1]*10+[0]*15+[1]*15,machine_type=Observed)
    assert not e.qualification_pending
    groups={}
    for item in e.qualification_checked:
        if item['stage'].startswith('event2-'):
            groups.setdefault(item['stage'],[]).append(item)
    for stage,items in groups.items():
        assert [v['entry'] for v in items]==[0x6CD96,0x6CE24,0x6CF06,0x6CFD8]
        for before,after in zip(items,items[1:]):
            assert before['after']==after['before'],stage
    assert len(groups)==2, list(groups)
    row.update(qualification=e.qualification_checked,qualification_writes=e.qualification_writes,
               same_task_freshness_groups=len(groups))
    Path(__file__).with_name(filename).write_text(json.dumps(row,indent=2)+'\n')
    print('qualification groups',len(groups),'boundaries',len(e.qualification_checked),
          'cache oracles',sum(v['cache_oracle'] for v in e.qualification_checked))


if __name__=='__main__':main()
