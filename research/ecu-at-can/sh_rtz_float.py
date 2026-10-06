"""Bounded SH-2E round-to-zero arithmetic for normal/zero values.

Separate from the exact-only harness. Rejects subnormal operands/results,
overflow, division by zero and nonfinite operands. FPSCR exception behavior
is not simulated. Other instructions retain SHExactFloat's strict limits,
including exact-only FLOAT. Renesas REJ09B0316-0200 p14 fixes RM=01;
p185 specifies FMAC as rounded FMUL followed by rounded FADD.
"""
from fractions import Fraction

from sh_exact_float import SHExactFloat, exact_value


def rtz_bits(value, negative_zero=False):
    value = Fraction(value)
    if value == 0:
        return 0x80000000 if negative_zero else 0
    sign = 0x80000000 if value < 0 else 0
    value = abs(value)
    n, d = value.numerator, value.denominator
    exponent = n.bit_length() - d.bit_length()
    if value < Fraction(2) ** exponent:
        exponent -= 1
    if exponent < -126 or exponent > 127 or value > exact_value(0x7F7FFFFF):
        raise ValueError("RTZ result outside supported normal range")
    scale = 23 - exponent
    significand = (n << scale) // d if scale >= 0 else n // (d << -scale)
    assert 1 << 23 <= significand < 1 << 24
    return sign | ((exponent + 127) << 23) | (significand - (1 << 23))


class SHNormalRTZFloat(SHExactFloat):
    def instruction(self, pc):
        opcode = self.read(pc, 2)
        n, m, op = (opcode >> 8) & 15, (opcode >> 4) & 15, opcode & 15
        if opcode >> 12 == 15 and op == 14:
            a, b, c = self.fr[0], self.fr[m], self.fr[n]
            product = rtz_bits(exact_value(a) * exact_value(b), bool((a ^ b) >> 31))
            p, v = exact_value(product), exact_value(c)
            negative_zero = p == v == 0 and product >> 31 == c >> 31 == 1
            self.fr[n] = rtz_bits(p + v, negative_zero)
            self.visited.add(pc)
            return pc + 2, False
        if opcode >> 12 != 15 or op not in (0, 1, 2, 3):
            return super().instruction(pc)
        lhs, rhs = self.fr[n], self.fr[m]
        a, b = exact_value(lhs), exact_value(rhs)
        if op in (0, 1):
            value = a + b if op == 0 else a - b
            # Exact cancellation is +0; same-sign zero operands preserve sign.
            rhs_sign = (rhs >> 31) ^ (op == 1)
            negative_zero = a == b == 0 and lhs >> 31 == rhs_sign == 1
        else:
            if op == 3 and b == 0:
                raise ValueError("RTZ division by zero unsupported")
            value = a * b if op == 2 else a / b
            negative_zero = bool((lhs ^ rhs) >> 31)
        self.fr[n] = rtz_bits(value, negative_zero)
        self.visited.add(pc)
        return pc + 2, False
