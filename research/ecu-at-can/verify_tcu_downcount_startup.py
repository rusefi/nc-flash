"""Original14972 DSTR and1460E TCNR: independent RAM/register/MMIO checks."""
import hashlib
import json
import random
from pathlib import Path
from sh_rotate import SHRotate
from tcu_startup_connection import Registers as ConnectionRegisters
from tcu_startup_downcount import Registers
from verify_can201_byte6 import TCU,w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent


class Machine(SHRotate):
    def __init__(self,initial):
        super().__init__(TCU)
        self.downcount=Registers(initial)
        self.connection=ConnectionRegisters()

    def read(self,address,size):
        if address in self.connection.values:return self.connection.read(address,size)
        if address>=0xFFFFE000:return self.downcount.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address in self.connection.values:return self.connection.write(address,value,size)
        if address>=0xFFFFE000:return self.downcount.write(address,value,size)
        return super().write(address,value,size)


def main():
    rng=random.Random(0x14972)
    initials=[0,65535,0x5555,0xAAAA]+[1<<n for n in range(16)]+[rng.randrange(65536) for _ in range(236)]
    for initial in initials:
        t=Machine(initial);t.r[:15]=[rng.randrange(1<<32) for _ in range(15)]
        t.sr=0xF0|rng.randrange(2)
        for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,rng.randrange(256))
        before=ram(t);regs=t.r.copy();sr=t.sr;pr=t.pr
        regs[0]=0xFFFFF666;regs[2]=0
        execute_slice(t,0x14972,0xFFFFFFF0)
        assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
        assert t.downcount.values=={0xFFFFF666:initial}
        assert t.downcount.accesses==[['write',0xFFFFF666,2,0]]
        t.connection.values[0xFFFFF662]=initial
        regs=t.r.copy();regs[2]=0xFFFFF662;regs[3]=0
        execute_slice(t,0x1460E,0xFFFFFFF0)
        assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
        assert t.connection.values=={0xFFFFF662:0}
        assert t.connection.accesses==[['write',0xFFFFF662,2,0]]
        assert t.downcount.values=={0xFFFFF666:initial}
    for initial in range(65536):
        owner=Registers(initial);owner.write(owner.ADDRESS,0,2)
        assert owner.read(owner.ADDRESS,2)==initial
    rejected=0
    bad=[(0xFFFFF666,2,1<<n) for n in range(16)]+[(0xFFFFF666,1,0),(0xFFFFF666,4,0),(0xFFFFF664,2,0),(0xFFFFF667,2,0)]
    for address,size,value in bad:
        owner=Registers(0xFFFF);before=owner.values.copy()
        try:owner.write(address,value,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported DSTR write accepted')
        assert owner.values==before and not owner.accesses
    roundtrips=0
    for value in initials:
        owner=ConnectionRegisters();owner.write(0xFFFFF662,value,2)
        assert owner.read(0xFFFFF662,2)==value
        roundtrips+=1
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        original_whole_ram_register_cases=2*len(initials),connection_roundtrips=roundtrips,zero_write_read_cases=65536,
        rejected_writes=rejected,limits='No new down-count starts, decrement, reload, terminate or interrupt events; sampled state only.')
    (ROOT/'tcu-downcount-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
