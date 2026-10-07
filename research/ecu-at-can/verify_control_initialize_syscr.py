"""SYSCR2 fixtures and original clock-write/status-classification helpers."""
import hashlib
import itertools
import json
from pathlib import Path
from sh_control_initialize_syscr import SystemStartup
from sh_control_initialize_dma import DMAOR,CONTROL
from verify_control_contributions import ECU
from verify_control_raw_inputs import application


def main():
    values=list(range(16))+list(range(128,144))
    writes=helpers=classifiers=rejected=0
    for old,new in itertools.product(values,repeat=2):
        e=SystemStartup();e.syscr2=old
        want=new if not old&2 else new|2
        memory=e.ram.copy();registers=e.registers.copy()
        e.write(0xFFFFF70A,0x3C00+new,2)
        assert e.read(0xFFFFF70B,1)==want and e.ram==memory and e.registers==registers
        writes+=1
        e=SystemStartup();e.syscr2=old;saved=e.r[8:16].copy();gbr=e.gbr;sr=e.sr
        before=application(e);e.run(0xE7B6,new)
        assert e.syscr2==want and application(e)==before and e.r[8:16]==saved and e.gbr==gbr and e.sr==sr
        assert e.accesses==[('write',0xFFFFF70A,0x3C00+new,2)]
        assert {0xE7C6,0xE7C8,0xE7CA,0xE7CC} <= e.visited
        helpers+=1
    for old,sample in itertools.product(values,[0x0B00,0x0B01]):
        e=SystemStartup();e.syscr2=old;e.sdsr_sample=sample
        before=application(e);saved=e.r[8:16].copy();gbr=e.gbr;sr=e.sr
        assert e.run(0xF52C)==0
        assert e.syscr2==old and application(e)==before and e.r[8:16]==saved and e.gbr==gbr and e.sr==sr|1
        assert e.accesses==[('read',0xFFFFF70B,old,1),('write',0xFFFFF70A,0x3C00+(old&251),2),
                            ('read',0xFFFFF7C2,sample,2),('write',0xFFFFF70A,0x3C00+old,2)]
        classifiers+=1
    for write,address,size,value in [(False,0xFFFFF70A,1,0),(False,0xFFFFF70B,2,0),
        (False,0xFFFFF70A,4,0),(True,0xFFFFF70B,1,0),(True,0xFFFFF70A,1,0),
        (True,0xFFFFF70A,4,0),(True,0xFFFFF70A,2,0x3D01),(True,0xFFFFF70A,2,0x3C71),
        (False,0xFFFFF7C2,1,0),(False,0xFFFFF7C2,4,0),(True,0xFFFFF7C2,2,0)]:
        e=SystemStartup()
        try:e.write(address,value,size) if write else e.read(address,size)
        except (ValueError,NotImplementedError):rejected+=1
        else:raise AssertionError('Unsupported access accepted')
        assert e.syscr2==1 and not e.accesses
    e=SystemStartup();e.syscr2=5
    try:e.read(0xFFFFF7C2,2)
    except NotImplementedError:rejected+=1
    else:raise AssertionError('Halted H-UDI read accepted')
    e=SystemStartup();e.write(0xFFFFF70A,0x3C03,2);e.write(0xFFFFF70A,0x3C01,2)
    assert e.syscr2==3
    e.rom=bytes.fromhex('f09d')
    try:e.instruction(0)
    except NotImplementedError:rejected+=1
    else:raise AssertionError('Stopped FPU executed')
    assert e.fr[0]==0 and not e.visited
    e=SystemStartup();e.dma[DMAOR]=1;e.dma[CONTROL]=0x1F0129
    try:e.write(0xFFFFF70A,0x3C81,2)
    except NotImplementedError:rejected+=1
    else:raise AssertionError('Clock change admitted during enabled DMA')
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,register_write_cases=writes,
                original_write_helper_cases=helpers,original_status_classifier_cases=classifiers,
                expected_rejections=rejected,limitations='No hardware clock, reset, TAP, AUD or UBC simulation.')
    Path(__file__).with_name('control-initialize-syscr-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
