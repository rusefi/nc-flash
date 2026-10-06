"""Execute CAN201 invalid-word qualification, substitution, cut and recovery.

Original unmodified TCU/ECU instructions; explicit task/tick order and admitted
engine fixture. The CAN201 callback receives explicit payloads, with no CAN
peripheral, complete scheduler, actuator or physical-time simulation.
"""
import itertools
import json

from sh_software_arithmetic import SHSoftwareArithmetic
from verify_can201_cut_loop import TCU, ECU, w, r, receive, engine_response
from sh_rtz_float import SHNormalRTZFloat
from sh_exact_float import exact_bits


def initial(raw=16000, recovery_gate=0):
    t = SHSoftwareArithmetic(TCU)
    t.run(0x5327C)
    for address, value, size in [(0xA936, 1, 1), (0xA939, 1, 1), (0x8464, 200, 2),
                                  (0x868C, 1, 1), (0x80A4, recovery_gate, 2)]:
        w(t, address, value, size)
    receive(t, raw)
    return t


def step(t, tick, raw, payload=None):
    w(t, 0x84D0, tick, 4)
    if payload is None:
        receive(t, raw)
    else:
        assert len(payload) == 8 and int.from_bytes(payload[:2], "big") == raw
        # The ECU publishes8 bytes; the TCU receiver's configured copy length
        # is7 (5C8E4 table). Do not overwrite the neighbouring buffer byte.
        for i, value in enumerate(payload[:7]):
            w(t, 0x8F39+i, value)
        t.run(0x1ACD8)
        t.run(0x2055C)
    t.run(0x583DC)
    t.run(0x56658)
    t.run(0x57F50)
    for fn in [0x570F6, 0x57258, 0x21C1C, 0x2055C, 0x24FA0]:
        t.run(fn)
    commands = engine_response(t)
    count = t.run(0x558CC, 0xFFFFB000)
    t.run(0x5329A)
    t.run(0x19414, 1)
    result = {"tick": tick, "can201_word0": raw, "validity": r(t, 0x8816),
              "held_word": r(t, 0x8814, 2), "raw_group3a": r(t, 0xA770),
              "active_group3a": r(t, 0xA726), "deadline": r(t, 0xA868, 4),
              "qualification_count": r(t, 0xA918, 2),
              "mapped_summary": r(t, 0xA97C), "aggregate": r(t, 0xA98E),
              "scaled_value": r(t, 0x80E8, 2), "application_status": r(t, 0xA4E4),
              "cut_request": r(t, 0x9454), "ecu_commands": commands,
              "can216_report_bit": r(t, 0x8F04) & 2,
              "can231_active_bit": r(t, 0x8EEE) & 0x40,
              "stored_report": bytes(r(t, 0xB000+i) for i in range(count*3)).hex(" ")}
    assert not result["stored_report"]
    assert result["can216_report_bit"] == result["can231_active_bit"] == 0
    return result


