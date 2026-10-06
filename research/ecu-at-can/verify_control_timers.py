"""ECU timer producers and GPIO enable in retained paired command lifecycles.

Full bodies, original stock ROMs, synthetic SCI1 peer and sampled registers.
Selected task bodies follow observed order; omitted task/hardware remain open.
"""
import hashlib
import itertools
import json
from fractions import Fraction

from verify_control_admission import (
    fixture, check, local_gates, override, gated_monitor, ECU, TCU, w, r, f, rf,
    paired, publish, angle, selected, appcheck, payload, framed, q, number,
)
from verify_traction_flags import protected_byte


def pre_timers(e):
    mode, prior, request = r(e, 0x722A), r(e, 0x566E), r(e, 0x93C3)
    count, other = r(e, 0x5664, 2), r(e, 0x5666, 2)
    if mode:
        count = 0
    elif prior == 1 or request == 1 or (r(e, 0x92CB) == r(e, 0x932A) == 0):
        count = min(65535, count+1)
    eligible = int(mode == 0 and count >= 6)
    other = min(65535, other+1) if mode == 1 else 0
    stack = e.r[15]
    e.run(0x247B6)
    assert e.r[15] == stack
    assert (r(e, 0x5664, 2), r(e, 0x5666, 2), r(e, 0x566A)) == (count, other, eligible)


def post_timers(e):
    count = min(65535, r(e, 0x5668, 2)+1) if r(e, 0x5670) == 1 else 0
    enabled = int(r(e, 0x566B) == 0 and count < 201)
    port = e.registers[0xFFFFF746]
    stack, sr = e.r[15], e.sr
    e.run(0x24B82); e.run(0x24BAE)
    assert e.r[15] == stack
    # Helpers restore the incoming interrupt mask; comparisons may change T
    # before22E4 captures SR. Do not assert an unchanged condition bit.
    assert e.sr & 0xF0 == sr & 0xF0
    assert r(e, 0x5668, 2) == count and r(e, 0x5676) == enabled
    assert e.registers[0xFFFFF746] == (port & ~0x800) | (enabled << 11)


def filtered_source(e):
    old, source = rf(e, 0x536C), rf(e, 0x6CB4)
    # Original2508 uses rounded FMUL then rounded FADD, not a fused operation.
    blend = q(source + q(q(1-number(0xBAE28))*q(old-source)))
    want = source if abs(q(source-blend)) < number(0x1DF08) else blend
    e.run(0x1DEE2)
    assert rf(e, 0x536C) == want


def setup_loop(numeric_fixtures=True):
    e = fixture(); w(e, 0x99D8, 0x8000, 2)
    # Replace prior direct536C fixture with original initialization/filter.
    f(e, 0x6CB4, 11); e.run(0x1DED8); assert rf(e, 0x536C) == 11
    for a, v in [(0x6DC4, 100), (0x6D40, 20), (0x71D8, 3), (0x71D0, 4),
                 (0x71C4, 32), (0x7154, Fraction(1,2)), (0x7E0C, 40), (0x72F8, 50)]: f(e, a, v)
    if numeric_fixtures:
        for a, v in [(0x5620, 3), (0x5650, 14)]: f(e, a, v)
    appcheck(e, payload(), 2)
    return e


def cycle(e, call, valid=True, update_can=False, numeric_producers=None):
    p = bytearray(payload(seed=1000+call, complement=valid))
    p[4:6] = (400).to_bytes(2, 'big'); p[14] = 128
    outgoing = bytes(r(e, 0x437A+j) for j in range(38)); base = len(e.tx)
    previous_command = rf(e, 0x56A0)
    e.run(0xE86E)
    for byte in framed(p): e.rdr = byte; e.run(0xE86E)
    assert bytes(e.tx[base:]) == framed(outgoing)
    appcheck(e, p, r(e, 0x43A7), inject=False)
    want = max(0, min(65535, int(q(q(previous_command/number(0x22750))+Fraction(1,2)))))
    assert r(e, 0x437E, 2) == want
    monitor = gated_monitor(e)
    if update_can:
        active = call % 2
        _, e = paired(3200, 1600, 10040, 10060, active, e=e); w(e, 0x718C, active)
        e.run(0xA477E, limit=100000); publish(e)
    filtered_source(e)
    pre_timers(e); result = check(e); post_timers(e); gates = local_gates(e)
    angle(e)
    # Optional independently checked producers preserve observed task order:
    # 246E8, 21D18, 23A24, 245FC, then selection (257D8 still omitted).
    if numeric_producers: numeric_producers[0](e)
    override(e)
    if numeric_producers:
        for producer in numeric_producers[1:]: producer(e)
    selection = selected(e)
    return dict(call=call, mode=r(e, 0x722A), branch=result['branch'], selection=selection,
                counters=[r(e, a, 2) for a in [0x5664, 0x5666, 0x5668]],
                eligible=r(e, 0x566A), enable=r(e, 0x5676), qualified=r(e, 0x5677),
                conditional_input=r(e, 0x5354), protected_gate=r(e, 0x2110),
                monitor=monitor, gates=gates, command=float(rf(e, 0x56A0)), can_update=update_can)


