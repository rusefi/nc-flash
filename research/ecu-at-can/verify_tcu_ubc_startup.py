"""Original UBC initialization with independent RAM/register/MMIO expectations."""
import hashlib
import json
import random
from pathlib import Path
from tcu_startup_ubc import Registers
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.ubc=Registers()

    def read(self,address,size):
        if address>=0xFFFFE000:return self.ubc.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address>=0xFFFFE000:return self.ubc.write(address,value,size)
        return super().write(address,value,size)


def main():
    rng=random.Random(0x14432)
    masks={0xFFFFEC00:65535,0xFFFFEC02:65535,0xFFFFEC04:65535,0xFFFFEC06:65535,0xFFFFEC08:255,0xFFFFEC0A:7}
    specs=[(0x14432,0xFFFFFFF0,[0xFFFFEC00,0xFFFFEC02],{2:0xFFFFEC02,3:0xFFFFEC00,4:0}),
           (0x1443E,0xFFFFFFF0,[0xFFFFEC04,0xFFFFEC06],{2:0xFFFFEC06,3:0xFFFFEC04,4:0}),
           (0x1444A,0xFFFFFFF0,[0xFFFFEC08],{1:0xFFFFEC08,3:0}),
           (0x14452,0x14458,[0xFFFFEC0A],{0:0xFFFFEC0A,2:0})]
    cases=0
    for begin,end,addresses,changes in specs:
        for _ in range(128):
            t=Machine();t.r[:15]=[rng.randrange(1<<32) for _ in range(15)];t.sr=rng.randrange(2)|0xF0
            t.ubc.values={a:rng.randrange(mask+1) for a,mask in masks.items()}
            for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,rng.randrange(256))
            expected=t.ubc.values.copy()
            for a in addresses:expected[a]=0
            saved=ram(t);regs=t.r.copy();sr=t.sr;pr=t.pr
            for n,v in changes.items():regs[n]=v
            execute_slice(t,begin,end)
            assert ram(t)==saved and t.r==regs and t.sr==sr and t.pr==pr
            assert t.ubc.values==expected
            assert t.ubc.accesses==[['write',a,2,0] for a in addresses]
            cases+=1
    roundtrips=0
    for a,mask in masks.items():
        for value in sorted({0,1,mask,mask//2,*[1<<bit for bit in range(mask.bit_length())]}):
            owner=Registers();owner.write(a,value,2)
            assert owner.read(a,2)==value
            assert all(v==0 for address,v in owner.values.items() if address!=a)
            roundtrips+=1
    rejected=0
    bad=[(a,2,1<<bit) for a,first in [(0xFFFFEC08,8),(0xFFFFEC0A,3)] for bit in range(first,16)]
    bad += [(0xFFFFEC00,1,0),(0xFFFFEC00,4,0),(0xFFFFEC01,2,0),(0xFFFFEC0C,2,0)]
    for a,size,value in bad:
        owner=Registers();before=owner.values.copy()
        try:owner.write(a,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported write accepted')
        assert owner.values==before and not owner.accesses
    for a,size in [(0xFFFFEC00,1),(0xFFFFEC00,4),(0xFFFFEC01,2),(0xFFFFEC0C,2)]:
        try:Registers().read(a,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported read accepted')
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        original_whole_ram_register_mmio_cases=cases,control_roundtrips=roundtrips,
        rejected_accesses=rejected,
        limits='14432/1443E/1444A complete;14452 only through14458 before BSC. Bounded configuration latches, no userbreak matching/IRQ/pin timing/full15574.')
    (ROOT/'tcu-ubc-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
