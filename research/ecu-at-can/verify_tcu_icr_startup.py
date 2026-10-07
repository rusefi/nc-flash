"""Documented ICR controls/read-only NMIL and original14422/1442A configuration.

Finite constant NMI input; no pin transitions/interrupt acceptance. Legal
byte/long accesses remain outside this word-only fixture. Reserved writes
rejected without inventing hardware behavior. Optional zero IRQ-status input
is bounded to no pending flags/pin assertions. Existing INTC owner is reused.
"""
import hashlib
import json
from pathlib import Path

from verify_tcu_interrupt_setup import InterruptRegisters,Machine
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice
from verify_can201_byte6 import TCU,w

ROOT=Path(__file__).resolve().parent
ICR=0xFFFFED18


def main():
    controls=originals=rejects=0
    for level in [0,1]:
        for value in range(512):
            for written_pin in [0,0x8000]:
                owner=InterruptRegisters(value,nmi_level=level)
                before=owner.values.copy()
                owner.write(ICR,value|written_pin,2)
                assert owner.read(ICR,2)==(level<<15)|value
                assert {a:v for a,v in owner.values.items() if a!=ICR}=={a:v for a,v in before.items() if a!=ICR}
                assert owner.accesses==[['write',ICR,2,value|written_pin],['read',ICR,2,(level<<15)|value]]
                controls+=1
            t=Machine(seed=value);t.intc=InterruptRegisters(value,nmi_level=level)
            t.intc.values[ICR]|=value
            for a in [0x868B,0x868C,0x868D,0x868E]:w(t,a,(value+a)&255)
            before=ram(t);saved=t.r.copy();sr=t.sr
            t.pr=0xFFFFFFF0
            expected=saved.copy();expected[0]=ICR;expected[3]=255
            execute_slice(t,0x14422,0xFFFFFFF0)
            assert ram(t)==before and t.r==expected and t.sr==sr and t.pr==0xFFFFFFF0
            assert t.intc.values[ICR]==(level<<15)|255
            assert t.intc.accesses==[['write',ICR,2,255]]
            originals+=1
    for address,size,value in [(ICR,2,1<<bit) for bit in range(9,15)]+[(ICR,1,0),(ICR,4,0),(ICR+1,2,0),(ICR+2,2,0)]:
        owner=InterruptRegisters(0,nmi_level=1);before=owner.values.copy()
        try:owner.write(address,value,size)
        except ValueError:rejects+=1
        else:raise AssertionError('Unsupported write accepted')
        assert owner.values==before and owner.accesses==[]
    for address,size in [(ICR,1),(ICR,4),(ICR+1,2),(ICR+2,2)]:
        owner=InterruptRegisters(0,nmi_level=1)
        try:owner.read(address,size)
        except ValueError:rejects+=1
        else:raise AssertionError('Unsupported read accepted')
        assert owner.accesses==[]
    status_cases=0
    for seed in range(64):
        t=Machine(seed=seed);t.intc=InterruptRegisters(seed,nmi_level=seed&1,irq_status=0)
        w(t,0x868C,seed);w(t,0x868D,255-seed)
        before=ram(t);saved=t.r.copy();sr=t.sr;t.pr=0xFFFFFFF0
        expected=saved.copy();expected[1]=ICR+2;expected[2]=0
        execute_slice(t,0x1442A,0xFFFFFFF0)
        assert ram(t)==before and t.r==expected and t.sr==sr and t.pr==0xFFFFFFF0
        assert t.intc.values[ICR+2]==0
        assert t.intc.accesses==[['write',ICR+2,2,0]]
        assert t.intc.read(ICR+2,2)==0
        status_cases+=1
    status_rejections=0
    for value,size in [(1,2),(255,2),(65535,2),(0,1),(0,4)]:
        owner=InterruptRegisters(0,irq_status=0);before=owner.values.copy()
        try:owner.write(ICR+2,value,size)
        except ValueError:status_rejections+=1
        else:raise AssertionError('Unsupported status access accepted')
        assert owner.values==before and owner.accesses==[]
    try:InterruptRegisters(0,irq_status=1)
    except ValueError:status_rejections+=1
    else:raise AssertionError('Unsupported nonzero IRQ fixture accepted')
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),
        icr_control_cases=controls,original14422_whole_ram_register_cases=originals,
        rejected_accesses=rejects,original1442a_zero_status_cases=status_cases,
        rejected_irq_status_cases=status_rejections,source='SH7055S REJ09B0045-0200H PDFzero136/149/150',
        limits='ICR word accesses with constant external NMIL; optional IRQ-status0 only, no pending flags/pin assertions or read-one clearing semantics. No IRQ/NMI events/full15574 completion.')
    (ROOT/'tcu-icr-startup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