def valid_record_comparison():
    e = setup_loop()
    for a in [0x210C, 0x2076, 0x2088, 0x208A]: protected_byte(e, a, 0)
    w(e, 0x722A, 1)
    rows = [cycle(e, call, update_can=True) for call in range(1, 4)]
    assert [x['branch'] for x in rows] == ['normal', 'feedback', 'feedback']
    assert all(x['conditional_input'] == x['protected_gate'] == 0 for x in rows)
    return rows


def main():
    pre_cases = 0
    for mode, prior, request, flag0, flag1, count in itertools.product(
            [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 4, 5, 6, 65534, 65535]):
        e = fixture()
        for a, v in [(0x722A, mode), (0x566E, prior), (0x93C3, request), (0x92CB, flag0), (0x932A, flag1)]:w(e, a, v)
        w(e, 0x5664, count, 2); w(e, 0x5666, count, 2)
        pre_timers(e); pre_cases += 1
    post_cases = 0
    for relative, bypass, count, port, sr in itertools.product(
            [0, 1, 2], [0, 1, 2], [0, 36, 37, 124, 199, 200, 201, 65535], [0, 0xFFFF, 0xA555], [0x20, 0xF1]):
        e = fixture(); w(e, 0x5670, relative); w(e, 0x566B, bypass); w(e, 0x5668, count, 2)
        e.registers[0xFFFFF746] = port; e.sr = sr
        post_timers(e); post_cases += 1
    filter_cases = 0
    for old, source in itertools.product([0, 5, 6, 6.5, 9.5, 10, 11, 20], repeat=2):
        e = fixture(); f(e, 0x536C, old); f(e, 0x6CB4, source)
        for _ in range(25): filtered_source(e); filter_cases += 1
    e = setup_loop()
    # Every cycle has a complete synthetic serial exchange; actual paired CAN
    # source updates at listed boundaries, retained in between.
    boundaries = {1, 2, 5, 6, 7, 624, 625, 661, 662, 673, 674, 748, 749, 824, 825, 826, 1875, 1876, 1878}
    transitions = []; checkpoints = []; last = None
    for call in range(1, 1879):
        row = cycle(e, call, update_can=call in boundaries)
        assert row['counters'][0] == call and row['counters'][1] == 0
        want = 'normal' if call < 6 else 'feedback' if call < 625 else 'relative' if call <= 1875 else 'bypass'
        assert row['branch'] == want, row
        assert row['enable'] == int(call < 825), row
        signature = (row['branch'], row['enable'], row['qualified'])
        if signature != last: transitions.append(row); last = signature
        if call in boundaries: checkpoints.append(row)
    mode_history = []
    w(e, 0x722A, 1)
    for step in range(1, 631):
        # Original protected readers set5354 for zero-filled test records.
        # With protected2110=0, mode1 is
        # rejected despite qualified reply; change this explicit upstream
        # input only after retaining and checking the rejected transition.
        if step == 4: protected_byte(e, 0x2110, 1)
        row = cycle(e, 1878+step, update_can=step in [1, 2, 3, 4, 624, 625, 630])
        assert row['counters'][:2] == [0, step]
        assert row['branch'] == ('feedback' if 4 <= step < 625 else 'normal'), row
        if step in [1, 2, 3, 4, 624, 625, 630]: mode_history.append(row)
    w(e, 0x722A, 0)
    for step in range(1, 7):
        row = cycle(e, 2508+step, update_can=step in [1, 6])
        assert row['counters'][:2] == [step, 0]
        assert row['branch'] == ('normal' if step < 6 else 'feedback'), row
        if step in [1, 6]: mode_history.append(row)
    # New loop: real failures with all local timer/enable producers executing.
    e = setup_loop(); loss = []
    for call in range(1, 38):
        row = cycle(e, call, valid=call <= 6 or call >= 34, update_can=True)
        assert row['monitor']['fault'] == int(call >= 32), row
        assert row['branch'] == ('feedback' if 6 <= call < 32 else 'normal'), row
        loss.append(row)
    e.run(0x28552); cleared = cycle(e, 38, update_can=True)
    assert cleared['branch'] == 'feedback' and cleared['monitor']['fault'] == 0
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
          pre_timer_cases=pre_cases, post_timer_gpio_cases=post_cases, filter_checks=filter_cases,
          retained_serial_cycles=2514, paired_boundary_updates=len(boundaries)+9,
          transitions=transitions, boundary_checkpoints=checkpoints, mode_history=mode_history,
          fault_lifecycle=loss, explicit_clear=cleared,
          valid_record_comparison=valid_record_comparison(),
          limits='Selected task bodies in observed relative order; full task, numeric5620/5650 producers,6CB4/mode inputs, physical GPIO/SCI1 peer and real-time rates remain open.'), indent=2))


if __name__ == '__main__': main()
