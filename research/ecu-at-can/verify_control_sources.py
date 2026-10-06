"""Original ECU lookup-input selection, override source limits and coupling.

Finite RTZ independent lookup/state oracles, original stock ROMs and reused
serial/paired-CAN harness. Complete task scheduler and physical units are open.
"""
import hashlib
import itertools
import json
import struct
from fractions import Fraction

from verify_control_overrides import (setup_loop, integrated, initialize, ECU, TCU,
                                      w, r, f, rf, q, number, fixture, protected)
from verify_model_sources import lookup1, axis
from verify_throttle_candidate import checksum
from verify_traction_flags import protected_byte


def input_map(e):
    want = lookup1(0xA35A4, rf(e, 0x6D28))
    stack = e.r[15]; e.run(0x58092)
    assert e.r[15] == stack and rf(e, 0x8010) == want
    return want


def input_select(e, protected_valid=True):
    if r(e, 0x735A) & 128:
        want = number(0xD9E8C)
        branch = 'status_bit7'
    elif r(e, 0x6536) == 0:
        want = rf(e, 0x8010)
        branch = 'mapped'
    else:
        saved = rf(e, 0x2310) if protected_valid else number(0xD9E84)
        want = min(number(0xD9E90), max(saved, rf(e, 0x8018)))
        branch = 'retained_bound'
    stack = e.r[15]; e.run(0x580AC)
    assert e.r[15] == stack and rf(e, 0x8014) == want
    return branch


def bounds(e):
    want = [lookup1(a, rf(e, 0x6D20)) for a in [0xA1A0C, 0xA1A00]]
    stack = e.r[15]; e.run(0x5C500)
    assert e.r[15] == stack
    for a, v in zip([0x8254, 0x825C], want):
        assert rf(e, a) == v; checksum(e, a)
    return want


def source_map(e):
    want = lookup1(0xA19F4, rf(e, 0x8014))
    stack = e.r[15]; e.run(0x5C53A)
    assert e.r[15] == stack and rf(e, 0x8250) == want
    return want


def bounded(e):
    source, lo, hi = [rf(e, a) for a in [0x8250, 0x8254, 0x825C]]
    # Original207C tests low first, including equality; then upper.
    want = lo if source <= lo else hi if source >= hi else source
    stack = e.r[15]; e.run(0x5C54E)
    assert e.r[15] == stack and rf(e, 0x8248) == want
    checksum(e, 0x8248)
    return want


def coupling(e):
    scale = number(0xBACA8); epsilon = number(0x39E0C)
    old = rf(e, 0x6D00)
    want = q(rf(e, 0x8248)/scale) if abs(scale) > epsilon else old
    stack = e.r[15]; e.run(0x39D24)
    assert e.r[15] == stack and rf(e, 0x6D00) == want
    return want


def sources(e):
    input_map(e); branch = input_select(e)
    bounds(e); source_map(e); bounded(e); coupling(e)
    return branch


def sample_points(descriptor):
    n = int.from_bytes(ECU[descriptor:descriptor+2], 'big')
    xp = int.from_bytes(ECU[descriptor+4:descriptor+8], 'big')
    xs = axis(xp, n)
    # Every exact knot, interior midpoint and small offset on either side.
    return sorted(set([xs[0]-100, xs[-1]+100] + xs +
                      [q((a+b)/2) for a,b in zip(xs,xs[1:])] +
                      [q(x+d) for x in xs for d in [Fraction(-1,8),Fraction(1,8)]]))


def main():
    map_cases = selector_cases = bound_cases = coupling_cases = 0
    for descriptor, address, function in [(0xA35A4,0x6D28,input_map),
            (0xA1A0C,0x6D20,bounds),(0xA19F4,0x8014,source_map)]:
        for value in sample_points(descriptor):
            e = fixture(); f(e, address, value); function(e); map_cases += 1
    for flags, mode, history, saved, corrupt in itertools.product(
            [0,1,127,128,129,255], [0,1,2,255], [-10,0,100,23819,30000],
            [-20,1000,30000], [False,True]):
        e = fixture(); w(e, 0x735A, flags); w(e, 0x6536, mode)
        f(e, 0x8010, -7); f(e, 0x8018, history); protected(e, 0x2310, saved)
        if corrupt: w(e, 0x2314, 0, 2); w(e, 0x2316, 0, 2)
        input_select(e, not corrupt); selector_cases += 1
    for source, lo, hi in itertools.product([-10,0,1,4,5,6,30,60,100], [-5,0,5,30], [4,30,60]):
        e=fixture();f(e,0x8250,source);protected(e,0x8254,lo);protected(e,0x825C,hi)
        bounded(e); bound_cases += 1
    for value in [-20,-1,0,Fraction(1,8),1,5,30,60,100]:
        e=fixture();f(e,0x8248,value);f(e,0x6D00,-99);coupling(e);coupling_cases += 1
    # Retain produced values through original priority/timer/serial pipeline.
    # Earlier bodies execute explicitly in each cycle; cross-task rate unknown.
    e=setup_loop(numeric_fixtures=False);initialize(e)
    for a in [0x210C,0x2076,0x2088,0x208A]:protected_byte(e,a,0)
    protected(e,0x2310,1000);f(e,0x8018,2000)
    f(e,0x6CB4,8);e.run(0x1DED8);w(e,0x722A,1)
    w(e,0x5634,3);w(e,0x5635,1)
    rows=[]
    boundaries={1,2,20,21,40,41,63,64,65,66,80,81,100,101,120,121,140,141,160,161,180}
    for call in range(1,181):
        if call==1:f(e,0x6D28,80);f(e,0x6D20,90)
        if call==21:f(e,0x6D28,0)
        if call==41:w(e,0x735A,128)
        if call==66:f(e,0x6D20,-30)
        if call==81:w(e,0x5635,0)
        if call==101:w(e,0x735A,0);w(e,0x6536,1);f(e,0x8018,23819)
        if call==121:w(e,0x5635,1)
        if call==141:f(e,0x6D20,120);f(e,0x8018,0);protected(e,0x2310,0)
        if call==161:w(e,0x5635,0)
        branch=sources(e)
        row=integrated(e,call,update_can=call in boundaries)
        assert row['selection']==('normal' if 81<=call<121 or call>=161 else '5672'),row
        row.update(input_branch=branch, mapped_input=float(rf(e,0x8010)),
                   selected_input=float(rf(e,0x8014)), unbounded_source=float(rf(e,0x8250)),
                   bounds=[float(rf(e,a)) for a in [0x8254,0x825C]],
                   normal_offset=float(rf(e,0x6D00)), normal_candidate=float(rf(e,0x569C)))
        if call in boundaries:rows.append(row)
    tables={}
    for a in [0xA35A4,0xA19F4,0xA1A0C,0xA1A00]:
        n,kind,pad,xp,vp=struct.unpack_from('>HBBII',ECU,a)
        tables[hex(a)]=dict(count=n,kind=kind,axis_address=hex(xp),values_address=hex(vp),
                            axis=list(map(float,axis(xp,n))),values=list(map(float,axis(vp,n))))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
          map_cases=map_cases,selector_cases=selector_cases,bound_cases=bound_cases,coupling_cases=coupling_cases,
          serial_cycles=180,paired_can_updates=len(boundaries),tables=tables,lifecycle=rows,
          limits='6D28/6D20/mode/status/2310/8018 andstage/enable remain inputs; finite RTZ only. Cross-task rate/order, upstream acquisition andphysical units/actuation unproved. Synthetic serial peer.'),indent=2))


if __name__=='__main__':main()
