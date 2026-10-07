"""Original diagnostic timer startup, admission and finite-sample ISR prefixes.

Independent startup/gate/profile models, differential original1218E body RAM.
Stops before RTE; no full boot, hardware IRQ acceptance or physical cadence.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_tcu_capture_interrupts import CaptureSamples,run_preserving_prefix
from verify_control_acquisition_schedule import execute_slice

ROOT = Path(__file__).resolve().parent
WIDTHS = {0xFFFFF401:1,0xFFFFF480:2,0xFFFFF482:2,0xFFFFF4AB:1,
          0xFFFFF4A0:2,0xFFFFF4A2:2}


class Samples(CaptureSamples):
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if WIDTHS.get(address) != size:
            raise ValueError('Unsupported diagnostic timer write')
        self.accesses.append(['write',address,size,value&((1<<(8*size))-1)])


class Machine(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.io = Samples()

    def read(self,address,size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.io.write(address,value,size)
        return super().write(address,value,size)


def initialization_inputs(old,status,enable,control,*,start_bit=16,status_bit=1,
                          control_address=0xFFFFF4AB,counter_address=0xFFFFF4A0,
                          compare=15625):
    """Finite read samples and independent ordered write model for native callers."""
    stopped = old & (255 ^ start_bit)
    samples = {(0xFFFFF401,1):[old,stopped],(0xFFFFF480,2):[status],
        (0xFFFFF482,2):[enable],(control_address,1):[control,control&247,control&243,control&241]}
    expected = [['read',0xFFFFF401,1,old],['write',0xFFFFF401,1,stopped],
        ['read',0xFFFFF480,2,status],['write',0xFFFFF480,2,status&(65535 ^ status_bit)],
        ['read',0xFFFFF482,2,enable],['write',0xFFFFF482,2,enable|status_bit]]
    value = control
    for mask in [247,251,253]:
        expected += [['read',control_address,1,value],['write',control_address,1,value&mask]]
        value &= mask
    expected += [['read',control_address,1,value],['write',control_address,1,value|1],
        ['write',counter_address,2,0],['write',counter_address+2,2,compare],
        ['read',0xFFFFF401,1,stopped],['write',0xFFFFF401,1,old|start_bit]]
    return samples,expected


def check_init(old):
    t = Machine()
    status,enable = (old*257)&65535,(old*131)&65535
    t.io.samples,expected = initialization_inputs(old,status,enable,old)
    before = ram(t)
    saved,sp,sr = t.r[8:15],t.r[15],t.sr
    t.run(0x167E4)
    assert ram(t) == before and (t.r[8:15],t.r[15],t.sr) == (saved,sp,sr)
    assert t.io.accesses == expected and all(not v for v in t.io.samples.values())
    return expected


PREFIX = dict(index=9,flag=1,compare=0xFFFFF4A2,counter=0xFFFFF4A0,
              increment=15625,entry=0x1682C,stop=0x1688C,body=0x1218E,mode=0x8006)


def execute_prefix(t,status,second,compare,count,reloaded,start,end,*,spec=None,reference=None,io=None):
    spec = PREFIX if spec is None else spec
    index,flag = spec['index'],spec['flag']
    cmp_address,cnt_address = spec['compare'],spec['counter']
    io = t.io if io is None else io
    assert int.from_bytes(TCU[0x5F600+4*index:0x5F604+4*index],'big') == 16
    armed = bool(status&flag)
    ref = reference
    if ref is None:
        ref = SHRotate(TCU)
        ref.ram = dict(t.ram)
    w(ref,0x8728+4*index,start,4)
    latency = min(65535,((count-compare)&65535)*16//10)
    w(ref,0x86E0+2*index,latency,2)
    w(ref,0x8704+2*index,max(r(ref,0x8704+2*index,2),latency),2)
    if armed:
        ref.run(spec['body'],limit=2000000)
    duration = min(65535,((end-start)&0xFFFFFFFF)//10)
    w(ref,0x8698+2*index,duration,2)
    w(ref,0x86BC+2*index,max(r(ref,0x86BC+2*index,2),duration),2)
    io.accesses = []
    io.samples = {(cmp_address,2):[compare,reloaded] if armed else [compare],
        (cnt_address,2):[count],(0xFFFFF480,2):[status,second] if armed else [status],
        (0xFFFFF6C0,4):[start,end]}
    run_preserving_prefix(t,spec['entry'],spec['stop'])
    assert ram(t) == ram(ref)
    expected = [['read',cmp_address,2,compare],['read',cnt_address,2,count],
        ['read',0xFFFFF6C0,4,start],['read',0xFFFFF480,2,status]]
    if armed:
        expected += [['read',0xFFFFF480,2,second],['write',0xFFFFF480,2,second&(~flag&65535)],
                     ['read',cmp_address,2,reloaded],['write',cmp_address,2,(reloaded+spec['increment'])&65535]]
    expected += [['read',0xFFFFF6C0,4,end]]
    assert io.accesses == expected and all(not v for v in io.samples.values())
    return dict(armed=armed,latency=latency,duration=duration,mode_after=r(t,spec['mode']),
        accesses=expected,differential_application_ram_checked=True,registers_checked=True)


def main():
    examples = []
    for old in range(256):
        accesses = check_init(old)
        if old in [0,255]:
            examples.append(accesses)
    cases = [(mode,values) for mode in range(256)
             for values in itertools.product([0,3],repeat=3)]
    for field in range(3):
        for value in range(256):
            values = [3,3,3]
            values[field] = value
            cases.append((1,values))
    cases += [(3,[value,0,0]) for value in range(256)]
    initializations = promotions = 0
    for mode,values in cases:
        t = SHRotate(TCU)
        w(t,0x8006,mode)
        for a,v in zip([0x84A0,0x84D8,0x8007],values):
            w(t,a,v)
        ref = SHRotate(TCU)
        ref.ram = dict(t.ram)
        admitted = mode == 1 and all(v == 3 for v in values)
        promoted = mode == 3 and values[0] == 4
        if not admitted:
            w(ref,0x8006,5 if promoted else mode)
        execute_slice(t,0x1218E,0x1267C if admitted else 0x12682)
        assert ram(t) == ram(ref)
        assert r(t,0x8006) == (mode if admitted else 5 if promoted else mode)
        initializations += admitted
        promotions += promoted
    rejected = 0
    for address,size in [(0xFFFFF4A2,1),(0xFFFFF480,4),(0xFFFFF4AC,1)]:
        try:
            Samples().write(address,0,size)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('Unexpected write accepted')
    from probe_tcu_qualified_receive import fixture
    base = fixture()
    prefixes = []
    for mode,ready,armed in itertools.product([0,1,3,5,255],[False,True],[False,True]):
        t = Machine()
        t.ram = dict(base.ram)
        w(t,0x8006,mode)
        for a in [0x84A0,0x84D8,0x8007]:
            w(t,a,3 if ready else 0)
        n = len(prefixes)
        compare,count = [(0,65535),(65530,4),(2000,2010),(3000,3000)][n%4]
        start,end = [(1000,2000),(0xFFFFFF00,500),(100,900100),(1234,1234)][n%4]
        event = execute_prefix(t,0xA500|int(armed),0xBEEF,compare,count,65530,start,end)
        assert event['mode_after'] == (3 if armed and mode == 1 and ready else mode)
        prefixes.append(dict(initial_mode=mode,ready=ready,**event))
    result = dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        initializers=256,initializer_accesses=18,independent_gate_cases=len(cases),
        initialization_boundaries=initializations,mode3_to5=promotions,
        rejected_writes=rejected,examples=examples,prefix_cases=len(prefixes),prefixes=prefixes,
        limits='Isolated finite-sample prefixes; diagnostic body RAM is differential against original1218E. No full boot, hardware acceptance, RTE or physical clock proof.')
    (ROOT/'tcu-diagnostic-timer-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['examples','prefixes','limits']})


if __name__ == '__main__':
    main()
