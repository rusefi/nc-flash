"""Independent whole-application-RAM model of the original20CBC hold gates.

Synthetic boundary/overflow inputs; no physical capture units or cadence.
The original402 selected-output cases remain in verify_tcu_reference_source.
"""
import hashlib
import json
from pathlib import Path
import random
from sh_rotate import SHRotate
from sh_subset import signed
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_tcu_reference_source import RESET,udiv

ROOT=Path(__file__).resolve().parent


def state(t):
    out={hex(a):r(t,a,n) for a,n in [(0x91A6,1),(0x9194,1),(0x8158,1),
          (0x91AC,2),(0x91B4,1),(0x809A,2),(0x8080,1),(0x8081,1),
          (0x92C6,1),(0xAC87,1)]}
    out['history']=[r(t,0x91CC+4*i,4) for i in range(18)]
    return out


def model(t):
    before=state(t);values=before['history'];head=before['0x91b4']
    assert 0<=head<18
    total=sum(values)&0xFFFFFFFF
    ratio=udiv(before['0x91ac']<<16,values[head]>>2)
    held=total<=91643 and ratio>538
    flags=before['0x91a6'];timer=before['0x8158'] if held else 0
    flags=(flags|1) if held else (flags&~1)
    reset=timer>=244
    if reset:
        flags|=6
        for i in range(18):w(t,0x91CC+4*i,RESET,4)
        w(t,0x91B4,0)
    if signed(before['0x809a'],16)<2560 and before['0x8080']!=0 and before['0x8081']==0:
        flags &= ~2
    summary=(before['0x9194']&~1)|int(bool(flags&2 or before['0x92c6']&2 or before['0xac87']))
    w(t,0x91A6,flags);w(t,0x8158,timer);w(t,0x9194,summary)
    return dict(total=total,period=values[head],ratio=ratio,held=held,
                timer=timer,flags=flags,summary=summary,history_reset=reset)


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rng=random.Random(0x20CBC);counts=dict(held=0,reset=0,zero_divisor=0)
    for case in range(2048):
        t=SHRotate(TCU)
        for a in range(0x9190,0x9220):w(t,a,rng.randrange(256))
        head=case%18;values=[rng.randrange(RESET+1) for _ in range(18)]
        values[head]=[0,1,2,3,4,1216,6000,RESET,0xFFFFFFFF][case%9]
        total=[0,91642,91643,91644,0x7FFFFFFF,0x80000000,0xFFFFFFFF][case%7]
        other=(head+1)%18;values[other]=(total-sum(values)+values[other])&0xFFFFFFFF
        for i,value in enumerate(values):w(t,0x91CC+4*i,value,4)
        for a,v,n in [(0x91B4,head,1),(0x91A6,case%256,1),(0x9194,rng.randrange(256),1),
                      (0x91AC,[0,1,2,3,100,65535][case%6],2),
                      (0x8158,[0,1,243,244,255][case%5],1),
                      (0x809A,[2559,2560,32767,32768,65535][case%5],2),
                      (0x8080,[0,1,255][case%3],1),(0x8081,(case//3)%2,1),
                      (0x92C6,(case//6)%256,1),(0xAC87,(case//12)%2,1)]:w(t,a,v,n)
        ref=SHRotate(TCU);ref.ram=dict(t.ram);expected=model(ref)
        t.run(0x20CBC,limit=200000)
        assert ram(t)==ram(ref),(case,expected,state(t),state(ref))
        counts['held']+=expected['held'];counts['reset']+=expected['history_reset']
        counts['zero_divisor']+=values[head]>>2==0
    result=dict(status='PASS',scope=__doc__,independent_whole_application_ram_cases=2048,
                counts=counts,seed=hex(0x20CBC),rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-reference-hold-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
