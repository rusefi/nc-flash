"""Original filtered input25 -> source selection -> phase mode -> CAN216/ECU.

Peripheral reads and task cadence are explicit samples. Complete source-policy
bodies execute against independent models; no source/mode result is injected.
Physical switch identity, actual scheduler and remote ECU actuation stay open.
"""
import itertools
import json
import random

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_maps import interpolate
from verify_tcu_phase_mode import ObservedMode
from verify_tcu_ascending_map import lifecycle
from verify_tcu_request_admission import paired_snapshot


def word(address):
    return int.from_bytes(TCU[address:address+2], 'big')


def word_curve(address, axis):
    count, shift = word(address), word(address+2)
    assert count == 11 and shift == 0
    axes = [word(address+4+2*i) for i in range(count)]
    values = [word(address+4+2*count+2*i) for i in range(count)]
    return interpolate(axis & 65535, axes, values)


CURVES = {
    0x498F6: (0x7533C, 0x7542C, False),
    0x49960: (0x7551C, 0x7560C, True),
    0x499A4: (0x756FC, 0x757EC, True),
    0x499E2: (0x758DC, 0x759CC, True),
    0x49A20: (0x75ABC, 0x75BAC, False),
    0x49A8C: (0x75C9C, 0x75D8C, True),
}


def threshold(function, state, source, flags, axis):
    first, second, decrement = CURVES[function]
    bank = min(((state & 255)-int(decrement)) & 255, 4)
    special = bool(flags & 4) if function == 0x49960 else source == 17
    return word_curve((first if special else second)+48*bank, axis)


BYTE_FIELDS = [0x8080, 0x8083, 0x8084, 0x9316, 0x916D, 0x916F,
               0x9B40, 0x9B3D, 0x9C90, 0x9C91, 0x9C92, 0x9C93,
               0x9C94, 0x9AEA, 0x82AD, 0x92C5, 0x92D2, 0x92C7, 0x6277]
WORD_FIELDS = [0x80EA, 0x809C, 0x9C96]
INNER_OUTPUTS = [0x9C90, 0x9C92, 0x9C93, 0x82AD]
OUTER_OUTPUTS = INNER_OUTPUTS + [0x9B40, 0x9C91, 0x9C94, 0x9AEA, 0x9C96]


def inputs(t):
    return {**{a: r(t, a) for a in BYTE_FIELDS},
            **{a: r(t, a, 2) for a in WORD_FIELDS}}


def inner_model(d, requested, state, operation):
    """496F0 policy, including retained flags, timer reset and cache fallback."""
    requested &= 255
    measured, axis = d[0x80EA], d[0x9C96]
    source, flags = d[0x9B40], d[0x916F]
    lookup = lambda function, value: threshold(function, value, source, flags, axis)
    edge = int(bool(d[0x92C5] & 2))
    held = 0
    if d[0x8083] == 1 and requested < 5:
        if measured >= lookup(0x498F6, requested):
            requested += 1
            state, operation = 1, 10
            if measured < lookup(0x499A4, requested):
                d[0x9C92] = 1
    elif d[0x8083] == 2 and requested > 0:
        if measured < lookup(0x49960, requested):
            requested -= 1
            state, operation = 1, 10
            d[0x9C92] = 0
        else:
            held = 1
    d[0x9C90] = held
    if d[0x9C92] == 1:
        if requested > 0:
            if measured >= lookup(0x499A4, requested):
                if d[0x82AD] > TCU[0x75336+requested-1]:
                    d[0x9C92] = 0
            else:
                d[0x82AD] = 0
    elif requested > 0 and measured < lookup(0x499E2, requested):
        requested -= 1
        state, operation = 2, 10
    if (requested < 5 and measured >= lookup(0x49A20, requested)
            and (TCU[0x7736D] == 1 or edge) and d[0x92D2] & 1):
        requested += 1
        state, operation = 2, 10
    if TCU[0x7736C] == 1 and edge and edge != d[0x9C93]:
        for _ in range(5):
            if requested <= 0 or measured >= lookup(0x49A8C, requested):
                break
            requested -= 1
            state, operation = 2, 10
    d[0x9C93] = edge
    if ((d[0x92C7] & 64 or d[0x6277] == 1)
            and measured <= word(0x7736E) and requested >= 1):
        requested = 0
        state, operation = 2, 10
        d[0x9C92] = 0
    return min(requested & 255, 5), state, operation


