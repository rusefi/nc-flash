"""Original capture ISR prefixes, explicit status/count/profiling samples.

Stop before RTE; no interrupt delivery, hardware status-clear semantics, clock
rate or pin identity. Whole application RAM is compared with the already-tested
original callback plus an independent profiling model: this is differential
handler-to-callback evidence, not a new independent capture-history oracle.
"""
import hashlib
import json
import random
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram

ROOT=Path(__file__).resolve().parent
CHANNELS={
 'A':dict(entry=0x16C7C,stop=0x16CCA,mask=1,capture=0xFFFFF434,callback=0x179A8,index=5,prior=0x88FC),
 'B':dict(entry=0x16B44,stop=0x16B92,mask=2,capture=0xFFFFF438,callback=0x17A58,index=6,prior=0x890C)}


class CaptureSamples:
    """Finite register samples shared by isolated and full-task observers."""
    def __init__(self):
        self.samples={};self.accesses=[]

    def read(self,address,size):
        key=(address & 0xFFFFFFFF,size)
        if key not in self.samples or not self.samples[key]:
            raise ValueError(f'Missing capture sample {key[0]:08X}/{size}')
        value=self.samples[key].pop(0)
        self.accesses.append(['read',key[0],size,value]);return value

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if (address,size)!=(0xFFFFF42C,2):raise ValueError('Capture fixture write')
        self.accesses.append(['write',address,size,value&65535])


class Registers(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.capture_io=CaptureSamples();self.capture_callbacks=[]

    def read(self,address,size):
        if address & 0xFFFFFFFF >= 0xFFFFE000:
            return self.capture_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address & 0xFFFFFFFF >= 0xFFFFE000:
            return self.capture_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if pc in [0x179A8,0x17A58]:self.capture_callbacks.append([pc,self.r[4]])
        return super().instruction(pc)


def run_preserving_prefix(t,entry,stop):
    """Run original instructions to the pre-RTE boundary; verify saved registers."""
    saved,pr,macl,mask=t.r.copy(),t.pr,t.macl,t.sr&~0x301
    pc=entry
    for _ in range(200000):
        if pc==stop:break
        nxt,delay=t.instruction(pc)
        if delay:
            _,nested=t.instruction(pc+2);assert not nested
        pc=nxt
    else:raise AssertionError('Interrupt prefix bound')
    assert TCU[pc:pc+2]==bytes.fromhex('002b')
    assert (t.r,t.pr,t.macl,t.sr&~0x301)==(saved,pr,macl,mask)
    return pc


def execute_prefix(t,channel,status,second,captured,start,end):
    cfg=CHANNELS[channel];armed=bool(status&cfg['mask']);i=cfg['index']
    assert int.from_bytes(TCU[0x5F600+4*i:0x5F604+4*i],'big')==0
    previous=r(t,cfg['prior'],4);maximum=r(t,0x86BC+2*i,2)
    t.capture_callbacks=[];t.capture_io.accesses=[]
    ref=SHRotate(TCU);ref.ram=dict(t.ram)
    w(ref,0x8728+4*i,start,4)
    if armed:ref.run(cfg['callback'],captured,limit=200000)
    duration=min(65535,((end-start)&0xFFFFFFFF)//10)
    w(ref,0x8698+2*i,duration,2);w(ref,0x86BC+2*i,max(maximum,duration),2)
    t.capture_io.samples={(0xFFFFF42C,2):[status,second] if armed else [status],
               (0xFFFFF6C0,4):[start,end]}
    if armed:t.capture_io.samples[(cfg['capture'],4)]=[captured]
    pc=run_preserving_prefix(t,cfg['entry'],cfg['stop'])
    assert ram(t)==ram(ref)
    assert t.capture_callbacks==([[cfg['callback'],captured]] if armed else [])
    expected=[['read',0xFFFFF6C0,4,start],['read',0xFFFFF42C,2,status]]
    if armed:
        expected += [['read',0xFFFFF42C,2,second],['write',0xFFFFF42C,2,second&~cfg['mask']],
                     ['read',cfg['capture'],4,captured]]
    expected += [['read',0xFFFFF6C0,4,end]]
    assert t.capture_io.accesses==expected and all(not v for v in t.capture_io.samples.values())
    return dict(channel=channel,status=status,second_status=second,callback=armed,
                captured=captured,previous=previous,profile_duration=duration,
                accesses=t.capture_io.accesses,stopped_before_rte=hex(pc))


def check(channel,status,second,captured,start,end,previous,maximum):
    cfg=CHANNELS[channel];armed=bool(status&cfg['mask']);i=cfg['index']
    assert int.from_bytes(TCU[0x5F600+4*i:0x5F604+4*i],'big')==0
    t=Registers();t.run(0x20658);t.run(0x211C4)
    for a,v,n in [(cfg['prior'],previous,4),(0x86BC+2*i,maximum,2),
                  (0x86E0+2*i,0xA55A,2),(0x8704+2*i,0x5AA5,2)]:w(t,a,v,n)
    t.r[:15]=[(0x12345678+0x11111111*j)&0xFFFFFFFF for j in range(15)]
    t.macl=0x87654321;t.pr=0x12345678;t.sr=0xF1
    return execute_prefix(t,channel,status,second,captured,start,end)


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rng=random.Random(0x16C7C);count=0;examples=[]
    times=[(0,9),(1000,2000),(0xFFFFFF00,500),(0,0xFFFFFFFF)]
    for channel in CHANNELS:
        for low in range(256):
            start,end=times[low%4]
            previous=rng.randrange(2**32)
            captured=(previous+[0,1,9,10,12160,0xFFFFFFFF][low%6])&0xFFFFFFFF
            row=check(channel,0xA500|low,rng.randrange(65536),captured,start,end,previous,
                      [0,100,65535][low%3])
            if low in [0,1,2,3,255]:examples.append(row)
            count+=1
    rejected=0
    for address,size,write in [(0xFFFFF42C,1,False),(0xFFFFF434,2,False),
                               (0xFFFFF438,4,False),(0xFFFFF6C0,4,False),
                               (0xFFFFF434,4,True),(0xFFFFF42C,1,True)]:
        t=Registers()
        try:
            t.write(address,0,size) if write else t.read(address,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Fixture accepted unspecified access')
    result=dict(status='PASS',scope=__doc__,differential_whole_application_ram_cases=count,
                predicate_set_cases=count//2,clear_cases=count//2,rejected_accesses=rejected,
                examples=examples,rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-capture-interrupt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='examples'},indent=2))


if __name__=='__main__':main()
