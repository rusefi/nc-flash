"""Original timer and port-B configuration, followed by both output callbacks.

Independent exact write tables and software register snapshots. No hardware
clock counting, reserved-bit side effects, pin voltage or interrupt delivery.
"""
import copy
import hashlib
import json
import random
from pathlib import Path
import verify_tcu_cycle_callback as cycle
from verify_tcu_cycle_callback import task,TCU,w,r,execute
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent

def writes(size,pairs):return [(a,size,v) for a,v in pairs]

WRITES={
 0x1447E:writes(1,[(0xF401,0),(0xF400,0),(0xF402,0)]),
 0x14962:writes(1,[(0xF484,0)]),
 0x1448E:writes(1,[(0xF404,1),(0xF406,1),(0xF408,1),(0xF40A,1)]),
 0x144A2:writes(1,[(0xF45D,4),(0xF45C,4),(0xF62B,0),(0xF62A,0),(0xF4AC,4),(0xF4CC,5),(0xF4EC,4),
                    (0xF521,0),(0xF520,0),(0xF5A1,0),(0xF5A0,0),(0xF668,0x53),(0xF698,0),(0xF69A,0),(0xF69C,0),(0xF5C8,0)]),
 0x1454E:writes(1,[(0xF42A,0),(0xF459,0),(0xF458,0),(0xF45B,0),(0xF45A,0),(0xF627,1),(0xF626,0),(0xF629,0),
                    (0xF628,0),(0xF4AB,1),(0xF4AA,0),(0xF4CB,0),(0xF4CA,16),(0xF4EB,17),(0xF4EA,0),(0xF5C6,1)]),
 0x14598:writes(2,[(a,0) for a in [0xF42C,0xF45E,0xF460,0xF62C,0xF62E,0xF480,0xF522,0xF5A2,0xF66A,0xF69E,0xF5CA]]),
 0x145C8:writes(2,[(0xF42E,0),(0xF462,0),(0xF464,1),(0xF630,1),(0xF632,0),(0xF482,0),(0xF524,1),
                    (0xF5A4,0),(0xF66C,0),(0xF6A0,0),(0xF6EA,0),(0xF5CC,1)]),
 0x1496A:writes(1,[(0xF526,0)]),
 0x147AA:writes(2,[(0xF730,0x80FF),(0xF732,0xA5),(0xF734,0x55),(0xF738,0x500)])}
CALLS=[0x1447E,0x14962,0x1448E,0x144A2,0x1454E,0x14598,0x145C8]
WIDTHS={a:n for rows in WRITES.values() for a,n,v in rows}
WIDTHS.update({a:2 for a in range(0xF500,0xF520,2)})
WIDTHS.update({0xF600:2,0xF604:2,0xF736:2})


class ConfigurationRegisters(cycle.CycleRegisters):
    def read(self,address,size):
        if self.configuring and address>=0xFFFFE000:
            a=address-0xFFFF0000
            if WIDTHS.get(a)!=size:raise ValueError('Unsupported configuration read')
            value=self.configuration[a];self.configuration_trace.append(('read',a,size,value));return value
        return super().read(address,size)
    def write(self,address,value,size):
        if self.configuring and address>=0xFFFFE000:
            a=address-0xFFFF0000
            if WIDTHS.get(a)!=size:raise ValueError('Unsupported configuration write')
            value &= (1<<(8*size))-1
            self.configuration[a]=value;self.configuration_trace.append(('write',a,size,value));return
        super().write(address,value,size)


def fixture(seed=0):
    t=cycle.fixture();t.__class__=ConfigurationRegisters;t.configuring=True
    rng=random.Random(seed);t.configuration={a:rng.randrange(1<<(8*n)) for a,n in WIDTHS.items()};t.configuration_trace=[]
    return t


def model_writes(t,rows):
    for a,n,v in rows:t.configuration[a]=v;t.configuration_trace.append(('write',a,n,v))


def equal(t,ref):
    task.equal(t,ref)
    assert t.configuration==ref.configuration and t.configuration_trace==ref.configuration_trace


def component(t,entry):
    ref=copy.deepcopy(t);model_writes(ref,WRITES[entry]);execute(t,entry);equal(t,ref)


def start_model(t):
    old=t.configuration[0xF401];t.configuration_trace.append(('read',0xF401,1,old))
    model_writes(t,[(0xF401,1,old&251),(0xF400,1,0)])
    w(t,0x87F4,0)
    model_writes(t,[(a,2,0) for a in [0xF506,0xF504,0xF502,0xF500]])
    model_writes(t,[(a,2,33333) for a in [0xF50A,0xF508,0xF50E,0xF50C,0xF512,0xF510,0xF516,0xF514,0xF51A,0xF518,0xF51E,0xF51C]])
    model_writes(t,[(0xF400,1,0),(0xF600,2,0),(0xF604,2,4166),(0xF400,1,15)])
    t.configuration_trace.append(('read',0xF401,1,old&251));model_writes(t,[(0xF401,1,old|4)])


