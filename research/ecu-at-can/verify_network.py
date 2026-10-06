"""Execute original ECU CAN211 decode, numeric consumer and receipt faults.

Synthetic state with explicit calls; no sender, scheduler, DSC/roof controller,
actuator, CAN peripheral or complete fault-recovery behavior is simulated.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH
from sh_exact_float import SHExactFloat, exact_bits, exact_value

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
SHA = hashlib.sha256(ECU).hexdigest()
assert SHA == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert ECU[0xB8243] == 1 and ECU[0xC11E9] == 0
assert exact_value(int.from_bytes(ECU[0xC11F8:0xC11FC], "big")) == 16


def setup(word=10500, flags=0):
    e = SHExactFloat(ECU)
    e.sr = 0xF0
    e.write(0xFFFF6A10, word, 2)
    e.write(0xFFFF6A12, 0xDEAD, 2)  # unrelated payload, deliberately nonzero
    e.write(0xFFFF6A14, flags, 2)
    e.write(0xFFFF6A16, 0xBEEF, 2)
    e.run(0x34B8C)
    e.run(0x34BB2)
    assert e.read(0xFFFF6A2A, 2) == word
    assert e.read(0xFFFF6A2C, 2) == flags
    assert e.read(0xFFFF6A1E, 1) == 20
    return e


def output(e):
    e.run(0x3FF2C)
    bits = e.read(0xFFFF714C, 4)
    checksum = ~((bits >> 16) + (bits & 0xFFFF)) & 0xFFFF
    assert e.read(0xFFFF7150, 2) == checksum
    assert e.read(0xFFFF7152, 2) == checksum
    assert 0x15522 in e.visited  # real protected writer, no mocked helpers
    return int(exact_value(bits))


flag_cases = 0
flag_bits = [0, 1, 2, 4, 5, 9, 10, 12, 13]
for pattern, fault, fresh in itertools.product(range(512), range(2), range(2)):
    flags = sum(((pattern >> i) & 1) << bit for i, bit in enumerate(flag_bits))
    e = setup(flags=flags)
    e.write(0xFFFF69E1, fault, 1)
    e.write(0xFFFF6A1E, fresh, 1)
    e.run(0x349CA)
    assert e.read(0xFFFF6A1C, 2) == (10500 if fresh else 65535)
    for raw_bit, addr in [(12, 0x6A1F), (9, 0x6A22), (4, 0x6A24), (0, 0x6A27)]:
        assert e.read(0xFFFF0000 + addr, 1) == bool(flags & (1 << raw_bit))
    for request, inhibit, addr in [(13, 12, 0x6A20), (10, 9, 0x6A21),
                                    (5, 4, 0x6A23), (2, 0, 0x6A25),
                                    (1, 0, 0x6A26)]:
        expected = bool(flags & (1 << request)) and not (fault or flags & (1 << inhibit))
        assert e.read(0xFFFF0000 + addr, 1) == expected
    flag_cases += 1

word_examples = []
for word, fresh in itertools.product([0, 1, 9999, 10000, 10500, 32767, 32768, 65534, 65535], range(2)):
    e = setup(word)
    e.write(0xFFFF6A1E, fresh, 1)
    e.run(0x349CA)
    value = output(e)
    assert value == (word if fresh else 65535) - 10000
    word_examples.append({"raw": word, "fresh": bool(fresh), "value_714c": value})

gate_cases = 0
for ramp, inhibit_a, inhibit_b, config, old in itertools.product(range(2), range(2), range(2), range(2), [100, 70000]):
    e = setup()
    e.run(0x349CA)
    for addr, value in [(0x718E, ramp), (0x7190, inhibit_a), (0x7191, inhibit_b), (0x7346, config)]:
        e.write(0xFFFF0000 + addr, value, 1)
    e.write(0xFFFF714C, exact_bits(old), 4)
    e.write(0xFFFF7140, exact_bits(1000), 4)
    expected = (65537 if config or old > 1000 else min(old + 16, 65537)) if ramp else (65537 if inhibit_a or inhibit_b else 500)
    assert output(e) == expected
    gate_cases += 1

# Saturating ramp boundary, with comparison threshold above previous output.
for old, expected in [(65520, 65536), (65521, 65537), (65530, 65537)]:
    e = setup()
    e.write(0xFFFF718E, 1, 1)
    e.write(0xFFFF714C, exact_bits(old), 4)
    e.write(0xFFFF7140, exact_bits(70000), 4)
    assert output(e) == expected

fault_counts = {}
for name, function, counters, config, destination in [
    ("at_receipts", 0x34806, [0x6A5D, 0x6A90, 0x6AD8, 0x6B0E], 0x734C, 0x69E2),
    ("other_receipts", 0x347B8, [0x6B04, 0x6A1E, 0x6AB4], 0x7353, 0x69E1),
]:
    count = 0
    for fresh_mask, enabled, configured, previous in itertools.product(range(1 << len(counters)), range(2), range(2), range(2)):
        e = SH(ECU)
        for i, counter in enumerate(counters):
            e.write(0xFFFF0000 + counter, (fresh_mask >> i) & 1, 1)
        for addr, value in [(0x722A, enabled), (config, configured), (destination, previous)]:
            e.write(0xFFFF0000 + addr, value, 1)
        e.run(function)
        expected = bool(configured and fresh_mask != (1 << len(counters)) - 1) if enabled else previous
        assert e.read(0xFFFF0000 + destination, 1) == expected
        count += 1
    fault_counts[name] = count

# Explicitly scheduled receipt decay -> network fault -> flag suppression,
# then receipt/recovery. The numeric branch gates are held at zero here;
# this does not claim the full ECU leaves them at zero in a fault condition.
e = setup(flags=0x2426)
for addr in [0x722A, 0x7353, 0x6B04, 0x6AB4]:
    e.write(0xFFFF0000 + addr, 1, 1)
lifecycle = []
for step in range(22):
    if step:
        e.run(0x34968)
    e.run(0x347B8)
    e.run(0x349CA)
    counter = e.read(0xFFFF6A1E, 1)
    fault = e.read(0xFFFF69E1, 1)
    assert counter == max(20 - step, 0)
    assert fault == (counter == 0)
    assert e.read(0xFFFF6A20, 1) == (counter > 0)
    lifecycle.append({"call": step, "receipt_counter": counter, "fault_69e1": fault, "value_714c_with_gates_zero": output(e)})
e.run(0x34BB2)
e.run(0x347B8)
e.run(0x349CA)
assert e.read(0xFFFF69E1, 1) == 0 and e.read(0xFFFF6A20, 1) == 1
assert output(e) == 500

print(json.dumps({
    "ecu_sha256": SHA,
    "scope": "Original ECU functions, synthetic RAM and explicit calls; no sender attribution, physical units, scheduling, actuator or complete fault behavior proven.",
    "flag_cases": flag_cases,
    "word_cases": word_examples,
    "numeric_gate_cases": gate_cases,
    "ramp_saturation_cases": 3,
    "receipt_fault_cases": fault_counts,
    "receipt_lifecycle": lifecycle,
    "receipt_recovery_passed": True,
}, indent=2))
