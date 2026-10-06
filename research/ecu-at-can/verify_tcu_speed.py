"""Original TCU speed calculation/limiter -> CAN216 -> ECU CAN201.

Explicit synthetic source states/call order. No sensor hardware, real timing,
DSC sender or PRHT receiver. Numeric producer is executed without mocked
division helpers; period acquisition and calibration provenance remain open.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_integer_arithmetic import SHIntegerArithmetic
from sh_rtz_float import SHNormalRTZFloat
from sh_subset import signed
from verify_integer_arithmetic import trunc_div

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, a, v, size=1):
    t.write(0xFFFF0000+a, v, size)


def r(t, a, size=1):
    return t.read(0xFFFF0000+a, size)


def through_ecu(t, use_4b0=False):
    e = SHNormalRTZFloat(ECU)
    w(e, 0x734A, 0x80)
    w(e, 0x734C, 1)
    w(e, 0x6A5D, 1)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    for fn in [0x35034, 0x34CEC, 0x3B7CE]:
        e.run(fn)
    w(e, 0x7353, use_4b0)
    for a in [0x6AF8, 0x6AFA]:
        w(e, a, 12345, 2)
    for fn in [0x3A05E, 0x3679C, 0x365D0]:
        e.run(fn)
    expected = 65535 if r(t, 0x8F02, 2) == 65535 else 12345 if use_4b0 else r(t, 0x8F02, 2)
    assert r(e, 0x6B30, 2) == expected
    return expected


limiter_cases = 0
for candidate, previous, initialized, fault, mode in itertools.product(
        [0, 1, 999, 1000, 1001, 9000, 10000, 11000, 11001, 29999, 30000, 30001, 65535],
        [0, 500, 1000, 10000, 29999, 30000], range(2), range(2), [0, 1, 16]):
    t = SHIntegerArithmetic(TCU)
    w(t, 0xA5AC, candidate, 2)
    w(t, 0x8AE8, previous, 2)
    w(t, 0x8AE7, initialized)
    w(t, 0x92C6, fault*4)  # byte4 calculation is enabled, too
    w(t, 0x80EE, 12345, 2)
    t.run(0x18F8C, mode)
    latch, memory = initialized, previous
    if mode == 0:
        latch, memory, output, byte4 = 0, 0, 10000, 0
    elif mode == 16:
        output, byte4 = 65535, 255
    elif fault:
        latch, memory, output, byte4 = 0, 65535, 65535, 128
    else:
        memory = min(candidate, 30000)
        if initialized:
            memory = min(previous+1000, max(max(0, previous-1000), memory))
        latch, output, byte4 = 1, memory+10000, 128
    assert (r(t, 0x8AE7), r(t, 0x8AE8, 2), r(t, 0x8F02, 2), r(t, 0x8F01)) == (latch, memory, output, byte4)
    assert r(t, 0x8AF0, 2) == output
    through_ecu(t)
    limiter_cases += 1

byte4_cases = 0
for source, fault in itertools.product([0, 95, 96, 191, 192, 24384, 24480, 32767, 32768, 65535], range(2)):
    t = SHIntegerArithmetic(TCU)
    w(t, 0x80EE, source, 2)
    w(t, 0x92C6, fault*0x20)
    t.run(0x18F8C, 1)
    assert r(t, 0x8F01) == (255 if fault else min(254, max(0, trunc_div(signed(source, 16), 96))))
    assert r(t, 0x8F02, 2) == 10000  # independent speed fault bit clear
    byte4_cases += 1

upstream_cases = 0
cal_divisor = int.from_bytes(TCU[0x76E7A:0x76E7C], "big", signed=True)
alternate_scale = int.from_bytes(TCU[0x76E7C:0x76E7E], "big")
assert (cal_divisor, alternate_scale) == (4100, 1000)
for input_word, period_value, alternate in itertools.product(
        [0, 1, 299, 1000, 4096, 10000, 22391, 32767, 32768, 65535],
        [0, 1, 255, 256, 4096, 32767, 65535], range(2)):
    t = SHIntegerArithmetic(TCU)
    w(t, 0xA552, input_word, 2)
    w(t, 0x91A2, period_value, 2)
    w(t, 0x9330, alternate)
    # Signed clamped quotient, then unsigned word multiply/divide/shift.
    first = max(-32768, min(32767, trunc_div(signed(input_word, 16)*6000, cal_divisor)))
    second = min(65535, (first & 65535)*1000//(alternate_scale if alternate else 1000))
    expected = min(65535, period_value*second//256)
    t.run(0x52B10)
    assert r(t, 0xA5AC, 2) == expected
    assert r(t, 0xA5B6, 2) == expected//100
    t.run(0x18F8C, 1)
    assert r(t, 0x8F02, 2) == min(expected, 30000)+10000
    through_ecu(t)
    upstream_cases += 1

# Stateful source changes, fault reset, normal recovery and mode16 retention.
t = SHIntegerArithmetic(TCU)
lifecycle = []
for candidate, fault, mode, expected in [(0, 0, 1, 10000), (10000, 0, 1, 11000),
        (10000, 0, 1, 12000), (10000, 1, 1, 65535), (10000, 0, 1, 20000),
        (0, 0, 1, 19000), (0, 0, 16, 65535), (0, 0, 1, 18000),
        (30000, 0, 0, 10000), (30000, 0, 1, 40000)]:
    w(t, 0xA5AC, candidate, 2)
    w(t, 0x92C6, fault*4)
    t.run(0x18F8C, mode)
    assert r(t, 0x8F02, 2) == expected
    output201 = through_ecu(t, True)
    lifecycle.append({"candidate": candidate, "speed_fault": fault, "mode": mode,
                      "limiter_initialized": r(t, 0x8AE7), "limiter_value": r(t, 0x8AE8, 2),
                      "can216_word5": expected, "can201_with_valid_4b0": output201})

print(json.dumps({"scope": __doc__.strip(), "limiter_and_paired_ecu_cases": limiter_cases,
                  "byte4_cases": byte4_cases, "upstream_calculation_and_paired_cases": upstream_cases,
                  "lifecycle": lifecycle, "stock_calibrations": [cal_divisor, alternate_scale],
                  "limits": "Per-call limiter, not a physical rate;91A2 acquisition,A552 provenance,92C6 bit2 producer and roof receiver remain open."}, indent=2))
