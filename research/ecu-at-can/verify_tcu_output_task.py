"""Original output task, ADC history scan and compare-interrupt callback body.

Explicit result/status/timestamp latches; stop before RTE. No interrupt delivery,
clock rate, PWM pin behavior, peripheral side effects or physical actuator proof.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_output_adaptation as adaptation
from verify_tcu_output_adaptation import handoff,TCU,w,r,s,execute

ROOT=Path(__file__).resolve().parent
DESCRIPTORS=[int.from_bytes(TCU[a:a+4],'big') for a in range(0x5F7B0,0x5F7DC,4)]
SOURCES=[int.from_bytes(TCU[a:a+4],'big') for a in DESCRIPTORS]
ADC=sorted(set(SOURCES)-{0x400})
assert int.from_bytes(TCU[0x5F628:0x5F62C],'big')==1
assert SOURCES==[0xFFFFF800,0xFFFFF802,0xFFFFF806,0xFFFFF804,0xFFFFF814,
                 0x400,0x400,0x400,0xFFFFF820,0xFFFFF810,0xFFFFF812]


class TaskRegisters(handoff.OutputSink):
    WIDTHS={0xFFFFF600:2,0xFFFFF604:2,0xFFFFF62C:2,0xFFFFF6C0:4}
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if address in ADC:
            if size!=2 or address not in self.adc_samples:raise ValueError('Explicit ADC word required')
            self.adc_reads.append(address);return self.adc_samples[address]
        if address in self.WIDTHS:
            if size!=self.WIDTHS[address]:raise ValueError('Timer access width')
            if address==0xFFFFF6C0:
                if not self.timestamps:raise ValueError('Missing timestamp')
                value=self.timestamps.pop(0)
            else:value=self.timer[address]
            self.timer_trace.append(('read',address,size,value));return value
        return super().read(address,size)
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address in ADC or address==0xFFFFF6C0:raise ValueError('Read-only fixture')
        if address in self.WIDTHS:
            if size!=self.WIDTHS[address]:raise ValueError('Timer access width')
            self.timer[address]=value&65535
            self.timer_trace.append(('write',address,size,value&65535));return
        super().write(address,value,size)


def fixture():
    t=adaptation.fixture();handoff.prior.initialize(t);t.__class__=TaskRegisters
    t.adc_samples={a:400<<6 for a in ADC};t.timer={a:0 for a in TaskRegisters.WIDTHS if a!=0xFFFFF6C0}
    t.timer_trace=[];t.timestamps=[]
    w(t,0xA518,12000,2)
    return t


def equal(t,ref):
    handoff.equal(t,ref)
    assert t.timer==ref.timer and t.timer_trace==ref.timer_trace and t.timestamps==ref.timestamps


def history_model(t):
    index=r(t,0x8989);assert index<5
    for i,address in enumerate(SOURCES):
        if address==0x400:value=int.from_bytes(TCU[0x400:0x402],'big')>>6
        else:value=t.adc_samples[address]>>6;t.adc_reads.append(address)
        count=r(t,0x897E+i)
        slots=range(5) if count==0 else [index]
        for slot in slots:w(t,0x8910+10*i+2*slot,value,2)
        if r(t,0x898A+i)!=2:count=(count+1)&255;w(t,0x897E+i,count)
        w(t,0x898A+i,2 if count>=5 else 3)
    w(t,0x8989,(index+1)%5)


def history(t):
    ref=copy.deepcopy(t);history_model(ref);execute(t,0x17B1A);equal(t,ref)


def initialize_history(t):
    ref=copy.deepcopy(t)
    for base,length in [(0x8910,110),(0x897E,11),(0x898A,11),(0x8989,1)]:
        for a in range(base,base+length):w(ref,a,0)
    execute(t,0x17AF0);equal(t,ref)


def acquire_model(t):
    for i,address in zip([0,1,3,2],handoff.ADC):
        value=t.adc_samples[address]>>6;t.adc_reads.append(address)
        w(t,0x8A2C+2*i,value,2);w(t,0x8A64+2*i,r(t,0x8A64+2*i,2)+value,2)


def active_model(t):
    phase=r(t,0x84F8);acquire_model(t)
    if phase==3:adaptation.dispatch_model(t);history_model(t)
    if phase<4:
        handoff.prior.service_model(t,phase);handoff.prior.driver_model(t,phase);handoff.handoff_model(t,phase)


def task_model(t,callback=False):
    mode=r(t,0x8008)
    if callback and mode==1 and r(t,0x84A0)==3 and r(t,0x8007)==3 and r(t,0x84F8)==3:
        mode=3;w(t,0x8008,mode)
    if mode==1:history_model(t)
    elif mode==3:active_model(t)
    phase=r(t,0x84F8);w(t,0x84F8,3 if phase==0 else phase-1)


def task(t,callback=False):
    ref=copy.deepcopy(t);task_model(ref,callback)
    execute(t,0x1227E if callback else 0x127BA);equal(t,ref)


def profile_model(t,enter,stamp,latency=0):
    i=10
    t.timer_trace.append(('read',0xFFFFF6C0,4,stamp));assert t.timestamps.pop(0)==stamp
    if enter:
        w(t,0x8728+4*i,stamp,4)
        value=(latency&65535)//10
        w(t,0x86E0+2*i,value,2);w(t,0x8704+2*i,max(value,r(t,0x8704+2*i,2)),2)
    else:
        value=min(65535,((stamp-r(t,0x8728+4*i,4))&0xFFFFFFFF)//10)
        w(t,0x8698+2*i,value,2);w(t,0x86BC+2*i,max(value,r(t,0x86BC+2*i,2)),2)


def interrupt_model(t):
    compare=t.timer[0xFFFFF604];counter=t.timer[0xFFFFF600]
    t.timer_trace.extend([('read',0xFFFFF604,2,compare),('read',0xFFFFF600,2,counter)])
    profile_model(t,True,t.timestamps[0],counter-compare)
    status=t.timer[0xFFFFF62C];t.timer_trace.append(('read',0xFFFFF62C,2,status))
    if status&1:
        t.timer_trace.extend([('read',0xFFFFF62C,2,status),('write',0xFFFFF62C,2,status&65534)])
        t.timer[0xFFFFF62C]=status&65534
        phase=(r(t,0x87F4)+1)&255;w(t,0x87F4,phase)
        value=4166*(2*(phase&3)+1);t.timer[0xFFFFF604]=value
        t.timer_trace.append(('write',0xFFFFF604,2,value));task_model(t,True)
    profile_model(t,False,t.timestamps[0])


def interrupt(t):
    ref=copy.deepcopy(t);interrupt_model(ref)
    saved=t.r.copy();pr=t.pr;macl=t.macl;mask=t.sr&~0x301;pc=0x1692E
    t.visited.clear()
    for _ in range(300000):
        if pc==0x169A0:break
        nxt,delay=t.instruction(pc)
        if delay:
            _,nested=t.instruction(pc+2);assert not nested
        pc=nxt
    else:raise AssertionError('interrupt-body instruction bound')
    assert t.r==saved and t.pr==pr and t.macl==macl and t.sr&~0x301==mask
    assert int.from_bytes(TCU[pc:pc+2],'big')==0x002B
    equal(t,ref)


def direct():
    rng=random.Random(0x127BA);counts=dict(history_init=0,history=0,task=0,callback=0,interrupt=0,rejected=0)
    for _ in range(16):
        t=fixture()
        for a in range(0x8910,0x8995):w(t,a,rng.randrange(256))
        initialize_history(t);counts['history_init']+=1
    for index,count,status in itertools.product(range(5),[0,1,4,5,127,128,254,255],[0,1,2,3,255]):
        t=fixture();w(t,0x8989,index);t.adc_samples={a:rng.randrange(65536) for a in ADC}
        for i in range(11):w(t,0x897E+i,count);w(t,0x898A+i,status)
        history(t);counts['history']+=1
    for mode,phase in itertools.product(range(256),[0,1,2,3,4,255]):
        t=fixture();w(t,0x8008,mode);w(t,0x84F8,phase);task(t);counts['task']+=1
    for mode,a,b,phase in itertools.product([0,1,2,3,255],[0,1,2,3,255],[0,1,2,3,255],[0,1,2,3,4,255]):
        t=fixture()
        for address,value in [(0x8008,mode),(0x84A0,a),(0x8007,b),(0x84F8,phase)]:w(t,address,value)
        task(t,True);counts['callback']+=1
    for status,phase in itertools.product([0,1,2,3,0x8000,0xFFFF],[0,1,2,3,254,255]):
        t=fixture();w(t,0x8008,3);w(t,0x84F8,3);w(t,0x87F4,phase)
        t.timer={0xFFFFF600:rng.randrange(65536),0xFFFFF604:rng.randrange(65536),0xFFFFF62C:status}
        for address in [0x8718,0x86D0]:w(t,address,rng.choice([0,1,65535]),2)
        t.timestamps=[0xFFFFFE00,rng.choice([0xFFFFFE00,0xFFFFFF00,0x00000300,0x00200000])]
        interrupt(t);counts['interrupt']+=1
    t=fixture()
    for a,n,writing in [(ADC[0],1,False),(ADC[-1],2,True),(0xFFFFF6C0,4,False),
                         (0xFFFFF6C0,4,True),(0xFFFFF62C,1,False),(0xFFFFF604,4,True),(0xFFFFF808,2,False)]:
        try:
            if writing:t.write(a,0,n)
            else:t.read(a,n)
        except ValueError:counts['rejected']+=1
        else:raise AssertionError('unsupported access accepted')
    return counts


def retained():
    t=fixture();initialize_history(t);w(t,0x8008,1);w(t,0x84F8,3)
    rows=[]
    for call in range(1,161):
        t.adc_samples={a:(368+(call%5))<<6 for a in ADC}
        w(t,0x84A0,3 if call>=5 else 1);w(t,0x8007,3)
        if call==100:w(t,0x8008,2)
        if call==105:w(t,0x8008,3)
        t.timer[0xFFFFF62C]=0 if call in [50,51] else 1
        t.timer[0xFFFFF600]=(t.timer[0xFFFFF604]+7)&65535
        t.timestamps=[(call*10000)&0xFFFFFFFF,(call*10000+123)&0xFFFFFFFF]
        old_phase=r(t,0x84F8);t.adc_reads=[];t.output_writes=[];t.timer_trace=[]
        interrupt(t)
        rows.append(dict(call=call,mode=r(t,0x8008),old_phase=old_phase,next_phase=r(t,0x84F8),
            timer_phase=r(t,0x87F4),compare=t.timer[0xFFFFF604],history_index=r(t,0x8989),
            history_counts=[r(t,0x897E+i) for i in range(11)],
            adc_reads=[hex(a) for a in t.adc_reads],outputs=t.output_writes,
            sums=[r(t,0x8A64+2*i,2) for i in range(4)],
            adaptation_age=r(t,0x8AD0,2),profile_latency=r(t,0x86F4,2),profile_duration=r(t,0x86AC,2)))
    assert rows[3]['mode']==1 and rows[4]['mode']==3
    assert rows[49]['old_phase']==rows[49]['next_phase']==rows[50]['next_phase']
    assert not rows[49]['outputs'] and not rows[50]['adc_reads']
    assert all(not row['outputs'] and not row['adc_reads'] for row in rows[99:104])
    assert all(row['history_counts'][5:8]==[5]*3 for row in rows[8:])
    return rows


def main():
    counts=direct();print(counts,flush=True);rows=retained()
    out=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,
        descriptors=[hex(a) for a in DESCRIPTORS],sources=[hex(a) for a in SOURCES],
        zero_descriptor_sample=316,retained=rows,retained_calls=len(rows),
        limits='No RTE/context entry, real interrupt timing, timer hardware side effects, PWM pin output, physical units or remote-controller proof;169A4/full clock/mode/pin setup remain open.')
    (ROOT/'tcu-output-task-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('Retained',len(rows),flush=True)


if __name__=='__main__':main()