def outer_model(d, requested, operation):
    """495C0, observing pair arguments without publishing accepted8081."""
    enabled = d[0x9316] & 1
    admitted = enabled == 1 and d[0x8080] == 6 and not d[0x916D] & 8
    d[0x9C96] = (d[0x809C]*2) & 65535
    state, special = 0, False
    if admitted:
        special = d[0x9B40] == 6
        d[0x9B40] = 17 if special else 10
        requested, operation = d[0x8084], d[0x9B3D]
        if not d[0x9C94]:
            d[0x9C92] = d[0x9C93] = 0
            if (requested > 0 and d[0x9C96] < word(0x7532C+2*(requested-1))
                    and d[0x80EA] < threshold(0x49960, requested, d[0x9B40],
                                             d[0x916F], d[0x9C96])):
                requested -= 1
                state, operation = 1, 10
        requested, state, operation = inner_model(d, requested, state, operation)
    d[0x9C94] = enabled
    d[0x9C91] = state
    d[0x9AEA] = (d[0x9AEA] & ~10) | (2 if admitted else 0) | (8 if special else 0)
    return requested, operation


def check_outer(t, pointer=0xFFFFA900):
    d = inputs(t)
    requested, operation = t.read(pointer, 1), t.read(pointer+1, 1)
    pair = outer_model(d, requested, operation)
    t.r[5] = pointer+1
    t.run(0x495C0, pointer, limit=1000000)
    actual = (t.read(pointer, 1), t.read(pointer+1, 1))
    assert actual == pair, (actual, pair, d)
    for a in OUTER_OUTPUTS:
        assert r(t, a, 2 if a in WORD_FIELDS else 1) == d[a], (hex(a), d)
    return pair


class SampledSelection(ObservedMode):
    """Five original input acquisition registers, with explicit read-only values."""
    def __init__(self):
        super().__init__()
        self.samples = {0xFFFFF778: 0x1C, 0xFFFFF810: 500 << 6,
                        0xFFFFF812: 500 << 6, 0xFFFFF76C: 0, 0xFFFFF746: 0}
        self.source_checks = 0
        self.pending_source = None

    def read(self, address, size):
        if address in self.samples:
            assert size == 2
            return self.samples[address]
        return super().read(address, size)

    def instruction(self, pc):
        if pc == 0x495C0:
            d = inputs(self)
            p, q = self.r[4], self.r[5]
            pair = outer_model(d, self.read(p, 1), self.read(q, 1))
            self.pending_source = (p, q, pair, d)
        if pc == 0x496B8:
            p, q, expected, d = self.pending_source
            assert (self.read(p, 1), self.read(q, 1)) == expected
            for a in OUTER_OUTPUTS:
                assert r(self, a, 2 if a in WORD_FIELDS else 1) == d[a], hex(a)
            self.source_checks += 1
            self.pending_source = None
        return super().instruction(pc)


def sample(t, enabled, adc=500):
    # Active-low input3 asserted, active-high input25 controlled independently.
    t.samples[0xFFFFF778] = 0x1C | (int(enabled) << 11)
    t.samples[0xFFFFF812] = adc << 6
    for function in [0x17250, 0x174A0, 0x17D60, 0x22416]:
        t.run(function, limit=1000000)
    return dict(input25=r(t, 0x8818+5*25), status25=r(t, 0x881A+5*25),
                published=r(t, 0x89A4), status89a5=r(t, 0x89A5),
                enable=r(t, 0x9316) & 1, selection_class=r(t, 0x8080))


