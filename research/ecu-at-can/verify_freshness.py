"""Original TCU receipt deadlines and ECU CAN211 inhibition/recovery logic.

Explicitly called ROM functions with synthetic RAM. No hardware, full task
scheduler, physical torque units or remote DSC/roof firmware is simulated.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH
from sh_exact_float import SHExactFloat, exact_bits, exact_value

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"

# Independent ISA vectors: preserve MACL on stack, unsigned low-word product,
# copy product to R4, restore MACL. Product and SR/stack preservation checked.
isa_cases = 0
for a, b in itertools.product([0, 1, 0xFFFFFFFF, 0xABCD8000], repeat=2):
    p = SH(bytes.fromhex("4f12231e041a4f16000b0009"))
    p.r[1], p.r[3], p.macl, p.sr = a, b, 0x89ABCDEF, 0xF1
    p.run(0)
    assert p.r[4] == (a & 65535) * (b & 65535)
    assert p.macl == 0x89ABCDEF and p.sr == 0xF1 and p.r[15] == 0xFFFED000
    isa_cases += 1


def w(machine, address, value, size=1):
    machine.write(0xFFFF0000 + address, value, size)


def r(machine, address, size=1):
    return machine.read(0xFFFF0000 + address, size)


def f(machine, address, value):
    w(machine, address, exact_bits(value), 4)


# Table records correspond to the IDs, not to hardware-mailbox indices.
ids = [0x200, 0x201, 0x211, 0x215, 0x216, 0x218, 0x231, 0x240,
       0x420, 0x430, 0x4B0, 0x4C1, 0x4EC, 0x4F1, 0x6E0, 0x6E1, 0x6E2, 0x6E3]
intervals = [10, 10, 10, 10, 10, 20, 25, 100, 100, 100, 10, 100, 25, 1000, 100, 100, 100, 100]
table = []
deadline_cases = 0
for i, (can_id, period) in enumerate(zip(ids, intervals)):
    addr = 0x5C610 + i * 28
    assert int.from_bytes(TCU[addr:addr+4], "big") == can_id
    assert int.from_bytes(TCU[addr+8:addr+10], "big") == period
    table.append({"index": i, "id": hex(can_id), "ticks": period, "class": TCU[addr+13]})
    for slot in range(2):
        t = SH(TCU)
        w(t, 0x84D0, 10000, 4)
        t.r[5] = slot
        t.run(0x19D44, i)
        expected = 10000 + (period if slot == 0 else 0)
        assert r(t, 0x8B38 + 8*i + 4*slot, 4) == expected
        for now in [expected - 1, expected, expected + 1]:
            w(t, 0x84D0, now, 4)
            t.r[5] = slot
            assert t.run(0x19D04, i) == (now >= expected)
            deadline_cases += 1

# Isolate each watched record while other deadlines remain in the future.
# Field bits are synthetic inputs to the actual consume-and-clear accessor.
watched = [(0, 46), (1, 44), (2, 43), (3, 31), (7, 24), (8, 23),
           (9, 22), (10, 18), (12, 6), (13, 0)]
lifecycle = []
for index, field in watched:
    for clear_enabled in range(2):
        t = SH(TCU)
        w(t, 0x8F6C, 8)
        w(t, 0x868C, clear_enabled)
        for i in range(18):
            w(t, 0x8B38 + 8*i, 100000, 4)
        offset, mask = TCU[0x5C9A0 + field], TCU[0x5C9CF + field]
        period = intervals[index]
        states = []
        for now, fresh in [(100, True), (100 + period - 1, False),
                           (100 + period, False), (101 + period, True)]:
            w(t, 0x84D0, now, 4)
            if fresh:
                w(t, 0x8F82 + offset, mask)
            t.run(0x19AF0)
            states.append(r(t, 0x8EE2, 2))
        assert states == [0, 0, 1 << index, 0 if clear_enabled else 1 << index]
        assert r(t, 0x8B38 + 8*index, 4) == 101 + 2*period
        assert r(t, 0x8F82 + offset) & mask == 0
        lifecycle.append({"id": hex(ids[index]), "clear_enabled_868c": clear_enabled,
                          "fault_bitmap_sequence": states})

# CAN211: execute the receipt dispatcher and its real callback too. This
# callback does not invoke the unsupported general integer division helpers.
t = SH(TCU)
w(t, 0x8F6C, 8)
w(t, 0x868C, 1)
for i in range(18):
    w(t, 0x8B38 + i*8, 100000, 4)
paired_lifecycle = []
for now, fresh in [(100, True), (109, False), (110, False), (111, True)]:
    w(t, 0x84D0, now, 4)
    if fresh:
        assert t.run(0x1BF38, 7) == 1  # actual admission sets8F71
        w(t, 0x8F4E, 0x80)  # ISR receipt bit; controller itself not emulated
        t.run(0x1BD10)
        assert r(t, 0x8F87) & 12 == 12 and r(t, 0x8F8D) & 12 == 12
        assert r(t, 0x8F4E) == 0 and r(t, 0x8F71) == 0
    t.run(0x19AF0)
    paired_lifecycle.append({"tick": now, "received": fresh,
                             "deadline": r(t, 0x8B48, 4), "fault_bitmap": r(t, 0x8EE2, 2)})
assert [s["fault_bitmap"] for s in paired_lifecycle] == [0, 0, 4, 0]

admission_cases = 0
for mode, index in itertools.product(range(16), [7, 10, 11]):
    t = SH(TCU)
    w(t, 0x8F6C, mode)
    assert t.run(0x1BF38, index) == (index >= 10 or bool(mode & 12))
    assert r(t, 0x8F71) == (index < 10 and bool(mode & 12))
    admission_cases += 1

# ECU fault/configuration gate7191, including non-Boolean configuration2.
configuration_cases = 0
assert ECU[0xB8298] == 0 and ECU[0xB8299] == 255
for variant, runtime_option in itertools.product([0, 0x31, 255], range(2)):
    e = SH(ECU)
    w(e, 0x9708, variant)
    w(e, 0x9710, runtime_option)
    e.run(0x42728)
    assert r(e, 0x734E) == 0 and r(e, 0x7353) == runtime_option
    assert r(e, 0x734A) == 0x80
    configuration_cases += 1

fault_gate_cases = 0
for config, fault, a, b in itertools.product(range(3), range(2), range(2), range(2)):
    e = SH(ECU)
    for address, value in [(0x734E, config), (0x69E1, fault), (0x7265, a), (0x7266, b)]:
        w(e, address, value)
    e.run(0x3FB78)
    assert r(e, 0x7191) == ((config == 0 and fault == 1) or (config == 1 and (a == 1 or b == 1)))
    fault_gate_cases += 1

# ECU local inhibit7190: all combinations of nine byte gates and two values
# above the65536 sentinel threshold. Inputs are synthetic, names unassigned.
byte_gates = [0xA3A4, 0x8F4B, 0x8EF8, 0x8F30, 0x6DFB, 0x8FB6, 0x8EC6, 0xA38C, 0x8CF4]
local_gate_cases = 0
for mask in range(2048):
    e = SHExactFloat(ECU)
    for i, address in enumerate(byte_gates):
        w(e, address, (mask >> i) & 1)
    f(e, 0x6A38, 65537 if mask & 512 else 65536)
    f(e, 0x6A3C, 65537 if mask & 1024 else 65536)
    e.run(0x3FC58)
    assert r(e, 0x7190) == bool(mask)
    local_gate_cases += 1

ramp_gate_cases = 0
for previous, active, a, b, old in itertools.product(range(2), range(2), range(2), range(2), [500, 65535, 65536, 65537]):
    e = SHExactFloat(ECU)
    for address, value in [(0x718E, previous), (0x718C, active), (0x7190, a), (0x7191, b)]:
        w(e, address, value)
    f(e, 0x714C, old)
    e.run(0x3FCFC)
    expected = 0 if old > 65535 else (1 if active and (a or b) else previous)
    assert r(e, 0x718E) == expected
    ramp_gate_cases += 1

active_latch_cases = 0
for mask, request in itertools.product(range(1024), [500, 1000]):
    e = SHExactFloat(ECU)
    e.sr = 0xF0
    addresses = [0x7346, 0x7191, 0x7190, 0x718F, 0x718E,
                 0x8EF9, 0x8EFA, 0x8EF8, 0x718C, 0x72DC]
    values = [(mask >> i) & 1 for i in range(10)]
    for address, value in zip(addresses, values):
        w(e, address, value)
    f(e, 0x7258, 2)
    f(e, 0x7154, 10)
    f(e, 0x7140, 1000)
    f(e, 0x714C, request)
    e.run(0x3FDCA)
    selected = 1000 - 2*10 > request and not any(values[:4])
    if selected or values[4]:
        expected = 1
    elif not (values[5] or values[6]) or values[7]:
        expected = 0
    else:
        expected = values[8]
    assert r(e, 0x718C) == expected
    assert r(e, 0x7192) == bool(values[9] or values[2])
    active_latch_cases += 1

# Receipt fault -> real inhibit gate -> numeric consumer. A previously active
# request takes the ramp; an inactive request selects the65537 sentinel.
ecu_examples = []
for active in range(2):
    e = SHExactFloat(ECU)
    e.sr = 0xF0
    for address in [0x722A, 0x7353, 0x6B04, 0x6AB4]:
        w(e, address, 1)
    w(e, 0x6A10, 10500, 2)
    w(e, 0x718C, active)
    f(e, 0x714C, 500)
    f(e, 0x7140, 1000)
    e.run(0x34B8C)
    # Counter6A1E intentionally zero: simulate an expired211 receipt.
    for fn in [0x347B8, 0x349CA, 0x3FB78, 0x3FC58, 0x3FCFC, 0x3FF2C]:
        e.run(fn)
    value = int(exact_value(r(e, 0x714C, 4)))
    assert r(e, 0x7191) == 1 and value == (516 if active else 65537)
    ecu_examples.append({"prior_active_718c": active, "ramp_718e": r(e, 0x718E), "output_714c": value})

print(json.dumps({"scope": __doc__.strip(), "isa_vectors": isa_cases,
                  "tcu_table": table, "deadline_boundary_cases": deadline_cases,
                  "tcu_admission_cases": admission_cases,
                  "ecu_configuration_cases": configuration_cases,
                  "tcu_record_lifecycles": lifecycle, "tcu_211_dispatch_lifecycle": paired_lifecycle,
                  "ecu_fault_gate_cases": fault_gate_cases, "ecu_local_gate_cases": local_gate_cases,
                  "ecu_ramp_gate_cases": ramp_gate_cases, "ecu_active_latch_cases": active_latch_cases,
                  "ecu_expiry_examples": ecu_examples}, indent=2))
