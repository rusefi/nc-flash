"""Execute cycle callback, dual ADC filters and publication through output service.

Explicit MMIO/timestamp samples and callback order; both ISR bodies stop before
RTE. No clock, real interrupts, analog conversion, pin/plant or sensor identity.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_output_task as task
from verify_tcu_output_task import TCU,w,r,s,execute,handoff

ROOT=Path(__file__).resolve().parent
assert int.from_bytes(TCU[0x5F62C:0x5F630],'big')==1
CHANNELS=[(0xFFFFF812,0x8800,0x16F78,0x16FF6,0xA4DC,0x50B48,[0xA975,0xA976]),
          (0xFFFFF810,0x87F8,0x16E80,0x16EFE,0xA518,0x511CC,[0xA958])]


class CycleRegisters(task.TaskRegisters):
    WIDTHS={**task.TaskRegisters.WIDTHS,0xFFFFF500:2,0xFFFFF522:2}


def fixture():
    t=task.fixture();t.__class__=CycleRegisters
    t.timer.update({0xFFFFF500:0,0xFFFFF522:0})
    return t


def converted(count):
    original=300+handoff.sd(handoff.signed((count&65535)*64000),2976)
    value=max(0,min(22000,original))
    return value,2 if value==original else 1


def scale_model(t,channel):
    adc,base,*_=channel;count=t.adc_samples[adc]>>6;t.adc_reads.append(adc)
    value,state=converted(count);old=r(t,base,2);delta=old-value
    if -16<delta<-1:delta=-1
    elif 1<delta<16:delta=1
    if -48<delta<=-16 or 16<=delta<48:delta=handoff.trunc(delta,8)
    w(t,base,old-delta,2);w(t,base+2,count,2);w(t,base+4,state)


def scale(t,channel):
    ref=copy.deepcopy(t);scale_model(ref,channel);execute(t,channel[2]);task.equal(t,ref)


def publish_model(t,channel):
    _,base,_,_,output,_,flags=channel;values=[r(t,a) for a in flags]
    state=1 if r(t,base+4)==2 and all(v&1 for v in values) else 4 if any(v&4 for v in values) else 3 if any(v&2 for v in values) else 2
    w(t,output,r(t,base,2),2);w(t,output+2,state)


def publish(t,channel):
    ref=copy.deepcopy(t);publish_model(ref,channel);execute(t,channel[5]);task.equal(t,ref)


def callback_model(t,direct=False):
    mode=r(t,0x8002)
    if not direct and mode==1:mode=3;w(t,0x8002,3)
    if mode==3:
        for channel in CHANNELS:scale_model(t,channel);publish_model(t,channel)


def callback(t,direct=False):
    ref=copy.deepcopy(t);callback_model(ref,direct)
    execute(t,0x124AA if direct else 0x11F7C);task.equal(t,ref)


def profiling(t,entry,stamp,latency=0):
    i=11;t.timer_trace.append(('read',0xFFFFF6C0,4,stamp));assert t.timestamps.pop(0)==stamp
    if entry:
        w(t,0x8728+4*i,stamp,4);value=(latency&65535)//10
        w(t,0x86E0+2*i,value,2);w(t,0x8704+2*i,max(value,r(t,0x8704+2*i,2)),2)
    else:
        value=min(65535,((stamp-r(t,0x8728+4*i,4))&0xFFFFFFFF)//10)
        w(t,0x8698+2*i,value,2);w(t,0x86BC+2*i,max(value,r(t,0x86BC+2*i,2)),2)


def cycle_model(t):
    counter=t.timer[0xFFFFF500];t.timer_trace.append(('read',0xFFFFF500,2,counter))
    profiling(t,True,t.timestamps[0],counter-1)
    status=t.timer[0xFFFFF522];t.timer_trace.append(('read',0xFFFFF522,2,status))
    if status&1:
        events=[('read',0xFFFFF522,2,status),('write',0xFFFFF522,2,status&65534),
                ('write',0xFFFFF600,2,0),('write',0xFFFFF604,2,4166)]
        t.timer_trace.extend(events)
        for kind,address,size,value in events:
            if kind=='write':t.timer[address]=value
        w(t,0x87F4,0);callback_model(t)
    profiling(t,False,t.timestamps[0])


def cycle(t):
    ref=copy.deepcopy(t);cycle_model(ref);saved=t.r.copy();pr=t.pr;macl=t.macl;mask=t.sr&~0x301
    pc=0x169A4;t.visited.clear()
    for _ in range(300000):
        if pc==0x16A04:break
        nxt,delay=t.instruction(pc)
        if delay:
            _,nested=t.instruction(pc+2);assert not nested
        pc=nxt
    else:raise AssertionError('cycle instruction bound')
    assert t.r==saved and t.pr==pr and t.macl==macl and t.sr&~0x301==mask
    assert int.from_bytes(TCU[pc:pc+2],'big')==0x002B
    task.equal(t,ref)


def direct():
    counts=dict(convert=0,scale=0,publish=0,callback=0,cycle=0,rejected=0)
    rng=random.Random(0x169A4)
    for channel in CHANNELS:
        t=fixture()
        for count in list(range(1024))+[32767,32768,65535]:
            address=0xFFFF7F00;t.r[5]=address;t.write(address,255,1)
            result=execute(t,channel[3],count);value,state=converted(count)
            assert result==value and t.read(address,1)==state;counts['convert']+=1
        for count,old in itertools.product([0,1,500,1008,1009,1023],[0,1,32767,32768,65535]):
            t.adc_samples[channel[0]]=count<<6;w(t,channel[1],old,2);scale(t,channel);counts['scale']+=1
        # Every delta around both asymmetric tier boundaries.
        for delta in range(-60,61):
            value,_=converted(500);w(t,channel[1],value+delta,2);t.adc_samples[channel[0]]=500<<6
            scale(t,channel);counts['scale']+=1
        for _ in range(256):
            t.adc_samples[channel[0]]=rng.randrange(65536);w(t,channel[1],rng.randrange(65536),2)
            scale(t,channel);counts['scale']+=1
        for state in [0,1,2,255]:
            for flags in itertools.product(list(range(8))+[128,255],repeat=len(channel[-1])):
                w(t,channel[1],rng.randrange(65536),2);w(t,channel[1]+4,state)
                for a,v in zip(channel[-1],flags):w(t,a,v)
                publish(t,channel);counts['publish']+=1
    for mode,direct_mode in itertools.product(range(256),[False,True]):
        t=fixture();w(t,0x8002,mode);callback(t,direct_mode);counts['callback']+=1
    for status,mode,counter in itertools.product([0,1,2,3,0x8000,65535],[0,1,2,3,255],[0,1,32767,32768,65535]):
        t=fixture();w(t,0x8002,mode);w(t,0x87F4,255)
        t.timer.update({0xFFFFF500:counter,0xFFFFF522:status,0xFFFFF600:65535,0xFFFFF604:29162})
        t.timestamps=[0xFFFFFE00,rng.choice([0xFFFFFE00,0xFFFFFF00,0x300,0x200000])]
        for a in [0x871A,0x86D2]:w(t,a,rng.choice([0,1,65535]),2)
        cycle(t);counts['cycle']+=1
    t=fixture()
    for a,n,writing in [(0xFFFFF500,1,False),(0xFFFFF522,4,True),(0xFFFFF524,2,False),(0xFFFFF6C0,4,False)]:
        try:
            if writing:t.write(a,0,n)
            else:t.read(a,n)
        except ValueError:counts['rejected']+=1
        else:raise AssertionError('unsupported access')
    return counts


def retained():
    t=fixture();task.initialize_history(t)
    w(t,0x8002,1);w(t,0x8008,3);w(t,0x84F8,3)
    for a in [0xA975,0xA976,0xA958]:w(t,a,1)
    rows=[]
    for call in range(1,81):
        count=600 if call<=20 else 300 if call<=40 else 1023 if call<=60 else 600
        t.adc_samples={a:368<<6 for a in task.ADC};t.adc_samples[0xFFFFF810]=count<<6;t.adc_samples[0xFFFFF812]=(count-10)<<6
        t.timer[0xFFFFF500]=2;t.timer[0xFFFFF522]=0 if call in [21,22] else 1
        t.timestamps=[call*100000,call*100000+234];t.timer_trace=[];t.output_writes=[];t.adc_reads=[]
        cycle(t);cycle_trace=t.timer_trace.copy();cycle_reads=t.adc_reads.copy()
        outputs=[]
        for phase in range(4):
            t.timer[0xFFFFF62C]=1;t.timer[0xFFFFF600]=(t.timer[0xFFFFF604]+7)&65535
            t.timestamps=[call*100000+1000+phase*1000,call*100000+1123+phase*1000]
            t.output_writes=[];t.adc_reads=[];t.timer_trace=[];task.interrupt(t);outputs.extend(t.output_writes)
        rows.append(dict(cycle=call,count=count,source=r(t,0x87F8,2),published=r(t,0xA518,2),state=r(t,0xA51A),
            other=r(t,0xA4DC,2),other_state=r(t,0xA4DE),cycle_adc=[hex(a) for a in cycle_reads],cycle_trace=cycle_trace,
            outputs=outputs,compare=t.timer[0xFFFFF604],timer_phase=r(t,0x87F4),task_phase=r(t,0x84F8),
            adaptation_age=r(t,0x8AD0,2)))
    assert rows[19]['published']==rows[20]['published']==rows[21]['published']
    assert not rows[20]['cycle_adc'] and not rows[21]['cycle_adc']
    assert rows[22]['published']<rows[19]['published']
    assert rows[40]['published']==22000 and rows[40]['state']==2
    assert rows[60]['published']==converted(600)[0] and rows[60]['state']==1
    assert all(len(row['outputs'])==4 and row['task_phase']==3 for row in rows)
    assert all(row['published']==row['source'] for row in rows)
    return rows


def config_leads():
    result={}
    for value in [0xF520,0xF521,0xF524,0xF526,0xF62A,0xF628]:
        users=[]
        for pc in range(0,len(TCU)-2,2):
            op=int.from_bytes(TCU[pc:pc+2],'big')
            if op>>12==9:
                address=pc+4+2*(op&255)
                if int.from_bytes(TCU[address:address+2],'big')==value:users.append(hex(pc))
        result[hex(value)]=users
    lines=['Static candidate MOV.W PC-relative literals; data may resemble opcodes. Not writer proof.']
    lines.extend(key+' '+str(value) for key,value in result.items())
    (ROOT/'tcu-cycle-callback-config-leads.txt').write_text('\n'.join(lines)+'\n')
    return result


def main():
    counts=direct();print(counts,flush=True);rows=retained()
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,
        config_literal_candidates=config_leads(),
        factory_source=dict(path='sources/renesas-sh7055s-hardware-rej09b0045-0200h.pdf',
            sha256=hashlib.sha256((ROOT/'sources/renesas-sh7055s-hardware-rej09b0045-0200h.pdf').read_bytes()).hexdigest(),
            table_pages_zero=[243,245],note='F62C TSR2A; F522 TSR6; F521 TCR6A,F520 TCR6B,F526 PMDR. Compatible register interpretation, no physical chip or mode proof.'),
        retained_cycles=len(rows),compare_bodies=len(rows)*4,retained=rows,
        limits='Explicit cycle/four-compare ordering and register samples; no RTE, real interrupt timing or clock/pin setup. ADC identities/units, status writers, physical plant and remote-controller evidence remain open.')
    (ROOT/'tcu-cycle-callback-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('Retained',len(rows),len(rows)*4,flush=True)


if __name__=='__main__':main()
