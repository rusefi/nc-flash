"""Verify74D62 at actual outer-task boundaries and record consumer freshness.

Same explicit40-event/PFDR/CADE fixture as activity-retained. No hardware time.
"""
import hashlib
import json
from pathlib import Path
from verify_control_activity_retained import Boundaries
from verify_control_activity_hold import expected,expected_timer,FIELDS
from verify_control_contributions import ECU,r
from verify_control_raw_inputs import application

ROOT=Path(__file__).resolve().parent


class HoldBoundaries(Boundaries):
    def __init__(self):
        super().__init__();self.hold_pending=None;self.hold_checked=[];self.consumers=[];self.call=-1;self.hold_writes=[];self.timer_pending=None;self.timer_checked=[]
    def write(self,a,v,size):
        targets=[x for x in [0xFFFF9149,0xFFFF8FD4,0xFFFF915C] if a<=x<a+size]
        result=super().write(a,v,size)
        if targets:
            self.hold_writes.append(dict(call=self.call,pc=getattr(self,'instruction_pc',self.pc),branch_pc=self.pc,pr=self.pr,address=a,value=v,size=size,
                after={hex(x):self.read(x,2 if x==0xFFFF8FD4 else 1) for x in targets}))
        return result
    def instruction(self,pc):
        self.instruction_pc=pc  # includes the actual delay-slot instruction
        if self.timer_pending is not None and pc==self.timer_pending['return_pc']:
            item=self.timer_pending;self.timer_pending=None
            assert application(self)==item.pop('expected')
            self.timer_checked.append(item)
        if pc==0x6F422:
            want,value=expected_timer(self)
            self.timer_pending=dict(expected=want,value=value,old=r(self,0x8FD4,2),mode=r(self,0x735A),enabled=r(self,0x8FD8),call=self.call,return_pc=self.pr)
        if self.hold_pending is not None and pc==self.hold_pending['return_pc']:
            item=self.hold_pending;self.hold_pending=None
            assert application(self)==item.pop('expected')
            item['after']={hex(a):r(self,a) for a in [0x9149,0x914D,0x914E,0x5354]}
            self.hold_checked.append(item)
        if pc==0x74D62:
            assert self.hold_pending is None
            want,detail=expected(self)
            self.hold_pending=dict(expected=want,detail=detail,return_pc=self.pr,call=self.call,
                phase=r(self,0x5360),inputs={hex(a):r(self,a) for a in FIELDS+[0x282C,0x282D]},timer=r(self,0x8FD4,2))
        if pc==0x42BCC:
            self.consumers.append(dict(call=self.call,phase=r(self,0x5360),flag=r(self,0x9149),produced_count=len(self.hold_checked)))
        return super().instruction(pc)


def main():
    e=HoldBoundaries();e.registers[0xFFFFF74E]=1;e.run(0xCA94);e.write(0xFFFFD800,2,4)
    previous=1;rows=[]
    for i,value in enumerate([1]*10+[0]*15+[1]*15):
        e.call=i;start=len(e.hold_checked)
        try:
            if value!=previous:
                e.registers[0xFFFFF74E]=(e.registers[0xFFFFF74E]&~1)|value
                e.run(0xCADE);e.run(0xCADE)
                assert r(e,0x44A2,2)&1==value
            previous=value;sp=e.r[15];gbr=e.gbr
            e.run(0x2BCE6,0xFFFFD800,limit=1000000)
            assert e.hold_pending is None and e.pending is None and e.r[15]==sp and e.gbr==gbr
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            (ROOT/'control-activity-hold-retained-limit.json').write_text(json.dumps(dict(call=i,status=str(exc),pc=e.pc,tail=e.tail,rows=rows),indent=2)+'\n');raise
        rows.append(dict(call=i,input=value,outer_phase=r(e,0x651C),control_phase=r(e,0x5360),hold_checks=e.hold_checked[start:]))
    assert len(e.hold_checked)==8 and len(e.consumers)==8
    assert [x['produced_count'] for x in e.consumers]==list(range(1,9))
    assert all(c['call']==p['call'] and c['flag']==p['detail']['flag'] for c,p in zip(e.consumers,e.hold_checked))
    assert e.timer_pending is None and len(e.timer_checked)==8
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,complete_outer_calls=40,hold_boundaries=len(e.hold_checked),timer_boundaries=e.timer_checked,mode_flag_edge_boundaries=len(e.checked),consumers=e.consumers,writes=e.hold_writes,rows=rows)
    (ROOT/'control-activity-hold-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('40 outer calls;',len(e.hold_checked),'hold boundaries;',len(e.checked),'mode/flag/edge boundaries')
    for row in e.hold_checked:print(row['call'],row['detail'],row['timer'],row['inputs'])

if __name__=='__main__':main()
