"""Execute ECU CAN4B0 words -> selected value -> CAN201 bytes4/5.

Unmodified ECU instructions, synthetic RAM and explicit call order. The D504
fallback executes its cached-value branch (4564=0). No peripheral, scheduler,
DSC sender or PRHT receiver is simulated. Physical speed units are unproven.
Independent binary-search RTZ reference models each rounded operation.
"""
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from sh_exact_float import exact_bits
from sh_rtz_float import SHNormalRTZFloat
from sh_subset import SH
from verify_rtz_float import reference, value

ROOT = Path(__file__).resolve().parents[2]
ROM = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
SHA = hashlib.sha256(ROM).hexdigest()
assert SHA == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert ROM[0x378DC:0x378E8] == bytes.fromhex("0000020100020800ffff6b2c")
assert ROM[0x379FC:0x37A08] == bytes.fromhex("000004b001240800ffff6af0")
assert int.from_bytes(ROM[0x36874:0x36878], "big") == 0x3C23D70A
COEFF = value(0x3C23D70A)
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
TCU_SHA = hashlib.sha256(TCU).hexdigest()
assert TCU_SHA == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def w(e, address, number, size=1):
    e.write(0xFFFF0000 + address, number, size)


def r(e, address, size=1):
    return e.read(0xFFFF0000 + address, size)


def f(e, address, number):
    w(e, address, exact_bits(number), 4)


def q(number):
    return value(reference(number))


def decode(raw):
    return max(Fraction(0), q(q(raw*COEFF)-100))


def encode(number):
    quantized = int(q(q(q(number+100)/COEFF)+Fraction(1, 2)))
    return min(40000, max(10000, min(65535, max(0, quantized))))


cases = 0
examples = []
words = [0, 9999, 10000, 10001, 12345, 14567, 32767, 40000, 65534, 65535]
for a, b, cfg, mt, invalid, expired in itertools.product(words, words, range(2), range(2), range(2), range(2)):
    e = SHNormalRTZFloat(ROM)
    for address, number in [(0x7353, cfg), (0x734A, 0x40 if mt else 0x80),
                            (0x8EC6, invalid), (0x6B00, expired), (0x4564, 0)]:
        w(e, address, number)
    f(e, 0x452C, 17)
    f(e, 0x6E18, 23)
    payload = bytes.fromhex("a55ac33c") + a.to_bytes(2, "big") + b.to_bytes(2, "big")
    for i, byte in enumerate(payload):
        w(e, 0x6AF0+i, byte)
    e.run(0x35FA6)
    assert (r(e, 0x6B08, 2), r(e, 0x6B0A, 2)) == (a, b)
    e.run(0x35EBA)
    bad_a, bad_b = cfg == 1 and a == 65535, cfg == 1 and b == 65535
    assert (r(e, 0x6B01), r(e, 0x6B02)) == (bad_a, bad_b)
    assert r(e, 0x6B03) == (bad_a and bad_b or expired and cfg)
    assert (r(e, 0x6AF8, 2), r(e, 0x6AFA, 2)) == (a, b)
    selected = Fraction(17 if mt else 23)
    if cfg and not (bad_a and bad_b):
        selected = decode(b) if bad_a else decode(a) if bad_b else q(q(decode(a)+decode(b))/2)
    if invalid:
        selected = Fraction(65537)
    e.run(0x3A05E)
    assert r(e, 0x6D58, 4) == reference(selected)
    assert r(e, 0x6D64, 4) == exact_bits(17)
    assert 0xD504 in e.visited and 0x20B0 in e.visited
    e.run(0x3679C)
    output = 65535 if invalid else encode(selected)
    assert r(e, 0x6B38, 2) == output
    w(e, 0x6B3C, 0x1234, 2)
    w(e, 0x6B3E, 0x5678, 2)
    w(e, 0x6B40, 0x9A)
    w(e, 0x6B41, 0xBC)
    e.run(0x365D0)
    expected = bytes.fromhex("12345678") + output.to_bytes(2, "big") + bytes.fromhex("9abc")
    assert bytes(r(e, 0x6B2C+i) for i in range(8)) == expected
    if cfg and not mt and not invalid and not expired and (a, b) in [(12345, 14567), (65535, 14567), (12345, 65535), (65535, 65535), (10000, 10000), (65534, 65534)]:
        examples.append({"input_words": [a, b], "selected_binary32": hex(r(e, 0x6D58, 4)),
                         "selected_decimal": float(selected), "output_word": output,
                         "can201_fixture_payload": expected.hex()})
    cases += 1

