"""Full ECU A6490 execution, independently checked CAN numeric subpaths.

Two stock binaries, bounded RTZ arithmetic, synthetic local model inputs and
explicit scheduling. Only named outputs have an independent oracle; this
does not validate all branches of the large function or physical actuators.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import random

from sh_model_float import SHModelFloat
from sh_software_arithmetic import SHSoftwareArithmetic
from verify_traction_flags import ECU, TCU, w, r, f, rf, receive211, receive21a
from verify_model_sources import rounded as q, number, initialize_sources


EPS = number(0xA65E8)
SCALE = number(0xA6AC4)


def fixture():
    e = SHModelFloat(ECU)
    for a, v in [(0x6DC4, 100), (0x6D40, 20), (0x71D8, 3), (0x71D0, 4),
                 (0x71C4, 32), (0x7154, Fraction(1, 2)), (0xA5A0, 2000),
                 (0x7E0C, 40)]:
        f(e, a, v)
    return e


def check(e):
    # Snapshot inputs before the full function updates its local histories.
    x = {a: rf(e, a) for a in [0x6DC4, 0x6D40, 0x71D8, 0x71D0, 0x71C4,
                              0x7154, 0x6AA0, 0x6A80, 0x714C, 0x6A9C, 0x6A30]}
    denominator = 1 if r(e, 0x6A28) else max(EPS, x[0x7154])
    high = q(max(q(x[0x6AA0]/denominator), x[0x6A80], -10000)+x[0x71C4])
    low = q(min(q(max(x[0x714C], x[0x6A9C], -10000)/denominator),
                x[0x6A30])+x[0x71C4])

    def convert(v):
        return q(q(q(q(q(q(v*SCALE)/293)/max(x[0x6DC4], EPS))
                         *q(x[0x6D40]+273))-x[0x71D8])-x[0x71D0])

    expected = {0xA710: high, 0xA70C: low, 0xA700: convert(high), 0xA6F0: convert(low)}
    stack = e.r[15]
    e.run(0xA6490, limit=50000)
    assert 0xA7432 in e.visited and e.r[15] == stack
    for a, value in expected.items():
        assert rf(e, a) == value, (hex(a), rf(e, a), value, x)
    # Conditional consistency check; A650's producer is not independently modeled.
    assert rf(e, 0xA6FC) == min(expected[0xA6F0], rf(e, 0xA650))
    return {hex(a): float(value) for a, value in expected.items()}


def paired(source216, source218, word211, word21a, flag, mode=1, fresh=20, e=None):
    t = SHSoftwareArithmetic(TCU)
    e = fixture() if e is None else e
    w(t, 0x915A, 32767, 2)
    w(t, 0x80BC, source216, 2)
    w(t, 0x9118, source218, 2)
    t.run(0x18F10, mode)
    t.run(0x191A8, mode)
    for a, v in [(0x734A, 128), (0x734C, 1), (0x6A5D, fresh), (0x6A90, fresh)]:
        w(e, a, v)
    # Actual packed first four216 bytes and218 byte6; other fields initialized0.
    for src, dst in [(0x8EFD, 0x6A40), (0x8EF5, 0x6A68)]:
        for i in range(8):
            w(e, dst+i, r(t, src+i))
    for fn in [0x35034, 0x34CEC, 0x34EB8, 0x35420, 0x35218]:
        e.run(fn)
    raw216 = (65535 if mode == 16 else 65534 if mode == 0 or source216 == 32767
              else max(0, (source216 >> 5)+512))
    raw218 = (255 if mode != 1 or source218 == 32767 else
              min(254, max(0, (source218 >> 6)+50)))
    expected216 = (16 if not fresh else 65537 if raw216 == 65535 else
                   65022 if 312 <= raw216 <= 502 else raw216-512)
    #218 byte6 does not directly test its receipt counter; grouped fault is0.
    expected218 = -10000 if raw218 == 255 else min(50, 2*raw218-100)
    assert r(t, 0x8EFF, 2) == raw216 and r(t, 0x8EFB) == raw218
    assert rf(e, 0x6A30) == expected216 and rf(e, 0x6A80) == expected218
    receive211(e, flag << 13)
    e.run(0x34BBC)  #Real stock initialization: conversion bypass6A28=1.
    assert r(e, 0x6A28) == 1
    w(e, 0x6A10, word211, 2)
    e.run(0x34B8C)
    e.run(0x349CA)
    e.run(0x3FF2C)
    receive21a(e, word21a, word21a)
    e.run(0x3558E)
    assert rf(e, 0x714C) == word211-10000
    assert rf(e, 0x6A9C) == (-10000 if word21a == 65535 else max(-1000, word21a-10000))
    assert rf(e, 0x6AA0) == (-10000 if not flag or word21a in [65534, 65535]
                            else min(10000, word21a-10000))
    return t, e


def main():
    assert number(0xC5678) == number(0xC567C) == -10000
    direct = 0
    # Denominator floor/bypass and four-way numeric precedence, including ties.
    for ratio, bypass, values in itertools.product(
            [-1, 0, EPS/2, EPS, EPS*2, Fraction(1, 2), 1, 2], [0, 1, 2],
            [(-10000, -10000, -10000, -10000, 65537),
             (40, 20, 30, 50, 100), (20, 40, 50, 30, 100),
             (40, 40, 50, 50, 20), (0, 0, 0, 0, 0),
             (-12000, -13000, -14000, -15000, -20000),
             (55534, 50, 55535, 55534, 65022)]):
        e = fixture()
        f(e, 0x7154, ratio)
        w(e, 0x6A28, bypass)
        for a, value in zip([0x6AA0, 0x6A80, 0x714C, 0x6A9C, 0x6A30], values):
            f(e, a, value)
        check(e)
        direct += 1
    rng = random.Random(0xA6490)
    varied = 0
    for _ in range(128):
        e = fixture()
        for a in [0x6AA0, 0x6A80, 0x714C, 0x6A9C, 0x6A30, 0x71C4, 0x71D8, 0x71D0]:
            f(e, a, Fraction(rng.randrange(-4000, 4001), 8))
        f(e, 0x7154, rng.choice([EPS/2, EPS, EPS*2, Fraction(1, 2), 1, 2]))
        f(e, 0x6DC4, rng.choice([0, EPS/2, EPS, EPS*2, 1, 100]))
        f(e, 0x6D40, rng.choice([-40, 0, 20, 80]))
        w(e, 0x6A28, rng.choice([0, 1]))
        check(e)
        varied += 1
    paired_cases = 0
    examples = []
    for source216, source218, words in itertools.product(
            [-32768, -6432, -6400, -320, -288, -32, 0, 3200, 6400, 32766, 32767],
            [-32768, -1, 0, 1600, 32767], [(10040, 10060, 1), (10060, 10040, 0)]):
        t, e = paired(source216, source218, *words)
        outputs = check(e)
        paired_cases += 1
        if source216 in [3200, 32767] and source218 in [1600, 32767]:
            examples.append(dict(source216=source216, source218=source218,
                                 word211=words[0], word21a=words[1], flag=words[2], outputs=outputs))
    mode_cases = 0
    for mode, fresh, word21a in itertools.product([0, 1, 16], [0, 20], [0, 10040, 65534, 65535]):
        _, e = paired(6400, 1600, 65535, word21a, 1, mode, fresh)
        check(e)
        mode_cases += 1
    produced_model_cases = 0
    for x, y, active in itertools.product([1000, 2000], [Fraction(1, 2), 1], [0, 1]):
        e = initialize_sources(x=x, y=y, active=active)
        #71C4/71D8/71D0 stay as produced by original stock maps.
        for a, v in [(0x6DC4, 100), (0x6D40, 20), (0xA5A0, x), (0x7E0C, 40)]:
            f(e, a, v)
        _, e = paired(6400, 1600, 10040, 10060, 1, e=e)
        check(e)
        produced_model_cases += 1
    # Same ECU across input changes: large function histories are retained.
    _, e = paired(6400, 1600, 10040, 10060, 1)
    sequence = []
    for raw in [10060, 10040, 10000, 0, 65534, 65535, 10060]:
        receive21a(e, raw, raw)
        e.run(0x3558E)
        sequence.append(dict(raw21a=raw, outputs=check(e)))
    # Only218 ages; original grouped monitor governs218 invalidation and216 ramp.
    _, e = paired(6400, 1600, 10300, 10060, 0)
    e.sr = 0xF0
    for a in [0x722A, 0x6AD8, 0x6B0E]:
        w(e, a, 1)
    f(e, 0x7138, 1000)
    e.run(0x3545E)
    reload = ECU[0xB824A]
    loss = []
    for call in range(reload+3):
        if call:
            e.run(0x3519E)
        if call == reload+2:
            e.run(0x35420)
            e.run(0x3545E)
        e.run(0x34806)
        e.run(0x35218)
        e.run(0x34EB8)
        fault = int(call in [reload, reload+1])
        assert r(e, 0x69E2) == fault
        assert rf(e, 0x6A80) == (-10000 if fault else 50)
        expected_limit = 200+16*(call-reload+1) if fault else 200
        assert rf(e, 0x6A30) == expected_limit
        loss.append(dict(call=call, receipt218=r(e, 0x6A90), fault=fault,
                         limit216=expected_limit, outputs=check(e)))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),
                         tcu_sha256=hashlib.sha256(TCU).hexdigest(), scope=__doc__.strip(),
                         direct_cases=direct, varied_model_cases=varied,
                         paired_cases=paired_cases, mode_receipt_sentinel_cases=mode_cases,
                         produced_model_cases=produced_model_cases,
                         full_function_entry='0xA6490', full_function_return_delay='0xA7432',
                         examples=examples, retained_history_sequence=sequence,
                         grouped_fault_lifecycle=loss), indent=2))


if __name__ == '__main__':
    main()
