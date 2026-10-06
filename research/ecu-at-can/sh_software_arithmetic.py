"""Additional integer ISA used by TCU software floating-point routines.

The ROM arithmetic helpers still execute instruction by instruction. This
class does not substitute Python floats or implement a hardware FPU.
"""
from sh_integer_arithmetic import SHIntegerArithmetic


class SHSoftwareArithmetic(SHIntegerArithmetic):
    def instruction(self, pc):
        opcode = self.read(pc, 2)
        operation, n = opcode & 0xF0FF, (opcode >> 8) & 15
        if opcode == 0x0008:  # CLRT
            self.t(False)
            self.visited.add(pc)
            return pc + 2, False
        if opcode & 0xF00F == 0x6009:  # SWAP.W Rm,Rn; T unchanged
            value = self.r[(opcode >> 4) & 15]
            self.r[n] = ((value & 65535) << 16) | (value >> 16)
            self.visited.add(pc)
            return pc + 2, False
        if operation not in (0x4025, 0x4005):
            return super().instruction(pc)
        value = self.r[n]
        incoming = self.sr & 1 if operation == 0x4025 else value & 1
        self.t(value & 1)
        self.r[n] = (value >> 1) | (incoming << 31)
        self.visited.add(pc)
        return pc + 2, False
