"""Original ECU F758..F760 VBR/FPSCR prefix and compatible CMT1 vector binding.

Isolated startup slice, not reset reachability or physical IRQ acceptance.
Reuse tested LDC implementation from TCU setup without its MMIO fixture.
"""
import hashlib
import json
import random
from pathlib import Path
from sh_control_interrupt import ControlInterrupt,execute_to
from verify_tcu_interrupt_setup import Machine
from verify_control_contributions import ECU


class VectorPrefix(ControlInterrupt):
    def __init__(self):
        super().__init__();self.vbr=0
    def instruction(self,pc):
        if self.read(pc,2)&0xF0FF==0x402E:return Machine.instruction(self,pc)
        return super().instruction(pc)


def main():
    for seed in range(256):
        e=VectorPrefix();rng=random.Random(seed)
        e.r=[rng.randrange(1<<32) for _ in range(16)];e.vbr=rng.randrange(1<<32)
        e.fpscr=(rng.randrange(1<<32)&0x18C60)|0x40001;e.sr=seed&0x3F3
        registers=e.r.copy();registers[3]=0xFFC50;registers[2]=0x40001
        memory=e.ram.copy();saved=(e.fr.copy(),e.fpul,e.gbr,e.macl,e.mach,e.pr,e.sr)
        assert execute_to(e,0xF758,{0xF760})==0xF760
        assert e.r==registers and e.ram==memory and e.vbr==0xFFC50 and e.fpscr==0x40001
        assert (e.fr,e.fpul,e.gbr,e.macl,e.mach,e.pr,e.sr)==saved
        assert e.read(e.vbr+192*4,4)==0x2F78
    report=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        original_prefix_cases=256,vbr=0xFFC50,compatible_cmt1_vector=192,
        pointer_address=0xFFF50,wrapper=0x2F78,
        source='SH7058 REJ09B0046-0300H table7.3 printed113/PDFzero155; CMTI1 vector192,IPRJbits7..4',
        limits='Chip compatibility, resetpath, INTCpriority and hardwareacceptance unproved.')
    Path(__file__).with_name('control-interrupt-vector-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report)


if __name__=='__main__':main()
