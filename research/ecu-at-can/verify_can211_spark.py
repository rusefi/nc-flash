"""Execute CAN211 numeric request through ECU per-cylinder spark values.

Unchanged ROM, real helpers, synthetic model inputs and explicit scheduling.
No DSC sender identification, ignition timer, vehicle or general FPU emulation.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

from sh_exact_float import SHExactFloat, exact_bits, exact_value

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
SHA = hashlib.sha256(ECU).hexdigest()
assert SHA == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(e, addr, value, size=1):
    e.write(0xFFFF0000+addr, value, size)


def f(e, addr, value):
    w(e, addr, exact_bits(value), 4)


def rf(e, addr):
    return exact_value(e.read(0xFFFF0000+addr, 4))


# Independent ISA vectors: register selection, sign/bit preservation, integer
# truncation and unchanged SR. No firmware-derived expected values here.
normal = [0, 0x80000000, 0x3F400000, 0xBF400000, 0x402ED9EB,
          0xC02ED9EB, 0x4EFFFFFF, 0xCF000000]
truncated = [0, 0, 0, 0, 2, 0xFFFFFFFE, 0x7FFFFF80, 0x80000000]
special = [1, 0x7F800000, 0xFF800000, 0x7FC12345]
isa_cases = rejected_cases = 0
for reg, bits in itertools.product(range(16), normal+special):
    e = SHExactFloat((0xF01D | reg << 8).to_bytes(2, "big"))
    e.fr[reg], e.sr = bits, 0xF1
    assert e.instruction(0) == (2, False)
    assert e.fpul == bits and e.fr[reg] == bits and e.sr == 0xF1
    isa_cases += 1
for reg, bits in itertools.product(range(16), normal):
    for opcode in [0xF05D, 0xF03D]:
        e = SHExactFloat((opcode | reg << 8).to_bytes(2, "big"))
        e.fr[reg], e.sr = bits, 0xF1
        assert e.instruction(0) == (2, False)
        if opcode == 0xF05D:
            assert e.fr[reg] == bits & 0x7FFFFFFF
        else:
            assert e.fpul == truncated[normal.index(bits)]
            assert e.fr[reg] == bits
        assert e.sr == 0xF1
        isa_cases += 1
for opcode, bits in itertools.product([0xF05D, 0xF03D], special):
    e = SHExactFloat(opcode.to_bytes(2, "big"))
    e.fr[0] = bits
    try:
        e.instruction(0)
    except ValueError:
        rejected_cases += 1
    else:
        raise AssertionError("Non-finite/subnormal arithmetic was accepted")
for bits in [0x4F000000, 0xCF000001]:
    e = SHExactFloat(bytes.fromhex("f03d"))
    e.fr[0] = bits
    try:
        e.instruction(0)
    except ValueError:
        rejected_cases += 1
    else:
        raise AssertionError("Out-of-range FTRC was accepted")

factor_cases = 0
for mt, gear, valid, fallback in itertools.product(range(2), range(8), range(2), range(2)):
    e = SHExactFloat(ECU)
    for addr, val in [(0x734A, 0x40 if mt else 0x80), (0x717F, gear),
                      (0x7187, valid), (0x7185, fallback)]:
        w(e, addr, val)
    f(e, 0x716C, 7)
    f(e, 0x6A38, 2)
    f(e, 0x6A3C, 4)
    e.run(0x3F600)
    expected = 8
    if mt:
        addr = 0xC1200+4*gear if 1 <= gear <= 6 else 0xC121C
        expected = exact_value(int.from_bytes(ECU[addr:addr+4], "big")) if valid and not fallback else 7
    assert rf(e, 0x7154) == expected
    factor_cases += 1

bound_cases = inexact_bound_cases = 0
epsilon = exact_value(int.from_bytes(ECU[0x3FBC8:0x3FBCC], "big"))
for ratio, bypass, request, floor in itertools.product(
        [-2, 0, Fraction(1, 131072), Fraction(1, 65536), 1, 2], range(2), [-16, 0, 16, 65537], [0, 32]):
    e = SHExactFloat(ECU)
    for addr, val in [(0x7154, ratio), (0x714C, request), (0x7148, floor), (0x71C4, 8), (0x711C, 99)]:
        f(e, addr, val)
    w(e, 0x6A28, bypass)
    expected = 99 if abs(ratio) <= epsilon else Fraction(max(request, floor))/(1 if bypass else Fraction(ratio))+8
    try:
        exact_bits(expected)
    except ValueError:
        try:
            e.run(0x3F97C)
        except ValueError as error:
            assert "Inexact FPU" in str(error)
            inexact_bound_cases += 1
            continue
        raise AssertionError("Inexact result was accepted")
    e.run(0x3F97C)
    assert rf(e, 0x715C) == expected
    bound_cases += 1

count_cases = 0
for count in range(9):
    e = SHExactFloat(ECU)
    w(e, 0x71F0, count)
    f(e, 0x715C, 56*(8-count))
    e.run(0x3F9EC)
    assert rf(e, 0x7170) == (448 if count < 8 else 0)
    count_cases += 1

root_cases = 0
for q in [-4, *range(65)]:
    e = SHExactFloat(ECU)
    f(e, 0x71A8, 1)
    f(e, 0x71B0, q)
    f(e, 0x71AC, 30)
    e.run(0x3FA3E)
    expected = 30-Fraction(math.isqrt(max(q, 0)*16), 4)
    assert rf(e, 0x7174) == expected
    root_cases += 1
for curvature in [0, -1, Fraction(1, 2048)]:
    e = SHExactFloat(ECU)
    f(e, 0x71A8, curvature)
    f(e, 0x7174, 117)
    e.run(0x3FA3E)
    assert rf(e, 0x7174) == 117
    root_cases += 1

correction_cases = 0
for active, enabled, uncapped, difference in itertools.product(range(2), [0, 1, 2], range(2), [-4, 0, 3, 20]):
    e = SHExactFloat(ECU)
    for addr, val in [(0x718C, active), (0x6590, enabled), (0x7D35, uncapped)]:
        w(e, addr, val)
    f(e, 0x7A84, 30)
    f(e, 0x7174, 30-difference)
    f(e, 0x7D38, 8)
    e.run(0x53438)
    expected = (max(difference, 0) if uncapped else min(max(difference, 0), 8)) if active and enabled else 0
    assert rf(e, 0x7D2C) == expected
    correction_cases += 1

examples = []
assert ECU[0xB8244] == 1
assert ECU[0xD0594:0xD05A4] == bytes(16)  # Stock cylinder trims are zero.
for word, enabled, cap in itertools.product([10000, 10016, 10023, 10025, 10050], range(2), [2, 100]):
    e = SHExactFloat(ECU)
    for addr, val in [(0x734A, 0x80), (0x6590, enabled)]:
        w(e, addr, val)
    for addr, val in [(0x7140, 50), (0x71A8, 1), (0x71B0, 25), (0x71AC, 30),
                      (0x7A84, 30), (0x7D38, cap), (0x7C74, 2), (0x7F0C, 4),
                      (0x7D84, 1), (0x7D48, 3), (0x7BD8, 1), (0x7EDC, 2),
                      (0x7A7C, -60), (0x7C94, 30), (0x7ACC, 60)]:
        f(e, addr, val)
    w(e, 0x6A10, word, 2)
    for fn in [0x34B8C, 0x34BB2, 0x349CA, 0x34BBC, 0x34FFA, 0x3F600,
               0x3FF2C, 0x3F97C, 0x3FDCA, 0x3F9EC, 0x3FA3E, 0x53438,
               0x4FD9C, 0x4FBDA, 0x4FB4E]:
        e.run(fn)
    request = word-10000
    root = Fraction(math.isqrt(max(25-request, 0)*16), 4)
    correction = min(root, cap) if request < 50 and enabled else 0
    assert rf(e, 0x714C) == request
    assert rf(e, 0x7D2C) == correction
    outputs = [rf(e, a) for a in [0x7A9C, 0x7AA0, 0x7AA4, 0x7AA8]]
    assert outputs == [24-correction]*4
    examples.append({"can211_word0": word, "enable_6590": enabled, "cap_7d38": cap,
                     "numeric_714c": request, "correction_7d2c": float(correction),
                     "per_cylinder_spark": [float(v) for v in outputs]})

print(json.dumps({"ecu_sha256": SHA, "isa_cases": isa_cases, "rejected_isa_cases": rejected_cases,
                  "factor_cases": factor_cases, "bound_cases": bound_cases,
                  "inexact_bound_cases_rejected": inexact_bound_cases, "count_cases": count_cases,
                  "root_cases": root_cases, "correction_gate_cases": correction_cases,
                  "wire_to_spark_examples": examples,
                  "limits": "Synthetic coefficients/RAM and explicit calls; no full scheduler, DSC sender, physical CAN211 units, ignition timer or vehicle simulation."}, indent=2))
