"""Validate new initialized observations and reused ADC interface integration.

Task probe is explicitly incomplete at the scheduler handoff. Original4CE2
has independent existing schedule-model checks on the new fixture class.
"""
import copy
import itertools
import json
from pathlib import Path
from probe_control_acquisition_task import AcquisitionTask
from verify_control_acquisition import REGISTERS
from verify_control_acquisition_schedule import CONTROL, schedule_model, equal
from verify_control_contributions import w

ROOT=Path(__file__).resolve().parent


def validate_retained(d):
    assert d['status']=='returned' and len(d['tasks'])==40 and len(d['checked'])==41
    periodic=[v for v in d['acquisition_entries'] if v['stage'].startswith('event2-')]
    assert sum(v['entry']==0x39894 for v in periodic)==40
    assert [(v['stage'],v['entry']) for v in periodic if v['entry']!=0x39894]==[
        ('event2-5',0x74DF8),('event2-5',0x6CD96),('event2-25',0x74DF8),('event2-25',0x6CD96)]


def main():
    validate_retained(json.loads((ROOT/'control-acquisition-retained-probe.json').read_text()))
    d=json.loads((ROOT/'control-acquisition-task-probe.json').read_text())
    assert d['status']=='ValueError: Non-RAM write 00000003' and d['pc']==0x3CD4
    assert not d['tasks'] and d['stage']=='acquisition-0'
    assert [v['entry'] for v in d['entries'] if v['stage']=='acquisition-0']==[0xE26C,0x4CE2,0x6718,0x1DF32]
    assert d['registers'][13]==0 and not d['adc_reads']
    accesses=0
    for address,value in itertools.product(REGISTERS,[0,1,0x8000,0xFFFF]):
        e=AcquisitionTask();e.adc_samples[address]=value
        assert e.read(address,2)==value and e.adc_reads==[address];accesses+=1
    for address,value in itertools.product([a+i for a in CONTROL for i in [0,1]], [0,1,0xA5,0xFF,0x1234]):
        e=AcquisitionTask();e.write(address,value,1)
        assert e.read(address,1)==value&255;accesses+=1
    rejects=0
    for address,size,write in [(REGISTERS[0],1,False),(REGISTERS[0],4,False),
                               (REGISTERS[0],2,True),(0xFFFFF81A,2,False),
                               (CONTROL[0],2,False),(CONTROL[0],2,True)]:
        e=AcquisitionTask()
        try:e.write(address,1,size) if write else e.read(address,size)
        except ValueError:rejects+=1
        else:raise AssertionError((address,size,write))
    schedules=0
    for phase,oldmode in itertools.product([0,3,15,63,255],range(3)):
        e=AcquisitionTask();e.sr=0xF0
        for a,v in [(0x4048,phase),(0x404C,oldmode),(0x404A,3),
                    (0x404F,12),(0x4052,12),(0x4055,8)]:w(e,a,v)
        e.adc_samples={a:((i*1023+17)&0xFFFF) for i,a in enumerate(REGISTERS)}
        ref=copy.deepcopy(e);schedule_model(ref)
        sp=e.r[15];e.run(0x4CE2)
        equal(e,ref);assert e.r[15]==sp and e.sr&0xF0==0xF0;schedules+=1
    result=dict(status='PASS',scope=__doc__,event2_returns=40,activity_boundaries=41,
                acquisition_task_returns=0,expected_scheduler_limit='3CD4 null current descriptor',
                interface_cases=accesses,expected_rejections=rejects,original_schedule_cases=schedules)
    (ROOT/'control-acquisition-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
