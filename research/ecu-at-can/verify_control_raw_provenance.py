"""Execute ADC28/29 scales and raw-input qualification with independent RAM oracles.

Explicit routine order and result-register fixtures, not real task timing,
board/sensor identities, DSC execution or physical validation.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_control_raw_inputs as raw
import verify_control_acquisition as acquisition
from verify_control_contributions import ECU, w, r, f, rf, q, number, run
from verify_model_sources import lookup1

ROOT = Path(__file__).resolve().parent
LOW, HIGH, LONG, SHORT = ECU[0xE03AC:0xE03B0]
CHANNELS = [(28, 0x40F8, 0x40F4, 0x701C, 0x7024, 0x7064, 0xDC48C, 0xA3A30),
            (29, 0x40E4, 0x40E0, 0x6670, 0x6678, 0x66B8, 0xDC470, 0xA3A24)]


def compare(e, entry, want):
    run(e, entry)
    actual = raw.application(e)
    assert actual == want, (hex(entry), [(hex(a), actual.get(a, 0), want.get(a, 0))
        for a in actual.keys() | want.keys() if actual.get(a, 0) != want.get(a, 0)])


def scale(e, channel, initialize=False):
    index, filtered, output, init, update, classify, limits, table = channel
    assert int.from_bytes(ECU[limits+4:limits+6], 'big') == 256
    value = r(e, 0x4008+2*index, 2)
    # Stock filter gain256 passes the unsigned input unchanged.
    mapped = lookup1(table, q(value * number(0x66F4)))
    want = raw.application(e)
    raw.expected_write(want, filtered, value, 2)
    raw.expected_float(want, output, mapped)
    compare(e, init if initialize else update, want)


def classify(e, channel):
    _, filtered, _, _, _, entry, limits, _ = channel
    value = r(e, filtered, 2)
    lo = int.from_bytes(ECU[limits:limits+2], 'big')
    hi = int.from_bytes(ECU[limits+2:limits+4], 'big')
    want = 1 if value >= hi else 2 if value < lo else 0
    memory = raw.application(e)
    run(e, entry)
    assert e.r[0] == want and raw.application(e) == memory


def qualifier_model(memory, value, enabled, mode, old):
    for address, flag in [(0x8F31, value < LOW and enabled == 1),
                          (0x8F32, value > HIGH and enabled == 1), (0x8F38, False)]:
        raw.expected_write(memory, address, int(flag), 1)
    if mode == 1:
        raw.expected_write(memory, 0x8F37, 0, 1)
    elif LOW <= value <= HIGH:
        for a in [0x8F37, 0x8F38]: raw.expected_write(memory, a, 1, 1)


def qualify(e):
    want = raw.application(e)
    qualifier_model(want, r(e, 0x6CAE), r(e, 0x914B), r(e, 0x9462), r(e, 0x8F37))
    compare(e, 0x6D876, want)


def countdown(e):
    want = raw.application(e)
    reset = r(e, 0x9462) == 1 or r(e, 0x8F38) == 1
    for i in range(4):
        value = r(e, 0x8F2C+i)
        if reset: value = LONG if i < 2 else SHORT
        elif r(e, 0x8F31+i%2) == 1: value = max(0, value-1)
        raw.expected_write(want, 0x8F2C+i, value, 1)
    compare(e, 0x6D904, want)


def initialize(e):
    # Compose expectations on a separate original CPU; compare whole wrapper.
    expected = copy.deepcopy(e)
    qualify(expected)
    for i in range(4): w(expected, 0x8F2C+i, LONG if i < 2 else SHORT)
    raw.fallback_latch(expected)
    compare(e, 0x6D850, raw.application(expected))


def caller(e):
    expected = copy.deepcopy(e)
    qualify(expected); countdown(expected); raw.fallback_latch(expected)
    pc, sp, sr = 0x1B17E, e.r[15], e.sr
    for _ in range(10000):
        if pc == 0x1B190: break
        nxt, delay = e.instruction(pc)
        if delay:
            _, nested = e.instruction(pc+2)
            assert not nested
        pc = nxt
    else: raise AssertionError('caller instruction bound')
    assert e.r[15] == sp and (e.sr & ~1) == (sr & ~1)
    assert raw.application(e) == raw.application(expected)


def direct():
    counts = dict(scale=0, classify=0, qualify=0, countdown=0, initialize=0)
    for channel in CHANNELS:
        for value, old, init in itertools.product(
                [0, 1, 63, 64, 2047, 2048, 2559, 2560, 32767, 32768, 58326, 58327, 63486, 63487, 65535],
                [0, 32768, 65535], [False, True]):
            e = raw.setup(); w(e, 0x4008+2*channel[0], value, 2); w(e, channel[1], old, 2)
            scale(e, channel, init); classify(e, channel)
            counts['scale'] += 1; counts['classify'] += 1
        for count in range(1024):
            e = raw.setup(); w(e, 0x4008+2*channel[0], count<<6, 2)
            scale(e, channel); classify(e, channel)
            counts['scale'] += 1; counts['classify'] += 1
    for value, enabled, mode in itertools.product(range(256), [0, 1, 2, 255], [0, 1, 2, 255]):
        e = raw.setup()
        for a, v in [(0x6CAE,value), (0x914B,enabled), (0x9462,mode), (0x8F37,255), (0x8F38,255)]: w(e,a,v)
        qualify(e); counts['qualify'] += 1
    rng = random.Random(0x6D904)
    for _ in range(2048):
        e = raw.setup()
        for a in [0x9462,0x8F38,0x8F31,0x8F32]: w(e,a,rng.choice([0,1,2,255]))
        for a in range(0x8F2C,0x8F30): w(e,a,rng.choice([0,1,2,3,49,50,127,128,255]))
        countdown(e); counts['countdown'] += 1
    for value, mode in itertools.product([0,LOW,HIGH,255], [0,1,2,255]):
        e = raw.setup()
        for a in range(0x8F2C,0x8F39): w(e,a,255)
        w(e,0x6CAE,value); w(e,0x9462,mode); w(e,0x914B,1)
        initialize(e); counts['initialize'] += 1
    return counts


def retained():
    e = acquisition.setup(); rows=[]
    w(e,0x914B,1); w(e,0x6CAE,128); initialize(e)
    f(e,0x67E0,7); f(e,0x6D5C,23)
    for call in range(1,181):
        # Low/high runs, qualification suspended, inclusive recovery endpoints,
        # and exact-one mode reset. Call ordering is an explicit fixture.
        count = 0 if call <= 60 else LOW*4 if call == 61 else 1023 if call <= 125 else HIGH*4 if call == 126 else 0
        enabled = 2 if 3 <= call <= 7 else 1
        mode = 1 if call == 150 else 0
        w(e,0x914B,enabled); w(e,0x9462,mode)
        samples=[0]*32; samples[28]=600<<6; samples[29]=count<<6
        acquisition.acquire(e,samples); acquisition.decode(e)
        for channel in CHANNELS: scale(e,channel)
        caller(e)
        raw.first(e); raw.second(e); branch=raw.target.source(e)
        rows.append(dict(call=call,count29=count,enabled=enabled,mode=mode,
            counters=[r(e,0x8F2C+i) for i in range(4)],
            flags={hex(a):r(e,a) for a in range(0x8F30,0x8F39)},
            raw40e0=float(rf(e,0x40E0)),published6d40=float(rf(e,0x6D40)),
            target=float(rf(e,0x67E4)),branch=branch))
    by={row['call']:row for row in rows}
    assert by[2]['counters'][2] == by[7]['counters'][2] == 1
    assert by[7]['flags']['0x8f30'] == 0 and by[8]['flags']['0x8f30'] == 1
    for call in [61,126,150]:
        assert by[call]['flags']['0x8f30'] == 0
        assert by[call]['counters'] == [LONG,LONG,SHORT,SHORT]
    assert by[55]['flags']['0x8f33'] == 1
    assert by[64]['flags']['0x8f30'] == 1
    assert by[111]['flags']['0x8f34'] == 1
    assert by[153]['flags']['0x8f30'] == 1
    return rows


def main():
    counts=direct(); print(counts,flush=True)
    rows=retained()
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),counts=counts,
        qualification_constants=dict(low=LOW,high=HIGH,long=LONG,short=SHORT),
        retained_cycles=len(rows),retained=rows,
        limits='Original callers and actual cadence, 914B writer, 8EF8 qualification, board wiring, units, remote DSC, and physical behavior remain open.')
    (ROOT/'control-raw-provenance-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Retained',len(rows),flush=True)


if __name__ == '__main__': main()
