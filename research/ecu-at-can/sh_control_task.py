"""ECU full-task research harness: existing FPU/peripheral model plus integer ISA.

Dispatch selected opcodes to existing tested integer/rotate implementations.
Add STS MACH, LDS MACH/MACL, DMULS.L and bit-preserving FSTS. Renesas REJ09B0316-0200 sections7.2.19,
7.2.27,7.2.59,7.3.13; see control-task-isa-source.txt. No hardware timing or FPU
exception extension. Unsupported operations/accesses still fail closed.
"""
from verify_control_reply import ControlApplication
from sh_integer_arithmetic import SHIntegerArithmetic
from sh_software_arithmetic import SHSoftwareArithmetic
from sh_rotate import SHRotate
from sh_subset import MASK, signed


class ControlTaskArithmetic(ControlApplication):
    # PBDR/PFDR/PHDR/PJDR, BFR6A..D and frozen TCNT0 software latches.
    # No pin changes, input clock, counter increments or overflow interrupt.
    # SH7058 tables22.3/22.11/22.15/22.17, sections11.2.15/11.2.23.
    WIDTHS = {**ControlApplication.WIDTHS, 0xFFFFF738: 2, 0xFFFFF74E: 2,
              0xFFFFF72C: 2, 0xFFFFF76C: 2, 0xFFFFF430: 4, 0xFFFFF002: 1,
              **{0xFFFF0000 + a: 2 for a in [0xF510, 0xF512, 0xF514, 0xF516]}}

    def instruction(self, pc):
        opcode = self.read(pc, 2)
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        unary, binary = opcode & 0xF0FF, opcode & 0xF00F
        if unary == 0x000A:  # STS MACH,Rn
            self.r[n] = self.mach
        elif unary == 0x400A:  # LDS Rn,MACH
            self.mach = self.r[n] & MASK
        elif unary == 0x401A:  # LDS Rn,MACL
            self.macl = self.r[n] & MASK
        elif unary == 0xF00D:  # FSTS FPUL,FRn: raw bits, no arithmetic
            self.fr[n] = self.fpul
        elif binary == 0x300B:  # SUBV: signed overflow -> T
            a, b = self.r[n], self.r[m]
            value = (a - b) & MASK
            overflow = bool((a ^ b) & (a ^ value) & 0x80000000)
            self.r[n] = value
            self.sr = (self.sr & ~1) | int(overflow)
        elif binary == 0x300D:  # DMULS.L Rm,Rn
            product = signed(self.r[n]) * signed(self.r[m])
            self.mach, self.macl = (product >> 32) & MASK, product & MASK
        elif unary in [0x4004, 0x4005]:
            return SHRotate.instruction(self, pc)
        elif opcode == 0x0008 or binary == 0x6009 or unary == 0x4025:
            return SHSoftwareArithmetic.instruction(self, pc)
        elif (opcode == 0x0019 or binary in [0x2007, 0x3004, 0x300E, 0x300A]
              or unary in [0x4024, 0x4028, 0x4029]):
            return SHIntegerArithmetic.instruction(self, pc)
        else:
            return super().instruction(pc)
        self.visited.add(pc)
        return pc + 2, False
