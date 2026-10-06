"""Full stock ECU24910 priority dispatcher; independent Boolean/state oracle.

Original helpers and both ROMs execute. Local mode/timer/source values and
remote serial replies are fixtures. No complete scheduler or physical model.
"""
import hashlib
import itertools
import json
import random
from fractions import Fraction

from verify_control_policy import (
    setup, override, gated_monitor, ECU, TCU, w, r, f, rf, protected,
    protected_byte, paired, publish, angle, selected, appcheck, payload,
    framed, q, number,
)


def pb(e, a, default=0):
    v = r(e, a)
    return v if r(e, a+1) == v ^ 255 else default


def expected(e):
    assert list(ECU[0xBAE40:0xBAE44]) == [1, 0, 0, 1]
    states = {}
    x, temp, speed = rf(e, 0x536C), rf(e, 0x6D20), rf(e, 0x6DB4)
    def hysteresis(a, value, hi, lo):
        states[a] = 1 if value >= hi else 0 if value < lo else r(e, a)
    hysteresis(0x568A, x, number(0xBAE70), q(number(0xBAE70)-number(0xBAE74)))
    hysteresis(0x568B, x, number(0xBAE8C), number(0xBAE88))
    hysteresis(0x568C, speed, number(0xBAE80), q(number(0xBAE80)-number(0xBAE84)))
    for a, c in [(0x568D, 0xBAE78), (0x568E, 0xBAE7C)]:
        hysteresis(a, temp, number(c), q(number(c)+number(0x24A18)))
    M, count = r(e, 0x722A), r(e, 0x5664, 2)
    old, request = r(e, 0x566E), r(e, 0x93C3)
    remote = [r(e, a) for a in [0x92CB, 0x932A]]
    bypass = bool((not old and not request and 1 in remote)
                  or (M == 0 and count > int.from_bytes(ECU[0xBAE4A:0xBAE4C], 'big'))
                  or r(e, 0x5633) == 1
                  or (not r(e, 0x6642) and not r(e, 0x6643) and not pb(e, 0x213A)))
    # Stock BAE40=1 makes25242 false. Later helpers are reached only if
    # bypass and every preceding winner are false.
    first = second = third = fourth = normal = 0
    retained_tag = r(e, 0x5675)
    reached = [0x251B4]
    if not bypass:
        reached += [0x25242, 0x252C4]
        ready = states[0x568A] == 1 and r(e, 0x5677) == 1 and not pb(e, 0x20A8)
        early = (M == 0 and count < 625 and r(e, 0x566A) == 1
                 and not pb(e, 0x2136) and not states[0x568C])
        limiting = any([pb(e, 0x2138), r(e, 0x5628), r(e, 0x5629), r(e, 0x5354)])
        late = (M == 1 and r(e, 0x5666, 2) < 625
                and (not limiting or ((not states[0x568D] or states[0x568E] == 1)
                     and not pb(e, 0x2134) and pb(e, 0x2110, 1) == 1 and not states[0x568C])))
        if ready and (early or late):
            second = 1
            retained_tag = 0 if early else 1
        else:
            reached.append(0x2543A)
            third = int(states[0x568B] == 1 and M == 0
                        and (not any(remote) or request == 1)
                        and ((pb(e, 0x2136) == 1 and r(e, 0x566A) == 1) or count >= 625))
            if not third:
                reached.append(0x25512)
                fourth = r(e, 0x5635)
                normal = int(not fourth)
    states.update({0x566B:int(bypass), 0x566C:first, 0x566E:second,
                   0x5670:third, 0x5672:fourth, 0x5674:normal, 0x5675:retained_tag})
    return states, reached


def check(e):
    want, reached = expected(e)
    stack = e.r[15]
    e.visited.clear(); e.run(0x24910, limit=50000)
    assert e.r[15] == stack
    actual = {a:r(e, a) for a in want}
    assert actual == want, {hex(a):(actual[a],want[a]) for a in want if actual[a] != want[a]}
    helpers = [0x251B4, 0x25242, 0x252C4, 0x2543A, 0x25512]
    assert [a for a in helpers if a in e.visited] == reached
    if actual[0x566B]: branch = 'bypass'
    elif actual[0x566E]: branch = 'feedback'
    elif actual[0x5670]: branch = 'relative'
    elif actual[0x5672]: branch = 'absolute'
    else: branch = 'normal'
    return dict(branch=branch, mode=r(e, 0x722A), old_feedback_enable=r(e, 0x552C),
                states={hex(a):v for a,v in actual.items()})


BYTES = [0x722A, 0x566E, 0x93C3, 0x92CB, 0x932A, 0x5633, 0x6642, 0x6643,
         0x566A, 0x5677, 0x5628, 0x5629, 0x5354, 0x5635, 0x5675]
PROTECTED = [0x213A, 0x2136, 0x2134, 0x20A8, 0x2138, 0x2110]


