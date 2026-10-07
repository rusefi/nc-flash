"""Locate real acquisition/publication calls in initialized outer event2.

Observation only; no added ADC fixture or internal input writes. Retains full
original callees and existing activity oracles. No physical cadence claim.
"""
import json
from pathlib import Path
from verify_control_qualification_freshness import Observed as Qualification
from verify_control_clear_startup import run_sequence
from verify_control_contributions import r

TARGETS=[0x4CE2,0x6710,0x6718,0x3976C,0x39894,0x1DF14,0x1DF32,
         0x74DF8,0x6CD96,0xE26C,0xE514,0x7024,0x6678]
FIELDS={0x400A:2,0x4040:2,0x40EC:2,0x40E8:4,0x6C92:2,0x6CB4:4,
        0x914B:1,0x4048:1,0x404C:1,0x404F:1,0x4052:1,0x4055:1}


class AcquisitionTrace(Qualification):
    def __init__(self):
        super().__init__();self.acquisition_entries=[];self.acquisition_writes=[]
    def instruction(self,pc):
        if pc in TARGETS:
            self.acquisition_entries.append(dict(stage=self.stage,entry=pc,pr=self.pr,
                fields={hex(a):r(self,a,n) for a,n in FIELDS.items()}))
        return super().instruction(pc)
    def write(self,address,value,size):
        result=super().write(address,value,size)
        if self.stage.startswith('event2-') and any(address<0xFFFF0000+a+n and 0xFFFF0000+a<address+size for a,n in FIELDS.items()):
            self.acquisition_writes.append(dict(stage=self.stage,pc=self.instruction_pc,address=address,value=value,size=size))
        return result


def main():
    filename='control-acquisition-retained-probe.json'
    e,row=run_sequence(entry=0x10022,filename=filename,scope=__doc__,
                       samples=[1]*10+[0]*15+[1]*15,machine_type=AcquisitionTrace)
    row.update(acquisition_entries=e.acquisition_entries,acquisition_writes=e.acquisition_writes,
               qualification=e.qualification_checked)
    Path(__file__).with_name(filename).write_text(json.dumps(row,indent=2)+'\n')
    for stage in ['initializer']+[f'event2-{i}' for i in range(40)]:
        entries=[hex(v['entry']) for v in e.acquisition_entries if v['stage']==stage]
        if entries:print(stage,entries,flush=True)


if __name__=='__main__':main()
