"""Execute PCM receipt qualification -> TCU diagnostic -> CAN216 -> ECU.

Synthetic RAM/ticks, unchanged ROMs, actual helpers. No transport hardware,
EEPROM durability, full task scheduler, lamp driver or mechanical fallback.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH
from sh_exact_float import SHExactFloat

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, addr, value, size=1):
    t.write(0xFFFF0000 + addr, value, size)


def r(t, addr, size=1):
    return t.read(0xFFFF0000 + addr, size)


def group(t, action, number=0x36):
    t.r[5] = number
    t.run(0x1A598, action)


def list_dtcs(t):
    count = t.run(0x558CC, 0xFFFFB000)
    return bytes(r(t, 0xB000+i) for i in range(count*3)).hex(" ")


def receive216(t, e):
    # Existing sender path: mark unrelated byte4 unavailable to avoid divider.
    # Flags remain valid; no helper/ROM instructions replaced.
    w(t, 0x92C6, 0x20)
    t.run(0x18F10, 1)
    t.run(0x18F8C, 1)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    for fn in [0x35034, 0x34CEC, 0x3B282, 0x775CA]:
        e.run(fn)
    e.r[5] = 0
    normalized = e.run(0x15146, 0xFFFF2184)
    e.r[5] = 0
    combined = e.run(0x15146, 0xFFFF24EE)
    return [r(t, 0x8F04) & 2, normalized, r(e, 0x6E53), combined]


def pid01(t):
    # Synthetic request context; execute the service handler and PID table.
    # 90B6=1 selects an admitted diagnostic protocol mode, not live transport.
    w(t, 0x90B6, 1)
    w(t, 0xB400, 0xFFFFB480, 4)
    w(t, 0xB404, 0xFFFFB500, 4)
    w(t, 0xB408, 1, 2)
    w(t, 0xB480, 1)
    assert t.run(0x54234, 0xFFFFB400) == 5
    return bytes(r(t, 0xB500+i) for i in range(5))


def pack420(e):
    # Execute just the original straight packing slice. Full3707A stops in
    # an inexact floating-point conversion at2F326, outside this harness.
    for pc in range(0x370A6, 0x370DE, 2):
        nxt, delay = e.instruction(pc)
        assert nxt == pc+2 and not delay
    return bytes(r(e, 0x6B80+i) for i in range(8))


# Qualification flags and diagnostic code in the actual group36 ROM record.
base = 0x5EB78 + 16*0x36
assert TCU[base] == 1 and TCU[base+7] == 0xC7
assert int.from_bytes(TCU[0x5EB60:0x5EB64], "big") == 0x56908
assert int.from_bytes(TCU[base+8:base+10], "big") == 0xC100
assert TCU[0x5F0E0:0x5F0E8] == bytes.fromhex("2100010013880001")

enabled = [0, 1, 3, 7, 8, 12, 13]
lifecycles = []
for missing, recovery_gate in itertools.product(enabled, [0, 1]):
    t, e = SH(TCU), SHExactFloat(ECU)
    t.run(0x5327C)
    w(t, 0x8464, 200, 2)
    for g in [0x36, 0x37, 0x38]:
        group(t, 0, g)
    w(t, 0xA939, 1)
    w(t, 0x868C, 1)
    w(t, 0x80A4, recovery_gate, 2)
    for addr, value in [(0x734A, 0x80), (0x734C, 1), (0x6A5D, 1), (0x6536, 1)]:
        w(e, addr, value)
    record = 0x5C610 + 28*missing
    duration = int.from_bytes(TCU[record+22:record+24], "big")
    failure, receipt = 100+duration, 101+duration
    clear_tick = receipt + 5000
    timeline = []
    for now in [100, failure-1, failure, receipt, clear_tick-1, clear_tick, clear_tick+1]:
        w(t, 0x84D0, now, 4)
        for index in enabled:
            if index != missing or now >= receipt:
                t.run(0x19DC0, index)
        group(t, 1)
        t.run(0x56908, 0x36)
        # Actual diagnostic task56F80 calls group processing before57F50.
        # Other diagnostic producers are deliberately not part of this test.
        t.run(0x57F50)
        t.run(0x570F6)
        active = now >= failure and (now <= clear_tick or recovery_gate != 0)
        remembered = now >= failure
        expected_flags = (4 if active else 0) | (0x80 if now > clear_tick and recovery_gate else 0)
        assert r(t, 0xA722) == expected_flags, (missing, recovery_gate, now, hex(r(t, 0xA722)))
        assert r(t, 0xA666) == active
        assert r(t, 0xA99B) == remembered
        encoded = list_dtcs(t)
        assert encoded == ("c1 00 ff" if remembered else "")
        wire_ecu = receive216(t, e)
        assert wire_ecu == [2*remembered, remembered, remembered, remembered]
        pid = pid01(t)
        assert pid == bytes([1, 0x81 if remembered else 0, 4, 0, 0])
        t.run(0x5329A)
        t.run(0x19414, 1)
        active_wire = r(t, 0x8EEE) & 0x40
        assert active_wire == 0x40*active
        e.run(0x7774A)
        e.run(0x371F0)
        lamp_wire = pack420(e)
        assert r(e, 0x91BE) == remembered
        assert lamp_wire[5] & 0x40 == 0x40*remembered
        timeline.append({"tick": now, "active_group_a722": r(t, 0xA722),
                         "aggregate_a666": r(t, 0xA666),
                         "stored_list": encoded, "tcu_a99b": r(t, 0xA99B),
                         "wire_and_ecu": wire_ecu,
                         "pid01_body": pid.hex(" "),
                         "can231_byte1_bit6": active_wire,
                         "ecu_can420_payload": lamp_wire.hex(" "),
                         "healthy_status_aa30": r(t, 0xAA30),
                         "healthy_group_aa78": r(t, 0xAA78)})
    lifecycles.append({"missing_id": hex(int.from_bytes(TCU[record:record+4], "big")),
                       "recovery_gate_80a4": recovery_gate, "timeline": timeline})

# Receiver mode/config gating and ECU aggregate inhibit, independently varied.
receiver_cases = 0
for bit, mt, enabled_config, inhibit, local_request in itertools.product(range(2), repeat=5):
    e = SHExactFloat(ECU)
    for addr, value in [(0x734A, 0x40 if mt else 0x80), (0x734C, enabled_config),
                        (0x6A5D, 1), (0x6A47, 2*bit), (0x9462, inhibit)]:
        w(e, addr, value)
    e.r[5] = local_request
    e.run(0x1529C, 0xFFFF24EC)
    for fn in [0x35034, 0x34CEC, 0x3B282, 0x775CA]:
        e.run(fn)
    accepted = bit and not mt and enabled_config
    assert r(e, 0x6E53) == accepted
    e.r[5] = 0
    assert e.run(0x15146, 0xFFFF24EE) == ((accepted or local_request) and not inhibit)
    receiver_cases += 1

# Startup latch and explicit diagnostic override affect the active aggregate.
startup_cases = 0
for ticks, active, override, forced in itertools.product([199, 200, 201], range(2), range(2), range(2)):
    t = SH(TCU)
    t.run(0x5327C)
    for addr, value in [(0xA666, active), (0xA668, override), (0xA667, forced)]:
        w(t, addr, value)
    w(t, 0x8464, ticks, 2)
    t.run(0x5329A)
    expected = 1 if ticks < 200 else (forced if override else active)
    assert r(t, 0xA665) == expected
    for mode in [0, 1, 16]:
        t.run(0x19414, mode)
        assert r(t, 0x8EEE) & 0x40 == (0x40*expected if mode == 1 else 0)
        startup_cases += 1

# Display gating and stock descriptor-controlled diagnostic override.
assert ECU[0xAD474] == 0xE0
assert int.from_bytes(ECU[0xAD478:0xAD47C], "big") == 0xFFFF960C
display_cases = 0
for request, inhibit, ready, mode, permit, forced, other in itertools.product(
        range(2), range(2), range(2), [0, 7, 3], range(2), range(2), range(2)):
    e = SHExactFloat(ECU)
    e.r[5] = request
    e.run(0x1529C, 0xFFFF24EE)
    for addr, value in [(0x91BD, inhibit), (0x6536, ready), (0x960C, mode),
                        (0x966C, 0x20 if permit else 0), (0x9638, forced), (0x693A, other)]:
        w(e, addr, value)
    e.run(0x7774A)
    selected = forced if mode == 7 and permit else (not inhibit and (request or not ready))
    assert r(e, 0x91BE) == selected
    e.run(0x371F0)
    payload = pack420(e)
    assert payload[5] == 0x80*inhibit + 0x40*selected
    assert payload[6] == 0x40*other
    display_cases += 1

print(json.dumps({"roms": {"TCU": hashlib.sha256(TCU).hexdigest(),
                           "ECU": hashlib.sha256(ECU).hexdigest()},
                  "paired_lifecycles": lifecycles,
                  "receiver_gate_cases": receiver_cases,
                  "startup_override_sender_cases": startup_cases,
                  "display_override_packing_cases": display_cases,
                  "limits": "RAM persistence only; synthetic protocol mode; PID body without transport header; CAN420 packing slice only; no bus/EEPROM/vehicle, cluster lamp driver or mechanical fallback simulation."}, indent=2))
