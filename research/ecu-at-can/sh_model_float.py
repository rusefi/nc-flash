"""Bounded RTZ FPU plus MACH saves/restores, MULS.W and finite FNEG for ECU model maps.

Separate from existing interpreters. Original lookup helpers execute normally;
no map or firmware-function substitution. Renesas SH-2E REJ09B0316-0200
LDS/STS and MULS.W define these register transfers and signed16 product.
"""
from sh_rtz_float import SHNormalRTZFloat
from sh_subset import MASK, signed
from sh_exact_float import exact_value


class SHModelFloat(SHNormalRTZFloat):
    def __init__(self, rom):
        super().__init__(rom)
        self.mach = 0

    def instruction(self, pc):
        opcode = self.read(pc, 2)
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        if opcode & 0xF0FF == 0x4002:  # STS.L MACH,@-Rn
            self.r[n] = (self.r[n]-4) & MASK
            self.write(self.r[n], self.mach, 4)
        elif opcode & 0xF0FF == 0x4006:  # LDS.L @Rn+,MACH
            self.mach = self.read(self.r[n], 4)
            self.r[n] = (self.r[n]+4) & MASK
        elif opcode & 0xF00F == 0x200F:  # MULS.W Rm,Rn
            self.macl = (signed(self.r[n], 16)*signed(self.r[m], 16)) & MASK
        elif opcode & 0xF0FF == 0xF04D:  # FNEG FRn; finite normal/zero scope
            exact_value(self.fr[n])
            self.fr[n] ^= 0x80000000
        else:
            return super().instruction(pc)
        self.visited.add(pc)
        return pc+2, False
