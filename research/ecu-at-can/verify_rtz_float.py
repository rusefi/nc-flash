"""Independent binary-search reference for bounded normal binary32 RTZ."""
from fractions import Fraction
import itertools
import json
import random
import struct

from sh_rtz_float import SHNormalRTZFloat, rtz_bits


def value(bits):
    return Fraction(struct.unpack(">f", bits.to_bytes(4, "big"))[0])


def reference(x, negative_zero=False):
    if not x:
        return 0x80000000 if negative_zero else 0
    sign = 0x80000000 if x < 0 else 0
    x = abs(x)
    assert value(0x00800000) <= x <= value(0x7F7FFFFF)
    lo, hi = 0x00800000, 0x7F7FFFFF
    while lo < hi:
        mid = (lo+hi+1)//2
        if value(mid) <= x:
            lo = mid
        else:
            hi = mid-1
    return sign | lo


def main():
    rng = random.Random(201)
    cases = [Fraction(0), Fraction(1, 10), Fraction(-1, 10)]
    for exponent in [-126, -100, -23, -1, 0, 1, 23, 100, 126]:
        for numerator in [1, 3, (1 << 24)-1, (1 << 24)+1]:
            x = Fraction(numerator, 1 << 24) * Fraction(2) ** exponent
            if abs(x) >= value(0x00800000):
                cases.extend([x, -x])
    for _ in range(256):
        a = rng.randrange(0x00800000, 0x7F7FFFFF)
        x = (2*value(a) + value(a+1))/3
        cases.extend([x, -x])
    for x in cases:
        assert rtz_bits(x) == reference(x)

    isa = 0
    operands = [0, 0x80000000, 0x3F800000, 0xBF800000, 0x3DCCCCCD,
                0xBDCCCCCD, 0x42C80000, 0xC2C80000, 0x3F800001]
    for op, a, b in itertools.product(range(4), operands, operands):
        if op == 3 and value(b) == 0:
            continue
        rom = (0xF230 | op).to_bytes(2, "big")
        t = SHNormalRTZFloat(rom)
        t.fr[2], t.fr[3], t.sr = a, b, 0xF1
        av, bv = value(a), value(b)
        x = [lambda: av+bv, lambda: av-bv, lambda: av*bv, lambda: av/bv][op]()
        negative = (av == bv == 0 and a >> 31 == ((b >> 31) ^ (op == 1)) == 1) if op < 2 else bool((a ^ b) >> 31)
        assert t.instruction(0) == (2, False)
        assert t.fr[2] == reference(x, negative)
        assert t.fr[3] == b and t.sr == 0xF1
        isa += 1

    mac_cases = 0
    for a, b, c in itertools.product(operands, repeat=3):
        t = SHNormalRTZFloat(bytes.fromhex("f23e"))
        t.fr[0], t.fr[3], t.fr[2], t.sr = a, b, c, 0xF1
        product = reference(value(a)*value(b), bool((a ^ b) >> 31))
        negative = value(product) == value(c) == 0 and product >> 31 == c >> 31 == 1
        expected = reference(value(product)+value(c), negative)
        assert t.instruction(0) == (2, False)
        assert (t.fr[2], t.fr[0], t.fr[3], t.sr) == (expected, a, b, 0xF1)
        mac_cases += 1
    # Distinguishes two rounded operations from a fused exact product-plus-add.
    a, b, c = 0x3F800001, 0x3F7FFFFE, 0xBF800000
    product = reference(value(a)*value(b))
    separate = reference(value(product)+value(c))
    assert separate != reference(value(a)*value(b)+value(c))
    for opcode, registers in [(0xF03E, {0: a, 3: b}), (0xF20E, {0: a, 2: c})]:
        t = SHNormalRTZFloat(opcode.to_bytes(2, "big"))
        for register, bits in registers.items():
            t.fr[register] = bits
        n, m = (opcode >> 8) & 15, (opcode >> 4) & 15
        x, y, z = t.fr[0], t.fr[m], t.fr[n]
        expected = reference(value(reference(value(x)*value(y)))+value(z))
        t.instruction(0)
        assert t.fr[n] == expected
        mac_cases += 1
    t = SHNormalRTZFloat(bytes.fromhex("f23e"))
    t.fr[0], t.fr[3], t.fr[2] = a, b, c
    t.instruction(0)
    assert t.fr[2] == separate
    mac_cases += 1

    rejections = 0
    for x in [Fraction(2)**-127, -Fraction(2)**-127, Fraction(2)**128, -Fraction(2)**128]:
        try:
            rtz_bits(x)
        except ValueError:
            rejections += 1
        else:
            raise AssertionError("Unsupported range accepted")
    for a, b in [(1, 0x3F800000), (0x7F800000, 0x3F800000),
                 (0x7FC00000, 0x3F800000), (0x3F800000, 0)]:
        t = SHNormalRTZFloat(bytes.fromhex("f233"))
        t.fr[2], t.fr[3] = a, b
        try:
            t.instruction(0)
        except ValueError:
            rejections += 1
        else:
            raise AssertionError("Unsupported operands accepted")

    print(json.dumps({"scope": __doc__, "rounding_reference_cases": len(cases),
                      "isa_cases": isa, "fmac_cases": mac_cases,
                      "expected_rejections": rejections}, indent=2))


if __name__ == "__main__":
    main()
