"""Locate full15574 hardware startup boundary; independently verify final flags.

Combine only the existing strict INTC and configuration register owners. No
new register behavior, skipped callees or injected recovery/admission flags.
Input state is the pre-existing native timeline fixture, not power-on reset.
"""
import hashlib
import json
from pathlib import Path

import verify_tcu_native_can_timeline as native
from verify_tcu_interrupt_setup import InterruptRegisters
from verify_control_acquisition_schedule import execute_slice
from verify_tcu_base_publication import ram
from verify_can201_byte6 import TCU,r,w
from sh_rotate import SHRotate
from tcu_startup_ubc import Registers as UBCRegisters
from tcu_startup_bsc import Registers as BSCRegisters
from tcu_startup_dmaor import Registers as DMAORRegisters
from tcu_startup_interval import Registers as IntervalRegisters
from tcu_startup_downcount import Registers as DowncountRegisters
from tcu_startup_connection import Registers as ConnectionRegisters

ROOT=Path(__file__).resolve().parent


class Machine(native.Machine):
    def read(self,address,size):
        if address >= 0xFFFFE000:
            self.last_startup_mmio=dict(operation="read",address=hex(address),size=size)
        if self.connection is not None and address in self.connection.values:
            return self.connection.read(address,size)
        if self.downcount is not None and address in self.downcount.values:
            return self.downcount.read(address,size)
        if self.interval is not None and address in self.interval.values:
            return self.interval.read(address,size)
        if self.dmaor is not None and address in self.dmaor.values:
            return self.dmaor.read(address,size)
        if self.bsc is not None and address in self.bsc.values:
            return self.bsc.read(address,size)
        if self.ubc is not None and address in self.ubc.values:
            return self.ubc.read(address,size)
        if address in self.intc.values:
            return self.intc.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if address >= 0xFFFFE000:
            self.last_startup_mmio=dict(operation="write",address=hex(address),size=size,value=value)
        if self.connection is not None and address in self.connection.values:
            return self.connection.write(address,value,size)
        if self.downcount is not None and address in self.downcount.values:
            return self.downcount.write(address,value,size)
        if self.interval is not None and address in self.interval.values:
            return self.interval.write(address,value,size)
        if self.dmaor is not None and address in self.dmaor.values:
            return self.dmaor.write(address,value,size)
        if self.bsc is not None and address in self.bsc.values:
            return self.bsc.write(address,value,size)
        if self.ubc is not None and address in self.ubc.values:
            return self.ubc.write(address,value,size)
        if address in self.intc.values:
            return self.intc.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self,pc):
        self.startup_pc=pc
        opcode=self.read(pc,2)
        if opcode&0xF0FF in [0x400B,0x402B]:
            self.startup_calls.append(dict(pc=hex(pc),target=hex(self.r[(opcode>>8)&15])))
        return super().instruction(pc)


def main(nmi_level=None, filename="tcu-hardware-startup-probe.json", irq_status=None, ubc=False, wcr_initial=None, dmaor=False, interval=False, downcount=False, connection=False):
    cases=0
    for value in range(256):
        t=SHRotate(TCU)
        w(t,0x868C,value);w(t,0x868D,255-value)
        w(t,0x868B,0xA5);w(t,0x868E,0x5A)
        ref=SHRotate(TCU);ref.ram=t.ram.copy()
        w(ref,0x868C,1);w(ref,0x868D,1)
        execute_slice(t,0x1570C,0x15716)
        assert ram(t)==ram(ref)
        cases+=1
    t=native.fixture()
    t.__class__=Machine
    t.intc=InterruptRegisters(0,nmi_level=nmi_level,irq_status=irq_status)
    t.connection=ConnectionRegisters() if connection else None
    t.downcount=DowncountRegisters() if downcount else None
    t.interval=IntervalRegisters() if interval else None
    t.dmaor=DMAORRegisters() if dmaor else None
    t.ubc=UBCRegisters() if ubc else None
    t.bsc=BSCRegisters(wcr_initial=wcr_initial) if wcr_initial is not None else None
    t.configuring=True
    t.startup_calls=[];t.startup_pc=None;t.last_startup_mmio=None
    before=dict(recovery=r(t,0x868C),second=r(t,0x868D))
    try:
        t.run(0x15574,limit=2000000)
        status,error='RETURNED',None
    except (ValueError,RuntimeError,AssertionError,KeyError) as exc:
        status,error='REJECTED',type(exc).__name__+': '+str(exc)
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        final_flag_slice_whole_ram_cases=cases,status=status,error=error,
        last_instruction=hex(t.startup_pc),pc=hex(t.pc),last_mmio=t.last_startup_mmio,before=before,
        after=dict(recovery=r(t,0x868C),second=r(t,0x868D)),
        indirect_calls=t.startup_calls,intc_accesses=t.intc.accesses,
        configuration_trace=t.configuration_trace,
        limits='Final1570C..15716 slice is independent component evidence only. Full15574 not reached its flag-setting tail unless status RETURNED. Prior configuration/state remain explicit fixture, not reset.')
    if nmi_level is not None:
        result["icr_fixture"] = dict(external_constant_nmi_level=nmi_level,final_value=t.intc.values[0xFFFFED18])
    if irq_status is not None:
        result["irq_status_fixture"] = dict(external_constant_status=irq_status,no_external_irq_arrivals=True)
    if t.ubc is not None:
        result["ubc_fixture"]=dict(values={hex(a):v for a,v in t.ubc.values.items()},accesses=t.ubc.accesses,no_break_events=True)
    if t.bsc is not None:
        result["bsc_fixture"]=dict(explicit_wcr_initial=wcr_initial,values={hex(a):v for a,v in t.bsc.values.items()},accesses=t.bsc.accesses,no_external_bus_cycles=True)
    if t.connection is not None:
        result["connection_fixture"]=dict(values={hex(a):v for a,v in t.connection.values.items()},accesses=t.connection.accesses,no_compare_events=True)
    if t.downcount is not None:
        result["downcount_fixture"]=dict(values={hex(a):v for a,v in t.downcount.values.items()},accesses=t.downcount.accesses,no_counter_events=True)
    if t.interval is not None:
        result["interval_fixture"]=dict(values={hex(a):v for a,v in t.interval.values.items()},accesses=t.interval.accesses,no_counter_edges=True)
    if t.dmaor is not None:
        result["dmaor_fixture"]=dict(values={hex(a):v for a,v in t.dmaor.values.items()},accesses=t.dmaor.accesses,no_dma_transfers=True)
    (ROOT/filename).write_text(json.dumps(result,indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['scope','indirect_calls','intc_accesses','configuration_trace','limits']})


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nmi-level',type=int,choices=[0,1])
    parser.add_argument('--irq-status-zero',action='store_true')
    parser.add_argument('--ubc',action='store_true')
    parser.add_argument('--wcr-initial',type=lambda value:int(value,0))
    parser.add_argument('--dmaor',action='store_true')
    parser.add_argument('--interval',action='store_true')
    parser.add_argument('--downcount',action='store_true')
    parser.add_argument('--connection',action='store_true')
    parser.add_argument('--filename',default='tcu-hardware-startup-probe.json')
    args=parser.parse_args()
    main(args.nmi_level,args.filename,0 if args.irq_status_zero else None,args.ubc,args.wcr_initial,args.dmaor,args.interval,args.downcount,args.connection)
