"""Original14452/14466 bus setup under explicit bounded configuration inputs."""
import hashlib
import json
import random
from pathlib import Path
from tcu_startup_bsc import Registers
from verify_tcu_ubc_startup import Machine as UBCMachine
from verify_control_acquisition_schedule import execute_slice
from verify_tcu_base_publication import ram
from verify_can201_byte6 import TCU,w

ROOT=Path(__file__).resolve().parent


class Machine(UBCMachine):
    def __init__(self,initial):
        super().__init__();self.bsc=Registers(wcr_initial=initial)

    def read(self,address,size):
        if address in self.bsc.values:return self.bsc.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address in self.bsc.values:return self.bsc.write(address,value,size)
        return super().write(address,value,size)


def main():
    rng=random.Random(0x14452);cases=0
    for initial in [0,0x7777,0xFFFF,0x3333]:
        for _ in range(64):
            t=Machine(initial);t.r[:15]=[rng.randrange(1<<32) for _ in range(15)]
            t.sr=0xF0|rng.randrange(2)
            t.bsc.values[0xFFFFEC20]=rng.randrange(16)
            t.bsc.values[0xFFFFEC22]=rng.randrange(65536)
            t.ubc.values[0xFFFFEC0A]=rng.randrange(8)
            for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,rng.randrange(256))
            before=ram(t);regs=t.r.copy();sr=t.sr;pr=t.pr
            execute_slice(t,0x14452,0xFFFFFFF0)
            for n,v in {0:0xFFFFEC0A,1:0xFFFFEC20,2:7,3:0xFFFFEC22}.items():regs[n]=v
            assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
            assert t.bsc.values=={0xFFFFEC20:15,0xFFFFEC22:7,0xFFFFEC24:initial}
            assert t.bsc.accesses==[['write',0xFFFFEC20,2,15],['write',0xFFFFEC22,2,7]]
            assert t.ubc.accesses==[['write',0xFFFFEC0A,2,0]]
            execute_slice(t,0x14466,0xFFFFFFF0)
            regs[0]=0xFFFFEC24;regs[1]=0x3333
            assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
            assert t.bsc.values=={0xFFFFEC20:15,0xFFFFEC22:7,0xFFFFEC24:0x3333}
            assert t.bsc.accesses[-1]==['write',0xFFFFEC24,2,0x3333]
            cases+=1
    rejected=0
    bad=[(0xFFFFEC20,2,1<<b) for b in range(4,16)]
    bad += [(0xFFFFEC20,1,0),(0xFFFFEC20,4,0),(0xFFFFEC21,2,0),(0xFFFFEC26,2,0)]
    for a,size,value in bad:
        owner=Registers(wcr_initial=0);before=owner.values.copy()
        try:owner.write(a,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported BSC write accepted')
        assert owner.values==before and not owner.accesses
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        original_function_pairs=cases,whole_ram_register_function_returns=2*cases,
        rejected_accesses=rejected,explicit_wcr_initials=[0,0x7777,0xFFFF,0x3333],
        limits='Configuration writes only. WCR reset-source conflict preserved. No external bus timing/CS/pin cycles/RAM emulation/full15574 proof.')
    (ROOT/'tcu-bsc-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
