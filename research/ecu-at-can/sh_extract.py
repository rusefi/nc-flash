"""Isolated XTRCT extension for original TCU software arithmetic.

Renesas SH-2E Software Manual REJ09B0316-0200, section7.2.68, page167:
https://www.renesas.com/en/document/mah/sh-2e-software-manual
Extract the middle word pair from Rm:Rn; preserve SR, including T.
"""
from sh_rotate import SHRotate


class SHExtract(SHRotate):
    def instruction(self, pc):
        opcode = self.read(pc, 2)
        if opcode & 0xF00F != 0x200D:
            return super().instruction(pc)
        self._pending_slot = None
        self.visited.add(pc)
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        self.r[n] = ((self.r[m] & 65535) << 16) | ((self.r[n] >> 16) & 65535)
        return pc + 2, False
