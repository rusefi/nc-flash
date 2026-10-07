"""Original145FE interval setup: independent full RAM/register/MMIO checks."""
import hashlib
import json
import random
from pathlib import Path
from sh_rotate import SHRotate
from tcu_startup_interval import Registers
from verify_can201_byte6 import TCU,w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.interval=Registers()

    def read(self,address,size):
        if address>=0xFFFFE000:return self.interval.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address>=0xFFFFE000:return self.interval.write(address,value,size)
        return super().write(address,value,size)


def main():
    rng=random.Random(0x145FE)
    addresses=[0xFFFFF424,0xFFFFF426,0xFFFFF428]
    for value in range(256):
        t=Machine();t.r[:15]=[rng.randrange(1<<32) for _ in range(15)]
        t.sr=0xF0|rng.randrange(2)
        t.interval.values=dict(zip(addresses,[value,255-value,value^0x55]))
        for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,rng.randrange(256))
        before=ram(t);regs=t.r.copy();sr=t.sr;pr=t.pr
        for n,v in {1:0xFFFFF428,2:0xFFFFF426,3:0xFFFFF424,4:0}.items():regs[n]=v
        execute_slice(t,0x145FE,0xFFFFFFF0)
        assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
        assert t.interval.values=={a:0 for a in addresses}
        assert t.interval.accesses==[['write',a,1,0] for a in addresses]
    roundtrips=0
    for a in addresses:
        for value in range(256):
            owner=Registers();owner.write(a,value,1)
            assert owner.read(a,1)==value
            assert all(v==0 for b,v in owner.values.items() if b!=a)
            roundtrips+=1
    rejected=0
    for a,size in [(a,s) for a in addresses for s in (2,4)]+[(0xFFFFF425,1),(0xFFFFF42A,1)]:
        for op in ('read','write'):
            owner=Registers();before=owner.values.copy()
            try:
                if op=='read':owner.read(a,size)
                else:owner.write(a,0,size)
            except ValueError:rejected+=1
            else:raise AssertionError('Unsupported access accepted')
            assert owner.values==before and not owner.accesses
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        original_whole_ram_register_cases=256,register_roundtrips=roundtrips,
        rejected_accesses=rejected,limits='No counter edges, ADC events, physical IRQ admission or full15574 completion.')
    (ROOT/'tcu-interval-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
