"""Original14476 DMAOR write and independently specified flag-clear sequences."""
import hashlib,json
from pathlib import Path
from tcu_startup_dmaor import Registers
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent
A=0xFFFFECB0


class Machine(SHRotate):
    def __init__(self,initial):super().__init__(TCU);self.dmaor=Registers(initial)
    def read(self,address,size):
        if address>=0xFFFFE000:return self.dmaor.read(address,size)
        return super().read(address,size)
    def write(self,address,value,size):
        if address>=0xFFFFE000:return self.dmaor.write(address,value,size)
        return super().write(address,value,size)


def main():
    sequences=originals=rejects=0
    for initial in range(8):
        for read_first in [False,True]:
            for enabled in [0,1]:
                t=Machine(initial)
                if read_first:assert t.dmaor.read(A,2)==initial
                t.dmaor.write(A,enabled,2)
                expected=enabled
                if not read_first:
                    for bit in [1,2]:
                        if initial&(1<<bit):expected|=1<<bit
                assert t.dmaor.read(A,2)==expected
                t.dmaor.write(A,0,2)
                assert t.dmaor.read(A,2)==0
                sequences+=1
            for sr in [0,1,0xF0,0xF1]:
                t=Machine(initial);t.sr=sr
                if read_first:t.dmaor.read(A,2)
                t.dmaor.accesses=[]
                for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,(a+initial)&255)
                before=ram(t);regs=t.r.copy();pr=t.pr;regs[2]=A;regs[3]=0
                execute_slice(t,0x14476,0xFFFFFFF0)
                assert ram(t)==before and t.r==regs and t.sr==sr and t.pr==pr
                assert t.dmaor.values[A]==(0 if read_first else initial&6)
                assert t.dmaor.accesses==[['write',A,2,0]]
                originals+=1
    for address,size,value in [(A,2,1<<b) for b in range(1,16)]+[(A,1,0),(A,4,0),(A+2,2,0)]:
        owner=Registers();before=owner.values.copy()
        try:owner.write(address,value,size)
        except ValueError:rejects+=1
        else:raise AssertionError('Unsupported DMAOR write accepted')
        assert owner.values==before and not owner.accesses
    result=dict(status='PASS',rom_sha256=hashlib.sha256(TCU).hexdigest(),original_whole_ram_register_cases=originals,
        flag_clear_sequences=sequences,rejected_accesses=rejects,
        limits='Seeded status/no new events; no DMA transfers/channel reload counters. Writes with status-one unsupported.14476 initializesDMAOR only, not full15574.')
    (ROOT/'tcu-dmaor-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result)


if __name__=='__main__':main()