def manager_traces(t_factory=SampledSelection):
    traces = []
    measured = {80:5000,81:6000,84:5900,86:5750,88:5500,90:5250,
                92:5100,94:5051,96:5050,98:5000,150:6500,151:7000,
                160:6750,162:6600,164:6551,166:6550,168:6500}
    for enabled in [0,1]:
        t = t_factory()
        source_rows, ring_rows = [], []
        previous_ring = None
        def upstream(t, call):
            if call == 1:
                t.run(0x17230); t.run(0x17D54)
                # The full selection pipeline creates a second code0 record.
                # Supply that record's target reference as an explicit input.
                w(t, 0x921C, 6500, 4)
            row = sample(t, enabled)
            for function in [0x44CFE, 0x48C08]: t.run(function, limit=1000000)
            row.update(source=r(t,0x9B40), state=r(t,0x9C91), mode=r(t,0x8086),
                       proposed=r(t,0x8084), accepted=r(t,0x8081))
            if not source_rows or {k:v for k,v in source_rows[-1].items() if k!='call'} != row:
                source_rows.append(dict(call=call, **row))
        def observe(t, call, subcall):
            nonlocal previous_ring
            head, count = r(t,0x96C4), r(t,0x96C5)
            active = {(head+i)%16 for i in range(count)}
            records = [dict(index=i, code=r(t,0x95DE+15*i),
                            phase=r(t,0x95E1+15*i), active=i in active) for i in [0,1]]
            state = dict(head=head, count=count, records=records,
                         source915a=r(t,0x915A,2), mode=r(t,0x8086))
            if state != previous_ring:
                ring_rows.append(dict(call=call, subcall=subcall, **state, **paired_snapshot(t)))
                previous_ring = state
        trace = lifecycle(25000, samples=measured, t=t, calls=320,
                          upstream=upstream, observe=observe)
        assert t.pending_source is None and t.source_checks == 320
        assert ring_rows[0]['count'] == 2 and ring_rows[-1]['count'] == 0
        traces.append(dict(sample25=enabled, input_changes=source_rows, trace=trace,
                           ring_checkpoints=ring_rows, numeric_entries=t.numeric_entries,
                           source_checks=t.source_checks, mode_checks=len(t.mode_checks),
                           initial_checks=t.initial_checks, phase_checks=len(t.phase_checks),
                           release_checks=len(t.release_checks)))
    return traces


