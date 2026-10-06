"""Original ECU map inversion, publication and selection; bounded synthetic RAM.

RTZ independent arithmetic oracle. No peripheral or physical actuator claim.
"""
import bisect
import hashlib
import itertools
import json
from fractions import Fraction

from sh_control_float import SHControlFloat
from verify_traction_flags import ECU, TCU, w, r, f, rf
from verify_model_sources import rounded as q, number, lookup1, lookup2, map2_info
from verify_numeric_arbitration import paired


def inverse(address, x, target):
    ys = map2_info(address)[1]
    zs = [lookup2(address, x, y) for y in ys]
    assert all(a <= b for a, b in zip(zs, zs[1:])), (hex(address), x)
    i = max(0, min(len(ys)-2, bisect.bisect_right(zs, target)-1))
    lo, hi = ys[i:i+2]
    a, b = zs[i:i+2]
    return q(q(q(q(b-target)*lo)+q(q(target-a)*hi)) /
             max(number(0xA60C8), min(10000, q(b-a))))


def expected(e):
    target = q(q(q(rf(e, 0xA720)*number(0xC56FC))*number(0xA50FC))/number(0xCA974))
    a = inverse(0xA25CC, rf(e, 0xA5A0), target)
    b = inverse(0xA25E0, rf(e, 0xA5A0), target)
    weight = max(0, min(1, q(rf(e, 0xA630)+(number(0xC5680) if r(e, 0x718C) else -number(0xC5684)))))
    blend = q(q(b*weight)+q(a*q(1-weight)))
    delta = q(blend-rf(e, 0xA5A8))
    positive = max(delta, 0)
    hi = lookup1(0xA2484, rf(e, 0xA5A4))
    lo = lookup1(0xA2490, rf(e, 0xA5A4))
    return {0xA654: target, 0xA740: a, 0xA738: b, 0xA630: weight,
            0xA734: blend, 0xA73C: delta, 0xA730: positive, 0xA72C: positive,
            0xA648: hi, 0xA644: lo, 0xA660: max(min(positive, hi), lo)}, int(not lo < positive < hi)


def check(e):
    want, flag = expected(e)
    stack = e.r[15]
    e.run(0xA4FF8, limit=100000)
    assert e.r[15] == stack and 0xA61A6 in e.visited
    for a, v in want.items():
        assert rf(e, a) == v, (hex(a), rf(e, a), v)
    assert r(e, 0xA5AC) == flag
    return {hex(a): float(v) for a, v in want.items()}


def publish(e, alternate=0, low=0, high=100):
    copies = [(0xA660, 0x72C8), (0xA65C, 0x72CC), (0xA658, 0x72D0),
              (0xA650, 0x72D4), (0xA654, 0x72D8)]
    wanted = {b: r(e, a, 4) for a, b in copies}
    flags = {0x72DC: int(r(e, 0xA613) == 1), 0x72DD: int(r(e, 0xA612) == 1)}
    e.sr = 0xF0
    e.run(0x41A68)
    assert all(r(e, b, 4) == v for b, v in wanted.items())
    assert all(r(e, b) == v for b, v in flags.items())
    w(e, 0xA3A4, alternate)
    f(e, 0x72F4, low); f(e, 0x72F0, high)
    source = rf(e, 0x72F8 if alternate == 1 else 0x72C8)
    want = low if source <= low else high if source >= high else source
    e.run(0x42240)
    assert rf(e, 0x72FC) == want
    return float(want)


