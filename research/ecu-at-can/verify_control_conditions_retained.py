"""Check activity admission and independent hold at actual outer-task boundaries.

Explicit40 event2 deliveries and PFDR/CADE samples; no real elapsed time.
"""
import hashlib
import json
from pathlib import Path
from verify_control_activity_hold_retained import HoldBoundaries
from verify_control_activity_conditions import expected,ENTRIES,IDS
from verify_control_contributions import ECU,r
from verify_control_raw_inputs import application

ROOT=Path(__file__).resolve().parent
FIELDS={0x735A:1,0x8FE0:1,0x8FDF:1,0x8FD8:1,0x9125:1,0x915C:1,0x9158:2,0x915E:1,0x6D40:4,0x6D20:4,0x2444:2}


def inputs(e):return {hex(a):r(e,a,size) for a,size in FIELDS.items()}


class Integrated(HoldBoundaries):
    def __init__(self):
        super().__init__();self.condition_pending=None;self.condition_checked=[];self.freshness=[]
    def instruction(self,pc):
        if self.condition_pending is not None and pc==self.condition_pending['return_pc']:
            item=self.condition_pending;self.condition_pending=None
            assert application(self)==item.pop('expected'),hex(item['entry'])
            item['after']=inputs(self);self.condition_checked.append(item)
        if pc in ENTRIES:
            assert self.condition_pending is None
            self.condition_pending=dict(entry=pc,return_pc=self.pr,call=self.call,expected=expected(self,pc),before=inputs(self),statuses={hex(i):r(self,0x9935+i) for i in IDS})
        if pc in [0x74D62,0x6F34C,0x6F422]:
            source={0x74D62:0x74ED2,0x6F34C:0x6F2C8,0x6F422:0x6F34C}[pc]
            producers=[x for x in self.condition_checked if x['entry']==source]
            assert producers and producers[-1]['call']==self.call,(hex(pc),source,self.call)
            fields={0x74D62:[0x915C],0x6F34C:[0x8FE0,0x8FDF],0x6F422:[0x8FD8]}[pc]
            assert all(r(self,a)==producers[-1]['after'][hex(a)] for a in fields)
            self.freshness.append(dict(call=self.call,producer=source,consumer=pc,values={hex(a):r(self,a) for a in fields}))
        return super().instruction(pc)


def main():
    e=Integrated();e.registers[0xFFFFF74E]=1;e.run(0xCA94);e.write(0xFFFFD800,2,4)
    previous=1;rows=[]
    for i,value in enumerate([1]*10+[0]*15+[1]*15):
        e.call=i;start=len(e.condition_checked)
        try:
            if value!=previous:
                e.registers[0xFFFFF74E]=(e.registers[0xFFFFF74E]&~1)|value
                e.run(0xCADE);e.run(0xCADE)
                assert r(e,0x44A2,2)&1==value
            previous=value;sp=e.r[15];gbr=e.gbr
            e.run(0x2BCE6,0xFFFFD800,limit=1000000)
            assert e.condition_pending is None and e.r[15]==sp and e.gbr==gbr
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            (ROOT/'control-conditions-retained-limit.json').write_text(json.dumps(dict(call=i,status=type(exc).__name__+': '+str(exc),pc=e.pc,tail=e.tail,rows=rows,conditions=e.condition_checked),indent=2)+'\n');raise
        rows.append(dict(call=i,input=value,outer_phase=r(e,0x651C),control_phase=r(e,0x5360),conditions=e.condition_checked[start:]))
    counts={hex(entry):sum(x['entry']==entry for x in e.condition_checked) for entry in ENTRIES}
    assert list(counts.values())==[8,8,8]
    assert len(e.freshness)==24
    total=len(e.condition_checked)+len(e.hold_checked)+len(e.timer_checked)+len(e.checked)
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,complete_outer_calls=40,new_boundaries=counts,total_full_ram_boundaries=total,freshness=e.freshness,rows=rows)
    (ROOT/'control-conditions-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('40 outer calls;',total,'full-RAM boundaries;',counts)

if __name__=='__main__':main()