def main():
    gate_cases = 0
    t = SHRotate(TCU)
    for argument, state, flags in itertools.product(range(256), [0, 1, 2, 4, 5, 6, 255], [0, 8, 247, 255]):
        w(t, 0x8080, state); w(t, 0x916D, flags)
        assert t.run(0x498D2, argument) == int(argument == 1 and state == 6 and not flags & 8)
        gate_cases += 1
    application_cases = 0
    for value, old, mask in itertools.product(range(256), [0, 1, 85, 170, 255], [0, 1, 8, 15]):
        w(t, 0x89A4, value); w(t, 0x9316, old)
        for i in range(4): w(t, 0x88B4+i, int(bool(mask & (1 << i))))
        t.run(0x22416)
        assert r(t, 0x9316) & 1 == int(value != 0)
        application_cases += 1
    curve_cases = 0
    for function, state, source, flags in itertools.product(CURVES, [0, 1, 2, 3, 4, 5, 6, 255], [0, 17], [0, 4]):
        first, second, decrement = CURVES[function]
        bank = min(((state- int(decrement)) & 255), 4)
        address = first+48*bank
        axes = [word(address+4+2*i) for i in range(11)]
        samples = sorted({0, 65535, *axes, *(max(a-1, 0) for a in axes),
                          *(min(a+1, 65535) for a in axes),
                          *((a+b)//2 for a, b in zip(axes, axes[1:]))})
        w(t, 0x9B40, source); w(t, 0x916F, flags)
        for axis in samples:
            w(t, 0x9C96, axis, 2)
            actual = t.run(function, state, limit=1000000)
            expected = threshold(function, state, source, flags, axis)
            assert actual == expected, (hex(function), state, axis, actual, expected)
            curve_cases += 1
    rng = random.Random(0x495C0)
    inner_cases = outer_cases = 0
    boundary_measurements = [0, 1116, 1117, 1396, 1397, 1920, 1921, 3258,
                             3259, 4190, 4191, 4656, 4657, 4672, 7448,
                             7449, 7728, 7729, 23279, 23744, 32768, 65535]
    for requested, control, source, measured, latched in itertools.product(
            range(6), [0, 1, 2, 255], [10, 17], boundary_measurements, [0, 1]):
        for a in BYTE_FIELDS: w(t, a, rng.randrange(256))
        for a in WORD_FIELDS: w(t, a, rng.randrange(65536), 2)
        for a, v in [(0x8083, control), (0x9B40, source), (0x9C92, latched),
                     (0x9C93, rng.randrange(2)), (0x6277, rng.randrange(3))]: w(t, a, v)
        w(t, 0x80EA, measured, 2)
        state, operation = rng.randrange(3), rng.randrange(256)
        w(t, 0xA900, state); w(t, 0xA901, operation)
        d = inputs(t)
        expected = inner_model(d, requested, state, operation)
        t.r[5], t.r[6] = 0xFFFFA900, 0xFFFFA901
        actual = (t.run(0x496F0, requested, limit=1000000), r(t, 0xA900), r(t, 0xA901))
        assert actual == expected, (requested, control, measured, actual, expected, d)
        for a in INNER_OUTPUTS: assert r(t, a) == d[a], (hex(a), d)
        inner_cases += 1
    for enabled, state, inhibit, source, requested, previous in itertools.product(
            [0, 1, 2, 3], [0, 6, 255], [0, 8], [0, 6, 10, 17], range(6), [0, 1]):
        for a in BYTE_FIELDS: w(t, a, rng.randrange(256))
        for a in WORD_FIELDS: w(t, a, rng.randrange(65536), 2)
        for a,v in [(0x9316, enabled), (0x8080, state), (0x916D, inhibit),
                    (0x9B40, source), (0x8084, requested), (0x9C94, previous),
                    (0x8083, rng.randrange(3)), (0x9C92, rng.randrange(2)),
                    (0x9C93, rng.randrange(2)), (0x6277, rng.randrange(3))]: w(t, a, v)
        w(t, 0x80EA, rng.choice(boundary_measurements), 2)
        w(t, 0x809C, rng.choice([0, 511, 512, 20000, 32768, 65535]), 2)
        w(t, 0xA900, rng.randrange(6)); w(t, 0xA901, rng.randrange(256))
        check_outer(t)
        outer_cases += 1
    t = SampledSelection(); t.run(0x17230); t.run(0x17D54)
    input_trace = []
    for enabled, adc in [(0,500), (0,500), (1,500), (1,500), (0,372),
                         (0,372), (0,372), (0,500), (0,500), (1,500), (1,500)]:
        input_trace.append(dict(sample=enabled, adc=adc, **sample(t,enabled,adc)))
    assert [x['enable'] for x in input_trace] == [0,0,0,1,1,1,1,1,0,0,1]
    assert all(x['status89a5'] == 2 for x in input_trace)
    assert [x['status25'] for x in input_trace[4:7]] == [3,3,3]
    traces = manager_traces()
    print(json.dumps(dict(scope=__doc__, gate_cases=gate_cases,
        application_cases=application_cases, curve_cases=curve_cases,
        inner_policy_cases=inner_cases, source_policy_cases=outer_cases,
        input_trace=input_trace, manager_calls=640, manager_traces=traces,
        limits='GPIO/ADC values, task cadence, initial creation and ECU coefficients are fixtures. Full44CFE/48C08 execute in periodic traces, but the whole scheduler/hardware is not modeled. Physical input25 identity and source meaning remain unproved.'), indent=2))


if __name__ == '__main__':
    main()
