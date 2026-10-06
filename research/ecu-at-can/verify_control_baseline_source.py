"""Execute the retained 809C baseline source and its transmission-mode maps.

Original ROM bodies, independent finite RTZ oracles and explicit cross-task
scheduling. Physical signal meanings and production task rates remain open.
"""
import hashlib
import itertools
import json
from fractions import Fraction

from verify_control_input_history import (
    ECU, TCU, w, r, f, rf, q, number, fixture, run, setup_loop, initialize,
    protected_byte, init_history, baseline, initialize_records, group,
    publish_records, inputs, ratio, remainder, input_map, hysteresis,
    input_select, timer, holdoff, decay, bounds, source_map, bounded, coupling,
    integrated)
from verify_model_sources import lookup1, lookup2, map2_info, axis
from verify_control_sources import sample_points


def countdown(e):
    old = r(e, 0x80A8)
    want = ECU[0xDA03C] if r(e, 0x7010) == 1 else max(0, old-1)
    run(e, 0x58B9C)
    assert r(e, 0x80A8) == want


def target(e):
    old = [rf(e, a) for a in [0x80AC, 0x80B0]] + [r(e, 0x80B8)]
    enabled = (r(e, 0x7346) != 1 and r(e, 0xA3A4) != 1 and
               (r(e, 0x80A8) != 0 or r(e, 0x7012) != 0))
    descriptor = None
    if enabled:
        descriptor = 0xA3628 if r(e, 0x734A) & 0x40 or r(e, 0x7EEE) > 0 else 0xA363C
        mapped = lookup2(descriptor, rf(e, 0x6DB4), rf(e, 0x6CD4))
        knots = axis(0xDA1BC, 8)
        index = max(0, sum(rf(e, 0x6D28) >= x for x in knots)-1)
        scale = number(0xDA1DC+4*index)
        want = q(q(mapped*scale)/number(0x58DB8))
        side = [mapped, scale, index]
    else:
        want, side = 0, old
    run(e, 0x58BD0)
    assert rf(e, 0x80A0) == want
    assert [rf(e, a) for a in [0x80AC, 0x80B0]] + [r(e, 0x80B8)] == side
    return descriptor


def raise_source(e):
    enabled = r(e, 0xA3A4) != 1 and (r(e, 0x7012) != 0 or r(e, 0x80A8) != 0)
    want = max(rf(e, 0x809C), rf(e, 0x80A0)) if enabled else 0
    run(e, 0x58D44)
    assert rf(e, 0x809C) == want


def scale_source(e):
    mapped = lookup1(0xA35E0, rf(e, 0x6D5C))
    want = q(rf(e, 0x809C)*mapped)
    run(e, 0x58B78)
    assert rf(e, 0x80B4) == mapped == 1
    assert rf(e, 0x8098) == want


def decay_step(e):
    if r(e, 0x80A8) > 0 and r(e, 0x7010) == 0:
        descriptor = 0xA35EC
    elif r(e, 0x7EEE) != 0:
        descriptor = 0xA35F8
    elif r(e, 0x75DC) == 1:
        descriptor = 0xA3610
    else:
        descriptor = 0xA3604
    want = lookup1(descriptor, rf(e, 0x6DB4))
    run(e, 0x58DD8)
    assert rf(e, 0x80A4) == want
    return descriptor


def lower_source(e):
    old = rf(e, 0x809C)
    if not r(e, 0x734A) & 0x40 and old < number(0xDA040):
        want = 0
    else:
        floor = 0 if r(e, 0x7346) == 1 else rf(e, 0x80A0)
        want = max(q(old-rf(e, 0x80A4)), floor)
    run(e, 0x58E68)
    assert rf(e, 0x809C) == want


def source_group(e):
    countdown(e)
    selected = target(e)
    raise_source(e)
    scale_source(e)
    return selected


