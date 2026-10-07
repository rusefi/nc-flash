"""Original CMT0 initialization and interrupt-prefix mode admission.

Explicit status/profiling register samples; stop before RTE. Whole RAM compares
with original128B6 plus independent1->3 mode transition and profiling equations.
This does not independently model all11A64 timer effects or prove clock units,
hardware interrupt delivery, timer side effects or application scheduling.
"""
import hashlib
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_tcu_capture_interrupts import CaptureSamples,run_preserving_prefix

ROOT=Path(__file__).resolve().parent


class Samples(CaptureSamples):
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if size!=2 or address not in [0xFFFFF710,0xFFFFF712,0xFFFFF716]:
            raise ValueError('CMT0 fixture write')
        self.accesses.append(['write',address,size,value&65535])


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU);self.cmt_io=Samples();self.cmt_entries=[]

    def read(self,address,size):
        if (address & 0xFFFFFFFF)>=0xFFFFE000:return self.cmt_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if (address & 0xFFFFFFFF)>=0xFFFFE000:return self.cmt_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if pc in [0x123C2,0x128B6,0x11864,0x1E506,0x11A64]:self.cmt_entries.append(hex(pc))
        return super().instruction(pc)


def execute_prefix(t,status,second,start,end):
    """Execute the native prefix with finite inputs and differential whole RAM."""
    assert int.from_bytes(TCU[0x5F630:0x5F634],'big')==0
    mode=r(t,0x800A);tick=r(t,0x84D0,4);elapsed=r(t,0x91AC,2)
    maximum=r(t,0x86D4,2);armed=bool(status&128)
    t.cmt_entries=[];t.cmt_io.accesses=[]
    ref=SHRotate(TCU);ref.ram=dict(t.ram);w(ref,0x8758,start,4)
    if armed:
        w(ref,0x800A,3 if mode==1 else mode)
        ref.run(0x128B6,limit=200000)
    duration=min(65535,((end-start)&0xFFFFFFFF)//10)
    w(ref,0x86B0,duration,2);w(ref,0x86D4,max(maximum,duration),2)
    t.cmt_io.samples={(0xFFFFF6C0,4):[start,end],(0xFFFFF712,2):[status,second] if armed else [status]}
    run_preserving_prefix(t,0x16D6C,0x16DB6)
    assert ram(t)==ram(ref)
    active=armed and mode in [1,3]
    assert r(t,0x800A)==(3 if armed and mode==1 else mode)
    assert r(t,0x84D0,4)==(tick+int(active))&0xFFFFFFFF
    assert r(t,0x91AC,2)==min(65535,elapsed+int(active))
    assert t.cmt_entries==(['0x123c2','0x128b6']+(['0x11864','0x1e506','0x11a64'] if active else []) if armed else [])
    accesses=[['read',0xFFFFF6C0,4,start],['read',0xFFFFF712,2,status]]
    if armed:accesses += [['read',0xFFFFF712,2,second],['write',0xFFFFF712,2,second&0xFF7F]]
    accesses += [['read',0xFFFFF6C0,4,end]]
    assert t.cmt_io.accesses==accesses and all(not x for x in t.cmt_io.samples.values())
    return dict(mode=mode,armed=armed,active=active,entries=t.cmt_entries,
                tick=r(t,0x84D0,4),elapsed=r(t,0x91AC,2))


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    assert int.from_bytes(TCU[0x5F630:0x5F634],'big')==0
    init_count=0
    for entry in [0x16D5C,0x123B0]:
        for low in range(256):
            t=Machine();old=0xA500|low;t.cmt_io.samples={(0xFFFFF710,2):[old]}
            for address,value,size in [(0x800A,low,1),(0x84D0,0xABCDEF01,4),
                        (0x84D4,9,1),(0x84D5,8,1),(0x84D6,7,1),(0x91AC,1234,2)]:
                w(t,address,value,size)
            ref=SHRotate(TCU);ref.ram=dict(t.ram)
            if entry==0x123B0:
                for address,value,size in [(0x800A,1,1),(0x84D0,0,4),
                           (0x84D4,0,1),(0x84D5,0,1),(0x84D6,0,1)]:w(ref,address,value,size)
            t.run(entry)
            assert ram(t)==ram(ref) and not t.cmt_io.samples[(0xFFFFF710,2)]
            assert t.cmt_io.accesses==[['write',0xFFFFF716,2,624],['read',0xFFFFF710,2,old],['write',0xFFFFF710,2,old|1]]
            init_count+=1
    cases=0;examples=[]
    for case,mode in enumerate(list(range(256))+[1,3]):
        for armed in [False,True]:
            t=Machine();status=0xA500|int(armed)*128;second=0xBEEF
            start,end=(0xFFFFFF00,500) if mode%2 else (1000,2000)
            tick=[0,100,0xFFFFFFFF][mode%3];elapsed=[0,65534,65535][mode%3]
            if case>=256:tick,elapsed=0xFFFFFFFF,65535
            for a,v,n in [(0x800A,mode,1),(0x84D0,tick,4),(0x91AC,elapsed,2),
                          (0x84D4,mode%10,1),(0x86D4,500,2),(0x86F8,0xA55A,2),(0x871C,0x5AA5,2)]:w(t,a,v,n)
            for index,a in enumerate(range(0x8420,0x844E,2)):w(t,a,[0,1,99,65535][index%4],2)
            t.r[:15]=[(0x12345678+i*0x11111111)&0xFFFFFFFF for i in range(15)]
            t.pr=0x12345678;t.macl=0x87654321;t.sr=0xF1
            event=execute_prefix(t,status,second,start,end)
            if mode in [0,1,2,3,255]:examples.append(event)
            cases+=1
    result=dict(status='PASS',scope=__doc__,initialization_cases=init_count,
                differential_whole_application_ram_cases=cases,examples=examples,
                rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-cmt0-interrupt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