encoder_cases = 0
for selected, fallback, invalid in itertools.product(
        [-200, -100, -1, 0, Fraction(1, 256), 299, 300, 301, 555, 65536, 65537],
        [0, 65536, 65537], range(2)):
    e = SHNormalRTZFloat(ROM)
    f(e, 0x6D58, selected)
    f(e, 0x6E18, fallback)
    w(e, 0x8EC6, invalid)
    e.run(0x3679C)
    expected = 65535 if invalid or fallback > 65536 else encode(Fraction(selected))
    assert r(e, 0x6B38, 2) == expected
    encoder_cases += 1

# Actual TCU setter -> ECU216 unpack/normalize -> fallback -> selection/201.
# These are setter arguments, not a claim about the TCU's numeric producer.
paired_cases = 0
paired_examples = []
for raw, mt, receive_gate, fresh, can4b0 in itertools.product(
        [9999, 10000, 12345, 40000, 65534, 65535], range(2), range(2), range(2), range(2)):
    t, e = SH(TCU), SHNormalRTZFloat(ROM)
    t.run(0x1C666, raw)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    w(e, 0x734A, 0x40 if mt else 0x80)
    w(e, 0x734C, receive_gate)
    w(e, 0x6A5D, fresh)
    e.run(0x35034)
    assert r(e, 0x6A50, 2) == raw
    e.run(0x34CEC)
    accepted_raw = (raw if receive_gate and not mt else 10000) if fresh else 65535
    assert r(e, 0x6A56, 2) == accepted_raw
    e.run(0x3B7CE)
    fallback = Fraction(0) if mt else Fraction(65537) if accepted_raw == 65535 else decode(accepted_raw)
    assert r(e, 0x6E18, 4) == reference(fallback)
    w(e, 0x7353, can4b0)
    w(e, 0x6AF8, 14567, 2)
    w(e, 0x6AFA, 14567, 2)
    f(e, 0x452C, 17)
    e.run(0x3A05E)
    selected = decode(14567) if can4b0 else Fraction(17) if mt else fallback
    assert r(e, 0x6D58, 4) == reference(selected)
    e.run(0x3679C)
    e.run(0x365D0)
    output = 65535 if fallback > 65536 else encode(selected)
    assert r(e, 0x6B30, 2) == output
    if not mt and receive_gate and can4b0 and raw in [12345, 65535]:
        paired_examples.append({"tcu_word5_argument": raw, "receipt_live": bool(fresh),
                                "can4b0_words": [14567, 14567],
                                "selected_value": float(selected), "fallback_value": float(fallback),
                                "can201_word4": output})
    paired_cases += 1

pack_cases = 0
for mode in [0, 0x40, 0x80, 0xC0]:
    e = SHNormalRTZFloat(ROM)
    w(e, 0x734A, mode)
    for i in range(8):
        w(e, 0x6B2C+i, 0xAA)
    e.run(0x365D0)
    assert bytes(r(e, 0x6B2C+i) for i in range(8)) == (bytes(8) if mode else bytes([0xAA])*8)
    pack_cases += 1

e = SHNormalRTZFloat(ROM)
e.run(0x35FD8)
assert all(r(e, a, 2) == 10000 for a in [0x6AF8, 0x6AFA, 0x6AFC, 0x6AFE, 0x6B08, 0x6B0A])
e.run(0x35FCE)
assert r(e, 0x6B04) == ROM[0xB8248] == 20

print(json.dumps({"scope": __doc__.strip(), "ecu_sha256": SHA, "tcu_sha256": TCU_SHA,
                  "end_to_end_cases": cases, "encoder_boundary_cases": encoder_cases,
                  "pack_mode_cases": pack_cases, "initialization_and_receipt_reload": "pass",
                  "examples": examples, "paired_tcu216_cases": paired_cases,
                  "paired_examples": paired_examples,
                  "limits": "RAM fixtures and explicit scheduling; speed units, DSC ownership and roof consumption unproven."}, indent=2))
