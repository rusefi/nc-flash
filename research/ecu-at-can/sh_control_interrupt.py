"""Local ECU interrupt fixture: FPSCR/FPUL stack transfers, original ROM intact.

Renesas SH-2E REJ09B0316-0200 sections7.3.16/17 and figure4.2.
Only aligned mapped-RAM longword transfers; no hardware interrupt acceptance.
Existing floating moves and bounded NOP-delay RTE are reused unchanged.
"""
from probe_control_timer_queue2 import Queue2Timer


class ControlInterrupt(Queue2Timer):
    def instruction(self,pc):
        opcode=self.read(pc,2);kind=opcode&0xF0FF
        if kind==0x402A:  # LDS Rn,PR, including an ordinary branch delay slot.
            self.pr=self.r[(opcode>>8)&15]&0xFFFFFFFF
            self.visited.add(pc);return pc+2,False
        if kind not in [0x4052,0x4056,0x4062,0x4066]:
            return super().instruction(pc)
        n=(opcode>>8)&15;store=kind in [0x4052,0x4062]
        address=(self.r[n]-(4 if store else 0))&0xFFFFFFFF
        if address&3 or not 0xFFFE0000<=address<=0xFFFFDFFC:
            raise ValueError('FPU stack transfer requires aligned mapped RAM')
        field='fpul' if kind in [0x4052,0x4056] else 'fpscr'
        if store:
            self.write(address,getattr(self,field),4);self.r[n]=address
        else:
            value=self.read(address,4)
            if field=='fpscr':value=(value&0x18C60)|0x40001
            setattr(self,field,value);self.r[n]=(address+4)&0xFFFFFFFF
        self.visited.add(pc)
        return pc+2,False


def execute_to(e,start,stops,limit=20000):
    """Run original instructions to an observed boundary without altering inputs."""
    e.pc=start
    for _ in range(limit):
        if e.pc in stops:return e.pc
        nxt,delay=e.instruction(e.pc)
        if delay:
            _,nested=e.instruction(e.pc+2)
            if nested:raise ValueError('branch in delay slot')
        e.pc=nxt
    raise RuntimeError('interrupt prefix instruction limit at '+hex(e.pc))
