"""Model FPU with BRAF restricted to an explicit NOP delay slot.

Separate bounded extension; existing interpreters are unchanged. BRAF target
is PC+4+Rn modulo32, captured before its slot (Renesas SH-2E REJ09B0316-0200,
BRAF). Every non-NOP BRAF slot fails closed; no general delay-slot claim.
"""
from sh_model_float import SHModelFloat


class SHControlFloat(SHModelFloat):
    def instruction(self, pc):
        op = self.read(pc, 2)
        if op & 0xF0FF == 0x0023:
            if self.read(pc+2, 2) != 0x0009:
                raise ValueError('Control FPU BRAF requires NOP delay slot')
            self.visited.add(pc)
            return (pc+4+self.r[(op >> 8) & 15]) & 0xFFFFFFFF, True
        return super().instruction(pc)
