"""Original84A0 ADC readiness, low-input transition and recovery state machine.

Independent complete-RAM arithmetic model with finite external ADC/time inputs.
No sensor units, native caller cadence, conversion latency or full boot claim.
"""
import hashlib
import itertools
import json

from verify_tcu_readiness_b import Machine,ROOT,TCU,SHRotate,r,w,ram,converted

assert int.from_bytes(TCU[0x5C578:0x5C57C],'big') == 0xFFFFF810


def state(t):
    return {hex(a):r(t,a,n) for a,n in [(0x84A0,1),(0x84A2,2),(0x84A4,4),
                                      (0x84A8,4),(0x84AC,4),(0x84B0,4)]}


def model(t,count,now):
    value,_ = converted(count)
    w(t,0x84A2,value,2)
    w(t,0x84A4,count,4)
    mode = r(t,0x84A0)
    address = target = other = None
    if mode in [1,2]:
        high,threshold,next_mode = (0x84A8,5525,2) if mode == 1 else (0x84AC,9000,3)
        if value > threshold:
            address,target,other = high,next_mode,0x84B0
        elif value <= 3600:
            address,target,other = 0x84B0,4,high
        else:
            w(t,high,0,4)
            w(t,0x84B0,0,4)
    elif mode == 3:
        if value <= 3600:
            address,target = 0x84B0,4
        else:
            w(t,0x84B0,0,4)
    elif mode == 4:
        if value > 5525:
            address,target = 0x84A8,2
        else:
            w(t,0x84A8,0,4)
    if address is None:
        return False
    old = r(t,address,4)
    if old == 0:
        if other is not None:
            w(t,other,0,4)
        w(t,address,now,4)
    elif ((now-old)&0xFFFFFFFF) >= 100000:
        w(t,address,0,4)
        w(t,0x84A0,target)
    return True


def execute(t,count,now,low_bits=0,polls=(0,128)):
    before = state(t)
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    timed = model(ref,count,now)
    raw = (count<<6)|low_bits
    t.io.accesses = []
    t.io.samples = {(0xFFFFF818,1):list(polls),(0xFFFFF810,2):[raw]}
    wanted = [['read',0xFFFFF818,1,p] for p in polls]+[['read',0xFFFFF810,2,raw]]
    if timed:
        t.io.samples[(0xFFFFF6C0,4)] = [now]
        wanted.append(['read',0xFFFFF6C0,4,now])
    saved,sp,mask = t.r[8:15],t.r[15],t.sr&~0x301
    t.run(0x112E6,limit=200000)
    assert ram(t) == ram(ref),(before,count,now,state(t),state(ref))
    assert (t.r[8:15],t.r[15],t.sr&~0x301) == (saved,sp,mask)
    assert t.io.accesses == wanted and all(not v for v in t.io.samples.values())
    return dict(before=before,count=count,now=now,after=state(t),accesses=wanted,
                whole_application_ram_checked=True)


def initialized(seed):
    t = Machine()
    for a in range(0x849C,0x84B8):
        w(t,a,(a*37+seed*19)&255)
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    for a,v,n in [(0x84A0,1,1),(0x84A2,0,2),(0x84A8,0,4),(0x84AC,0,4),(0x84B0,0,4)]:
        w(ref,a,v,n)
    t.run(0x112CC)
    assert ram(t) == ram(ref)
    return t


def main():
    for seed in range(256):
        initialized(seed)
    clocks = [(0,0),(0,1),(1,100000),(1,100001),(1,100002),(0xFFFF0000,34464)]
    cases = 0
    for mode in [1,2,3,4]:
        for count in range(1024):
            for old,now in clocks:
                t = Machine()
                w(t,0x84A0,mode)
                for a in [0x84A8,0x84AC,0x84B0]:
                    w(t,a,old,4)
                t.r[8:15] = [(0x10203040*n)&0xFFFFFFFF for n in range(1,8)]
                execute(t,count,now,low_bits=count&63)
                cases += 1
    for mode in range(256):
        t = Machine()
        w(t,0x84A0,mode)
        for a in [0x84A8,0x84AC,0x84B0]:
            w(t,a,7,4)
        execute(t,600,200000,polls=(128,))
        cases += 1
    for mode,count,clocks in itertools.product([1,2,3,4],[100,200,300,600],
                                                itertools.product([0,7],repeat=3)):
        t = Machine()
        w(t,0x84A0,mode)
        for a,v in zip([0x84A8,0x84AC,0x84B0],clocks):
            w(t,a,v,4)
        execute(t,count,100007)
        cases += 1
    t = initialized(0)
    stimulus = [(600,n) for n in [1,100000,100001,100002,200001,200002]]
    stimulus += [(100,200003),(100,300003),(600,300004),(600,400004),(600,400005),(600,500005)]
    chain = [execute(t,count,now) for count,now in stimulus]
    assert [e['after']['0x84a0'] for e in chain] == [1,1,2,2,2,3,3,4,4,2,2,3]
    result = dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        initializers=256,independent_whole_ram_cases=cases,initialized_low_recovery_chain=chain,
        limits='Explicit F810 ADC/statusF818/F6C0 samples. No sensor units/native caller cadence/full boot; capture84EC remains separate.')
    (ROOT/'tcu-readiness-a-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(status='PASS',initializers=256,cases=cases,
               chain_modes=[e['after']['0x84a0'] for e in chain]))


if __name__ == '__main__':
    main()
