"""TCU sampled inputs through CAN231 to the ECU's combined state flag.

Five peripheral read addresses return explicit constant test samples. This
executes original input filtering and application code, not physical GPIO,
ADC conversions, interrupts, CAN hardware or a complete task scheduler.
Physical P/R/N/D assignment and PRHT interpretation remain unverified.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, addr, value, size=1):
    t.write(0xFFFF0000 + addr, value, size)


def r(t, addr, size=1):
    return t.read(0xFFFF0000 + addr, size)


# Independent MOV.B/W/L R0,@(disp,GBR) vectors: scaled unsigned displacement,
# big-endian truncated writes, guards, and unchanged registers/status.
isa_cases = 0
for size, disp, value, gbr in itertools.product([1, 2, 4], [0, 1, 128, 255],
                                               [0, 1, 0x80, 0x89ABCDEF, 0xFFFFFFFF],
                                               [0xFFFF8000, 0xFFFF9000]):
    op = (0xC000 + {1: 0, 2: 0x100, 4: 0x200}[size]) | disp
    t = SH(op.to_bytes(2, "big") + bytes.fromhex("000b0009"))
    t.gbr, t.r[0], t.sr = gbr, value, 0xF1
    addr = gbr + size*disp
    for i in range(-1, size+1):
        t.write(addr+i, 0x5A, 1)
    t.run(0)
    assert bytes(t.read(addr+i, 1) for i in range(size)) == value.to_bytes(4, "big")[-size:]
    assert t.read(addr-1, 1) == t.read(addr+size, 1) == 0x5A
    assert t.r[0] == value and t.sr == 0xF1 and t.gbr == gbr
    isa_cases += 1


class SampledInputs(SH):
    """Read-only test samples; all other peripheral accesses still fail."""
    def __init__(self):
        super().__init__(TCU)
        self.samples = {0xFFFFF778: 0x003C, 0xFFFFF810: 500 << 6,
                        0xFFFFF812: 500 << 6, 0xFFFFF76C: 0, 0xFFFFF746: 0}
        self.sample_reads = set()

    def read(self, addr, size):
        if addr in self.samples:
            assert size == 2
            self.sample_reads.add(addr)
            return self.samples[addr]
        return super().read(addr, size)


def set_inputs(t, mask):
    # Descriptor polarity0 means a low PKDR bit produces asserted input1.
    t.samples[0xFFFFF778] = (15 ^ mask) << 2


def flags(t):
    return sum(r(t, 0x88B4+i) << i for i in range(4))


def expected_wire(mask, fault=0):
    if mask.bit_count() > 1 or fault:
        return 15
    return mask.bit_length() if mask else 0


def sample_and_build(t):
    for fn in [0x17250, 0x174A0, 0x22416]:
        t.run(fn)
    t.run(0x19414, 1)


def paired_flag(t):
    e = SH(ECU)
    e.sr = 0xF0
    w(e, 0x734A, 0x80)
    w(e, 0x734C, 1)
    for i in range(8):
        w(e, 0x6ABC+i, r(t, 0x8EED+i))
    for fn in [0x35BB8, 0x3585C, 0x411F0]:
        e.run(fn)
    low = r(t, 0x8EED) & 15
    assert [r(e, 0x6AD1+i) for i in range(7)] == [int(i == low) for i in range(7)]
    expected = int(low in [1, 3])
    assert r(e, 0x723A, 2) == r(e, 0x7244, 2) == (0x01FE if expected else 0x00FF)
    return expected


descriptors = []
for i in range(4):
    a = 0x5F648 + i*12
    assert TCU[a:a+4] == bytes.fromhex("02020000")
    ptr = int.from_bytes(TCU[a+4:a+8], "big")
    assert ptr == 0x5C530 + i*8 and TCU[a+8] == 3
    assert int.from_bytes(TCU[ptr:ptr+4], "big") == 0xFFFFF778
    assert TCU[ptr+4:ptr+6] == bytes([i+2, 0])
    descriptors.append({"channel": i, "pin_candidate": f"PK{i+2}",
                        "processed_input": hex(0xFFFF88B4+i), "wire_low_nibble": i+1,
                        "assert_samples": 2, "release_samples": 2})

# Every four-bit input transition, including invalid simultaneous assertions.
transition_cases = 0
for old, new in itertools.product(range(16), repeat=2):
    t = SampledInputs()
    t.run(0x17230)
    set_inputs(t, old)
    sample_and_build(t)
    sample_and_build(t)
    assert flags(t) == old
    set_inputs(t, new)
    sample_and_build(t)
    assert flags(t) == old
    assert r(t, 0x8EED) & 15 == expected_wire(old)
    paired_flag(t)
    sample_and_build(t)
    assert flags(t) == new
    assert r(t, 0x8EED) & 15 == expected_wire(new)
    paired_flag(t)
    assert t.sample_reads == set(t.samples)
    transition_cases += 1

# Both ADC checks in14368 must pass. Threshold counts375 and373, from ROM.
assert int.from_bytes(TCU[0x5FCF4:0x5FCF6], "big") == 375
assert int.from_bytes(TCU[0x5FCF6:0x5FCF8], "big") == 373
adc_boundary_cases = 0
for first, second in itertools.product([374, 375, 376], [372, 373, 374]):
    t = SampledInputs()
    t.samples[0xFFFFF810], t.samples[0xFFFFF812] = first << 6, second << 6
    assert t.run(0x14368, 3) == (first < 375 or second < 373)
    adc_boundary_cases += 1

held_input_cases = 0
for channel, failed_adc in itertools.product(range(4), [0, 1, 2]):
    t = SampledInputs()
    t.run(0x17230)
    set_inputs(t, 1 << channel)
    sample_and_build(t)
    sample_and_build(t)
    set_inputs(t, 0)
    if failed_adc in [0, 2]:
        t.samples[0xFFFFF810] = 374 << 6
    if failed_adc in [1, 2]:
        t.samples[0xFFFFF812] = 372 << 6
    for _ in range(3):
        sample_and_build(t)
        assert flags(t) == 1 << channel
        assert r(t, 0x8818 + 5*channel + 2) == 3
        assert r(t, 0x8EED) & 15 == channel+1
        paired_flag(t)
    t.samples[0xFFFFF810] = t.samples[0xFFFFF812] = 500 << 6
    sample_and_build(t)
    assert flags(t) == 1 << channel
    sample_and_build(t)
    assert flags(t) == 0
    held_input_cases += 1

fault_cases = 0
examples = []
for mask, fault in itertools.product(range(16), range(2)):
    t = SampledInputs()
    t.run(0x17230)
    set_inputs(t, mask)
    sample_and_build(t)
    sample_and_build(t)
    w(t, 0x92CD, fault << 6)
    t.run(0x19414, 1)
    assert r(t, 0x8EED) & 15 == expected_wire(mask, fault)
    combined = paired_flag(t)
    fault_cases += 1
    if not fault and mask.bit_count() <= 1:
        examples.append({"asserted_mask": mask, "class_8080": r(t, 0x8080),
                         "byte0": hex(r(t, 0x8EED)), "ecu_combined_723a": combined})

# ECU combined flag's override and local-input branch, separate from CAN decode.
ecu_gate_cases = 0
for override, can_enabled, local_high, low in itertools.product(range(2), range(2), range(2), range(16)):
    e = SH(ECU)
    w(e, 0x7002, override)
    w(e, 0x734C, can_enabled)
    w(e, 0x44A4, local_high)
    w(e, 0x6AD2, int(low == 1))
    w(e, 0x6AD4, int(low == 3))
    e.run(0x411F0)
    value = bool(override or (low in [1, 3] if can_enabled else not local_high))
    assert r(e, 0x723A, 2) == r(e, 0x7244, 2) == (0x1FE if value else 0xFF)
    ecu_gate_cases += 1

print(json.dumps({"scope": __doc__.strip(), "isa_gbr_store_vectors": isa_cases,
                  "input_descriptors": descriptors, "all_four_bit_transitions": transition_cases,
                  "adc_boundary_cases": adc_boundary_cases, "adc_hold_recovery_cases": held_input_cases,
                  "sender_fault_cases": fault_cases, "ecu_combined_flag_gate_cases": ecu_gate_cases,
                  "single_input_examples": examples,
                  "unresolved": "P versus N physical pin assignment, gearbox motion, absolute task timing, downstream diagnostics and PRHT CAN interpretation."}, indent=2))