def main():
    record = TCU[0x5EB78+16*0x3A:0x5EB88+16*0x3A]
    assert record.hex() == "000101f4000111000000000027002400"
    mappings = [(0x8816, 0x3A), (0xAC7A, 0x3B), (0x880A, 0x3C),
                (0x880E, 0x3D), (0x8812, 0x3E)]
    assert [(int.from_bytes(TCU[a:a+4], "big") & 65535, TCU[a+4])
            for a in range(0x5F198, 0x5F1C0, 8)] == mappings

    producer_cases = 0
    for validity, admitted, fault35, fault36 in itertools.product(
            range(256), range(2), range(2), range(2)):
        t = initial()
        w(t, 0x8816, validity)
        w(t, 0xA939, admitted)
        w(t, 0xA977, fault35*8)
        w(t, 0xA978, fault36*8)
        t.run(0x583DC)
        enabled = admitted and not fault35 and not fault36
        expected = (3 if validity == 1 else 1) if enabled else 0
        assert r(t, 0xA770) == expected
        producer_cases += 1

    # The original helper builds the second record's input from two validities.
    aggregate_cases = 0
    for a, b in itertools.product([0, 1, 2, 3, 255], repeat=2):
        t = initial()
        w(t, 0x88EE, a)
        w(t, 0x88EA, b)
        t.run(0x58504)
        assert r(t, 0xAC7A) == (1 if 1 in [a, b] else 2 if a == b == 2 else 3)
        aggregate_cases += 1

    lifecycles = []
    for old_raw, recovery_gate in itertools.product([0, 16000, 65534], range(2)):
        t = initial(old_raw, recovery_gate)
        timeline = []
        for tick, raw in [(0, old_raw), (100, 65535), (599, 65535), (600, 65535),
                          (601, 16000), (602, 16000), (1101, 16000),
                          (1102, 16000), (1103, 16000)]:
            d = step(t, tick, raw)
            active = tick >= 600 and (tick <= 1101 or recovery_gate != 0)
            held = old_raw//4 if tick < 601 else 4000
            assert d["held_word"] == held
            assert bool(d["aggregate"] & 8) == active
            assert d["scaled_value"] == (20480 if active else min(32767, held*256//100))
            assert d["application_status"] == (4 if active else 2 if raw == 65535 else 1)
            assert d["cut_request"] == (0 if active or held < 4000 else 1)
            assert bool(d["mapped_summary"] & 16) == (tick >= 600)
            timeline.append(d)
        lifecycles.append({"initial_raw": old_raw, "healthy_recovery_gate": recovery_gate,
                           "timeline": timeline})

    # A valid callback just before the deadline cancels qualification; the next
    # invalid interval starts a fresh500-tick deadline, not the old one.
    t = initial()
    interrupted = []
    for tick, raw in [(0, 16000), (100, 65535), (598, 65535), (599, 16000),
                      (600, 65535), (1099, 65535), (1100, 65535)]:
        d = step(t, tick, raw)
        assert bool(d["aggregate"] & 8) == (tick == 1100)
        if tick >= 600:
            assert d["deadline"] == 1100
        interrupted.append(d)

    gate_interruptions = []
    for gate in [0xA977, 0xA978]:
        t = initial()
        rows = []
        for tick, dependency in [(100, 0), (599, 8), (600, 0), (1099, 0), (1100, 0)]:
            w(t, 0x84D0, tick, 4)
            receive(t, 65535)
            w(t, gate, dependency)
            t.run(0x583DC)
            t.run(0x566E0, 0x3A)
            assert bool(r(t, 0xA726) & 4) == (tick == 1100)
            assert r(t, 0xA770) == (0 if dependency else 3)
            if tick >= 600:
                assert r(t, 0xA868, 4) == 1100
            rows.append({"tick": tick, "dependency": dependency,
                         "raw": r(t, 0xA770), "active": r(t, 0xA726),
                         "deadline": r(t, 0xA868, 4)})
        gate_interruptions.append({"summary_gate": hex(gate), "timeline": rows})

    diagnostic_gate_cases = []
    for gate in [0, 1, 2]:
        t = initial()
        w(t, 0xA936, gate)
        rows = [step(t, tick, 65535) for tick in [100, 599, 600]]
        assert bool(rows[-1]["aggregate"] & 8) == (gate == 1)
        diagnostic_gate_cases.append({"processing_gate_a936": gate, "timeline": rows})

    recovery_interruptions = []
    for recovery_gate in range(2):
        t = initial(recovery_gate=recovery_gate)
        rows = []
        for tick, raw in [(0, 16000), (100, 65535), (600, 65535), (601, 16000),
                          (1100, 65535), (1101, 16000), (1601, 16000), (1602, 16000)]:
            d = step(t, tick, raw)
            assert bool(d["aggregate"] & 8) == (tick >= 600 and (tick <= 1601 or recovery_gate))
            rows.append(d)
        recovery_interruptions.append({"healthy_recovery_gate": recovery_gate, "timeline": rows})

    # Corrected boundary: healthy index27 has a500-tick interval. The next
    # producer pass can consume readiness without advancing the tick counter.
    assert TCU[0x5F110:0x5F118].hex() == "2700010001f40001"
    t = initial()
    same_tick_recovery = [step(t, tick, 65535 if tick in [100, 600] else 16000)
                          for tick in [0, 100, 600, 601, 1100, 1101, 1101]]
    assert [d["active_group3a"] for d in same_tick_recovery] == [0, 1, 5, 68, 68, 68, 0]

    # Full ECU publisher -> TCU callback/diagnosis -> CAN216 -> ECU command path.
    t = initial()
    round_trip = []
    for tick, source, invalid in [(0, 4000, 0), (100, 0, 1), (599, 0, 1),
                                  (600, 0, 1), (601, 4500, 0),
                                  (1101, 4500, 0), (1102, 4500, 0)]:
        e = SHNormalRTZFloat(ECU)
        w(e, 0x6DB4, exact_bits(source), 4)
        w(e, 0x734A, 0x80)
        w(e, 0x6B4F, invalid)
        for fn in [0x3663E, 0x366EC, 0x365D0]:
            e.run(fn)
        payload = bytes(r(e, 0x6B2C+i) for i in range(8))
        raw = int.from_bytes(payload[:2], "big")
        assert raw == (65535 if invalid else source*4)
        d = step(t, tick, raw, payload)
        active = 600 <= tick <= 1101
        assert bool(d["aggregate"] & 8) == active
        assert d["scaled_value"] == (20480 if active else 10240 if tick < 601 else 11520)
        assert d["cut_request"] == (0 if active else 1)
        round_trip.append({"ecu_source": source, "ecu_invalid_6b4f": invalid,
                           "can201_payload": payload.hex(" "), **d})

    print(json.dumps({"scope": __doc__.strip(), "record3a": record.hex(" "),
                      "producer_cases": producer_cases, "aggregate_helper_cases": aggregate_cases,
                      "lifecycles": lifecycles, "interrupted_qualification": interrupted,
                      "dependency_gate_interruptions": gate_interruptions,
                      "diagnostic_processing_gate_cases": diagnostic_gate_cases,
                      "interrupted_recovery": recovery_interruptions,
                      "same_tick_recovery": same_tick_recovery,
                      "ecu_tcu_ecu_lifecycle": round_trip,
                      "limits": "Explicit scheduling and tick values; no physical timing/actuators. ECU command fixture restarts each checkpoint. CAN201byte6 downstream control, traction arbitration and roof internals remain open."}, indent=2))


if __name__ == "__main__":
    main()