def start(t):
    ref=copy.deepcopy(t);start_model(ref);execute(t,0x168AC);equal(t,ref)


def caller(t,begin,end,entries):
    ref=copy.deepcopy(t)
    for entry in entries:model_writes(ref,WRITES[entry])
    sp,mask=t.r[15],t.sr&~0x301;execute_slice(t,begin,end)
    assert t.r[15]==sp and t.sr&~0x301==mask
    equal(t,ref)


def configure(t):
    caller(t,0x155C8,0x155F0,CALLS)
    caller(t,0x14902,0x14906,[0x147AA])
    caller(t,0x15650,0x15654,[0x1496A])
    start(t)
    assert len(t.configuration_trace)==93
    assert all(t.configuration[a]==1 for a in [0xF404,0xF406,0xF408,0xF40A,0xF630,0xF524])
    assert all(t.configuration[a]==0 for a in [0xF62B,0xF62A,0xF521,0xF520,0xF526])
    assert t.configuration[0xF734]==0x55 and t.configuration[0xF400]==15 and t.configuration[0xF401]==4


def direct():
    counts=dict(component=0,start=0,caller_sequence=0,rejected=0)
    for seed in range(16):
        for entry in WRITES:
            t=fixture(seed);component(t,entry);counts['component']+=1
        t=fixture(seed);start(t);counts['start']+=1
        t=fixture(seed);old=t.configuration[0xF736];configure(t)
        assert t.configuration[0xF736]==old;counts['caller_sequence']+=1
    t=fixture()
    for a,n,writing in [(0xFFFFF404,2,False),(0xFFFFF520,2,True),(0xFFFFF734,1,True),
                         (0xFFFFF528,1,True),(0xFFFFF632,1,False),(0xFFFFF800,2,False)]:
        try:
            if writing:t.write(a,0,n)
            else:t.read(a,n)
        except ValueError:counts['rejected']+=1
        else:raise AssertionError('unsupported configured access')
    return counts


def retained():
    rows=[];snapshots=[]
    for inversion in [0,15]:
        t=fixture(inversion);t.configuration[0xF736]=inversion;configure(t)
        snapshots.append(dict(inversion=inversion,registers={hex(a):v for a,v in t.configuration.items()},trace=t.configuration_trace))
        # Transfer only explicitly configured callback latches. Configuration
        # snapshot stays historical; runtime bufferwrites use prior output sink.
        for address in t.timer:
            a=address-0xFFFF0000
            if a in t.configuration:t.timer[address]=t.configuration[a]
        t.configuring=False;task.initialize_history(t);w(t,0x8002,1);w(t,0x8008,3);w(t,0x84F8,3)
        for a in [0xA975,0xA976,0xA958]:w(t,a,1)
        for call in range(1,17):
            t.adc_samples={a:368<<6 for a in task.ADC};t.adc_samples[0xFFFFF810]=600<<6;t.adc_samples[0xFFFFF812]=590<<6
            t.timer[0xFFFFF500]=2;t.timer[0xFFFFF522]=1;t.timestamps=[call*100000,call*100000+234]
            t.timer_trace=[];t.adc_reads=[];t.output_writes=[];cycle.cycle(t)
            outputs=[]
            for phase in range(4):
                t.timer[0xFFFFF62C]=1;t.timer[0xFFFFF600]=(t.timer[0xFFFFF604]+7)&65535
                t.timestamps=[call*100000+1000+phase*1000,call*100000+1123+phase*1000]
                t.timer_trace=[];t.adc_reads=[];t.output_writes=[];task.interrupt(t);outputs.extend(t.output_writes)
            assert len(outputs)==4 and r(t,0xA518,2)==13203 and t.configuration[0xF736]==inversion
            rows.append(dict(inversion=inversion,cycle=call,published=r(t,0xA518,2),outputs=outputs,phase=r(t,0x84F8)))
    assert [row['outputs'] for row in rows[:16]]==[row['outputs'] for row in rows[16:]]
    return rows,snapshots


def main():
    counts=direct();rows,snapshots=retained();print(counts,'retained',len(rows),flush=True)
    pdf=ROOT/'sources/renesas-sh7055s-hardware-rej09b0045-0200h.pdf'
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,
        source_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source_pages_zero=[240,266,268,269,271,272,346,347,685,696,697],
        config_snapshots=snapshots,retained_cycles=len(rows),compare_bodies=4*len(rows),retained=rows,
        limits='Selected actual initialization caller slices, not full15574/boot. CompatibleSH7055S register interpretation; Pclock absolutefrequency, PBIR writer/resetcontext, hardwaretimer/pin/plant, delivery/RTE remain open.')
    (ROOT/'tcu-timer-configuration-verification.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
