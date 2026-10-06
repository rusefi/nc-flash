"""MOVA and BRAF for original TCU jump-table execution.

Renesas SH-2E software manual REJ09B0316-0200, sections7.2.8 and7.2.34.
MOVA in a delay slot uses branch destination+2. Other PC-relative loads in
slots fail closed here; the existing shared interpreters remain unchanged.
"""
from sh_software_arithmetic import SHSoftwareArithmetic


class SHRelativeBranch(SHSoftwareArithmetic):
    def instruction(self, pc):
        pending = getattr(self, '_pending_slot', None)
        self._pending_slot = None
        slot_target = pending[1] if pending is not None and pending[0] == pc else None
        opcode = self.read(pc, 2)
        if slot_target is not None and opcode >> 12 in (9, 13):
            raise ValueError('PC-relative memory load in delay slot is outside this model')
        if opcode >> 8 == 0xC7:  # MOVA @(disp,PC),R0; T unchanged
            base = pc+4 if slot_target is None else slot_target+2
            self.r[0] = ((base & ~3) + (opcode & 255)*4) & 0xFFFFFFFF
            self.visited.add(pc)
            result = pc+2, False
        elif opcode & 0xF0FF == 0x0023:  # BRAF Rm; capture before delay slot
            target = (pc+4+self.r[(opcode >> 8) & 15]) & 0xFFFFFFFF
            self.visited.add(pc)
            result = target, True
        else:
            result = super().instruction(pc)
        if result[1]:
            self._pending_slot = pc+2, result[0]
        return result
