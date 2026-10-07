"""Observe stock flag publication and its consumer in original retained outer tasks.

Forty explicit events and synthetic port/SCI/timer samples; not boot/cadence proof.
"""
import hashlib
import json
from pathlib import Path
from verify_control_conditions_retained import Integrated
from verify_control_flag_bank import expected,MAPPING
from verify_control_contributions import ECU,r
from verify_control_raw_inputs import application

ROOT=Path(__file__).resolve().parent


class Bank(Integrated):
    def __init__(self):
        super().__init__();self.bank_pending=None;self.bank_checked=[];self.bank_consumers=[]
    def instruction(self,pc):
        if self.bank_pending is not None and pc==self.bank_pending['return_pc']:
            item=self.bank_pending;self.bank_pending=None
            assert application(self)==item.pop('expected')
            item['after_9125']=r(self,0x9125);self.bank_checked.append(item)
        if pc==0x744C6:
            assert self.bank_pending is None
            self.bank_pending=dict(expected=expected(self),return_pc=self.pr,call=self.call,phase=r(self,0x5360),before_9125=r(self,0x9125))
        if pc==0x6F34C:
            value=int(ECU[MAPPING[0x9125]]==0) if self.bank_checked else 0
            assert r(self,0x9125)==value
            self.bank_consumers.append(dict(call=self.call,phase=r(self,0x5360),value=r(self,0x9125),publications=len(self.bank_checked)))
        return super().instruction(pc)


def main():
    e=Bank();e.registers[0xFFFFF74E]=1;e.run(0xCA94);e.write(0xFFFFD800,2,4)
    previous=1
    for i,value in enumerate([1]*10+[0]*15+[1]*15):
        e.call=i
        try:
            if value!=previous:
                e.registers[0xFFFFF74E]=(e.registers[0xFFFFF74E]&~1)|value
                e.run(0xCADE);e.run(0xCADE)
            previous=value;sp=e.r[15];gbr=e.gbr
            e.run(0x2BCE6,0xFFFFD800,limit=1000000)
            assert e.bank_pending is None and e.r[15]==sp and e.gbr==gbr
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            (ROOT/'control-flag-bank-retained-limit.json').write_text(json.dumps(dict(call=i,status=type(exc).__name__+': '+str(exc),pc=e.pc,tail=e.tail,bank=e.bank_checked,consumers=e.bank_consumers),indent=2)+'\n');raise
    total=len(e.bank_checked)+len(e.condition_checked)+len(e.hold_checked)+len(e.timer_checked)+len(e.checked)
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,complete_outer_calls=40,total_full_ram_boundaries=total,bank=e.bank_checked,consumers=e.bank_consumers)
    (ROOT/'control-flag-bank-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('40 complete outer calls;',total,'full-RAM boundaries; bank:',e.bank_checked,'consumers:',e.bank_consumers)

if __name__=='__main__':main()
