"""Original ECU CAN201 byte6 publication, TCU scaling/history and fault policy.

Explicit source, timer and scheduling fixtures. Physical source identities,
absolute tick duration and complete transmission actuator logic are unproved.
"""
from fractions import Fraction
import itertools
import json
import random

from verify_can201_cut_loop import ECU, TCU, w, r, engine_response
from sh_rtz_float import SHNormalRTZFloat
from sh_exact_float import exact_bits
from sh_software_arithmetic import SHSoftwareArithmetic as SH


def ecu_payload(source, alternate, invalid):
    e = SHNormalRTZFloat(ECU)
    for a, value in [(0x6CF8, source), (0x6718, alternate), (0x6DB4, 4000)]:
        w(e, a, exact_bits(value), 4)
    w(e, 0xA3A4, invalid)
    w(e, 0x734A, 0x80)
    for fn in [0x3663E, 0x366EC, 0x366D4, 0x368A2, 0x365D0]:
        e.run(fn)
    return bytes(r(e, 0x6B2C+i) for i in range(8))


def receive(t, payload):
    for i, value in enumerate(payload[:7]):
        w(t, 0x8F39+i, value)
    t.run(0x1ACD8)


def expected_history(value, old, history, flags, timer):
    updated = [old, *history[:3]]
    short, long = value-old, value-history[2]
    if abs(short) >= 15360:
        timer = 0
        if abs(long) >= 2560:
            flags |= 1
    if abs(long) < 2560 and timer >= 6:
        flags &= ~1
    return updated, flags, timer, 0 if flags & 1 else long


