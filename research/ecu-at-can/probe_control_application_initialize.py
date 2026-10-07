"""Bounded original1619A application-initializer probe; no callee stubs.

Zero RAM plus existing typed MMIO and explicit SCI0/TCNT0 samples. This is
an exploratory execution fixture, not reset/boot or external-controller proof.
"""
import hashlib
import json
from pathlib import Path
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r
from verify_control_flag_bank import expected
from verify_control_raw_inputs import application

ROOT=Path(__file__).resolve().parent
TARGETS=[0xCA94,0x744C6,0x74ED2,0x6F29C,0x6F2C8,0x6F34C,0x6F422,0x2C468,0x42A78]

class Initialize(Hooks):
    def __init__(self):
        super().__init__();self.initializer_entries=[];self.initializer_calls=[]
        self.bank_pending=None;self.bank_checked=[];self.fpu_limit_inputs=[]
    def instruction(self,pc):
        if self.bank_pending is not None and pc==self.bank_pending['return_pc']:
            item=self.bank_pending;self.bank_pending=None
            assert application(self)==item.pop('expected')
            item['after_9125']=r(self,0x9125);self.bank_checked.append(item)
        if pc==0x744C6:
            assert self.bank_pending is None
            self.bank_pending=dict(expected=expected(self),return_pc=self.pr,before_9125=r(self,0x9125))
        if pc==0x28F7A:
            self.fpu_limit_inputs.append(dict(pc=pc,opcode=self.read(pc,2),fr10=self.fr[10],fr11=self.fr[11],r14=self.r[14]))
        if self.read(pc,2)==0x0018:  # Renesas SETT; local probe extension only
            self.sr|=1;self.visited.add(pc)
            return pc+2,False
        if pc in TARGETS:self.initializer_entries.append(dict(pc=pc,pr=self.pr,sp=self.r[15]))
        op=self.read(pc,2)
        if 0x1619A<=pc<0x17880 and op&0xF0FF==0x400B:
            self.initializer_calls.append(dict(pc=pc,target=self.r[(op>>8)&15]))
        return super().instruction(pc)


def main():
    e=Initialize();e.registers[0xFFFFF74E]=1;sp=e.r[15];gbr=e.gbr
    try:
        e.run(0x1619A,limit=2000000);status='returned'
        assert e.r[15]==sp and e.gbr==gbr
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:status=type(exc).__name__+': '+str(exc)
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,status=status,pc=e.pc,tail=e.tail,registers=e.r,
        entries=e.initializer_entries,calls=e.initializer_calls,accesses=e.accesses,
        bank=e.bank_checked,fpu_limit_inputs=e.fpu_limit_inputs,float_registers=e.fr,
        fields={hex(a):r(e,a,size) for a,size in [(0x535C,4),(0x9125,1),(0x9158,2),(0x915E,1),(0x8FD4,2),(0x6605,1),(0x735C,1)]})
    (ROOT/'control-application-initialize-probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(status,hex(e.pc),'direct calls',len(e.initializer_calls),'entries',e.initializer_entries)

if __name__=='__main__':main()
