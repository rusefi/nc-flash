"""Execute group13/P0722 producer, capture counters, diagnosis and CAN propagation.

Synthetic admitted inputs and explicit call order; original ROM instructions.
Capture handlers receive counter arguments without emulating peripheral edges.
No physical time/pulse calibration, DSC or PRHT receiver is established.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_integer_arithmetic import SHIntegerArithmetic
from sh_rtz_float import SHNormalRTZFloat

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, a, v, size=1):
    t.write(0xFFFF0000+a, v, size)


def r(t, a, size=1):
    return t.read(0xFFFF0000+a, size)


def initial():
    t = SHIntegerArithmetic(TCU)
    t.run(0x5327C)
    for a in [0xA936, 0xA938, 0xA959, 0xA95A, 0xA95B, 0xA95C,
              0xA95D, 0xA95E, 0xA960, 0xA961, 0xA962, 0xA963,
              0xA964, 0xA97D, 0x88B7]:
        w(t, a, 1)
    w(t, 0xA4F8, 300, 2)
    return t


def paired(t):
    for fn in [0x58AA8, 0x56658, 0x570F6, 0x21C1C]:
        t.run(fn)
    t.run(0x18F8C, 1)
    e = SHNormalRTZFloat(ECU)
    for a, v in [(0x734A, 0x80), (0x734C, 1), (0x6A5D, 1), (0x7353, 1)]:
        w(e, a, v)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    # Healthy, identical decoded CAN4B0 source fixtures; test independent AT fault.
    for a in [0x6AF8, 0x6AFA]:
        w(e, a, 12345, 2)
    for fn in [0x35034, 0x34CEC, 0x3B7CE, 0x3A05E, 0x3679C, 0x365D0]:
        e.run(fn)
    count = t.run(0x558CC, 0xFFFFB000)
    return {"capture_counter_8900": r(t, 0x8900, 2),
            "raw_group13": r(t, 0xA749), "active_group13": r(t, 0xA6FF),
            "summary_a962": r(t, 0xA962), "flags_92c6": r(t, 0x92C6),
            "limiter_initialized": r(t, 0x8AE7), "can216_word5": r(t, 0x8F02, 2),
            "can201_with_healthy_4b0": r(e, 0x6B30, 2),
            "stored_report": bytes(r(t, 0xB000+i) for i in range(3*count)).hex(" ")}


assert TCU[0x5ECA8:0x5ECB8].hex() == "0100000001f411c7072200000a000a00"
assert int.from_bytes(TCU[0x5EB60:0x5EB64], "big") == 0x56908

# One-hot search of the full mapped diagnostic summary, with original publisher.
contributors = []
for a, bit in itertools.product(range(0xA958, 0xA998), range(8)):
    t = SHIntegerArithmetic(TCU)
    w(t, a, 1 << bit)
    t.run(0x21C1C)
    if r(t, 0x92C6) & 4:
        contributors.append([hex(a), bit])
assert contributors == [["0xa962", 2]]

selector_addresses = [0x88B4, 0x88B5, 0x88B6, 0x88B7, 0x88BA, 0x88BB, 0x88BC]
for mask in range(128):
    t = initial()
    for i, a in enumerate(selector_addresses):
        w(t, a, (mask >> i) & 1)
    assert t.run(0x58808) == (mask in [8, 16, 32, 64])
diagnostic_addresses = [0xA959, 0xA95A, 0xA95B, 0xA95C, 0xA95D, 0xA95E, 0xA960, 0xA961]
for mask in range(256):
    t = initial()
    for i, a in enumerate(diagnostic_addresses):
        w(t, a, (mask >> i) & 1)
    assert t.run(0x5885E) == (mask == 255)

gates = [(0xA938, 0, 1), (0xA735, 1, 1), (0x8420, 1, 2),
         (0xA964, 0, 1), (0xA97D, 0, 1), (0xA963, 0, 1),
         (0xA4F8, 299, 2), (0x88B7, 0, 1)]
gates += [(a, 0, 1) for a in diagnostic_addresses]
gates += [(a, 1, 1) for a in range(0xA5BC, 0xA5C0)]
for a, v, size in gates:
    t = initial()
    w(t, 0x8900, 6001, 2)
    w(t, a, v, size)
    t.run(0x58AA8)
    assert r(t, 0xA749) == r(t, 0x8900, 2) == 0

boundaries = []
for count in [0, 1, 11, 12, 13, 5999, 6000, 6001, 65535]:
    t = initial()
    w(t, 0x8900, count, 2)
    t.run(0x58AA8)
    expected = 1 if count <= 12 else 3 if count <= 6000 else 7
    assert r(t, 0xA749) == expected
    assert r(t, 0x8900, 2) == count
    boundaries.append({"counter": count, "raw": expected})

capture_cases = 0
for fn, increments, clears in [(0x17A58, [0x8900, 0x8902, 0x8904], 0x88F0),
                               (0x179A8, [0x88F0, 0x88F2, 0x88F4], 0x8900)]:
    for seed in [0, 1, 65534, 65535]:
        t = initial()
        for a in increments:
            w(t, a, seed, 2)
        w(t, clears, 555, 2)
        t.run(fn, 10000)
        assert [r(t, a, 2) for a in increments] == [min(seed+1, 65535)]*3
        assert r(t, clears, 2) == 0
        capture_cases += 1

recovery_cases = 0
for speed, count, healthy, other in itertools.product([0, 1, 65535], [0, 11, 12, 13], range(2), range(2)):
    t = initial()
    w(t, 0xA962, 0x1C)
    w(t, 0x80B6, speed, 2)
    w(t, 0x8900, count, 2)
    w(t, 0xA963, healthy)
    w(t, 0x80B8, other, 2)
    eligible = speed > 0 and count < 12 and healthy == 1
    assert t.run(0x58C42) == eligible
    t.run(0x58AA8)
    assert bool(r(t, 0xA749) & 0x80) == (eligible and other == 0)
    recovery_cases += 1

t = initial()
w(t, 0xA5AC, 10000, 2)
timeline = []
for count in range(6002):
    if count:
        t.run(0x17A58, count*10000)
    if count not in [0, 12, 13, 6000, 6001]:
        continue
    state = paired(t)
    active = 0 if count <= 12 else 2 if count <= 6000 else 4
    assert state["active_group13"] == active
    assert state["can216_word5"] == (65535 if count == 6001 else 20000)
    assert state["can201_with_healthy_4b0"] == (65535 if count == 6001 else 12345)
    assert state["stored_report"] == ("07 22 ff" if count == 6001 else "")
    timeline.append({"capture_handler_calls": count, **state})

t.run(0x179A8, 10000)
w(t, 0x80B6, 1, 2)
w(t, 0x80B8, 0, 2)
w(t, 0xA5AC, 30000, 2)
state = paired(t)
assert (state["raw_group13"], state["active_group13"], state["summary_a962"]) == (0x81, 0, 0x11)
assert state["can216_word5"] == 40000 and state["can201_with_healthy_4b0"] == 12345
assert state["stored_report"] == "07 22 ff"
timeline.append({"recovery_capture_179a8": True, **state})

print(json.dumps({"scope": __doc__.strip(), "one_hot_mapping_cases": 512,
                  "speed_fault_contributors": contributors,
                  "selector_helper_cases": 128, "diagnostic_helper_cases": 256,
                  "gate_rejections": len(gates), "counter_boundaries": boundaries,
                  "capture_saturation_cases": capture_cases, "recovery_gate_cases": recovery_cases,
                  "capture_handler_calls": 6001, "paired_timeline": timeline,
                  "limitations": "Explicit synthetic schedule; no real timing, physical pin identity, PRHT reception or actuator response."}, indent=2))
