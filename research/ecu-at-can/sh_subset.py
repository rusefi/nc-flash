"""Small, strict SH integer interpreter for isolated ROM pack/unpack routines.

This is not an ECU simulator. No peripherals, interrupts, time, or FPU are
implemented. Unsupported instructions and non-RAM accesses fail closed.
The synthetic stack is independent of each firmware's real RAM allocation.
"""

MASK = 0xFFFFFFFF


def signed(value, bits=32):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


class SH:
    def __init__(self, rom):
        self.rom = rom
        self.ram = {}
        self.r = [0] * 16
        self.r[15] = 0xFFFED000  # synthetic stack, not emulated hardware
        self.sr = 0
        self.gbr = 0xFFFF8000
        self.macl = 0
        self.pr = 0xFFFFFFF0
        self.pc = 0
        self.visited = set()

    def read(self, addr, size):
        addr &= MASK
        if addr + size <= len(self.rom):
            return int.from_bytes(self.rom[addr:addr + size], "big")
        if not 0xFFFE0000 <= addr < 0xFFFFE000:
            raise ValueError(f"Unmapped read {addr:08X}")
        return int.from_bytes(bytes(self.ram.get(addr + i, 0) for i in range(size)), "big")

    def write(self, addr, value, size):
        addr &= MASK
        if not 0xFFFE0000 <= addr < 0xFFFFE000:
            raise ValueError(f"Non-RAM write {addr:08X}")
        value &= (1 << (size * 8)) - 1
        self.ram.update({addr + i: b for i, b in enumerate(value.to_bytes(size, "big"))})

    def t(self, condition):
        self.sr = (self.sr & ~1) | bool(condition)

    def instruction(self, pc):
        """Execute one opcode; return (next_pc, has_delay_slot)."""
        self.visited.add(pc)
        w = self.read(pc, 2)
        n, m, lo = (w >> 8) & 15, (w >> 4) & 15, w & 15
        r = self.r
        nxt, delay = pc + 2, False
        if w == 0x0009:
            pass
        elif w == 0x000B:
            nxt, delay = self.pr, True
        elif w >> 12 == 0xE:
            r[n] = signed(w & 255, 8)
        elif w >> 12 == 0x7:
            r[n] += signed(w & 255, 8)
        elif w >> 12 == 0xD:
            r[n] = self.read(((pc + 4) & ~3) + (w & 255) * 4, 4)
        elif w >> 12 == 0x9:
            r[n] = signed(self.read(pc + 4 + (w & 255) * 2, 2), 16)
        elif w >> 12 in (0xA, 0xB):
            if w >> 12 == 0xB:
                self.pr = pc + 4
            nxt, delay = pc + 4 + signed(w & 4095, 12) * 2, True
        elif w & 0xF0FF in (0x400B, 0x402B):
            nxt, delay = r[n], True
            if w & 0xF0FF == 0x400B:
                self.pr = pc + 4
        elif w >> 8 in (0x89, 0x8B, 0x8D, 0x8F):
            take = bool(self.sr & 1) == (w >> 8 in (0x89, 0x8D))
            delay = w >> 8 in (0x8D, 0x8F)
            nxt = pc + 4 + signed(w & 255, 8) * 2 if take else pc + (4 if delay else 2)
        elif w & 0xF0FF == 0x0029:
            r[n] = self.sr & 1
        elif w & 0xF0FF == 0x0002:
            r[n] = self.sr
        elif w & 0xF0FF == 0x400E:
            self.sr = r[n]
        elif w & 0xF0FF == 0x4022:
            r[n] -= 4
            self.write(r[n], self.pr, 4)
        elif w & 0xF0FF == 0x4026:
            self.pr = self.read(r[n], 4)
            r[n] += 4
        elif w & 0xF0FF == 0x4012:  # STS.L MACL,@-Rn
            r[n] -= 4
            self.write(r[n], self.macl, 4)
        elif w & 0xF0FF == 0x4016:  # LDS.L @Rn+,MACL
            self.macl = self.read(r[n], 4)
            r[n] += 4
        elif w & 0xF0FF == 0x001A:  # STS MACL,Rn
            r[n] = self.macl
        elif w >> 12 == 0x2 and lo == 0xE:  # MULU.W Rm,Rn
            self.macl = (r[n] & 0xFFFF) * (r[m] & 0xFFFF)
        elif w >> 12 == 0x6 and lo in (0, 1, 2, 4, 5, 6):
            size = (1, 2, 4)[lo % 4]
            r[n] = signed(self.read(r[m], size), size * 8)
            if lo >= 4 and n != m:
                r[m] += size
        elif w >> 12 == 0x2 and lo in (0, 1, 2, 4, 5, 6):
            size = (1, 2, 4)[lo % 4]
            val = r[m]
            if lo >= 4:
                r[n] -= size
            self.write(r[n], val, size)
        elif w >> 12 == 0x6 and lo == 3:
            r[n] = r[m]
        elif w >> 12 == 0x6 and lo in (0xC, 0xD, 0xE, 0xF):
            bits = 8 if lo in (0xC, 0xE) else 16
            r[n] = r[m] & ((1 << bits) - 1) if lo < 0xE else signed(r[m], bits)
        elif w >> 12 == 0x6 and lo == 7:
            r[n] = ~r[m]
        elif w >> 12 == 0x6 and lo == 0xB:
            r[n] = -r[m]
        elif w >> 12 == 0x6 and lo == 8:
            r[n] = (r[m] & 0xFFFF0000) | ((r[m] & 255) << 8) | ((r[m] >> 8) & 255)
        elif w >> 12 == 0x2 and lo in (8, 9, 0xA, 0xB):
            if lo == 8:
                self.t((r[n] & r[m]) == 0)
            elif lo == 9:
                r[n] &= r[m]
            elif lo == 0xA:
                r[n] ^= r[m]
            else:
                r[n] |= r[m]
        elif w >> 12 == 0x3 and lo in (0, 2, 3, 6, 7, 8, 0xC):
            if lo == 0:
                self.t(r[n] == r[m])
            elif lo == 2:
                self.t(r[n] >= r[m])
            elif lo == 3:
                self.t(signed(r[n]) >= signed(r[m]))
            elif lo == 6:
                self.t(r[n] > r[m])
            elif lo == 7:
                self.t(signed(r[n]) > signed(r[m]))
            elif lo == 8:
                r[n] -= r[m]
            else:
                r[n] += r[m]
        elif w & 0xF0FF in (0x4011, 0x4015):
            self.t(signed(r[n]) >= 0 if w & 255 == 0x11 else signed(r[n]) > 0)
        elif w & 0xF0FF in (0x4000, 0x4001, 0x4021, 0x4008, 0x4009, 0x4018, 0x4019):
            op = w & 255
            if op == 0:
                self.t(r[n] & 0x80000000)
                r[n] <<= 1
            elif op in (1, 0x21):
                self.t(r[n] & 1)
                r[n] = (signed(r[n]) if op == 0x21 else r[n]) >> 1
            elif op in (8, 0x18):
                r[n] <<= 2 if op == 8 else 8
            else:
                r[n] >>= 2 if op == 9 else 8
        elif w >> 8 == 0x88:
            self.t(r[0] == (signed(w & 255, 8) & MASK))
        elif w >> 8 in (0xC8, 0xC9, 0xCA, 0xCB):
            op = w >> 8
            if op == 0xC8:
                self.t((r[0] & (w & 255)) == 0)
            elif op == 0xC9:
                r[0] &= w & 255
            elif op == 0xCA:
                r[0] ^= w & 255
            else:
                r[0] |= w & 255
        elif w >> 8 in (0x80, 0x81, 0x84, 0x85):
            size = 1 if w >> 8 in (0x80, 0x84) else 2
            addr = r[m] + lo * size
            if w >> 8 in (0x84, 0x85):
                r[0] = signed(self.read(addr, size), size * 8)
            else:
                self.write(addr, r[0], size)
        elif w >> 12 in (1, 5):
            if w >> 12 == 1:
                self.write(r[n] + lo * 4, r[m], 4)
            else:
                r[n] = self.read(r[m] + lo * 4, 4)
        elif w >> 12 == 0 and lo in (4, 5, 6, 0xC, 0xD, 0xE):
            size = (1, 2, 4)[(lo & 7) - 4]
            if lo < 8:
                self.write(r[n] + r[0], r[m], size)
            else:
                r[n] = signed(self.read(r[m] + r[0], size), size * 8)
        elif w >> 8 in (0xC0, 0xC1, 0xC2):
            size = (1, 2, 4)[(w >> 8) - 0xC0]
            self.write(self.gbr + (w & 255) * size, r[0], size)
        elif w >> 8 in (0xC4, 0xC5, 0xC6):
            size = (1, 2, 4)[(w >> 8) - 0xC4]
            r[0] = signed(self.read(self.gbr + (w & 255) * size, size), size * 8)
        else:
            raise NotImplementedError(f"Opcode {w:04X} at {pc:08X}")
        self.r = [v & MASK for v in r]
        return nxt & MASK, delay

    def run(self, start, argument=0, limit=20000):
        self.r[4] = argument & MASK
        self.pr = 0xFFFFFFF0
        self.pc = start
        for _ in range(limit):
            if self.pc == 0xFFFFFFF0:
                return self.r[0]
            nxt, delay = self.instruction(self.pc)
            if delay:
                _, nested = self.instruction(self.pc + 2)
                if nested:
                    raise ValueError("Branch in delay slot")
            self.pc = nxt
        raise RuntimeError(f"Instruction limit at {self.pc:08X}")
