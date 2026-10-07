"""Original E26C acquisition task after executed RAM/input/application setup.

Reuse existing strict ADC methods only on their handled address range. Explicit
result samples/control latches; no analog conversion, status completion,
interrupt dispatch or physical frequency. No original callee is stubbed.
"""
import hashlib
import json
from pathlib import Path
from probe_control_acquisition_retained import AcquisitionTrace, FIELDS
from verify_control_acquisition import Acquisition, REGISTERS
from verify_control_acquisition_schedule import ScheduledAcquisition, CONTROL
from verify_control_contributions import ECU, r


class AcquisitionTask(AcquisitionTrace):
    def __init__(self):
        super().__init__()
        self.adc_samples={a:0 for a in REGISTERS}
        self.adc_control={a+offset:0 for a in CONTROL for offset in [0,1]}
        self.adc_reads=[];self.adc_io=[]
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if address in self.adc_control:
            return ScheduledAcquisition.read(self,address,size)
        if 0xFFFFF800<=address<=0xFFFFF85F:
            return Acquisition.read(self,address,size)
        return super().read(address,size)
    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if address in self.adc_control:
            return ScheduledAcquisition.write(self,address,value,size)
        if 0xFFFFF800<=address<=0xFFFFF85F:
            return Acquisition.write(self,address,value,size)
        return super().write(address,value,size)


def main():
    e=AcquisitionTask();e.registers[0xFFFFF74E]=1
    row=dict(scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),tasks=[])
    try:
        for stage,entry in [('clear',0x10022),('filter',0xCA94),('initializer',0x1619A)]:
            e.stage=stage;e.run(entry,limit=2000000)
        # Explicit aligned result samples, not seeded application input values.
        e.adc_samples[REGISTERS[1]]=512<<6
        e.adc_samples[REGISTERS[28]]=500<<6
        for i in range(20):
            e.stage=f'acquisition-{i}';sp=e.r[15];e.adc_reads=[];e.adc_io=[]
            e.run(0xE26C,limit=1000000)
            assert e.r[15]==sp
            row['tasks'].append(dict(call=i,fields={hex(a):r(e,a,n) for a,n in FIELDS.items()},
                                     adc_reads=e.adc_reads.copy(),adc_io=e.adc_io.copy()))
        row['status']='returned'
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
        row.update(status=type(exc).__name__+': '+str(exc),stage=e.stage,pc=e.pc,tail=e.tail,
                   adc_reads=e.adc_reads,adc_io=e.adc_io)
    row.update(entries=e.acquisition_entries,accesses=e.accesses,registers=e.r)
    Path(__file__).with_name('control-acquisition-task-probe.json').write_text(json.dumps(row,indent=2)+'\n')
    print(row['status'],'stage',e.stage,'pc',hex(e.pc),'tasks',len(row['tasks']),flush=True)


if __name__=='__main__':main()