def main():
    encoder_cases = 0
    values = [Fraction(x, 16) for x in [-16, 0, 3, 4, 5, 8, 16, 639, 640, 1599, 1600, 1604, 1920, 2040]]
    quantize = lambda x: max(0, min(255, (2*x+Fraction(1, 2)).numerator//(2*x+Fraction(1, 2)).denominator))
    for source, alternate, invalid in itertools.product(values, values, range(2)):
        payload = ecu_payload(source, alternate, invalid)
        primary = quantize(source)
        expected = 255 if invalid else min(200, quantize(max(Fraction(primary, 2), alternate)))
        assert payload[6] == expected and int.from_bytes(payload[:2], "big") == 16000
        t = SH(TCU)
        w(t, 0x8808, 500, 2)
        receive(t, payload)
        t.run(0x21500)
        held = 500 if expected == 255 else expected*5
        assert r(t, 0x8808, 2) == held
        assert r(t, 0x8098, 2) == min(25600, held*256//10)
        assert r(t, 0xA4D4, 2) == min(1000, held)
        assert r(t, 0xA4D6) == (2 if expected == 255 else 1)
        encoder_cases += 1

    numeric_cases = 0
    for raw, old, fault in itertools.product(range(256), [0, 500, 1000], [0, 8]):
        t = SH(TCU)
        w(t, 0x8808, old, 2)
        receive(t, bytes.fromhex("3e8000000000")+bytes([raw, 0]))
        w(t, 0x92D5, fault)
        t.run(0x21500)
        held = old if raw == 255 else raw*5
        value = 0 if fault else min(25600, held*256//10)
        assert r(t, 0x8098, 2) == value
        assert r(t, 0xA4D4, 2) == value*10//256
        assert r(t, 0xA4D6) == (4 if fault else 2 if raw == 255 else 1)
        numeric_cases += 1

    mapping_cases = 0
    for group, active in itertools.product(range(0x49), [2, 4]):
        t = SH(TCU)
        w(t, 0xA6EC+group, active)
        for fn in [0x570F6, 0x57258, 0x21C1C]:
            t.run(fn)
        assert bool(r(t, 0x92D5) & 8) == (group in [0x35, 0x36, 0x3C, 0x3D])
        mapping_cases += 1

    aggregate_cases = 0
    for address, value in itertools.product([0xA98C, 0xA98D, 0xA98E, 0xA98F], range(256)):
        t = SH(TCU)
        w(t, address, value)
        t.run(0x21C1C)
        expected = address in [0xA98D, 0xA98F] and bool(value & 8)
        assert bool(r(t, 0x92D5) & 8) == expected
        assert bool(r(t, 0x92D5) & 128) == expected
        aggregate_cases += 1

    history_cases = 0
    rng = random.Random(2016)
    candidates = [0, 128, 2559, 2560, 15359, 15360, 25600]
    for _ in range(600):
        t = SH(TCU)
        raw = rng.randrange(255)
        value = min(25600, raw*128)
        old = rng.choice(candidates)
        history = [rng.choice(candidates) for i in range(4)]
        flags, timer = rng.choice([0, 1, 0xA4, 0xA5]), rng.choice([0, 5, 6, 255])
        w(t, 0x8808, raw*5, 2)
        w(t, 0x8098, old, 2)
        for i, sample in enumerate(history):
            w(t, 0x92BA+2*i, sample, 2)
        w(t, 0x92C2, flags)
        w(t, 0x8197, timer)
        updated, flags, timer, delta = expected_history(value, old, history, flags, timer)
        t.run(0x21500)
        assert [r(t, 0x92BA+2*i, 2) for i in range(4)] == updated
        assert r(t, 0x92C2) == flags and r(t, 0x8197) == timer
        assert r(t, 0x92B8, 2) == delta & 65535
        history_cases += 1

    timer_cases = 0
    for before in [0, 1, 5, 6, 254, 255]:
        t = SH(TCU)
        w(t, 0x8197, before)
        t.run(0x110B4)
        assert r(t, 0x8197) == min(255, before+1)
        timer_cases += 1
    t = SH(TCU)
    w(t, 0x8808, 1000, 2)
    t.run(0x21500)
    assert r(t, 0x92C2) & 1 and r(t, 0x8197) == 0
    jump_recovery = []
    for call in range(1, 7):
        t.run(0x110B4)
        t.run(0x21500)
        assert bool(r(t, 0x92C2) & 1) == (call < 6)
        jump_recovery.append({"timer_service_calls": call, "timer": r(t, 0x8197),
                              "jump_latch": r(t, 0x92C2), "change": r(t, 0x92B8, 2)})

    downstream_cases = 0
    assert TCU[0x77334:0x77337] == bytes(3)
    for delta, flag, valid, requested, timer in itertools.product(
            [-1, 0, 1], range(2), [1, 255], [0, 3, 6], [0, 1, 255]):
        t = SH(TCU)
        for a, v, size in [(0x92B8, delta, 2), (0x92D5, flag*32, 1),
                           (0x8080, valid, 1), (0x9B3C, 3, 1),
                           (0x82C5, timer, 1), (0xB600, requested, 1), (0xB601, 9, 1)]:
            w(t, a, v, size)
        t.r[5] = 0xFFFFB601
        t.run(0x46CC8, 0xFFFFB600)
        override = delta < 0 and flag and valid != 255 and requested < 3
        assert r(t, 0xB600) == (3 if override else requested)
        assert r(t, 0xB601) == (255 if override else 9)
        assert r(t, 0x82C5) == (0 if flag else timer)
        downstream_cases += 1

    paired_selection = []
    for source, flag in itertools.product([45, 55], range(2)):
        t = SH(TCU)
        for _ in range(5):
            receive(t, ecu_payload(50, 0, 0))
            t.run(0x21500)
        receive(t, ecu_payload(source, 0, 0))
        t.run(0x21500)
        delta = (source-50)*256
        assert r(t, 0x92B8, 2) == delta & 65535
        for a, value in [(0x92D5, flag*32), (0x8080, 1), (0x9B3C, 3),
                         (0xB600, 0), (0xB601, 9)]:
            w(t, a, value)
        t.r[5] = 0xFFFFB601
        t.run(0x46CC8, 0xFFFFB600)
        assert r(t, 0xB600) == (3 if delta < 0 and flag else 0)
        paired_selection.append({"ecu_source": source, "change": delta,
                                 "injected_flag20": flag, "selection": r(t, 0xB600)})

    assert TCU[0x5F118:0x5F120].hex() == "2800010001f40001"
    lifecycles = []
    for recovery_gate in range(2):
        t = SH(TCU)
        t.run(0x5327C)
        for a, value, size in [(0xA936, 1, 1), (0xA939, 1, 1), (0x8464, 200, 2),
                               (0x868C, 1, 1), (0x80A4, recovery_gate, 2)]:
            w(t, a, value, size)
        rows = []
        for index, (tick, invalid, source) in enumerate([(0, 0, 50), (100, 1, 0), (599, 1, 0),
                                      (600, 1, 0), (601, 0, 45),
                                      (1100, 0, 45), (1101, 0, 45), (1101, 0, 45)]):
            w(t, 0x84D0, tick, 4)
            payload = ecu_payload(source, 0, invalid)
            receive(t, payload)
            for fn in [0x583DC, 0x56658, 0x57F50, 0x570F6, 0x57258, 0x21C1C,
                       0x21500, 0x2055C, 0x24FA0]:
                t.run(fn)
            active = tick >= 600 and (index < 7 or recovery_gate)
            assert bool(r(t, 0x92D5) & 8) == active
            assert r(t, 0x8098, 2) == (0 if active else 12800 if tick < 601 else 11520)
            assert r(t, 0xA4D6) == (4 if active else 2 if invalid else 1)
            assert r(t, 0x80E8, 2) == 10240 and r(t, 0x9454) == 1
            commands = engine_response(t)
            assert commands == [0]*4
            count = t.run(0x558CC, 0xFFFFB000)
            assert count == 0
            rows.append({"tick": tick, "ecu_payload": payload.hex(" "),
                         "held_value": r(t, 0x8808, 2), "validity": r(t, 0x880A),
                         "active_group3c": r(t, 0xA728), "aggregate_a98d": r(t, 0xA98D),
                         "scaled_8098": r(t, 0x8098, 2), "status_a4d6": r(t, 0xA4D6),
                         "history_change": r(t, 0x92B8, 2), "cut_request": r(t, 0x9454),
                         "ecu_commands": commands, "serialized_dtc_count": count})
        lifecycles.append({"healthy_recovery_gate": recovery_gate, "timeline": rows})

    print(json.dumps({"scope": __doc__.strip(), "ecu_tcu_encoder_cases": encoder_cases,
                      "raw_conversion_cases": numeric_cases, "fault_mapping_cases": mapping_cases,
                      "aggregate_flag_cases": aggregate_cases, "paired_selection": paired_selection,
                      "history_cases": history_cases, "timer_cases": timer_cases,
                      "jump_recovery": jump_recovery, "downstream_selection_cases": downstream_cases,
                      "ecu_tcu_fault_lifecycles": lifecycles,
                      "limits": "Source physical identities and units unproved.46CC8 pointer/state fixtures establish a selection rule, not mechanical gear changes. Timer service/task order explicit; no vehicle or actuator tests."}, indent=2))


if __name__ == "__main__":
    main()
