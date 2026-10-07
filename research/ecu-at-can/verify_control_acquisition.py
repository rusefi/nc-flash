"""Bounded ADC-register copy, application decode and retained input publication.

Explicit conversion-result samples, not analog conversion/status/interrupt
simulation. Local firmware provenance does not identify board wiring, units,
DSC actuation or task cadence. Existing interpreters/verifiers are unchanged.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_control_mode_followers as prior
from verify_control_policy import ControlPolicy
from verify_control_contributions import ECU,TCU,w,r,f,rf,q,number,run
from verify_control_target_source import filter_value

ROOT=Path(__file__).resolve().parent
REGISTERS=[0xFFFFF800+2*i for i in range(12)]+[0xFFFFF820+2*i for i in range(12)]+[0xFFFFF840+2*i for i in range(8)]
FIELDS={0x6C90:(3,6,2),0x6C92:(28,6,2),0x6CAE:(29,8,1),0x6CAD:(13,8,1),
    0x6CAC:(8,8,1),0x6C94:(7,6,2),0x6C96:(14,6,2),0x6C9E:(30,6,2),
    0x6C98:(31,0,2),0x6C9A:(2,6,2),0x6C9C:(2,6,2),0x6CA0:(17,6,2),
    0x6CA2:(18,6,2),0x6CA4:(4,6,2),0x6CA6:(5,6,2),0x6CA8:(19,6,2),0x6CAA:(16,6,2)}
PARTIAL={a:FIELDS[a] for a in [0x6C94,0x6C96,0x6CAC,0x6CA0,0x6CA2,0x6CA4,0x6CA6]}


class Acquisition(ControlPolicy):
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if 0xFFFFF800<=address<=0xFFFFF85F:
            if address not in REGISTERS or size!=2 or address not in self.adc_samples:
                raise ValueError('Unsupported or missing ADC sample')
            self.adc_reads.append(address)
            return self.adc_samples[address]
        return super().read(address,size)

    def write(self,address,value,size):
        if 0xFFFFF800<=(address&0xFFFFFFFF)<=0xFFFFF85F:
            raise ValueError('ADC result registers are read-only')
        super().write(address,value,size)


def attach(e):
    # Preserve the existing CPU/RAM/serial state; add only this bounded
    #read-only register interface. No instruction implementation is replaced.
    assert type(e) is ControlPolicy
    e.__class__=Acquisition; e.adc_samples={}; e.adc_reads=[]
    return e


def setup(): return attach(prior.prior.setup())


def acquire(e,values):
    assert len(values)==32 and all(0<=v<=65535 for v in values)
    e.adc_samples=dict(zip(REGISTERS,values)); e.adc_reads=[]
    pc=0x4B80; sp=e.r[15]
    for _ in range(1000):
        if pc==0x4C94: break
        nxt,delay=e.instruction(pc)
        if delay:
            _,nested=e.instruction(pc+2); assert not nested
        pc=nxt
    else: raise AssertionError('acquisition slice bound')
    assert e.r[15]==sp and e.adc_reads==REGISTERS
    assert [r(e,0x4008+2*i,2) for i in range(32)]==values


def decode(e,partial=False):
    expected={a:r(e,a) for a in range(0x6C90,0x6CB0)}
    for address,(index,shift,size) in (PARTIAL if partial else FIELDS).items():
        value=r(e,0x4008+2*index,2)>>shift
        for off,byte in enumerate(value.to_bytes(size,'big')): expected[address+off]=byte
    run(e,0x39894 if partial else 0x3976C)
    assert {a:r(e,a) for a in expected}==expected


def scale(e,initialize=False):
    assert int.from_bytes(ECU[0xDC47C:0xDC47E],'big')==256
    raw=r(e,0x400A,2)
    want=q(q(raw/number(0x676C))*number(0xDC480))
    run(e,0x6710 if initialize else 0x6718)
    assert r(e,0x40EC,2)==raw and rf(e,0x40E8)==want


def publish(e,initialize=False):
    value=rf(e,0x40E8)
    if initialize:
        run(e,0x1DF14)
        assert all(rf(e,a)==value for a in [0x6CB0,0x6CB4,0x6CB8])
    else:
        old=r(e,0x6CBC); current=rf(e,0x6CB4); filtered=rf(e,0x6CB8)
        if old&1:
            current=value
            filtered=filter_value(value,filtered,number(0xBFA7C),number(0x1DF88))
        run(e,0x1DF32)
        assert rf(e,0x6CB4)==current and rf(e,0x6CB8)==filtered and r(e,0x6CBC)==(old+1)&255
    filtered=rf(e,0x6CB8); run(e,0x1DF28); assert rf(e,0x6CB0)==filtered


def direct():
    rng=random.Random(0x3976C); counts=dict(copy=0,decode=0,scale=0,publish=0,rejected=0)
    for i in range(100):
        e=setup(); values=[rng.randrange(65536) for _ in range(32)]
        acquire(e,values); counts['copy']+=1
        for partial in [False,True]:
            for a in range(0x6C90,0x6CB0): w(e,a,0xA5)
            decode(e,partial); counts['decode']+=1
    for value in range(1024):
        e=setup(); values=[0]*32; values[1]=value<<6; values[8]=value<<6
        acquire(e,values); decode(e); scale(e,value%2==0); publish(e,True)
        assert r(e,0x6CAC)==value>>2 and rf(e,0x6CB4)==q(value*number(0xDC480)/1024)
        counts['copy']+=1; counts['decode']+=1; counts['scale']+=1
    for raw,old,initialize in itertools.product([0,1,63,64,32767,32768,65535],[0,32768,65535],[False,True]):
        e=setup(); w(e,0x400A,raw,2); w(e,0x40EC,old,2); scale(e,initialize); counts['scale']+=1
    for counter,value,old in itertools.product([0,1,2,3,254,255],[-1,0,8,20],[0,8,20]):
        e=setup(); w(e,0x6CBC,counter); f(e,0x40E8,value); f(e,0x6CB4,9); f(e,0x6CB8,old)
        publish(e); counts['publish']+=1
    e=setup()
    for address,size,write in [(REGISTERS[0],2,False),(REGISTERS[0],1,False),(0xFFFFF818,1,False),(REGISTERS[0],2,True)]:
        try:
            if write:e.write(address,0,size)
            else:e.read(address,size)
        except ValueError: counts['rejected']+=1
        else: raise AssertionError('unsupported access accepted')
    return counts


def retained():
    e=setup(); values=[0]*32; values[1]=400<<6; values[8]=100<<6
    acquire(e,values);decode(e);scale(e,True);publish(e,True);w(e,0x6CBC,254)
    rows=[]
    for call in range(1,261):
        values[1]=(400 if call<=20 else 600 if call<=180 else 300)<<6
        values[8]=(call%1024)<<6
        acquire(e,values);decode(e,call%2==0);scale(e);publish(e)
        prior.group(e)
        rows.append(dict(call=call,counter=r(e,0x6CBC),raw1=values[1]>>6,raw8=values[8]>>6,
            direct=float(rf(e,0x6CB4)),filtered=float(rf(e,0x6CB8)),byte=r(e,0x6CAC)))
    assert rows[0]['counter']==255 and rows[1]['counter']==0 and rows[257]['counter']==0
    assert rows[20]['direct']==rows[19]['direct'] and rows[21]['direct']!=rows[20]['direct']
    assert rows[21]['filtered']!=rows[21]['direct']
    return rows


def prepare(e):
    prior.prepare(e);attach(e)
    values=[0]*32;values[1]=410<<6
    acquire(e,values);decode(e);scale(e,True);publish(e,True);w(e,0x6CBC,0)


def mode_step(e,call):
    prior.prior.mode_step(e,call)
    w(e,0x70F0,1 if 40<=call<=60 else 2);w(e,0x9462,1 if 201<=call<=210 else 0)
    values=[0]*32;values[1]=(410 if call<=160 else 600 if call<=220 else 350)<<6
    values[8]=(0 if call<=100 else 480 if call<=160 else 1023)<<6
    acquire(e,values);decode(e,True);scale(e);publish(e)
    prior.group(e)


def step(e,call):
    row=prior.prior.source.followers.step(e,call,input_producer=prior.input_step,mode_producer=mode_step)
    row.update(adc1=r(e,0x400A,2)>>6,adc8=r(e,0x4018,2)>>6,produced6cac=r(e,0x6CAC),
        produced6cb4=float(rf(e,0x6CB4)),filtered6cb8=float(rf(e,0x6CB8)),input_phase=r(e,0x6CBC),
        biased67d0=float(rf(e,0x67D0)),scaled67d4=float(rf(e,0x67D4)))
    return row


def main():
    counts=direct();history=retained();print('Direct',counts,'retained',len(history),flush=True)
    rows,boundaries=prior.prior.source.followers.adjustment.upstream.secondary.prior.lifecycle(
        prepare=prepare,upstream=step,checkpoints={1,2,100,101,160,161,162,220,221,222,255,256,257,320})
    by={r['call']:r for r in rows}
    assert by[161]['produced6cb4']==by[160]['produced6cb4'] and by[162]['produced6cb4']!=by[161]['produced6cb4']
    out=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts,retained=history,serial_cycles=320,paired_can_updates=len(boundaries),can211_latch_updates=320,lifecycle=rows)
    (ROOT/'control-acquisition-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Integrated',320,len(boundaries),flush=True)


if __name__=='__main__': main()