def fixture():
    e = setup()
    for a in PROTECTED: protected_byte(e, a, 0)
    w(e, 0x6642, 1)  # keep generic bypass off unless a case changes it
    for a, v in [(0x536C, 11), (0x6D20, 90), (0x6DB4, 150), (0x569C, 8)]: f(e, a, v)
    return e


def local_gates(e):
    """Original order218E2..218EA: reply qualification, timer, local enables."""
    assert ECU[0xBAE44] == 1 and ECU[0xBAE45] == ECU[0xBAE46] == 0
    assert ECU[0xDCE1D:0xDCE20] == b'\0\0\0'
    x, feedback = rf(e, 0x536C), rf(e, 0x5550)
    count = r(e, 0x5668, 2)
    short_window = int(count <= 37)
    h = lambda a, v: 1 if v >= Fraction(13, 2) else 0 if v < 6 else r(e, a)
    qualified = int(r(e, 0x5676) == 1 and (short_window or 50 <= count < 125)
                    and h(0x568F, x) == h(0x5690, feedback) == 1)
    timer = 125 if x < 6 and r(e, 0x6600) == 1 else max(0, r(e, 0x5680, 2)-1)
    above = int(x >= Fraction(13, 2))
    want = {0x567F:short_window, 0x568F:h(0x568F, x), 0x5690:h(0x5690, feedback),
            0x5677:qualified, 0x5678:above, 0x5679:int(r(e, 0x722A) == 1 and qualified),
            0x567A:int(above and timer == 0), 0x567B:above}
    stack = e.r[15]
    for fn in [0x24C88, 0x24DCE, 0x24E06]: e.run(fn)
    assert e.r[15] == stack and r(e, 0x5680, 2) == timer
    assert all(r(e, a) == value for a, value in want.items()), want
    return dict(timer=timer, qualified=qualified, monitor_enable=want[0x567A])


