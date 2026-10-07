"""Original ECU CAN201 source -> TCU conversion/cut request -> ECU cylinder commands.

Synthetic source and gate fixtures, explicit call schedule, no peripheral or
physical-time model. Original lookup interpolation and software arithmetic
execute using the independently tested extended integer instruction harness.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path

from sh_software_arithmetic import SHSoftwareArithmetic as SHIntegerArithmetic
from verify_software_lookup import expected_curve
from sh_subset import signed
from sh_rtz_float import SHNormalRTZFloat
from sh_exact_float import exact_bits, exact_value

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, a, v, size=1):
    t.write(0xFFFF0000+a, v, size)


def r(t, a, size=1):
    return t.read(0xFFFF0000+a, size)


def receive(t, raw):
    w(t, 0x8F39, raw, 2)
    t.run(0x1ACD8)
    t.run(0x2055C)


def engine_response(t):
    t.run(0x18F8C, 1)
    e = SHNormalRTZFloat(ECU)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    for a, v in {0x734A: 0x80, 0x734C: 1, 0x6A5D: 1, 0xA488: 1,
                 0x6530: 1, 0x6531: 0, 0x6567: 1, 0x700E: 1,
                 0x6E2E: 0, 0x65F0: 1}.items():
        w(e, a, v)
    for i in range(1, 5):
        w(e, 0x749E+i, 0x20)
    for a, v in [(0x73FC, 8), (0x73F4, 4), (0x73F8, 2), (0x7400, 1)]:
        w(e, a, exact_bits(v), 4)
    for fn in [0x35034, 0x34CEC, 0x3AE52, 0x3B4D4, 0x3AD04, 0x3AC14]:
        e.run(fn)
    for i in range(1, 5):
        w(e, 0x6DF2, ECU[0x4F4F0+4*i+3])
        e.run(0x4D716)
    e.run(0x44E50)
    commands = [int(exact_value(r(e, 0x7408+4*i, 4))) for i in range(1, 5)]
    assert commands == ([0]*4 if r(t, 0x9454) else [1]*4)
    return commands


def reference(t):
    # State equations derived from control branches, independent of the SH runner.
    selector_a = bool(r(t, 0x9317) & 4)
    selector_b = bool(r(t, 0x9316) & 4)
    flag = bool(r(t, 0x94F4) & 1)
    history = r(t, 0x9455)
    timers = [r(t, a) for a in [0x82A5, 0x82A6, 0x82A7]]
    for i, present in enumerate([selector_a, selector_b, flag]):
        if not present and history & (1 << i):
            timers[i] = 0
    a, b, c = timers
    phase = r(t, 0x828B)
    speed = r(t, 0x80E8, 2)
    threshold = expected_curve(r(t, 0x9334, 2))
    output = r(t, 0x9454)
    enabled = not (r(t, 0x92C9) & 64 or r(t, 0x9317) & 1 or r(t, 0x92C6) & 2)
    if enabled:
        if not (phase > 31 and c > 31) and speed >= threshold+1280:
            if (r(t, 0x800E) < 11 or a <= 31 or b <= 31) and not flag:
                output = 1
        if phase >= 61 and c >= 61 or r(t, 0x9317) & 8 or speed < threshold:
            output = 0
    else:
        output = 0
    history = (history & 0xF8) | selector_a | (selector_b << 1) | (flag << 2)
    return output, history, timers



def main():
    # Numeric receive -> application conversion; invalid raw holds old number.
    numeric_cases = 0
    for raw, old, fault in itertools.product(
            [0, 1, 3, 4, 399, 400, 13999, 14000, 15999, 16000, 51196, 51200, 65534, 65535],
            [0, 4000, 65535], range(2)):
        t = SHIntegerArithmetic(TCU)
        w(t, 0x8814, old, 2)
        w(t, 0x92C9, fault*64)
        receive(t, raw)
        number = old if raw == 65535 else raw//4
        scaled = 20480 if fault else min(32767, number*256//100)
        assert r(t, 0x8814, 2) == number
        assert r(t, 0x80E8, 2) == scaled and r(t, 0x809E, 2) == scaled*100//256
        assert r(t, 0xA4E4) == (4 if fault else 2 if raw == 65535 else 1)
        numeric_cases += 1

    # Independently decoded stock calibration; entire u16 curve tested separately.
    contributors = []
    for a, bit in itertools.product(range(0xA958, 0xA998), range(8)):
        t = SHIntegerArithmetic(TCU)
        w(t, a, 1 << bit)
        t.run(0x21C1C)
        if r(t, 0x92C9) & 64:
            contributors.append([hex(a), bit])
    assert contributors == [["0xa98e", 3]]

    assert TCU[0x703C0:0x703C9].hex() == "040a283c64231e1c1c"
    assert TCU[0x76EB8:0x76EBF].hex() == "1f3d05000b1f1f"
    assert int.from_bytes(TCU[0x76DDE:0x76DE0], "big") == 20480
    lookup_cases = 0
    for x in [0, 1, 1000, 2559, 25600, 30000, 65535]:
        t = SHIntegerArithmetic(TCU)
        t.r[5] = 0x703C0
        assert t.run(0x10764, x) == (8960 if x < 2560 else 7168)
        lookup_cases += 1

    axis_cases = []
    assert int.from_bytes(TCU[0x76DF4:0x76DF6], "big") == 10240
    for source, fault in itertools.product(
            [0, 1, 20, 60, 100, 215, 216, 255, 256, 511, 512, 32767, 32768, 65496, 65535], range(2)):
        t = SHIntegerArithmetic(TCU)
        w(t, 0x89A8, source, 2)
        w(t, 0x92C6, fault*64)
        t.run(0x22ECC)
        intermediate = 10240 if fault else (source*128) & 65535
        axis = ((signed(intermediate, 16)+5120)*2) & 65535
        assert r(t, 0x80F2, 2) == r(t, 0x9336, 2) == intermediate
        assert r(t, 0x9334, 2) == axis
        threshold = expected_curve(axis)
        t.r[5] = 0x703C0
        assert t.run(0x10764, axis) == threshold
        w(t, 0x80E8, threshold+1280, 2)
        t.run(0x24FA0)
        assert r(t, 0x9454) == 1
        engine_response(t)
        axis_cases.append({"source_89a8": source, "axis_fault": fault,
                           "axis_9334": axis, "clear_threshold": threshold})


    rng = random.Random(0x201216)
    control_cases = 0
    for i in range(800):
        t = SHIntegerArithmetic(TCU)
        # Include interior breakpoints and arbitrary u16 values.
        axis = rng.choice([0, 2559, 2560, 2561, 5000, 10239, 10240, 10241,
                           15359, 15360, 25600, 65535, rng.randrange(65536)])
        threshold = expected_curve(axis)
        w(t, 0x9334, axis, 2)
        w(t, 0x80E8, rng.choice([threshold-1, threshold, threshold+1279, threshold+1280, 20000]), 2)
        for a in [0x828B, 0x82A5, 0x82A6, 0x82A7]:
            w(t, a, rng.choice([0, 30, 31, 32, 60, 61, 62, 255]))
        for a, choices in [(0x9454, [0, 1]), (0x9455, [0, 1, 2, 4, 7, 0xA7]),
                           (0x9316, [0, 4]), (0x9317, [0, 0, 0, 1, 4, 8]),
                           (0x94F4, [0, 1]), (0x92C9, [0, 0, 0, 64]),
                           (0x92C6, [0, 0, 0, 2]), (0x800E, [0, 10, 11, 12, 255])]:
            w(t, a, rng.choice(choices))
        expected, history, timers = reference(t)
        t.run(0x24FA0)
        assert (r(t, 0x9454), r(t, 0x9455)) == (expected, history)
        assert [r(t, a) for a in [0x82A5, 0x82A6, 0x82A7]] == timers
        engine_response(t)
        control_cases += 1

    # ECU-originated round trip with persistent TCU hysteresis and explicit fault gates.
    t = SHIntegerArithmetic(TCU)
    timeline = []
    for value, invalid, fault, expected in [(3499, 0, 0, 0), (3500, 0, 0, 0),
            (3999, 0, 0, 0), (4000, 0, 0, 1), (3999, 0, 0, 1),
            (3500, 0, 0, 1), (3499, 0, 0, 0), (4000, 0, 0, 1),
            (0, 1, 0, 1), (0, 1, 1, 0), (4000, 0, 0, 1)]:
        e = SHNormalRTZFloat(ECU)
        w(e, 0x6DB4, exact_bits(value), 4)
        w(e, 0x734A, 0x80)
        w(e, 0x6B4F, invalid)
        for fn in [0x3663E, 0x366EC, 0x365D0]:
            e.run(fn)
        raw = r(e, 0x6B2C, 2)
        assert raw == (65535 if invalid else value*4)
        for i in range(7):
            w(t, 0x8F39+i, r(e, 0x6B2C+i))
        w(t, 0x92C9, fault*64)
        t.run(0x1ACD8)
        t.run(0x2055C)
        t.run(0x24FA0)
        assert r(t, 0x9454) == expected
        commands = engine_response(t)
        timeline.append({"ecu_source": value, "ecu_invalid": invalid, "tcu_fault": fault,
                         "can201_word0": raw, "received_validity": r(t, 0x8816),
                         "scaled_80e8": r(t, 0x80E8, 2), "application_status": r(t, 0xA4E4),
                         "cut_request": expected, "ecu_commands": commands})

    print(json.dumps({"scope": __doc__.strip(), "numeric_cases": numeric_cases,
                      "fault_publisher_one_hot_cases": 512, "fault_contributors": contributors,
                      "lookup_endpoint_cases": lookup_cases,
                      "axis_producer_cases": axis_cases,
                      "interpolation": "Full u16 stock curve verified by verify_software_lookup.py; mixed control cases include interior inputs.",
                      "control_and_paired_actuation_cases": control_cases,
                      "ecu_tcu_ecu_timeline": timeline,
                      "limits": "Synthetic admitted ECU gates and call order; held invalid input is local behavior, not full fault policy. Source physical units, timer scheduling and actuator hardware remain open."}, indent=2))


if __name__ == "__main__":
    main()
