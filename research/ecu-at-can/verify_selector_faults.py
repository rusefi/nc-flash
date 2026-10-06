"""Execute selector diagnostic producer, qualification and CAN231 publication.

Unchanged ROMs, synthetic application inputs and ticks, isolated task calls.
No GPIO, ADC hardware, complete scheduler, physical switch naming or PRHT.
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


records = []
for g, expected in [(0x15, "000107d0000510c7070700000c000c00"),
                    (0x16, "0100000000011007070800000c000c00")]:
    record = TCU[0x5EB78+16*g:0x5EB88+16*g]
    assert record.hex() == expected
    records.append({"group": hex(g), "rom_record": record.hex(" ")})

producer_cases = 0
for mask, enabled, inhibit, dependency, adc_status in itertools.product(
        range(16), range(2), range(2), range(2), [0, 2, 3]):
    t = SH(TCU)
    t.run(0x5853C)
    for i in range(4):
        w(t, 0x88B4+i, (mask >> i) & 1)
    for addr, value in [(0xA938, enabled), (0xA735, inhibit),
                        (0xA962, dependency), (0x88BD, adc_status)]:
        w(t, addr, value)
    t.run(0x58548)
    admitted = enabled and not inhibit
    assert r(t, 0xA74B) == (3 if mask.bit_count() >= 2 else 1) * admitted
    assert r(t, 0xA74C) == dependency * admitted
    assert r(t, 0x843E, 2) == (2000 if admitted and dependency and mask == 0 else 65535)
    assert r(t, 0x8440, 2) == 65535
    producer_cases += 1

# Actual countdown helper, including the sentinel and saturation boundaries.
timer_cases = 0
for value in [0, 1, 2, 2000, 28000, 65534, 65535]:
    t = SH(TCU)
    w(t, 0x843E, value, 2)
    t.run(0x11DB4, 0xFFFF843E)
    assert r(t, 0x843E, 2) == (value if value in [0, 65535] else value-1)
    timer_cases += 1

# No asserted input: explicit timer boundary fixtures, not elapsed wall time.
missing_cases = []
for speed, first, second in itertools.product([299, 300], [65535, 1, 0], [65535, 1, 0]):
    t = SH(TCU)
    w(t, 0xA938, 1)
    w(t, 0xA962, 1)
    w(t, 0x80BA, speed, 2)
    w(t, 0x843E, first, 2)
    w(t, 0x8440, second, 2)
    t.run(0x58548)
    expected_first = 2000 if first == 65535 else first
    expected_second = (28000 if second == 65535 else second) if speed >= 300 and first == 0 else 65535
    status = 1 | (2 if expected_first == 0 else 0) | (6 if expected_second == 0 else 0)
    assert r(t, 0x843E, 2) == expected_first
    assert r(t, 0x8440, 2) == expected_second
    assert r(t, 0xA74C) == status
    missing_cases.append({"raw_80ba": speed, "before": [first, second],
                          "after": [expected_first, expected_second], "status": status})

# Multiple asserted inputs qualify group15 in five 2000-tick intervals.
t, e = SH(TCU), SH(ECU)
t.run(0x5327C)
t.run(0x5853C)
w(t, 0xA938, 1)
w(t, 0x88B4, 1)
w(t, 0x88B5, 1)
w(e, 0x734A, 0x80)
w(e, 0x734C, 1)
timeline = []
for now in [100, 2099, 2100, 4100, 6100, 8100, 10099, 10100, 10101]:
    w(t, 0x84D0, now, 4)
    for fn in [0x58548, 0x566E0, 0x570F6, 0x21C1C, 0x22416]:
        t.run(fn, 0x15 if fn == 0x566E0 else 0)
    t.run(0x19414, 1)
    qualified = now >= 10100
    pending = now >= 2100
    assert r(t, 0xA701) == (5 if qualified else 3 if pending else 1)
    assert r(t, 0xA964) == (0x1C if qualified else 0xA if pending else 1)
    assert r(t, 0x92CD) & 0x60 == (0x60 if qualified else 0x20 if pending else 0)
    assert r(t, 0x8EED) == (0xFF if qualified else 0xEF)
    assert r(t, 0xA99B) == qualified
    count = t.run(0x558CC, 0xFFFFB000)
    stored = bytes(r(t, 0xB000+i) for i in range(count*3)).hex(" ")
    assert stored == ("07 07 ff" if qualified else "")
    for i in range(8):
        w(e, 0x6ABC+i, r(t, 0x8EED+i))
    for fn in [0x35BB8, 0x3585C, 0x411F0]:
        e.run(fn)
    assert all(r(e, 0x6ACB+i) == 0 for i in range(13))
    assert r(e, 0x723A, 2) == r(e, 0x7244, 2) == 0x00FF
    timeline.append({"tick": now, "group_flags": r(t, 0xA701),
                     "summary_a964": r(t, 0xA964), "flags_92cd": r(t, 0x92CD),
                     "can231_byte0": hex(r(t, 0x8EED)), "stored_list": stored,
                     "report_a99b": r(t, 0xA99B), "ecu_combined_flag": r(e, 0x723A)})

print(json.dumps({"scope": __doc__.strip(), "rom_records": records,
                  "producer_cases": producer_cases, "timer_helper_cases": timer_cases,
                  "missing_input_boundaries": missing_cases, "multiple_input_timeline": timeline,
                  "limits": "Timer boundaries are fixtures; recovery and full scheduler remain unexecuted. Varying 88BD proves no influence only on this isolated producer path. PRHT consumption and absolute time units remain unknown."}, indent=2))
