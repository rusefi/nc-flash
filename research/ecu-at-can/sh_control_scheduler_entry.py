"""Local STC.L SR stack transfer needed by original scheduler mode entry.

SH-2E software manual7.2.58: decrement Rn by4 then storeSR, T unchanged.
Only aligned mappedRAM; no exception/trap or interrupt acceptance model.
"""
from sh_control_interrupt import ControlInterrupt


class SchedulerEntry(ControlInterrupt):
    def instruction(self,pc):
        opcode=self.read(pc,2)
        if opcode&0xF0FF!=0x4003:return super().instruction(pc)
        n=(opcode>>8)&15;address=(self.r[n]-4)&0xFFFFFFFF
        if address&3 or not 0xFFFE0000<=address<=0xFFFFDFFC:
            raise ValueError('STC.L SR requires aligned mapped RAM')
        self.write(address,self.sr,4);self.r[n]=address
        self.visited.add(pc);return pc+2,False