def main():
    counts = dict(countdown=0, target_gates=0, target_maps=0, rise=0, scale=0,
                  decay_maps=0, decay=0)
    for flag, old in itertools.product([0, 1, 2, 255], range(256)):
        e = fixture(); w(e, 0x7010, flag); w(e, 0x80A8, old)
        countdown(e); counts['countdown'] += 1
    for a,b,c,d,mode,extra in itertools.product([0,1,2], [0,1,2], [0,1], [0,1,2], [0x40,0x80,0xC0], [0,1]):
        e = fixture()
        for address,value in [(0x7346,a),(0xA3A4,b),(0x80A8,c),(0x7012,d),(0x734A,mode),(0x7EEE,extra)]:
            w(e,address,value)
        f(e,0x6DB4,1750); f(e,0x6CD4,20); f(e,0x6D28,20)
        f(e,0x80AC,7); f(e,0x80B0,8); w(e,0x80B8,9)
        target(e); counts['target_gates'] += 1
    temperatures = sample_points(0xA361C)
    for mode, descriptor in [(0x40,0xA3628),(0x80,0xA363C)]:
        xs,ys,_ = map2_info(descriptor)
        points = lambda a: [a[0]-1,a[-1]+1]+a+[q((x+y)/2) for x,y in zip(a,a[1:])]
        for i,(x,y) in enumerate(itertools.product(points(xs),points(ys))):
            e=fixture(); w(e,0x7012,1); w(e,0x7346,0); w(e,0x734A,mode)
            f(e,0x6DB4,x); f(e,0x6CD4,y); f(e,0x6D28,temperatures[i%len(temperatures)])
            target(e); counts['target_maps'] += 1
    for flag,mode,count,old,value in itertools.product([0,1,2],[0,1,2],[0,1],[-1,0,Fraction(1,16),1],[-1,0,Fraction(1,32),1]):
        e=fixture(); w(e,0xA3A4,flag); w(e,0x7012,mode); w(e,0x80A8,count)
        f(e,0x809C,old); f(e,0x80A0,value)
        raise_source(e); counts['rise'] += 1
    for x,old in itertools.product(sample_points(0xA35E0),[-1,0,Fraction(1,32),1,16]):
        e=fixture(); f(e,0x6D5C,q(x)); f(e,0x809C,old)
        scale_source(e); counts['scale'] += 1
    for count,flag,extra,special in itertools.product([0,1],[0,1,2],[0,1,2],[0,1,2]):
        for x in sample_points(0xA35EC):
            e=fixture()
            for address,value in [(0x80A8,count),(0x7010,flag),(0x7EEE,extra),(0x75DC,special)]:w(e,address,value)
            f(e,0x6DB4,x); decay_step(e); counts['decay_maps'] += 1
    for mode,enabled,old,step,floor in itertools.product([0,0x40,0x80,0xC0],[0,1,2],[-1,0,Fraction(1,32),1],[0,Fraction(1,64),1],[-1,0,Fraction(1,16)]):
        e=fixture(); w(e,0x734A,mode); w(e,0x7346,enabled)
        f(e,0x809C,old); f(e,0x80A4,step); f(e,0x80A0,floor)
        lower_source(e); counts['decay'] += 1
    # Start the retained source at zero using its original clear branch.
    e=setup_loop(numeric_fixtures=False); initialize(e); init_history(e)
    for a in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,a,0)
    w(e,0xA3A4,1); raise_source(e); w(e,0xA3A4,0)
    f(e,0x7020,1500); f(e,0x6DB4,1500); f(e,0x6CD4,0)
    f(e,0x80C4,Fraction(1,2)); baseline(e); initialize_records(e)
    f(e,0x6CB4,8); e.run(0x1DED8); w(e,0x722A,1); w(e,0x6536,1)
    w(e,0x5634,3); w(e,0x5635,1); w(e,0x8194,1)
    w(e,0x7346,0); w(e,0x7012,1); w(e,0x7016,1); w(e,0x734A,0x80)
    f(e,0x6D28,80); f(e,0x6D20,90); f(e,0x6C20,0)
    boundaries={1,2,10,11,20,21,30,31,40,41,50,51,60,61,70,71,80,81,100,101,120,140}
    rows=[]
    for call in range(1,141):
        if call==11:f(e,0x6CD4,40)  # raise AT map target
        if call==21:f(e,0x6DB4,2500); f(e,0x6CD4,25)  # lower target
        if call==31:w(e,0x7346,1)  # target zero, separately decaying history
        if call==51:w(e,0x7346,0); w(e,0x7EEE,1)
        if call==61:w(e,0xA3A4,1)  # clear branch in the rise task
        if call==71:w(e,0xA3A4,0); w(e,0x7EEE,0); f(e,0x6DB4,1500)
        if call==81:w(e,0x7012,0)  # clear with stock countdown zero
        if call==101:w(e,0x7012,2); w(e,0x75DC,1)
        gate_before=r(e,0xA3A4)
        selected=source_group(e)
        before=rf(e,0x809C)
        group(e); inputs(e); ratio(e); remainder(e); input_map(e); hysteresis(e); input_select(e)
        timer(e); holdoff(e); decay(e); bounds(e); source_map(e); bounded(e); coupling(e)
        row=integrated(e,call,update_can=call in boundaries)
        # The paired publication helper explicitly resets A3A4 to zero.
        # Its before/after values are fixture actions, not a firmware writer.
        # The decay task and history publisher run at a synthetic cadence.
        # Local order matches their callers; cross-task phase is not established.
        step_map=decay_step(e); lower_source(e); publish_records(e)
        if call in boundaries:
            row.update(target_map=hex(selected) if selected else None,
                       source_gate_before=gate_before,source_gate_after=r(e,0xA3A4),
                       target=float(rf(e,0x80A0)),source_used=float(before),
                       source_after_decay=float(rf(e,0x809C)),step_map=hex(step_map),
                       step=float(rf(e,0x80A4)),baseline=float(rf(e,0x80BC)),
                       baseline_component=float(rf(e,0x80C0)),current=float(rf(e,0x8048)))
            rows.append(row)
    tables={}
    for descriptor in [0xA35E0,0xA35EC,0xA35F8,0xA3604,0xA3610,0xA361C]:
        n=int.from_bytes(ECU[descriptor:descriptor+2],'big')
        xp=int.from_bytes(ECU[descriptor+4:descriptor+8],'big'); vp=int.from_bytes(ECU[descriptor+8:descriptor+12],'big')
        tables[hex(descriptor)]=dict(axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n))))
    for descriptor in [0xA3628,0xA363C]:
        xs,ys,vp=map2_info(descriptor)
        tables[hex(descriptor)]=dict(x=list(map(float,xs)),y=list(map(float,ys)),values=list(map(float,axis(vp,len(xs)*len(ys)))))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        cases=counts,serial_cycles=140,paired_can_updates=len(boundaries),tables=tables,lifecycle=rows,
        limits='Original six producer bodies; source809C initialized by original clear branch. Other baseline contributions, source/status inputs, cross-task cadence and serial peer remain fixtures. Paired publication helper resets A3A4 to0 at CAN updates; this is not an executed firmware gate writer. No hardware or physical-signal attribution.'),indent=2))


if __name__ == '__main__':
    main()
