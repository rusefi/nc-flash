"""Execute TCU CAN216 production through ECU per-cylinder command selection.

Runs original function bodies with synthetic state and explicit scheduling.
No CAN controller, timer outputs, real-time behavior or vehicle is simulated.
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from sh_subset import SH
from sh_exact_float import SHExactFloat, exact_bits, exact_value

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"

# Independent manual example: FMAC FR0=2, FR3=4, FR5=1 gives9.
probe = SHExactFloat(bytes.fromhex("f53e000b0009"))
probe.fr[0], probe.fr[3], probe.fr[5] = 0x40000000, 0x40800000, 0x3f800000
probe.run(0)
assert probe.fr[5] == 0x41100000
for unsupported in [Fraction(1, 10), Fraction(16777217)]:
    try:
        exact_bits(unsupported)
    except ValueError:
        pass
    else:
        raise AssertionError("Inexact arithmetic must fail closed")

GATES = {0xffff6530: 1, 0xffff6531: 0, 0xffff6567: 1,
         0xffff700e: 1, 0xffff6e2e: 0, 0xffff65f0: 1}
FUNCTIONS = [0x35034, 0x34cec, 0x3ae52, 0x3b4d4, 0x3ad04, 0x3ac14]


def setup(flags=4, mode=1):
    t, e = SH(TCU), SHExactFloat(ECU)
    # Invalidate byte4 to avoid the integer divider; the flag path is still
    # the complete normal sender. Word5 stays valid. No helper is mocked.
    t.write(0xffff92c6, 0x20, 1)
    for bit, addr in enumerate([0xffffa99b, 0xffffa5ae, 0xffff9454, 0xffff98a0]):
        t.write(addr, (flags >> bit) & 1, 1)
    t.run(0x18f10, mode)
    t.run(0x18f8c, mode)
    for i in range(8):
        e.write(0xffff6a40 + i, t.read(0xffff8efd + i, 1), 1)
    e.sr = 0xf0
    for addr, value in GATES.items():
        e.write(addr, value, 1)
    for addr in [0xffff734c, 0xffff6a5d, 0xffffa488]:
        e.write(addr, 1, 1)
    e.write(0xffff734a, 0x80, 1)
    # Choose the nonzero alternative command for each cylinder when uncut.
    # This bit selects a command; the independent inhibition bit is0x40.
    for i in range(1, 5):
        e.write(0xffff749e+i, 0x20, 1)
    # Four nonzero alternatives prevent zero-initialized RAM proving a cut.
    for addr, value in [(0xffff73fc, 8), (0xffff73f4, 4),
                        (0xffff73f8, 2), (0xffff7400, 1)]:
        e.write(addr, exact_bits(value), 4)
    return t, e


def update(e):
    for fn in FUNCTIONS:
        e.run(fn)


def selected_commands(e):
    # Execute each event class from the ROM cylinder table, so every cylinder
    # status is updated through the real phase-gated routine.
    for cylinder in range(1, 5):
        e.write(0xffff6df2, ECU[0x4f4f0 + 4*cylinder + 3], 1)
        e.run(0x4d716)
    e.run(0x44e50)
    return [int(exact_value(e.read(0xffff7408 + 4*i, 4))) for i in range(1, 5)]


examples = []
for flags in range(16):
    for condition in ("active", "MT", "config_off", "receipt_expired", "network_fault"):
        t, e = setup(flags)
        if condition == "MT":
            e.write(0xffff734a, 0x40, 1)
        elif condition == "config_off":
            e.write(0xffff734c, 0, 1)
        elif condition == "receipt_expired":
            e.run(0x34c66)  # actual receipt decrement 1 -> 0
            assert e.read(0xffff6a5d, 1) == 0
        elif condition == "network_fault":
            e.write(0xffff69e2, 1, 1)
        update(e)
        request = int(bool(flags & 4) and condition not in ("MT", "config_off"))
        assert [e.read(0xffff6e34+i, 1) for i in range(1, 5)] == [request]*4
        assert e.read(0xffff6a64, 1) == 0  # supported bit2 never sent here
        commands = selected_commands(e)
        assert commands == ([0]*4 if request else [1]*4)
        assert e.read(0xffff736a, 2) == (15 if request else 0)
        examples.append({"source_flags": flags, "condition": condition,
                         "payload": bytes(t.read(0xffff8efd+i, 1) for i in range(8)).hex(' '),
                         "cut_flags": [request]*4, "selected_commands": commands})

gate_examples = []
for addr, expected in GATES.items():
    _, e = setup()
    e.write(addr, 1-expected, 1)
    update(e)
    assert [e.read(0xffff6e34+i, 1) for i in range(1, 5)] == [0]*4
    assert selected_commands(e) == [1]*4
    gate_examples.append(hex(addr))

for mode in (0, 16):
    _, e = setup(mode=mode)
    update(e)
    assert selected_commands(e) == [1]*4
    assert int(exact_value(e.read(0xffff6a34, 4))) == (65022 if mode == 0 else 65537)

# A held request loads100 once, reaches zero on the100th subsequent call,
# and does not continuously reload. Drop/reassert is needed to reload it.
_, e = setup()
update(e)
assert (e.read(0xffff6e28, 1), e.read(0xffff6e29, 1)) == (100, 100)
for step in range(1, 102):
    e.run(0x3ad04)
    e.run(0x3ac14)
    remaining = max(100-step, 0)
    assert (e.read(0xffff6e28, 1), e.read(0xffff6e29, 1)) == (remaining, remaining)
    assert selected_commands(e) == ([0]*4 if remaining else [1]*4)
e.write(0xffff6a61, 0, 1)
e.run(0x3b4d4)
e.run(0x3ad04)
e.write(0xffff6a61, 1, 1)
e.run(0x3b4d4)
e.run(0x3ad04)
assert e.read(0xffff6e28, 1) == 100

# The local selector supports pairs independently; stock TCU bit5 requests
# both. These are ECU-local cases, not extra stock TCU payload capabilities.
pair_examples = []
for pair23, pair14 in [(0, 0), (1, 0), (0, 1), (1, 1)]:
    _, e = setup(flags=0)
    for addr, val in [(0xffff6e2c, pair23), (0xffff6e2d, pair14),
                      (0xffff6e28, 1), (0xffff6e29, 1)]:
        e.write(addr, val, 1)
    e.run(0x3ac14)
    flags = [e.read(0xffff6e34+i, 1) for i in range(1, 5)]
    assert flags == [pair14, pair23, pair23, pair14]
    assert selected_commands(e) == [0 if flag else 1 for flag in flags]
    pair_examples.append(flags)

print(json.dumps({"rom_sha256": {"ECU": hashlib.sha256(ECU).hexdigest(),
                                  "TCU": hashlib.sha256(TCU).hexdigest()},
                  "paired_flag_condition_cases": examples,
                  "gate_rejection_cases": gate_examples,
                  "inactive_tcu_modes": [0, 16],
                  "held_request_followup_calls_checked": 101,
                  "release_and_reassert_reload": 100,
                  "ecu_local_pair_selection_cases": pair_examples,
                  "scope": "Original function execution, exact finite FPU only, synthetic RAM and scheduling; endpoint FFFF740C..7418 command selection, not timer or injector hardware."}, indent=2))
