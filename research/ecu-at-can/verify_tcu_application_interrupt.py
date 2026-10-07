"""Original application timer init/ISR with actual admission and complete task.

Finite peripheral samples, stop before RTE. Differential whole-RAM comparison
to original1220A plus independent profile/MMIO models. Not hardware cadence.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

import verify_tcu_application_order as app
from verify_tcu_capture_interrupts import CaptureSamples,run_preserving_prefix
from verify_tcu_base_publication import ram
from verify_can201_byte6 import TCU,r,w
from sh_subset import signed
from sh_rotate import SHRotate
from verify_control_acquisition_schedule import execute_slice

ROOT=Path(__file__).resolve().parent
ADDRESSES={0xFFFFF401,0xFFFFF442,0xFFFFF454,0xFFFFF460,0xFFFFF6C0}


class Samples(CaptureSamples):
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        widths={0xFFFFF401:1,0xFFFFF442:2,0xFFFFF454:2,0xFFFFF460:2}
        if widths.get(address)!=size:
            raise ValueError('Unsupported application timer write')
        self.accesses.append(['write',address,size,value&((1<<(8*size))-1)])


class Machine(app.ObservedTask):
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if address in ADDRESSES:return self.application_io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address in ADDRESSES:return self.application_io.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        if pc in [0x1220A,0x126DA,0x126EC,0x1E5F6]:
            self.application_entries.append(hex(pc))
        return super().instruction(pc)


def fixture(**kw):
    t=app.fixture(**kw);t.__class__=Machine
    t.application_io=Samples();t.application_entries=[]
    return t


def execute_prefix(t,status,second,compare,count,reloaded,start,end):
    phase=r(t,0x84F4)&7;index=[0,1,2,3,0,1,2,4][phase]
    assert int.from_bytes(TCU[0x5F600+4*index:0x5F604+4*index],'big')==16
    armed=bool(status&1)
    t.application_entries=[];t.application_io.accesses=[]
    ref=copy.deepcopy(t)
    w(ref,0x8728+4*index,start,4)
    latency=min(65535,((count-compare)&65535)*16//10)
    w(ref,0x86E0+2*index,latency,2)
    w(ref,0x8704+2*index,max(r(ref,0x8704+2*index,2),latency),2)
    if armed:
        ref.run(0x1220A,limit=2000000)
        ref.check_pending(0xFFFFFFF0)
        assert ref.pending is None
    duration=min(65535,((end-start)&0xFFFFFFFF)//10)
    w(ref,0x8698+2*index,duration,2)
    w(ref,0x86BC+2*index,max(r(ref,0x86BC+2*index,2),duration),2)
    t.application_io.samples={(0xFFFFF454,2):[compare,reloaded] if armed else [compare],
        (0xFFFFF442,2):[count],(0xFFFFF460,2):[status,second] if armed else [status],
        (0xFFFFF6C0,4):[start,end]}
    run_preserving_prefix(t,0x16A58,0x16B00)
    assert t.pending is None
    assert ram(t)==ram(ref),('application ISR differential RAM',phase,status)
    app.pins.setup.equal(t,ref)
    assert (t.mcr,t.gsr,t.hcan_trace,t.digital_trace)==(ref.mcr,ref.gsr,ref.hcan_trace,ref.digital_trace)
    assert (t.direct_calls,t.periodic_arguments,t.events,t.verified_boundaries)==(ref.direct_calls,ref.periodic_arguments,ref.events,ref.verified_boundaries)
    assert t.application_entries==ref.application_entries
    expected=[['read',0xFFFFF454,2,compare],['read',0xFFFFF442,2,count],
        ['read',0xFFFFF6C0,4,start],['read',0xFFFFF460,2,status]]
    if armed:expected += [['read',0xFFFFF460,2,second],['write',0xFFFFF460,2,second&65534],
        ['read',0xFFFFF454,2,reloaded],['write',0xFFFFF454,2,(reloaded+2560)&65535]]
    expected += [['read',0xFFFFF6C0,4,end]]
    assert t.application_io.accesses==expected and all(not v for v in t.application_io.samples.values())
    return dict(phase=phase,index=index,armed=armed,latency=latency,duration=duration,
        mode_after=r(t,0x8007),stage_after=r(t,0x84F5),phase_after=r(t,0x84F4),
        entries=t.application_entries,accesses=expected,
        differential_application_ram_checked=True,registers_and_mmio_checked=True,
        independent_command_pin_boundaries=len(t.verified_boundaries))


def main():
    assert hashlib.sha256(TCU).hexdigest()=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    base=fixture();initializations=0
    for old in range(256):
        t=copy.deepcopy(base);before=ram(t)
        t.application_io.samples={(0xFFFFF401,1):[old,old&247]}
        t.run(0x16A3C)
        assert ram(t)==before
        assert t.application_io.accesses==[['read',0xFFFFF401,1,old],
            ['write',0xFFFFF401,1,old&247],['write',0xFFFFF442,2,0],
            ['write',0xFFFFF454,2,2560],['read',0xFFFFF401,1,old&247],
            ['write',0xFFFFF401,1,old|8]]
        assert all(not v for v in t.application_io.samples.values())
        initializations+=1
    # Execute the original admission gate to its first child boundary. This
    # independently checks the predicate without using the task as an oracle.
    gates=[(mode,values) for mode in range(256)
           for values in itertools.product([0,3],repeat=3)]
    for field in range(3):
        for value in range(256):
            values=[3,3,3];values[field]=value
            gates.append((1,values))
    for mode,values in gates:
        t=SHRotate(TCU)
        w(t,0x8007,mode)
        for a,value in zip([0x84A0,0x84D8,0x84EC],values):w(t,a,value)
        before=ram(t)
        admitted=mode==1 and all(value==3 for value in values)
        execute_slice(t,0x1220A,0x126DA if admitted else 0x126EC)
        assert ram(t)==before
        assert (0x1223E in t.visited)==admitted
    rows=[]
    for phase,armed in itertools.product(range(8),[False,True]):
        t=fixture(phase=phase)
        pair=[(0,65535),(65530,4),(2000,2010),(3000,3000)][phase%4]
        start,end=[(1000,2000),(0xFFFFFF00,500),(100,900100),(1234,1234)][phase%4]
        row=execute_prefix(t,0xA500|int(armed),0xBEEF,*pair,65530,start,end)
        rows.append(dict(initial_mode=3,**row))
    for mode,ready in itertools.product([0,1,2,3,255],[False,True]):
        t=fixture(mode=mode,stage=2,phase=7)
        for a in [0x84A0,0x84D8,0x84EC]:w(t,a,3 if ready else 0)
        row=execute_prefix(t,1,1,2560,2567,2560,1000,1100)
        assert ('0x126da' in row['entries'])==(mode==1 and ready)
        assert row['mode_after']==(3 if mode==1 and ready else mode)
        rows.append(dict(initial_mode=mode,ready=ready,**row))
    rejected=0
    for address,size in [(0xFFFFF454,1),(0xFFFFF460,4),(0xFFFFF458,2)]:
        try:Samples().write(address,0,size)
        except ValueError:rejected+=1
        else:raise AssertionError('Unsupported timer write admitted')
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        initializer_cases=initializations,independent_admission_gate_cases=len(gates),
        prefix_cases=len(rows),rejected_writes=rejected,rows=rows,
        limits='Differential original1220A task, independent profile/MMIO and existing command/pin oracles. Not complete semantic oracle, fullboot, actual interrupt delivery, RTE, absolute clock, application/capture/CAN start offset or latency.')
    (ROOT/'tcu-application-interrupt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(dict(status='PASS',initializations=initializations,admission_gates=len(gates),
               prefixes=len(rows),rejected=rejected),flush=True)


if __name__=='__main__':main()
