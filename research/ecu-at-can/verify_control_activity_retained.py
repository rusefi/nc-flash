"""Check mode and edge oracles at actual outer-task return boundaries.

Forty explicit event2 deliveries; PFDR transitions sampled by original CADE
called twice. Sampling/call order is a fixture, not physical cadence or boot.
"""
import hashlib
import json
from pathlib import Path
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent


class Boundaries(Hooks):
    def __init__(self):
        super().__init__();self.pending=None;self.checked=[]

    def instruction(self,pc):
        if self.pending is not None and pc==self.pending['return_pc']:
            item=self.pending;self.pending=None
            assert application(self)==item.pop('expected'),hex(item['entry'])
            item['current']=r(self,0x735B);item['previous']=r(self,0x735E)
            item['counters']=[r(self,a) for a in [0x660E,0x660F,0x6610,0x6611]]
            self.checked.append(item)
        if pc in [0x42B36,0x42BCC,0x42C68,0x42CBE]:
            assert self.pending is None
            want=application(self)
            if pc==0x42B36:
                mode=128 if r(self,0x735C)==0 or r(self,0x6604)==1 else 64 if r(self,0x6536)==0 or r(self,0x73C4)&128 else 32
                expected_write(want,0x735A,mode,1)
            elif pc==0x42BCC:
                mode=r(self,0x735A)
                flag=int(bool(mode&0x60) or r(self,0x735C)==1 or bool(mode&0x80) and any(r(self,a)==1 for a in [0x82A8,0xA433,0x9149]))
                expected_write(want,0x735B,flag,1)
            else:
                old,current=r(self,0x735E),r(self,0x735B)
                expected_write(want,0x735E,current,1)
                address=0x660E if old==0 and current==1 else 0x660F if old==1 and current==0 else None
                if address is not None:expected_write(want,address,(r(self,address)+1)%256,1)
            self.pending=dict(entry=pc,return_pc=self.pr,expected=want,
                inputs={hex(a):r(self,a) for a in [0x735A,0x735B,0x735C,0x735E,0x6604,0x6536,0x73C4,0x82A8,0xA433,0x9149]})
        return super().instruction(pc)


def main():
    e=Boundaries();e.registers[0xFFFFF74E]=1;e.run(0xCA94);e.write(0xFFFFD800,2,4)
    previous=1;rows=[]
    for i,value in enumerate([1]*10+[0]*15+[1]*15):
        start=len(e.checked);events=len(e.descriptors)
        try:
            if value!=previous:
                e.registers[0xFFFFF74E]=(e.registers[0xFFFFF74E]&~1)|value
                e.run(0xCADE);e.run(0xCADE)
                assert r(e,0x44A2,2)&1==value
            previous=value
            saved=e.r[8:16].copy();gbr=e.gbr
            e.run(0x2BCE6,0xFFFFD800,limit=1000000)
            assert e.pending is None and e.r[8:16]==saved and e.gbr==gbr
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            (ROOT/'control-activity-retained-limit.json').write_text(json.dumps(dict(call=i,input=value,status=type(exc).__name__+': '+str(exc),pc=e.pc,tail=e.tail,registers=e.r,rows=rows),indent=2)+'\n')
            raise
        rows.append(dict(call=i,input=value,phase=r(e,0x651C),state=r(e,0x99FC),hold=r(e,0x735C),boundaries=e.checked[start:],descriptors=e.descriptors[events:]))
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,complete_outer_calls=len(rows),verified_boundaries=len(e.checked),rows=rows)
    (ROOT/'control-activity-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(len(rows),'complete outer calls;',len(e.checked),'mode/flag/edge boundaries')

if __name__=='__main__':main()
