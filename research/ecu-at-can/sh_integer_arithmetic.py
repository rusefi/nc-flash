"""SH integer multiply/carry/divide extensions for original TCU calculations.

Separate from the existing strict base. No firmware-helper substitution.
DIV1 implements one CPU step, not high-level division; M/Q/T are SR9/8/0.
Reference: Renesas SH-2E Software Manual REJ09B0316-0200, arithmetic ISA.
"""
from sh_subset import SH, MASK, signed


class SHIntegerArithmetic(SH):
    def instruction(self, pc):
        opcode = self.read(pc, 2)
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        r = self.r
        if opcode == 0x0019:  # DIV0U
            self.sr &= ~0x301
        elif opcode & 0xF00F == 0x2007:  # DIV0S
            q, divisor_sign = r[n] >> 31, r[m] >> 31
            self.sr = (self.sr & ~0x301) | (q << 8) | (divisor_sign << 9) | (q ^ divisor_sign)
        elif opcode & 0xF00F == 0x3004:  # DIV1
            old_q, divisor_sign = (self.sr >> 8) & 1, (self.sr >> 9) & 1
            top = r[n] >> 31
            r[n] = ((r[n] << 1) | (self.sr & 1)) & MASK
            shifted = r[n]
            if old_q == divisor_sign:
                result = shifted - r[m]
                carry = result < 0
            else:
                result = shifted + r[m]
                carry = result > MASK
            r[n] = result & MASK
            q = top ^ carry ^ divisor_sign
            self.sr = (self.sr & ~0x101) | (q << 8) | (q == divisor_sign)
        elif opcode & 0xF0FF == 0x4024:  # ROTCL
            incoming = self.sr & 1
            self.t(r[n] >> 31)
            r[n] = ((r[n] << 1) | incoming) & MASK
        elif opcode & 0xF0FF in (0x4028, 0x4029):  # SHLL16/SHLR16; T unchanged
            r[n] = (r[n] << 16) & MASK if opcode & 1 == 0 else r[n] >> 16
        elif opcode & 0xF00F in (0x300E, 0x300A):  # ADDC/SUBC
            addition = opcode & 15 == 14
            result = r[n] + r[m] + (self.sr & 1) if addition else r[n] - r[m] - (self.sr & 1)
            r[n] = result & MASK
            self.t(result > MASK if addition else result < 0)
        elif opcode & 0xF00F == 0x200F:  # MULS.W
            self.macl = (signed(r[n], 16) * signed(r[m], 16)) & MASK
        elif opcode & 0xF00F == 0x0007:  # MUL.L (low32 identical signed/unsigned)
            self.macl = (r[n] * r[m]) & MASK
        else:
            return super().instruction(pc)
        self.visited.add(pc)
        return pc + 2, False
