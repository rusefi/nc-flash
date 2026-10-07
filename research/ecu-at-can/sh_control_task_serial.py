"""Task probe with existing XTRCT, ADDV/DT and explicit SCI0 samples.

SCI0 status is a caller-provided constant sample; SSR writes are logged only.
Each RDR read consumes one explicit byte. No implicit serial peer or clock.
PGDR is a low-nibble word latch (reserved high bits read zero).
"""
from collections import deque
from probe_control_task import Probe
from sh_extract import SHExtract


class TaskSerial(Probe):
    WIDTHS = {**Probe.WIDTHS, **{0xFFFFF000+i: 1 for i in range(7)}, 0xFFFFF764: 2}

    def __init__(self):
        super().__init__()
        self.sci0_status = None
        self.sci0_rx = deque()
        self.sci0_tx = []
        self.terminal_entries = []
        self.timer_samples = None  # None retains prior frozen counter fixture

    def read(self, a, size):
        a &= 0xFFFFFFFF
        if a == 0xFFFFF430 and size == 4 and self.timer_samples is not None:
            if not self.timer_samples:
                raise ValueError('Missing explicit TCNT0 sample')
            value = self.timer_samples.popleft()
            if not isinstance(value, int) or not 0 <= value <= 0xFFFFFFFF:
                raise ValueError('TCNT0 sample must be a longword')
            self.accesses.append(('read', a, value, size))
            return value
        if size == 1 and a in [0xFFFFF004, 0xFFFFF005]:
            if a == 0xFFFFF004:
                if self.sci0_status is None:
                    raise ValueError('Missing explicit SCI0 SSR sample')
                value = self.sci0_status
            else:
                if not self.sci0_rx:
                    raise ValueError('Missing explicit SCI0 RDR sample')
                value = self.sci0_rx.popleft()
            if not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError('SCI0 sample must be a byte')
            self.accesses.append(('read', a, value, size))
            return value
        return super().read(a, size)

    def write(self, a, value, size):
        a &= 0xFFFFFFFF
        if a == 0xFFFFF005:
            raise ValueError('SCI0 RDR is read-only')
        if a == 0xFFFFF004 and size == 1:
            self.accesses.append(('write', a, value & 255, size))
            return
        if a == 0xFFFFF764:
            value &= 15
        super().write(a, value, size)
        if a == 0xFFFFF003:
            self.sci0_tx.append(value & 255)

    def instruction(self, pc):
        if pc == 0xF8D6:
            self.terminal_entries.append(dict(pc=pc, pr=self.pr, registers=self.r.copy()))
        opcode = self.read(pc, 2)
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        if opcode & 0xF0FF == 0x4010:  # DT Rn: decrement, T iff result zero
            self.r[n] = (self.r[n] - 1) & 0xFFFFFFFF
            self.sr = (self.sr & ~1) | int(self.r[n] == 0)
            self.visited.add(pc)
            return pc + 2, False
        if opcode & 0xF00F == 0x300F:  # ADDV: signed overflow -> T
            a, b = self.r[n], self.r[m]
            value = (a + b) & 0xFFFFFFFF
            self.r[n] = value
            self.sr = (self.sr & ~1) | int(bool(~(a ^ b) & (a ^ value) & 0x80000000))
            self.visited.add(pc)
            return pc + 2, False
        if opcode & 0xF00F == 0x200D:
            return SHExtract.instruction(self, pc)
        return super().instruction(pc)
