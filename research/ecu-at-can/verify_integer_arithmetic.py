"""ISA boundary tests and original TCU division helpers versus integer math."""
import hashlib
import itertools
import json
from pathlib import Path
import random

from sh_integer_arithmetic import SHIntegerArithmetic
from sh_subset import MASK, signed

ROM = (Path(__file__).resolve().parents[2] / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ROM).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def trunc_div(a, b):
    quotient = abs(a)//abs(b)
    return -quotient if (a < 0) != (b < 0) else quotient


def main():
    vectors = [0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x7FFFFFFF, 0x80000000, MASK]
    isa = 0
    for opcode, a, b, tbit in itertools.product([0x223F, 0x0237, 0x323E, 0x323A], vectors, vectors, range(2)):
        t = SHIntegerArithmetic(opcode.to_bytes(2, "big"))
        t.r[2], t.r[3], t.sr, t.macl = a, b, 0x3F0 | tbit, 0xAABBCCDD
        result = (signed(a, 16)*signed(b, 16) if opcode == 0x223F else a*b) if opcode < 0x3000 else (a+b+tbit if opcode == 0x323E else a-b-tbit)
        assert t.instruction(0) == (2, False)
        if opcode < 0x3000:
            assert t.macl == result & MASK and t.r[2] == a and t.sr == 0x3F0 | tbit
        else:
            assert t.r[2] == result & MASK and t.macl == 0xAABBCCDD
            assert t.sr == 0x3F0 | (result > MASK if opcode == 0x323E else result < 0)
        assert t.r[3] == b
        isa += 1
    for opcode, a, tbit in itertools.product([0x4224, 0x4228, 0x4229], vectors, range(2)):
        t = SHIntegerArithmetic(opcode.to_bytes(2, "big"))
        t.r[2], t.sr = a, 0x3F0 | tbit
        t.instruction(0)
        expected = ((a << 1) | tbit) & MASK if opcode == 0x4224 else (a << 16) & MASK if opcode == 0x4228 else a >> 16
        assert t.r[2] == expected
        assert t.sr == 0x3F0 | (a >> 31 if opcode == 0x4224 else tbit)
        isa += 1
    for a, b, flags in itertools.product(vectors, vectors, range(8)):
        old_q, m, incoming = (flags >> 1) & 1, flags >> 2, flags & 1
        top = bool(a & 0x80000000)
        shifted = ((a << 1) | incoming) & MASK
        # Explicit manual case table; independent of implementation's XOR form.
        if old_q == 0 and m == 0:
            expected = (shifted-b) & MASK
            bit = expected > shifted
            q = not bit if top else bit
        elif old_q == 0 and m == 1:
            expected = (shifted+b) & MASK
            bit = expected < shifted
            q = bit if top else not bit
        elif old_q == 1 and m == 0:
            expected = (shifted+b) & MASK
            bit = expected < shifted
            q = not bit if top else bit
        else:
            expected = (shifted-b) & MASK
            bit = expected > shifted
            q = bit if top else not bit
        t = SHIntegerArithmetic(bytes.fromhex("3234"))
        t.r[2], t.r[3], t.sr = a, b, 0xF0 | (m << 9) | (old_q << 8) | incoming
        t.instruction(0)
        assert t.r[2] == expected and t.r[3] == b
        assert t.sr == 0xF0 | (m << 9) | (q << 8) | (q == m)
        isa += 1
    for a, b in itertools.product(vectors, repeat=2):
        t = SHIntegerArithmetic(bytes.fromhex("2237"))
        t.r[2], t.r[3], t.sr = a, b, 0x3F1
        t.instruction(0)
        assert t.sr == 0xF0 | ((a >> 31) << 8) | ((b >> 31) << 9) | ((a ^ b) >> 31)
        t.rom = bytes.fromhex("0019")
        t.instruction(0)
        assert t.sr == 0xF0 and (t.r[2], t.r[3]) == (a, b)
        isa += 2

    rng = random.Random(216)
    pairs = list(itertools.product(vectors, [1, 2, 3, 96, 1000, 65535, 0x80000000, MASK]))
    pairs += [(rng.randrange(1 << 32), rng.randrange(1, 1 << 32)) for _ in range(512)]
    for numerator, denominator in pairs:
        t = SHIntegerArithmetic(ROM)
        t.r[0], t.r[1], t.r[2] = denominator, numerator, 0xABCDEF12
        assert t.run(0x5AF44) == numerator//denominator
        assert t.r[2] == 0xABCDEF12
    for raw in range(65536):
        t = SHIntegerArithmetic(ROM)
        t.r[0], t.r[1] = 96, raw
        assert signed(t.run(0x5AFEC)) == trunc_div(signed(raw, 16), 96)
    signed_pairs = list(itertools.product([-32768, -12345, -1, 0, 1, 12345, 32767], [-32768, -96, -1, 1, 96, 32767]))
    for numerator, denominator in signed_pairs:
        if numerator == -32768 and denominator == -1:
            continue  # quotient does not fit signed16; outside helper's valid range
        t = SHIntegerArithmetic(ROM)
        t.r[0], t.r[1] = denominator & MASK, numerator & MASK
        assert signed(t.run(0x5AFEC)) == trunc_div(numerator, denominator)
    print(json.dumps({"scope": __doc__, "isa_cases": isa, "unsigned32_divisions": len(pairs),
                      "signed16_divide96_cases": 65536, "signed16_sign_cases": len(signed_pairs)-1,
                      "source": "Renesas SH-2E REJ09B0316-0200 arithmetic ISA, DIV1 pp84-88",
                      "limitations": "No general chip, peripheral or timing simulation; base harness unchanged."}, indent=2))


if __name__ == "__main__":
    main()
