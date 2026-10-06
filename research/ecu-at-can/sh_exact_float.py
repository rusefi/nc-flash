"""SH subset with bit-preserving float moves and EXACT finite arithmetic only.

SH-2E rounds toward zero. Host float rounding must not silently stand in for
that hardware: Fraction computes exact results here, and any result which
cannot be represented exactly as binary32 raises an error. This supports the
integer-valued CAN216 normalization and command-copy paths without claiming
general FPU, exception, subnormal, timing or peripheral emulation.
FLDS preserves raw bits; FABS accepts finite normal/zero inputs; FTRC
implements specified truncation only for finite inputs within signed32 range.
Reference: Renesas SH-2E Software Manual, REJ09B0316-0200, FPU instructions.
"""
from fractions import Fraction
import struct

from sh_subset import MASK, SH, signed


def exact_value(bits):
    exponent = (bits >> 23) & 255
    if exponent == 255 or (exponent == 0 and bits & 0x7fffff):
        raise ValueError("Unsupported non-finite or subnormal FPU operand")
    return Fraction(struct.unpack(">f", bits.to_bytes(4, "big"))[0])


def exact_bits(value):
    bits = int.from_bytes(struct.pack(">f", float(value)), "big")
    if exact_value(bits) != value:
        raise ValueError("Inexact FPU result requires unimplemented SH-2E rounding")
    return bits


class SHExactFloat(SH):
    def __init__(self, rom):
        super().__init__(rom)
        self.fr = [0] * 16
        self.fpul = 0

    def instruction(self, pc):
        w = self.read(pc, 2)
        n, m, lo = (w >> 8) & 15, (w >> 4) & 15, w & 15
        r, fr = self.r, self.fr
        if w >> 8 == 0xc7:  # MOVA
            r[0] = ((pc + 4) & ~3) + (w & 255) * 4
        elif w & 0xf0ff == 0x405a:  # LDS Rn,FPUL
            self.fpul = r[n]
        elif w & 0xf0ff == 0x005a:  # STS FPUL,Rn
            r[n] = self.fpul
        elif w >> 12 != 0xf:
            return super().instruction(pc)
        elif lo == 0xc:
            fr[n] = fr[m]
        elif lo in (6, 8, 9):
            fr[n] = self.read(r[m] + (r[0] if lo == 6 else 0), 4)
            if lo == 9:
                r[m] = (r[m] + 4) & MASK
        elif lo in (7, 0xa, 0xb):
            if lo == 0xb:
                r[n] = (r[n] - 4) & MASK
            self.write(r[n] + (r[0] if lo == 7 else 0), fr[m], 4)
        elif w & 0xf0ff == 0xf08d:
            fr[n] = 0
        elif w & 0xf0ff == 0xf09d:
            fr[n] = 0x3f800000
        elif w & 0xf0ff == 0xf01d:  # FLDS FRn,FPUL: bit-preserving transfer
            self.fpul = fr[n]
        elif w & 0xf0ff == 0xf05d:  # FABS FRn; retain finite-only scope
            exact_value(fr[n])
            fr[n] &= 0x7fffffff
        elif w & 0xf0ff == 0xf03d:  # FTRC FRn,FPUL: finite, in-range only
            value = exact_value(fr[n])
            if not -(1 << 31) <= value < (1 << 31):
                raise ValueError("FTRC overflow/invalid handling is not implemented")
            self.fpul = int(value) & MASK  # Fraction truncates toward zero
        elif w & 0xf0ff == 0xf02d:
            fr[n] = exact_bits(Fraction(signed(self.fpul)))
        elif lo in (0, 1, 2, 3, 4, 5, 0xe):
            a, b = exact_value(fr[n]), exact_value(fr[m])
            if lo in (4, 5):
                self.t(a == b if lo == 4 else a > b)
            else:
                if lo == 0:
                    value = a + b
                elif lo == 1:
                    value = a - b
                elif lo == 2:
                    value = a * b
                elif lo == 3:
                    value = a / b
                else:
                    product = exact_value(fr[0]) * b
                    exact_bits(product)  # no assumption about fused rounding
                    value = a + product
                fr[n] = exact_bits(value)
        else:
            raise NotImplementedError(f"FPU opcode {w:04X} at {pc:08X}")
        self.visited.add(pc)
        return pc + 2, False
