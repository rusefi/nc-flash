"""Original CMT1 initialization/ISR prefix against independent whole RAM.

Finite status/profiling inputs; stop before RTE. Reuses the existing independent
primary-wheel schedule. No hardware interrupt delivery, clock units or cadence.
"""
import hashlib
import json
from pathlib import Path
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_tcu_capture_interrupts import CaptureSamples,run_preserving_prefix
from verify_tcu_request_timing import RANGES,advance_model

ROOT=Path(__file__).resolve().parent


class Samples(CaptureSamples):
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if size!=2 or address not in [0xFFFFF710,0xFFFFF718,0xFFFFF71C]:
            raise ValueError('CMT1 fixture write')
        self.accesses.append(['write',address,size,value&65535])


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU);self.cmt1_io=Samples();self.cmt1_entries=[]

    def read(self,address,size):
        if (address & 0xFFFFFFFF)>=0xFFFFE000:return self.cmt1_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if (address & 0xFFFFFFFF)>=0xFFFFE000:return self.cmt1_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if pc in [0x12386,0x12886,0x11014]:self.cmt1_entries.append(hex(pc))
        return super().instruction(pc)


def execute_prefix(t,status,second,start,end):
    assert int.from_bytes(TCU[0x5F634:0x5F638],'big')==0
    mode=r(t,0x8009);armed=bool(status&128);active=armed and mode in [1,3]
    maximum=r(t,0x86D6,2)
    t.cmt1_entries=[];t.cmt1_io.accesses=[]
    ref=SHRotate(TCU);ref.ram=dict(t.ram);w(ref,0x875C,start,4)
    if armed:w(ref,0x8009,3 if mode==1 else mode)
    if active:advance_model(ref)
    duration=min(65535,((end-start)&0xFFFFFFFF)//10)
    w(ref,0x86B2,duration,2);w(ref,0x86D6,max(maximum,duration),2)
    t.cmt1_io.samples={(0xFFFFF6C0,4):[start,end],
                      (0xFFFFF718,2):[status,second] if armed else [status]}
    run_preserving_prefix(t,0x16CF4,0x16D3E)
    assert ram(t)==ram(ref),('CMT1 independent RAM',mode,armed)
    assert t.cmt1_entries==(['0x12386','0x12886']+(['0x11014'] if active else []) if armed else [])
    accesses=[['read',0xFFFFF6C0,4,start],['read',0xFFFFF718,2,status]]
    if armed:accesses += [['read',0xFFFFF718,2,second],['write',0xFFFFF718,2,second&0xFF7F]]
    accesses += [['read',0xFFFFF6C0,4,end]]
    assert t.cmt1_io.accesses==accesses and all(not x for x in t.cmt1_io.samples.values())
    return dict(mode=mode,armed=armed,active=active,entries=t.cmt1_entries,
                phases=[r(t,a,4) for a in [0x8494,0x8498,0x849C]],
                counter90c8=r(t,0x90C8,2),profile_duration=duration)


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    init_count=0
    for entry in [0x16CE4,0x12374]:
        for low in range(256):
            t=Machine();old=0xA500|low;t.cmt1_io.samples={(0xFFFFF710,2):[old]}
            for a,v,n in [(0x8009,low,1),(0x8494,0x12345678,4),(0x8498,0xDEADBEEF,4),
                          (0x849C,1,4),(0x84D0,123456,4),(0x91AC,1234,2),(0x90C8,65535,2)]:w(t,a,v,n)
            ref=SHRotate(TCU);ref.ram=dict(t.ram)
            if entry==0x12374:
                w(ref,0x8009,1)
                for a in [0x8494,0x8498,0x849C]:w(ref,a,0,4)
            t.run(entry)
            assert ram(t)==ram(ref)
            assert t.cmt1_io.accesses==[['write',0xFFFFF71C,2,1279],
                                      ['read',0xFFFFF710,2,old],['write',0xFFFFF710,2,old|2]]
            assert all(not v for v in t.cmt1_io.samples.values())
            init_count+=1
    cases=[(mode,armed,mode) for mode in range(256) for armed in [False,True]]
    cases += [(1 if phase%2 else 3,True,phase) for phase in range(512)]
    examples=[]
    for case,(mode,armed,phase) in enumerate(cases):
        t=Machine()
        for a in range(0x8100,0x84A8):w(t,a,(a*37+case*19)&255)
        for start,end,size,cap,_,_ in RANGES:
            for i,a in enumerate(range(start,end,size)):
                w(t,a,[0,cap-1,cap,(1<<(8*size))-1][(i+case)%4],size)
        for a,v,n in [(0x8009,mode,1),(0x8494,phase%16,4),(0x8498,(phase//16)%16,4),
                      (0x849C,phase//256,4),(0x90C8,[0,1,65534,65535][case%4],2),
                      (0x84D0,123456,4),(0x91AC,1234,2),(0x86D6,500,2),
                      (0x86FA,0xA55A,2),(0x871E,0x5AA5,2)]:w(t,a,v,n)
        start,end=[(1000,1000),(1000,2000),(0xFFFFFF00,500),(100,900100)][case%4]
        t.r[:15]=[(0x12345678+i*0x11111111)&0xFFFFFFFF for i in range(15)]
        t.pr=0x12345678;t.macl=0x87654321;t.sr=0xF1
        event=execute_prefix(t,0xA500|int(armed)*128,0xBEEF,start,end)
        if case in [0,2,3,6,7,510,511,512,767,1023]:examples.append(dict(case=case,**event))
    rejections=0
    for address,size in [(0xFFFFF718,1),(0xFFFFF718,4),(0xFFFFF712,2)]:
        owner=Samples();owner.samples={(0xFFFFF718,2):[128]}
        try:owner.read(address,size)
        except ValueError:rejections+=1
        else:raise AssertionError('Unexpected read accepted')
    for address,size in [(0xFFFFF718,1),(0xFFFFF718,4),(0xFFFFF712,2)]:
        try:Samples().write(address,0,size)
        except ValueError:rejections+=1
        else:raise AssertionError('Unexpected write accepted')
    result=dict(status='PASS',scope=__doc__,initialization_cases=init_count,
        independent_whole_application_ram_prefix_cases=len(cases),
        valid_primary_phase_combinations=512,access_rejections=rejections,examples=examples,
        rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-cmt1-interrupt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
