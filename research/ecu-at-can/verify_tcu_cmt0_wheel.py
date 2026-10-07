"""Independent stock CMT0 mixed increment/decrement wheel RAM model.

All1000 valid phase triples with eight boundary patterns. The stock table
selectors are asserted, not executed by the reference. No clock-unit claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram

ROOT=Path(__file__).resolve().parent
# Each bank: byte increment, word increment, byte decrement, word decrement.
BANKS=[[(0x8410,0x8411),(0x8414,0x841C),(0x841C,0x841D),(0x8420,0x844E)],
       [(0x8450,0x8451),(0x8454,0x8456),(0x8458,0x8459),(0x845C,0x845E)],
       [(0x8460,0x8461),(0x8464,0x846C),(0x846C,0x846D),(0x8470,0x8474)],
       [(0x8474,0x8475),(0x8478,0x847A),(0x847C,0x847D),(0x8480,0x8482)],
       [(0x8484,0x8485),(0x8488,0x848A),(0x848C,0x848D),(0x8490,0x8492)]]


def model(t):
    phases=[r(t,a) for a in [0x84D4,0x84D5,0x84D6]]
    assert all(0<=p<10 for p in phases)
    p,q,z=phases;banks=[0]
    if p in [0,5]:banks.append(1)
    if p==1:banks.append(2)
    if p==6:
        if q==0:banks.append(3)
        if q==5:
            if z==0:banks.append(4)
            w(t,0x84D6,(z+1)%10)
        w(t,0x84D5,(q+1)%10)
    for bank in banks:
        for operation,(start,end) in enumerate(BANKS[bank]):
            size=1+operation%2;maximum=(1<<(8*size))-1
            for a in range(start,end,size):
                old=r(t,a,size)
                value=min(maximum,old+1) if operation<2 else old-int(old not in [0,maximum])
                w(t,a,value,size)
    w(t,0x84D4,(p+1)%10)
    return banks


def main():
    tables={0x5C170:[0x11B7C,0x11BDA,0x11DCC,0x11DCC,0x11DCC,0x11B7C,0x11A94,0x11DCC,0x11DCC,0x11DCC],
            0x5C198:[0x11C38,0x11DCC,0x11DCC,0x11DCC,0x11DCC,0x11AC0,0x11DCC,0x11DCC,0x11DCC,0x11DCC],
            0x5C1C0:[0x11C96]+[0x11DCC]*9}
    for address,values in tables.items():
        assert [int.from_bytes(TCU[a:a+4],'big') for a in range(address,address+40,4)]==values
    flattened=[x for bank in BANKS for pair in bank for x in pair]
    assert [int.from_bytes(TCU[a:a+4],'big') for a in range(0x76D24,0x76DC4,4)]==[x|0xFFFF0000 for x in flattened]
    cases=0;selected=[0]*5
    for phases in itertools.product(range(10),repeat=3):
        for pattern in range(8):
            t=SHRotate(TCU)
            for a in range(0x8400,0x84E0):w(t,a,(a*37+pattern*19)&255)
            index=0
            for bank in BANKS:
                for op,(start,end) in enumerate(bank):
                    size=1+op%2;maximum=(1<<(8*size))-1
                    edges=[0,1,2,127,128,maximum-2,maximum-1,maximum]
                    for a in range(start,end,size):
                        w(t,a,edges[(index+pattern)%8],size);index+=1
            for a,value in zip([0x84D4,0x84D5,0x84D6],phases):w(t,a,value)
            ref=SHRotate(TCU);ref.ram=dict(t.ram)
            for bank in model(ref):selected[bank]+=1
            t.run(0x11A64,limit=200000)
            assert ram(t)==ram(ref),(phases,pattern)
            cases+=1
    result=dict(status='PASS',scope=__doc__,independent_whole_application_ram_cases=cases,
                selected_banks=selected,rom_sha256=hashlib.sha256(TCU).hexdigest(),
                table_addresses=[hex(a) for a in tables],range_table='0x76d24..0x76dc3')
    (ROOT/'tcu-cmt0-wheel-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
