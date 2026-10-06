"""Execute TCU missing-selector countdown, qualification and selector recovery.

Synthetic constant inputs and explicit task schedule; original unchanged ROM
instructions throughout. No physical timing, ignition cycles, peripherals or
roof-controller execution. The diagnostic producer runs at listed checkpoints.
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


def report(t):
    count = t.run(0x558CC, 0xFFFFB000)
    return bytes(r(t, 0xB000+i) for i in range(3*count)).hex(" ")


def publish(t):
    for fn in [0x570F6, 0x21C1C, 0x22416]:
        t.run(fn)
    t.run(0x19414, 1)
    e = SH(ECU)
    w(e, 0x734A, 0x80)
    w(e, 0x734C, 1)
    for i in range(8):
        w(e, 0x6ABC+i, r(t, 0x8EED+i))
    for fn in [0x35BB8, 0x3585C, 0x411F0]:
        e.run(fn)
    return {"summary_a964": r(t, 0xA964), "flags_92cd": r(t, 0x92CD),
            "can231_byte0": r(t, 0x8EED), "ecu_combined_723a": r(e, 0x723A),
            "serialized_list": report(t), "report_a99b": r(t, 0xA99B)}


def initial():
    t = SH(TCU)
    t.run(0x5327C)
    t.run(0x5853C)
    w(t, 0xA938, 1)
    w(t, 0xA962, 1)
    w(t, 0x80BA, 300, 2)
    return t


# Assert the complete timer service's four ranges from ROM, not guessed RAM.
ranges = [int.from_bytes(TCU[a:a+4], "big") for a in range(0x76D24, 0x76D44, 4)]
assert ranges == [0xFFFF8410, 0xFFFF8411, 0xFFFF8414, 0xFFFF841C,
                  0xFFFF841C, 0xFFFF841D, 0xFFFF8420, 0xFFFF844E]
t = initial()
timeline = []
checkpoints = [0, 1999, 2000, 29999, 30000]
for calls in range(30001):
    if calls:
        t.run(0x11AEC)
    if calls not in checkpoints:
        continue
    # The tick and timer service have an explicit artificial 1:1 schedule here.
    # Their real hardware scheduling ratio is not established by this fixture.
    w(t, 0x84D0, calls, 4)
    t.run(0x58548)
    t.run(0x56908, 0x16)
    t.run(0x57F50)
    state = publish(t)
    expected = 0 if calls < 2000 else 2 if calls < 30000 else 4
    assert r(t, 0xA702) == expected
    assert state["can231_byte0"] == (0xFF if calls == 30000 else 0x10)
    assert state["ecu_combined_723a"] == 0
    assert state["serialized_list"] == "" and state["report_a99b"] == 0
    assert r(t, 0x843E, 2) == max(2000-calls, 0)
    assert r(t, 0x8440, 2) == (65535 if calls < 2000 else 30000-calls)
    timeline.append({"timer_service_calls": calls, "timers": [r(t, 0x843E, 2), r(t, 0x8440, 2)],
                     "raw_status": r(t, 0xA74C), "active_status": expected, **state})
assert r(t, 0x6188) == 0x16  # In internal list even before confirmed serialization.
assert r(t, 0x61D3+2*0x16) == 0x50
qualified = {0x16: t}

t = initial()
w(t, 0x88B4, 1)
w(t, 0x88B5, 1)
for now in [100, 2100, 4100, 6100, 8100, 10100]:
    w(t, 0x84D0, now, 4)
    t.run(0x58548)
    t.run(0x566E0, 0x15)
publish(t)
assert report(t) == "07 07 ff" and r(t, 0xA99B) == 1
qualified[0x15] = t

# Fresh copy of each actually qualified state for every recovery case.
recovery = []
for group, mask, extra_a, extra_b, gate in itertools.product(
        [0x15, 0x16], [1, 2, 4, 8], range(2), range(2), range(2)):
    t = SH(TCU)
    t.ram = qualified[group].ram.copy()
    for i in range(4):
        w(t, 0x88B4+i, (mask >> i) & 1)
    w(t, 0x88BA, extra_a)
    w(t, 0x88BC, extra_b)
    w(t, 0x80A4, gate, 2)
    recovered = mask == 8 and extra_a == extra_b == 0
    steps = []
    for now in [31000, 31001, 61001]:
        w(t, 0x84D0, now, 4)
        t.run(0x58548)
        t.run(0x566E0 if group == 0x15 else 0x56908, group)
        t.run(0x57F50)
        state = publish(t)
        expected_flags = 0 if recovered else 0x44 if group == 0x15 else 4
        assert r(t, 0xA6EC+group) == expected_flags
        assert state["summary_a964"] == (0x11 if recovered else 0x1C)
        assert state["can231_byte0"] == (0x14 if recovered else 0xFF)
        assert state["ecu_combined_723a"] == 0
        assert state["serialized_list"] == ("07 07 ff" if group == 0x15 else "")
        assert state["report_a99b"] == (group == 0x15)
        assert r(t, 0x843E, 2) == r(t, 0x8440, 2) == 65535
        steps.append({"tick": now, "group_flags": expected_flags, **state})
    recovery.append({"group": hex(group), "input_mask": mask,
                     "extra_88ba": extra_a, "extra_88bc": extra_b,
                     "gate_80a4": gate, "recovered": recovered, "steps": steps})

# Reporting gate: seed history bit20 explicitly, not an emulated drive cycle.
history_cases = []
for history in [0, 0x20]:
    t = initial()
    w(t, 0x61D3+2*0x16, history)
    w(t, 0x843E, 0, 2)
    w(t, 0x8440, 0, 2)
    t.run(0x58548)
    t.run(0x56908, 0x16)
    state = publish(t)
    assert state["serialized_list"] == ("07 08 ff" if history else "")
    assert state["report_a99b"] == bool(history)
    assert state["can231_byte0"] == 0xFF
    history_cases.append({"seeded_history": history, **state})

# A962 bit0 is the mapped no-active-fault indication for group13/code0722.
contributors = [g for g in range(0x49) if TCU[0x5EB86+16*g] == 10]
assert contributors == [0x13]
assert TCU[0x5EB80+16*0x13:0x5EB82+16*0x13] == bytes.fromhex("0722")
dependency_cases = []
for active in [0, 2, 4, 6]:
    t = initial()
    w(t, 0xA6EC+0x13, active)
    t.run(0x570F6)
    t.run(0x58548)
    summary = 1 if active == 0 else active | 8
    assert r(t, 0xA962) == summary
    assert r(t, 0xA74C) == (active == 0)
    assert r(t, 0x843E, 2) == (2000 if active == 0 else 65535)
    assert r(t, 0x8440, 2) == 65535
    dependency_cases.append({"group13_active": active, "summary_a962": summary,
                             "group16_raw_status": r(t, 0xA74C)})

print(json.dumps({"scope": __doc__.strip(), "timer_service_ranges": [hex(x) for x in ranges],
                  "timer_service_calls": 30000, "missing_input_timeline": timeline,
                  "recovery_cases": len(recovery), "recovery": recovery,
                  "history_gate_cases": history_cases,
                  "dependency_cases": dependency_cases,
                  "limits": "Physical units, MCU-to-selector wiring, actual ignition cycles/EEPROM persistence, global gates and PRHT receiver remain unverified."}, indent=2))
