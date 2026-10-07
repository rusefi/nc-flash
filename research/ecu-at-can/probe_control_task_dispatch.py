"""Selected index7 -> original dispatcher/RTE -> acquisition -> scheduler idle.

The selected index, stack and mask are explicit scheduler-input fixtures, not
clock/queue-admission proof. Original dispatch installs the descriptor. No
callee skipped. ADC result inputs are explicit; task body cannot normal-return.
"""
import hashlib,json
from pathlib import Path
from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import ECU,w,r
from verify_control_acquisition import REGISTERS
from probe_control_acquisition_retained import FIELDS


class IdleBoundary(Exception):pass


class Observed(TaskDispatch):
    def instruction(self,pc):
        if pc==0x3D0C:raise IdleBoundary
        return super().instruction(pc)


def main(queued=False, cycles=1, filename='control-task-dispatch-probe.json',
         machine_type=Observed, before_cycle=None, after_cycle=None):
    e=machine_type();e.registers[0xFFFFF74E]=1
    result=dict(scope=__doc__+('\nQueued variant: original38C4 initializes queues and391A selects index7/priority3; no selectedindex write.' if queued else ''),rom_sha256=hashlib.sha256(ECU).hexdigest(),queued=queued,cycles=[])
    try:
        for stage,entry in [('clear',0x10022),('filter',0xCA94),('initializer',0x1619A)]:
            e.stage=stage;e.run(entry,limit=2000000)
        e.stage='selected-task7'
        if queued:
            e.stage='queue-initialize';e.run(0x38C4,0xFFFF12B0)
        else:w(e,0x12B6,7,2)
        w(e,0x12BC,int.from_bytes(ECU[0x4078:0x407C],'big'),4)
        w(e,0x12C0,int.from_bytes(ECU[0x4054:0x4058],'big'),4)
        e.adc_samples[REGISTERS[1]]=512<<6;e.adc_samples[REGISTERS[28]]=500<<6
        for cycle in range(cycles):
            if before_cycle is not None:before_cycle(e,cycle)
            e.stage=f'queued-task7-{cycle}' if queued else 'selected-task7'
            e.adc_reads=[];e.adc_io=[]
            if queued:
                e.r[5]=7;e.r[6]=3;e.run(0x391A,0xFFFF12B0)
                assert r(e,0x12B6,2)==7
            try:e.run(0x3B8A,0xFFFF12B0,limit=1000000)
            except IdleBoundary:
                result['cycles'].append(dict(cycle=cycle,fields={hex(a):r(e,a,n) for a,n in FIELDS.items()},adc_reads=e.adc_reads.copy(),adc_io=e.adc_io.copy(),descriptor=[r(e,0x11E0+i) for i in range(8)]))
            else:raise AssertionError('unexpected ordinary task return')
            if after_cycle is not None:after_cycle(e,cycle)
        status='scheduler idle reached'
    except IdleBoundary:status='scheduler idle reached'
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:status=type(exc).__name__+': '+str(exc)
    result.update(status=status,stage=e.stage,pc=e.pc,tail=e.tail,rte=e.rte_transfers,registers=e.r,sr=e.sr,
        fields={hex(a):r(e,a,n) for a,n in FIELDS.items()},context={hex(a):r(e,a,n) for a,n in [(0x12B4,2),(0x12B6,2),(0x12B8,4),(0x12BC,4),(0x12C0,4),(0x12C4,4),(0x12C8,4)]},
        entries=e.acquisition_entries,adc_reads=e.adc_reads,adc_io=e.adc_io)
    Path(__file__).with_name(filename).write_text(json.dumps(result,indent=2)+'\n')
    print(status,hex(e.pc),'RTE count',len(e.rte_transfers),'fields',result['fields'],flush=True)
    return e,result


if __name__=='__main__':main()
