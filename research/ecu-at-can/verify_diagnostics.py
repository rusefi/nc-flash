"""Execute original TCU receive qualification, with synthetic RAM/ticks.

No hardware, complete scheduler, reported DTC or physical fallback simulation.
ROM is unchanged; every helper executes rather than being replaced by a mock.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH

ROOT = Path(__file__).resolve().parents[2]
ROM = (ROOT / "examples/LFG1TF000.bin").read_bytes()
SHA = hashlib.sha256(ROM).hexdigest()
assert SHA == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def w(t, address, value, size=1):
    t.write(0xFFFF0000 + address, value, size)


def r(t, address, size=1):
    return t.read(0xFFFF0000 + address, size)


def group_call(t, action, group):
    t.r[5] = group
    t.run(0x1A598, action)


def make_machine():
    t = SH(ROM)
    for group in [0x36, 0x37, 0x38]:
        group_call(t, 0, group)
    w(t, 0x868C, 1)
    w(t, 0xA939, 1)
    return t


records = []
for index in range(18):
    base = 0x5C610 + 28 * index
    records.append({
        "index": index, "id": hex(int.from_bytes(ROM[base:base+4], "big")),
        "class": ROM[base+13], "qualification_mode": ROM[base+20],
        "receive_ticks": int.from_bytes(ROM[base+8:base+10], "big"),
        "qualification_ticks": int.from_bytes(ROM[base+22:base+24], "big"),
        "count_threshold": ROM[base+24], "second_timer_multiplier": ROM[base+25],
    })
enabled = [p for p in records if p["class"] == 0 and p["qualification_mode"] == 1]
assert [p["index"] for p in enabled] == [0, 1, 3, 7, 8, 12, 13]

# Isolate one missing frame while executing real recovery for every other
# enabled record. Start with action0 initialization, avoiding zero-RAM state0
# falsely satisfying an already-qualified branch on the very first call.
lifecycles = []
for p in enabled:
    t = make_machine()
    i, period, qualify = p["index"], p["receive_ticks"], p["qualification_ticks"]
    assert p["count_threshold"] == 1 and p["second_timer_multiplier"] == 2
    w(t, 0x84D0, 100, 4)
    t.r[5] = 0
    t.run(0x19D44, i)
    timeline = []
    ticks = sorted({100, 100+period-1, 100+period, 100+2*period-1,
                    100+2*period, 100+qualify-1, 100+qualify, 101+qualify})
    for now in ticks:
        w(t, 0x84D0, now, 4)
        recovered = now == 101 + qualify
        for other in enabled:
            if other != p or recovered:
                t.run(0x19DC0, other["index"])
        if not recovered:
            t.run(0x19E10, i)
        group_call(t, 1, 0x36)
        elapsed = now - 100
        first = elapsed >= qualify and not recovered
        second = elapsed >= 2*period and not recovered
        assert r(t, 0x8CBC+2*i, 2) == first
        assert r(t, 0x8E38+2*i, 2) == second
        assert r(t, 0xA76C) == (7 if first else 1)
        assert r(t, 0xA9FD) == (1 if second else 3)
        assert r(t, 0x8EE2, 2) == (1 << i if elapsed >= period and not recovered else 0)
        timeline.append({"tick": now, "receipt_recovery": recovered,
                         "bitmap_8ee2": r(t, 0x8EE2, 2),
                         "group_status_a76c": r(t, 0xA76C),
                         "mapped_status_a9fd": r(t, 0xA9FD)})
    lifecycles.append({"id": p["id"], "timeline": timeline})

# All record timers are skipped for stock classes1/2 (+20 is2, not1).
# Exercise fault bits set and clear: qualification outputs stay identical.
skipped = []
for group, bitmap in itertools.product([0x37, 0x38], [0, 0xFFFF]):
    t = make_machine()
    w(t, 0x8EE2, bitmap, 2)
    for now in [100, 110, 600, 2100, 5100, 10000]:
        w(t, 0x84D0, now, 4)
        group_call(t, 1, group)
        g = group - 0x36
        for i in range(18):
            assert r(t, 0x8D28+18*g+i) == 2
            assert r(t, 0x8EA4+18*g+i) == 2
        assert r(t, 0xA736+group) == 1
        assert r(t, 0xA9DC+ROM[0x5EB84+16*group]) == 3
        assert r(t, 0x8EE2, 2) == bitmap
    skipped.append({"group": hex(group), "bitmap": bitmap, "six_ticks_verified": True})

# Qualification gate reset: actual action1 clears both timer state banks and
# reports zero status when9415!=0 or A939!=1. Retains the independent bitmap.
gate_cases = 0
for gate9415, gatea939 in itertools.product([0, 1, 2], [0, 1, 2]):
    if gate9415 == 0 and gatea939 == 1:
        continue
    t = make_machine()
    for now in [100, 5100]:
        w(t, 0x84D0, now, 4)
        group_call(t, 1, 0x36)
    assert r(t, 0xA76C) == 7 and r(t, 0xA9FD) == 1
    w(t, 0x9415, gate9415)
    w(t, 0xA939, gatea939)
    w(t, 0x8EE2, 0x4321, 2)
    group_call(t, 1, 0x36)
    assert r(t, 0xA76C) == r(t, 0xA9FD) == 0
    assert r(t, 0x8EE2, 2) == 0x4321
    for i in range(18):
        assert r(t, 0x8D28+i) == r(t, 0x8EA4+i) == 2
        assert r(t, 0x8CBC+2*i, 2) == r(t, 0x8E38+2*i, 2) == 0
        assert r(t, 0x8BE4+4*i, 4) == r(t, 0x8D60+4*i, 4) == 0
    gate_cases += 1

print(json.dumps({"rom_sha256": SHA, "records": records,
                  "isolated_record_lifecycles": lifecycles,
                  "stock_skipped_groups": skipped, "gate_reset_cases": gate_cases,
                  "limits": "Synthetic RAM/ticks; no physical units, final DTC or transmission fallback claim."}, indent=2))
