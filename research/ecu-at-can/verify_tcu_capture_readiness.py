"""Original capture readiness initialization/admission and native CMT0 chain.

Independent whole-RAM history/state and ordered-MMIO models. ADC/time/status
are explicit external inputs; no full boot or hardware interrupt delivery.
"""
import hashlib
import itertools
import json
from pathlib import Path

import verify_tcu_capture_configuration as config
import verify_tcu_readiness_b as adc
from verify_tcu_cmt0_interrupt import Samples,execute_prefix
from verify_tcu_cmt0_wheel import model as wheel_model
from verify_tcu_capture_interrupts import CaptureSamples
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent


class Machine(config.ConfigurationRegisters):
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if self.cmt_active and address >= 0xFFFFE000:
            return self.cmt_io.read(address,size)
        if address in [0xFFFFF812,0xFFFFF818,0xFFFFF6C0]:
            return self.io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if self.cmt_active and address >= 0xFFFFE000:
            return self.cmt_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if self.cmt_active and pc in [0x123C2,0x128B6,0x11864,0x1E506,0x11A64]:
            self.cmt_entries.append(hex(pc))
        return super().instruction(pc)


def fixture(seed):
    t = config.fixture(seed&255)
    t.__class__ = Machine
    t.cmt_active = False
    t.cmt_io = Samples()
    t.cmt_entries = []
    t.io = CaptureSamples()
    for lo,hi in [(0x88E0,0x8914),(0x9190,0x9300)]:
        for a in range(lo,hi):
            w(t,a,(a*37+seed*19)&255)
    return t


def histories_model(t):
    assert TCU[0x77444] == 18 and TCU[0x77448] == 24
    assert TCU[0x76E46] == 14 and TCU[0x76DE0] == 18
    for a in [0x88F0,0x88F2,0x88F4,0x8900,0x8902,0x8904]:
        w(t,a,0,2)
    for a in [0x88F8,0x88FC,0x8908,0x890C]:
        w(t,a,0,4)
    for a in [0x810D,0x8196,0x9195,0x810C,0x9244]:
        w(t,a,255)
    for base,count,value in [(0x91CC,18,57344),(0x9248,24,73728)]:
        for i in range(count):
            w(t,base+4*i,value,4)
    w(t,0x91B4,0)
    w(t,0x800D,0)
    w(t,0x9198,0xFFFFFFFF,4)
    w(t,0x919C,0xFFFFFFFF,4)
    w(t,0x9238,0x7FFFFFFF,4)


def initialize(t):
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    w(ref,0x84EC,1)
    w(ref,0x8450,255)
    registers,mask = t.r[8:].copy(),t.sr&~1
    t.configuration_trace = []
    t.run(0x122D8)
    assert ram(t) == ram(ref)
    assert t.r[8:] == registers and t.sr&~1 == mask
    assert not t.configuration_trace


def model(ref,wanted):
    """Independent RAM and ordered configuration model for native callers."""
    state,b_ready,age = [r(ref,a) for a in [0x84EC,0x84D8,0x8450]]
    trace = []
    admitted = state == 1 and b_ready == 3
    if admitted:
        histories_model(ref)
        w(ref,0x8450,0)
        w(ref,0x84EC,2)
        for channel in ['A','B']:
            config.model(wanted,trace,channel)
    elif state == 2 and age >= 20:
        w(ref,0x84EC,3)
    return trace,admitted


def check(t):
    state,b_ready,age = [r(t,a) for a in [0x84EC,0x84D8,0x8450]]
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    wanted = t.configuration.copy()
    trace,admitted = model(ref,wanted)
    t.configuration_trace = []
    saved,mask = t.r[8:].copy(),t.sr&~1
    t.run(0x122F4)
    assert ram(t) == ram(ref),(state,b_ready,age)
    assert t.configuration == wanted and t.configuration_trace == trace
    assert t.r[8:] == saved and t.sr&~1 == mask
    return dict(before=[state,b_ready,age],after=[r(t,a) for a in [0x84EC,0x84D8,0x8450]],
                capture_enabled=admitted,mmio_accesses=len(trace),whole_application_ram_checked=True)


def tick(t,n,start=None,end=None):
    start = n*1000 if start is None else start
    end = n*1000+100 if end is None else end
    duration = min(65535,((end-start)&0xFFFFFFFF)//10)
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    wheel_model(ref)
    w(ref,0x800A,3)
    w(ref,0x84D0,r(ref,0x84D0,4)+1,4)
    w(ref,0x91AC,min(65535,r(ref,0x91AC,2)+1),2)
    w(ref,0x8758,start,4)
    w(ref,0x86B0,duration,2)
    w(ref,0x86D4,max(duration,r(ref,0x86D4,2)),2)
    t.cmt_active = True
    try:
        event = execute_prefix(t,128,128,start,end)
    finally:
        t.cmt_active = False
    assert ram(t) == ram(ref)
    return event


def main():
    for seed in range(256):
        initialize(fixture(seed))
    cases = [(mode,b,age) for mode,b,age in itertools.product(range(256),[0,3],[0,19,20,255])]
    cases += [(1,b,123) for b in range(256)]
    cases += [(2,0,age) for age in range(256)]
    for seed,(mode,b,age) in enumerate(cases):
        t = fixture(seed)
        for a,v in [(0x84EC,mode),(0x84D8,b),(0x8450,age)]:
            w(t,a,v)
        check(t)
    # Additional admitted cases vary every configured TIOR0/start byte.
    for seed in range(256):
        t = fixture(seed)
        w(t,0x84EC,1)
        w(t,0x84D8,3)
        check(t)
    t = fixture(0)
    t.run(0x11DD8)
    initialize(t)
    t.cmt_io.samples = {(0xFFFFF710,2):[0]}
    t.cmt_active = True
    try:
        t.run(0x123B0)
    finally:
        t.cmt_active = False
    chain = []
    for now in [1,100001,100002,200002]:
        result = adc.execute(t,600,now)
        chain.append(dict(adc=result,capture=check(t)))
    assert [s['capture']['after'][0] for s in chain] == [1,1,1,2]
    ticks = []
    for n in range(1,97):
        event = tick(t,n)
        result = check(t)
        assert result['after'][2] == (n+4)//5
        assert result['after'][0] == (3 if n == 96 else 2)
        ticks.append(dict(tick=n,event=event,capture=result))
    result = dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        initializers=256,independent_readiness_cases=len(cases)+256,
        initialized_adc_capture_chain=chain,native_cmt0_chain=ticks,
        first_ready_tick=96,conditional_phi_since_first_clock_epoch=1920000,
        limits='CMT0 epoch0/phase0 and pollingaftereachtick arefixtures; actual122F4caller/admission timing separate. No forcedreadiness/ages inchain, no fullboot/physicalIRQ.')
    (ROOT/'tcu-capture-readiness-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(status='PASS',initializers=256,cases=len(cases)+256,ready_tick=96))


if __name__ == '__main__':
    main()
