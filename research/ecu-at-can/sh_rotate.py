"""Isolated ROTL/ROTR extension for original TCU software arithmetic.

Renesas SH-2E software manual, sections7.2.46/47:
https://www.renesas.com/ja/document/mah/sh-2e-software-manual
Both rotate the outgoing bit back into Rn and copy it to T; old T is unused.
Existing interpreters and their instruction coverage remain unchanged.
"""
from sh_relative_branch import SHRelativeBranch


class SHRotate(SHRelativeBranch):
    def instruction(self, pc):
        opcode = self.read(pc, 2)
        kind = opcode & 0xF0FF
        if kind not in (0x4004, 0x4005):
            return super().instruction(pc)
        self._pending_slot = None  # These instructions have no PC-relative operand.
        self.visited.add(pc)
        register = (opcode >> 8) & 15
        value = self.r[register] & 0xFFFFFFFF
        if kind == 0x4004:
            outgoing = value >> 31
            result = ((value << 1) | outgoing) & 0xFFFFFFFF
        else:
            outgoing = value & 1
            result = (value >> 1) | (outgoing << 31)
        self.r[register] = result
        self.t(outgoing)
        return pc+2, False