def isa():
    cases = 0
    for pc, n, value in itertools.product([0, 0xFFFFD000], range(16),
                                         [0, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]):
        code = (0x0023 | n << 8).to_bytes(2, 'big')+bytes.fromhex('0009')
        e = SHControlFloat(code)
        if pc:
            e.write(pc, int.from_bytes(code, 'big'), 4)
        e.r[n] = value
        before = e.r.copy()
        assert e.instruction(pc) == ((pc+4+value) & 0xFFFFFFFF, True)
        assert e.r == before and e.pr == 0xFFFFFFF0
        cases += 1
    e = SHControlFloat(bytes.fromhex('02230009e0630009000b0009'))
    e.r[2] = 4
    e.run(0)
    assert 2 in e.visited and 8 in e.visited and 4 not in e.visited and e.r[0] == 0
    rejected = 0
    for slot in [0xE201, 0x9000, 0xD000, 0x0023]:
        e = SHControlFloat(bytes.fromhex('0223')+slot.to_bytes(2, 'big'))
        try:
            e.instruction(0)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('Expected non-NOP rejection')
    return dict(braf_vectors=cases, executed_branch=1, rejected_slots=rejected)


def main():
    assert ECU[0xC563A] == ECU[0xC563B] == 0 and ECU[0xC90A0] == 1
    counts = isa()
    direct = 0
    examples = []
    for x, request, active, history in itertools.product(
            [500, 750, 1875, 2000, 7500, 8000], [-200, 0, 40, 100, 200, 400],
            [0, 1, 2], [-2, Fraction(1, 2), 3]):
        e = SHControlFloat(ECU)
        for a, v in [(0xA5A0, x), (0xA720, request), (0xA5A4, 100),
                     (0xA5A8, direct % 3 * 10), (0xA630, history)]:
            f(e, a, v)
        w(e, 0x718C, active)
        out = check(e)
        publish(e)
        direct += 1
        if x == 2000 and active == 0 and history == Fraction(1, 2):
            examples.append(dict(request=request, outputs=out))
    selection = 0
    for value, other, flag, lo, hi in itertools.product([-20, 0, 40, 100, 120],
            [-10, 50, 110], [0, 1, 2], [0, 20], [10, 100]):
        e = SHControlFloat(ECU)
        f(e, 0xA660, value); f(e, 0x72F8, other)
        w(e, 0xA612, flag); w(e, 0xA613, flag)
        publish(e, flag, lo, hi)
        selection += 1
    # Real paired CAN decoding, full five-stage caller; independently check only
    # its conversion stage using the exact inputs observed at that stage entry.
    integrated = []
    for source, word, active in itertools.product([3200, 6400, 32767], [10040, 10300], [0, 1]):
        e = SHControlFloat(ECU)
        for a, v in [(0x6DC4, 100), (0x6D40, 20), (0x71D8, 3), (0x71D0, 4),
                     (0x71C4, 32), (0x7154, Fraction(1, 2)), (0x6DB4, 2000),
                     (0x7E0C, 40), (0x72F8, 50), (0x6D00, 0)]:
            f(e, a, v)
        _, e = paired(source, 1600, word, 10060, active, e=e)
        w(e, 0x718C, active)
        original = e.instruction
        order, captured = [], []
        def observe(pc):
            if pc in [0xA61A8, 0xA4B98, 0xA6238, 0xA6490, 0xA4FF8]:
                order.append(pc)
            if pc == 0xA4FF8:
                captured.append(expected(e))
            return original(pc)
        e.instruction = observe
        e.sr = 0xF0
        e.run(0xA477E, limit=100000)
        assert order == [0xA61A8, 0xA4B98, 0xA6238, 0xA6490, 0xA4FF8]
        assert len(captured) == 1
        want, flag = captured[0]
        assert all(rf(e, a) == v for a, v in want.items()) and r(e, 0xA5AC) == flag
        selected = publish(e)
        integrated.append(dict(source216=source, word211=word, active=active,
                               request=float(rf(e, 0xA720)), selected=selected))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),
          tcu_sha256=hashlib.sha256(TCU).hexdigest(), isa=counts, direct_cases=direct,
          selection_cases=selection, integrated=integrated, examples=examples,
          limits='Synthetic RAM and explicit calls; full caller observed, only final conversion independently modeled. No physical actuator or scheduler proof.'), indent=2))


if __name__ == '__main__':
    main()