def main():
    direct = 0
    branches = dict.fromkeys(['bypass', 'feedback', 'relative', 'absolute', 'normal'], 0)
    for mode, count, gate, fault, flag in itertools.product(
            [0, 1, 2], [0, 624, 625, 1875, 1876, 65535], [0, 1, 2], [0, 1, 2], [0, 1, 2]):
        e = fixture(); w(e, 0x722A, mode); w(e, 0x5664, count, 2); w(e, 0x5666, count, 2)
        w(e, 0x5677, gate); w(e, 0x566A, 1); w(e, 0x5635, flag)
        protected_byte(e, 0x20A8, fault)
        out = check(e); branches[out['branch']] += 1
        override(e); selected(e)
        direct += 1
    varied = 0
    rng = random.Random(0x24910)
    for _ in range(1800):
        e = fixture()
        for a in BYTES: w(e, a, rng.choice([0, 0, 1, 2]))
        for a in PROTECTED:
            protected_byte(e, a, rng.choice([0, 0, 1, 2]))
            if rng.randrange(5) == 0: w(e, a+1, r(e, a))
        for a in [0x5664, 0x5666]: w(e, a, rng.choice([0, 124, 125, 624, 625, 1875, 1876, 32768, 65535]), 2)
        for a in range(0x568A, 0x568F): w(e, a, rng.randrange(3))
        for a, values in [(0x536C, [5, 6, 6.25, 6.5, 9.5, 9.75, 10, 11]),
                          (0x6D20, [97, 98, 99, 100, 101]), (0x6DB4, [199, 200, 250, 300, 301])]:
            f(e, a, rng.choice(values))
        out = check(e); branches[out['branch']] += 1; varied += 1
    conditional = 0
    for bits, count in itertools.product(range(256), [624, 625]):
        e = fixture(); w(e, 0x722A, 1); w(e, 0x5677, 1); w(e, 0x5666, count, 2)
        for i, a in enumerate([0x2138, 0x5628, 0x5629, 0x5354, 0x2134, 0x2110]):
            if a in PROTECTED: protected_byte(e, a, (bits >> i) & 1)
            else: w(e, a, (bits >> i) & 1)
        f(e, 0x6D20, 100 if bits & 64 else 90)
        f(e, 0x6DB4, 300 if bits & 128 else 150)
        check(e); conditional += 1
    for old_d, old_e in itertools.product([0, 1, 2], repeat=2):
        e = fixture(); w(e, 0x722A, 1); w(e, 0x5677, 1)
        protected_byte(e, 0x2138, 1); protected_byte(e, 0x2110, 1)
        f(e, 0x6D20, 99); w(e, 0x568D, old_d); w(e, 0x568E, old_e)
        check(e); conditional += 1
    hysteresis_cases = 0
    # Each threshold's both sides, equality and retained non-Boolean state.
    for old, x, temp, speed in itertools.product([0, 1, 2], [5.99, 6, 6.49, 6.5, 9.49, 9.5, 9.99, 10],
                                                [97.99, 98, 99.99, 100], [199, 200, 299, 300]):
        e = fixture()
        for a in range(0x568A, 0x568F): w(e, a, old)
        for a, v in [(0x536C, x), (0x6D20, temp), (0x6DB4, speed)]: f(e, a, q(Fraction(str(v))))
        check(e); hysteresis_cases += 1
    local_cases = 0
    for count, x, feedback, enable, reload_flag in itertools.product(
            [0, 37, 38, 49, 50, 124, 125, 65535], [5, 6, 6.25, 6.5, 11],
            [5, 6, 6.25, 6.5, 10], [0, 1, 2], [0, 1, 2]):
        e = fixture(); w(e, 0x5668, count, 2); f(e, 0x536C, x); f(e, 0x5550, feedback)
        w(e, 0x5676, enable); w(e, 0x6600, reload_flag); w(e, 0x722A, enable)
        w(e, 0x568F, local_cases%3); w(e, 0x5690, (local_cases//3)%3)
        w(e, 0x5680, [0, 1, 2, 125, 65535][local_cases%5], 2)
        local_gates(e); local_cases += 1
    # Countdown blocks monitor admission until expiration. At x==6 the
    # timer decrements; monitor admission still needs x>=6.5.
    e = fixture(); f(e, 0x536C, 5); f(e, 0x5550, 10); w(e, 0x6600, 1)
    timer_history = [local_gates(e)]
    f(e, 0x536C, 11)
    for _ in range(125): timer_history.append(local_gates(e))
    assert [x['monitor_enable'] for x in timer_history] == [0]*125+[1]
    # Actual prior output566E changes251B4's bypass decision with the same
    # 92CB input, so retaining history matters even before numeric override.
    history = []
    e = fixture(); w(e, 0x566A, 1); w(e, 0x5677, 1)
    for fault, remote in [(0, 0), (0, 1), (1, 1), (0, 1), (0, 0), (0, 1)]:
        protected_byte(e, 0x20A8, fault); w(e, 0x92CB, remote)
        history.append(check(e))
    assert [x['branch'] for x in history] == ['feedback', 'feedback', 'normal', 'bypass', 'feedback', 'feedback']
    # Real peer packers and transport/application admission; no 566E injection.
    e = fixture(); w(e, 0x99D8, 0x8000, 2)
    w(e, 0x566A, 1); w(e, 0x5676, 1); f(e, 0x5550, 10)
    local_gates(e)  # Explicit initialization produces5677/567A, no direct write.
    for a, v in [(0x6DC4, 100), (0x6D40, 20), (0x71D8, 3), (0x71D0, 4),
                 (0x71C4, 32), (0x7154, Fraction(1,2)), (0x7E0C, 40), (0x72F8, 50),
                 (0x5620, 3), (0x5650, 14)]: f(e, a, v)
    appcheck(e, payload(), 2)
    lifecycle = []
    previous_command = rf(e, 0x56A0)
    for i in range(32):
        good = i == 0 or i >= 28
        p = bytearray(payload(seed=800+i, complement=good)); p[4:6] = (400).to_bytes(2, 'big')
        p[14] = 128  # Original decoder produces5550=10, used by24C88.
        base = len(e.tx); outgoing = bytes(r(e, 0x437A+j) for j in range(38))
        e.run(0xE86E)
        for v in framed(p): e.rdr = v; e.run(0xE86E)
        assert bytes(e.tx[base:]) == framed(outgoing)
        appcheck(e, p, r(e, 0x43A7), inject=False)
        quantized = max(0, min(65535, int(q(q(previous_command/number(0x22750))+Fraction(1, 2)))))
        assert r(e, 0x437E, 2) == quantized
        monitor = gated_monitor(e)
        active = int(i%2 == 1)
        _, e = paired(3200, 1600, 10040, 10060, active, e=e); w(e, 0x718C, active)
        e.run(0xA477E, limit=100000); publish(e); angle(e)
        result = check(e); gates = local_gates(e); override(e); selection = selected(e)
        previous_command = rf(e, 0x56A0)
        result.update(call=i+1, valid_reply=good, monitor=monitor, selection=selection,
                      feedback=float(rf(e, 0x5534)), command=float(rf(e, 0x56A0)), local_gates=gates)
        lifecycle.append(result)
        assert result['branch'] == ('feedback' if i < 26 else 'normal')
    assert r(e, 0x20A8) == 1
    e.run(0x28552); result = check(e); override(e); selected(e)
    assert result['branch'] == 'feedback'
    cleared = dict(**result, command=float(rf(e, 0x56A0)))
    assert all(branches.values()), branches
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
          direct_cases=direct, varied_cases=varied, hysteresis_cases=hysteresis_cases,
          conditional_feedback_cases=conditional,
          local_gate_cases=local_cases, countdown_calls=len(timer_history),
          branch_counts=branches, retained_history=history, paired_lifecycle=lifecycle, explicit_clear=cleared,
          limits='Full24910 and24C88/24DCE/24E06 executed under stock calibration. Earlier local sources, complete task order, recovery consumers and physical effects remain open. Serial peer is synthetic.'), indent=2))


if __name__ == '__main__':
    main()
