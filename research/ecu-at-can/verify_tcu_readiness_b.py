"""Execute original84D8 readiness producer from finite ADC/status/time inputs.

Independent arithmetic and state-transition whole-RAM model. No sensor identity,
physical time, ADC conversion latency, full boot or forced readiness in chains.
"""
import hashlib
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_tcu_capture_interrupts import CaptureSamples
from verify_tcu_cycle_callback import converted

ROOT = Path(__file__).resolve().parent
assert int.from_bytes(TCU[0x5C57C:0x5C580],'big') == 0xFFFFF812


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.io = CaptureSamples()

    def read(self,address,size):
        if (address&0xFFFFFFFF) >= 0xFFFFE000:
            return self.io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if (address&0xFFFFFFFF) >= 0xFFFFE000:
            raise ValueError('No readiness MMIO writes expected')
        return super().write(address,value,size)


def state(t):
    return {hex(a):r(t,a,n) for a,n in [(0x84D8,1),(0x84DA,2),(0x84DC,4),
                                      (0x84E0,4),(0x84E4,4)]}


def model(ref,count,now):
    """Independent state model, also used at actual foreground-call boundaries."""
    value,_ = converted(count)
    w(ref,0x84DA,value,2)
    w(ref,0x84DC,count,4)
    mode = r(ref,0x84D8)
    time_read = False
    if mode in [1,2]:
        address,threshold = (0x84E0,5547) if mode == 1 else (0x84E4,9000)
        old = r(ref,address,4)
        if value <= threshold:
            w(ref,address,0,4)
        else:
            time_read = True
            if old == 0:
                w(ref,address,now,4)
            elif ((now-old)&0xFFFFFFFF) >= 100000:
                w(ref,address,0,4)
                w(ref,0x84D8,mode+1)
    return time_read


def execute(t,count,now,polls=(0,128),low_bits=0):
    before = state(t)
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    time_read = model(ref,count,now)
    assert polls[-1]&128 and all(not(p&128) for p in polls[:-1])
    raw = (count<<6)|low_bits
    t.io.accesses = []
    t.io.samples = {(0xFFFFF818,1):list(polls),(0xFFFFF812,2):[raw]}
    expected = [['read',0xFFFFF818,1,p] for p in polls]+[['read',0xFFFFF812,2,raw]]
    if time_read:
        t.io.samples[(0xFFFFF6C0,4)] = [now]
        expected.append(['read',0xFFFFF6C0,4,now])
    saved,sp,mask = t.r[8:15],t.r[15],t.sr&~0x301
    t.run(0x11DEE,limit=200000)
    assert ram(t) == ram(ref)
    assert (t.r[8:15],t.r[15],t.sr&~0x301) == (saved,sp,mask)
    assert t.io.accesses == expected and all(not v for v in t.io.samples.values())
    return dict(before=before,count=count,now=now,time_read=time_read,
                after=state(t),accesses=expected,whole_application_ram_checked=True)


def initialized(seed):
    t = Machine()
    for a in range(0x84D0,0x84F0):
        w(t,a,(a*37+seed*19)&255)
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    for a,v,n in [(0x84D8,1,1),(0x84DA,0,2),(0x84E0,0,4),(0x84E4,0,4)]:
        w(ref,a,v,n)
    t.run(0x11DD8)
    assert ram(t) == ram(ref)
    return t


def main():
    for seed in range(256):
        initialized(seed)
    cases = 0
    # Every ADC count under both advancing states, before/on/after deadlines,
    # timestamp-zero sentinel and modulo32 wrap. Low six result bits ignored.
    clocks = [(0,0),(0,1),(1,100000),(1,100001),(1,100002),(0xFFFF0000,34464)]
    for mode in [1,2]:
        for count in range(1024):
            for old,now in clocks:
                t = Machine()
                w(t,0x84D8,mode)
                w(t,0x84E0,old,4)
                w(t,0x84E4,old,4)
                t.r[8:15] = [(0x10203040*n)&0xFFFFFFFF for n in range(1,8)]
                execute(t,count,now,low_bits=count&63)
                cases += 1
    for mode in range(256):
        t = Machine()
        w(t,0x84D8,mode)
        w(t,0x84E0,7,4)
        w(t,0x84E4,9,4)
        execute(t,600,200000,polls=(128,))
        cases += 1
    t = initialized(0)
    chain = [execute(t,600,now) for now in [1,100000,100001,100002,200001,200002]]
    assert [e['after']['0x84d8'] for e in chain] == [1,1,2,2,2,3]
    assert state(t)['0x84e0'] == state(t)['0x84e4'] == 0
    # Zero is both a valid external timestamp and the firmware's unset marker.
    t = initialized(1)
    zero = [execute(t,600,now) for now in [0,100000,200000]]
    assert [e['after']['0x84d8'] for e in zero] == [1,1,2]
    data = dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
                initializers=256,independent_whole_ram_cases=cases,
                initialized_chain=chain,zero_epoch_chain=zero,
                limits='ADC completion/counts and F6C0 times are external samples. No physical units, timer cadence, caller scheduling or full boot;84A0/84EC producers remain separate.')
    (ROOT/'tcu-readiness-b-verification.json').write_text(json.dumps(data,indent=2)+'\n')
    print(dict(status='PASS',initializers=256,cases=cases,chain_modes=[e['after']['0x84d8'] for e in chain]))


if __name__ == '__main__':
    main()
