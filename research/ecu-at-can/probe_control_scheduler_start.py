"""Original3DD8 initializes task queues and runs firsttask17 toward background0.

Mode0 and synthetic caller stack supplied; scheduler selects native ROM stack.
No direct task/init calls or forced internal readiness. Strict existing peripherals.
"""
import hashlib,json
from pathlib import Path
from sh_control_interrupt import ControlInterrupt,execute_to
from verify_control_contributions import ECU,r


class SchedulerStart(ControlInterrupt):
    def __init__(self):
        super().__init__();self.startup_calls=[];self.startup_stages=[]
    def instruction(self,pc):
        if pc in [0x3DD8,0x3F90,0x3D10,0xDCF8,0xE030,0x10022,0xCA94,0x1619A,0x105FC,0x1061A,0xA942]:
            self.startup_stages.append(dict(pc=pc,pr=self.pr,sp=self.r[15],status=self.sr,argument=self.r[4]))
        opcode=self.read(pc,2)
        if opcode&0xF0FF==0x400B:
            self.startup_calls.append(dict(pc=pc,target=self.r[(opcode>>8)&15],sp=self.r[15],argument=self.r[4]))
        return super().instruction(pc)


def main(filename='control-scheduler-start-probe.json',machine_type=SchedulerStart):
    e=machine_type();e.r[15]=0xFFFED000;e.sr=0xB0;e.r[4]=0;e.stage='scheduler-start'
    e.registers[0xFFFFF74E]=1
    try:
        execute_to(e,0x3DD8,{0xE030},5000000);status='background task0 reached'
    except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
        status=type(exc).__name__+': '+str(exc)
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),status=status,
        pc=e.pc,tail=e.tail,registers=e.r,sr=e.sr,stages=e.startup_stages,calls=e.startup_calls,
        rte=e.rte_transfers,context={hex(a):r(e,a,n) for a,n in [(0x12B4,2),(0x12B6,2),(0x12B8,4),(0x12BC,4),(0x12C0,4),(0x12C4,4),(0x12C8,4)]})
    Path(__file__).with_name(filename).write_text(json.dumps(result,indent=2)+'\n')
    print(status,hex(e.pc),'calls',len(e.startup_calls),flush=True)
    return e,result


if __name__=='__main__':main()
