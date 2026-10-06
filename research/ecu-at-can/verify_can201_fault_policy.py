"""TCU diagnostic aggregation and communication loss -> CAN201 fallback/cut policy.

Explicit synthetic task/tick schedule and admitted engine gates. Other frames
are recovered via original record helpers; no bus or complete scheduler model.
Active faults, recovery and stored history are tested separately.
"""
import itertools
import json

from sh_software_arithmetic import SHSoftwareArithmetic
from verify_can201_cut_loop import TCU, w, r, receive, engine_response


def group(t, action):
    t.r[5] = 0x36
    t.run(0x1A598, action)


def report(t):
    count = t.run(0x558CC, 0xFFFFB000)
    return bytes(r(t, 0xB000+i) for i in range(count*3)).hex(" ")


assert TCU[0x5FCC8:0x5FCCC] == bytes.fromhex("1f202400")
contributors = [g for g in range(0x49) if TCU[0x5EB86+16*g] in [0x1F, 0x20, 0x24]]
assert contributors == [0x35, 0x36, 0x3A]
assert [TCU[0x5EB80+16*g:0x5EB82+16*g].hex() for g in contributors] == ["c073", "c100", "0000"]

mapping_cases = 0
for number, active in itertools.product(range(0x49), [2, 4]):
    t = SHSoftwareArithmetic(TCU)
    w(t, 0xA6EC+number, active)
    for fn in [0x570F6, 0x57258, 0x21C1C]:
        t.run(fn)
    assert bool(r(t, 0xA98E) & 8) == (number in contributors)
    assert bool(r(t, 0x92C9) & 64) == (number in contributors)
    mapping_cases += 1

# Aggregate rebuilds active bits from2/4; stored history16 alone does not inhibit.
summary_cases = 0
for a, b, c in itertools.product([1, 3, 5, 7, 17, 19, 21, 23], repeat=3):
    t = SHSoftwareArithmetic(TCU)
    receive(t, 16000)
    for address, value in zip([0xA977, 0xA978, 0xA97C], [a, b, c]):
        w(t, address, value)
    expected = (a | b | c) & 0x16
    expected |= 8 if expected & 6 else 1
    for fn in [0x57258, 0x21C1C, 0x2055C, 0x24FA0]:
        t.run(fn)
    fault = bool(expected & 8)
    assert r(t, 0xA98E) == expected
    assert r(t, 0x80E8, 2) == (20480 if fault else 10240)
    assert r(t, 0xA4E4) == (4 if fault else 1)
    assert r(t, 0x9454) == (0 if fault else 1)
    engine_response(t)
    summary_cases += 1

enabled = [0, 1, 3, 7, 8, 12, 13]
lifecycles = []
for missing, recovery_gate in itertools.product(enabled, range(2)):
    t = SHSoftwareArithmetic(TCU)
    t.run(0x5327C)
    w(t, 0x8464, 200, 2)
    group(t, 0)
    w(t, 0xA939, 1)
    w(t, 0x868C, 1)
    w(t, 0x80A4, recovery_gate, 2)
    receive(t, 16000)
    record = 0x5C610+28*missing
    interval = int.from_bytes(TCU[record+8:record+10], "big")
    duration = int.from_bytes(TCU[record+22:record+24], "big")
    failure, recovery = 100+duration, 101+duration
    clear = recovery+5000
    w(t, 0x84D0, 100, 4)
    t.r[5] = 0
    t.run(0x19D44, missing)
    timeline = []
    for now in sorted(set([100, 100+interval, failure-1, failure, recovery, clear-1, clear, clear+1])):
        w(t, 0x84D0, now, 4)
        for index in enabled:
            if index != missing or now >= recovery:
                t.run(0x19DC0, index)
        if now < recovery:
            t.run(0x19E10, missing)
        if missing != 1 or now >= recovery:
            receive(t, 16000)
        group(t, 1)
        t.run(0x56908, 0x36)
        t.run(0x57F50)
        for fn in [0x570F6, 0x57258, 0x21C1C, 0x2055C, 0x24FA0]:
            t.run(fn)
        active = now >= failure and (now <= clear or recovery_gate != 0)
        stored = now >= failure
        assert bool(r(t, 0xA98E) & 8) == active
        assert bool(r(t, 0x92C9) & 64) == active
        assert r(t, 0x80E8, 2) == (20480 if active else 10240)
        assert r(t, 0x9454) == (0 if active else 1)
        assert report(t) == ("c1 00 ff" if stored else "")
        commands = engine_response(t)
        timeline.append({"tick": now, "expiry_bitmap": r(t, 0x8EE2, 2),
                         "active_group36": r(t, 0xA722), "aggregate_a98e": r(t, 0xA98E),
                         "substitution_flag": active, "scaled_value": r(t, 0x80E8, 2),
                         "cut_request": r(t, 0x9454), "ecu_commands": commands,
                         "stored_report": report(t)})
    lifecycles.append({"missing_id": hex(int.from_bytes(TCU[record:record+4], "big")),
                       "healthy_recovery_gate_80a4": recovery_gate, "qualification_ticks": duration,
                       "timeline": timeline})

print(json.dumps({"scope": __doc__.strip(), "group_mapping_cases": mapping_cases,
                  "contributing_groups": [hex(g) for g in contributors],
                  "summary_and_paired_control_cases": summary_cases,
                  "loss_recovery_lifecycles": lifecycles,
                  "limits": "Tick units and full scheduler unknown; physical causes of groups35 and3A not established. No actuator timers or vehicle tests."}, indent=2))
