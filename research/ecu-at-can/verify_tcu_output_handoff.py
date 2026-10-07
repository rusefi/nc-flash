"""Execute TCU feedback correction through the original peripheral word write.

Four write-only MMIO sinks and four explicit ADC words are added locally. No physical actuator,
timer behavior or feedback source is simulated. ROM, shared ISA and existing
verifiers remain unchanged. Reference formulas independently predict all RAM
and the exact output address/value; nested arithmetic executes from ROM.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_output_service as prior
from verify_tcu_output_service import TCU, w, r, s, ram, trunc, clamp, execute, signed
from sh_extract import SHExtract

ROOT = Path(__file__).resolve().parent
TARGETS = [0xFFFFF510, 0xFFFFF512, 0xFFFFF516, 0xFFFFF514]
ADC = [0xFFFFF800, 0xFFFFF802, 0xFFFFF804, 0xFFFFF806]
assert [int.from_bytes(TCU[a:a+4], 'big') for a in range(0x5C588, 0x5C598, 4)] == TARGETS
assert [int.from_bytes(TCU[a:a+4], 'big') for a in range(0x5C568, 0x5C578, 4)] == ADC


class OutputSink(SHExtract):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address in ADC:
            if size != 2 or address not in self.adc_samples:
                raise ValueError('Explicit ADC word sample required')
            self.adc_reads.append(address)
            return self.adc_samples[address]
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address in TARGETS:
            if size != 2:
                raise ValueError('Output sink accepts word writes only')
            self.output_writes.append((address, value & 65535))
            return
        super().write(address, value, size)


def attach(t):
    assert type(t) is SHExtract
    t.__class__ = OutputSink
    t.output_writes = []
    t.adc_samples = {}; t.adc_reads = []
    return t


def fixture(): return attach(prior.fixture())
def u32(v): return v & 0xFFFFFFFF
def sd(n, d): return trunc(signed(n), d)
def ud(n, d): return u32(n) // d


def clamp_word(value, low, high, unsigned=False):
    # Helpers compare word interpretations but return the original register.
    convert = (lambda v: v & 65535) if unsigned else (lambda v: signed(v, 16))
    if convert(low) > convert(high): low, high = high, low
    if convert(value) <= convert(low): return low
    if convert(value) > convert(high): return high
    return value


def equal(t, ref):
    aa, bb = ram(t), ram(ref)
    assert aa == bb, {hex(a): (aa.get(a, 0), bb.get(a, 0))
                      for a in set(aa) | set(bb) if aa.get(a, 0) != bb.get(a, 0)}
    assert t.output_writes == ref.output_writes, (t.output_writes, ref.output_writes)
    assert t.adc_reads == ref.adc_reads


def calibration_model(t):
    checksum = signed(s(t, 0x63C8) - 1456 + sum(s(t, a) for a in range(0x63B8, 0x63C8, 2)), 16)
    valid = checksum == s(t, 0x63CA)
    for i in range(4):
        w(t, 0x8A4C + 2*i, clamp(s(t, 0x63B8 + 2*i), 900, 1100) if valid else 1000, 2)
        w(t, 0x8A54 + 2*i, clamp(s(t, 0x63C0 + 2*i), -100, 100) if valid else 0, 2)
    w(t, 0x8ABC, int(not valid))


def init_model(t):
    for i in range(4):
        for a, source in [(0x8A6C, 0x5F87C), (0x8A74, 0x5F87C),
                          (0x8A7C, 0x5F884), (0x8A84, 0x5F884),
                          (0x8A8C, 0x5F88C), (0x8A94, 0x5F88C)]:
            w(t, a + 2*i, prior.word(source + 2*i), 2)
        for a, value in [(0x8A34, 100), (0x8A3C, 0), (0x8A64, 0), (0x8A44, 0)]:
            w(t, a + 2*i, value, 2)
        w(t, 0x8A9C + 4*i, 0, 4); w(t, 0x8ABD + i, 0)
    for a, value in [(0x8AB4, 100), (0x8AB6, -100), (0x8AB8, 50), (0x8ABA, -50),
                     (0x8AD8, 1000), (0x8ACA, 1), (0x8ACC, 3), (0x8AD0, 0)]:
        w(t, a, value, 2)
    calibration_model(t)
    w(t, 0x8AD4, 0x5F84C, 4); w(t, 0x8ACE, 0)


def initialize(t):
    ref = copy.deepcopy(t); init_model(ref); execute(t, 0x18754); equal(t, ref)


def accumulator(error, gain, old, bound):
    value = signed(old + signed(error, 16) * (gain & 65535))
    limit = signed(bound, 16) * 1000
    return -limit if value < -limit else limit if value > limit else value


def peripheral_model(t, i, value):
    supply, offset = r(t, 0xA518, 2), s(t, 0x8A44 + 2*i)
    raw = 0x8221 if supply == 0 else ud((0x8235-offset) * signed(value, 16), supply) + offset
    output = clamp_word(u32(raw), 0, 0x8221, unsigned=True) & 65535
    t.output_writes.append((TARGETS[i], output))
    return output


def handoff_model(t, i, wrapper=True):
    j = 2*i
    base = sd(r(t, 0xA5D4+j, 2) * r(t, 0x8A6C+j, 2), 1000)
    measured = ud(r(t, 0x8A64+j, 2) * s(t, 0x8A4C+j), 1000)
    measured = ud(measured * r(t, 0x8AD8, 2), 0xB82) + s(t, 0x8A54+j)
    w(t, 0x8A3C+j, measured, 2)
    error = signed(s(t, 0xA5E4+j) - s(t, 0x8A3C+j), 16)
    w(t, 0x8A34+j, error, 2)
    proportional = clamp_word(sd(error * r(t, 0x8A7C+j, 2), 1000), -base, base)
    integral = accumulator(error, r(t, 0x8A8C+j, 2), s(t, 0x8A9C+4*i, 4), base)
    w(t, 0x8A9C+4*i, integral, 4)
    correction = sd(integral, 1000)
    inhibit = r(t, 0xA5A0) == 1
    reset = False
    if r(t, 0x8A60+i) == 1:
        test = signed(base - prior.word(0x5C5EA) + correction, 16)
        invalid = not 68 <= r(t, 0x8A2C+j, 2) <= 1000
        limited = r(t, 0xA518, 2) < 10500 and error > 0 and test >= r(t, 0xA518, 2)
        if invalid or limited or inhibit:
            reset = True; w(t, 0x8A5C+i, 1)
        else:
            reset = bool(r(t, 0x8A5C+i)); w(t, 0x8A5C+i, 0)
        if reset:
            proportional = 0
            correction = sd(signed(base, 16) * 20, 80)
            w(t, 0x8A9C+4*i, signed(correction, 16) * 1000, 4)
    elif inhibit:
        proportional = correction = 0
        w(t, 0x8A9C+4*i, 0, 4)
    output = clamp_word(base + proportional + correction, 0, s(t, 0xA518))
    w(t, 0x8AAC+j, output, 2)
    hardware = peripheral_model(t, i, s(t, 0x8AAC+j))
    if wrapper: w(t, 0x8A64+j, 0, 2)
    return dict(base=base, measured=s(t, 0x8A3C+j), error=error,
                proportional=proportional, correction=correction, reset=reset,
                accumulator=s(t, 0x8A9C+4*i, 4), output=s(t, 0x8AAC+j),
                peripheral_address=hex(TARGETS[i]), peripheral_value=hardware)


def handoff(t, i, wrapper=True):
    ref = copy.deepcopy(t); row = handoff_model(ref, i, wrapper)
    execute(t, 0x18816 if wrapper else 0x18A44, i+1 if wrapper else i)
    equal(t, ref)
    return row


def acquire(t, values):
    assert len(values) == 4 and all(0 <= v <= 65535 for v in values)
    t.adc_samples = dict(zip(ADC, values)); t.adc_reads = []
    ref = copy.deepcopy(t)
    ref.adc_reads.extend(ADC)
    for i, raw in zip([0, 1, 3, 2], values):
        value = raw >> 6
        w(ref, 0x8A2C + 2*i, value, 2)
        w(ref, 0x8A64 + 2*i, r(ref, 0x8A64 + 2*i, 2) + value, 2)
    execute(t, 0x188FC); equal(t, ref)


def caller(t, i):
    ref = copy.deepcopy(t)
    prior.service_model(ref, i); prior.driver_model(ref, i); handoff_model(ref, i)
    # Original caller tail includes its epilogue. Supply the saved caller frame,
    # rather than omitting the pops or replacing the final18816 tailcall.
    sp = t.r[15]; t.r[15] -= 16; t.r[13] = t.r[14] = i
    t.write(t.r[15]+4, 0xFFFFFFF0, 4)
    t.write(t.r[15]+8, i, 4); t.write(t.r[15]+12, i, 4)
    t.run(0x12826, limit=300000)
    assert t.r[15] == sp and t.r[13:15] == [i, i]
    equal(t, ref)


def seed(t, rng, i):
    for a in [0xA5D4, 0xA5E4, 0x8A6C, 0x8A64, 0x8A4C, 0x8A54, 0x8A7C, 0x8A8C, 0x8A2C, 0x8A44]:
        w(t, a+2*i, rng.randrange(65536), 2)
    for a in [0x8A60+i, 0x8A5C+i, 0xA5A0]: w(t, a, rng.choice([0, 1, 2, 255]))
    w(t, 0x8A9C+4*i, rng.randrange(1 << 32), 4)
    w(t, 0x8AD8, rng.randrange(65536), 2); w(t, 0xA518, rng.randrange(65536), 2)


def main():
    rng = random.Random(0x18A44); counts = {}; t = fixture()
    for n in range(40):
        for a in range(0x8A2C, 0x8ADA): w(t, a, rng.randrange(256))
        for a in range(0x63B8, 0x63CC): w(t, a, rng.randrange(256))
        if n % 2:
            w(t, 0x63CA, s(t, 0x63C8)-1456+sum(s(t, a) for a in range(0x63B8, 0x63C8, 2)), 2)
        initialize(t)
    counts['initialization'] = 40
    for n in range(800):
        i = n % 4; seed(t, rng, i); handoff(t, i, n % 3 != 0)
    counts['handoff_arbitrary'] = 800
    count = 0
    for i, supply, value, offset in itertools.product(range(4), [0, 1, 10500, 12000, 32767, 32768, 65535],
                                                     [0, 1, 200, 1000, 32767, 32768, 65535], [0, 100, 32767, 32768, 65535]):
        w(t, 0xA518, supply, 2); w(t, 0x8A44+2*i, offset, 2)
        ref = copy.deepcopy(t); peripheral_model(ref, i, value)
        t.r[5] = value; execute(t, 0x14280, i); equal(t, ref); count += 1
    counts['peripheral'] = count
    count = 0
    for error, gain, old, bound in itertools.product([-32768, -1, 0, 1, 32767], [0, 1, 65535],
                                                    [-2147483648, -1000, 0, 1000, 2147483647],
                                                    [-32768, -1, 0, 1, 32767]):
        t.r[5:8] = [gain, u32(old), u32(bound)]
        result = signed(execute(t, 0x18E48, error))
        assert result == accumulator(error, gain, old, bound)
        count += 1
    counts['accumulator'] = count
    count = 0
    for i, flag, inhibit, previous, raw, supply in itertools.product(range(4), [0, 1, 2], [0, 1, 2],
                                                                   [0, 1], [67, 68, 1000, 1001], [0, 10499, 10500, 12000]):
        t = fixture(); prior.initialize(t); initialize(t)
        w(t, 0x8A60+i, flag); w(t, 0x8A5C+i, previous); w(t, 0xA5A0, inhibit)
        w(t, 0x8A2C+2*i, raw, 2); w(t, 0xA518, supply, 2)
        handoff(t, i); count += 1
    counts['fallback_boundaries'] = count
    for count in range(1024):
        acquire(t, [((count + 211*i) % 1024) << 6 for i in range(4)])
    for _ in range(64): acquire(t, [rng.randrange(65536) for i in range(4)])
    counts['acquisition'] = 1088
    count = 0
    for i, value in itertools.product(range(4), [0, 1000, 5940, 32767, 65535]):
        t = fixture(); prior.initialize(t); initialize(t)
        w(t, 0xA518, 12000, 2); w(t, 0xA600+2*i, value, 2)
        acquire(t, [400 << 6, 500 << 6, 600 << 6, 700 << 6])
        caller(t, i); count += 1
    counts['original_caller_tails'] = count
    rows = []; t = attach(prior.base.bank_fixture()); prior.initialize(t); initialize(t); w(t, 0x9856, 4)
    w(t, 0xA518, 12000, 2)
    for call in range(1, 161):
        w(t, 0x80EE, 5500, 2); w(t, 0x98DC, 0 if call <= 80 else -1000, 2)
        w(t, 0x988A, int(call % 30 < 15)); w(t, 0x993E, call*20, 2); w(t, 0x993C, 300, 2)
        w(t, 0x9C58, int(60 <= call <= 65)); w(t, 0x8088, 2 if 90 <= call <= 95 else 0)
        # Explicit four-acquisition/one-channel-service harness cadence.
        # Other channels accumulate/wordwrap without service in this fixture.
        for _ in range(4):
            acquire(t, [400 << 6, (500 if call <= 80 else 600) << 6, 600 << 6, 700 << 6])
        w(t, 0x8A61, int(100 <= call <= 120)); w(t, 0xA5A0, int(110 <= call <= 115))
        prior.base.update(t); row = prior.base.integrated(t)
        row.update(call=call, service=prior.service(t, 1), driver=prior.driver(t, 1), handoff=handoff(t, 1))
        rows.append(row)
    counts['integrated_retained'] = len(rows)
    counts['rejected'] = 0
    for address, size, writing in [(TARGETS[0], 1, True), (TARGETS[1], 4, True), (0xFFFFF518, 2, True), (TARGETS[0], 2, False),
                                   (ADC[0], 1, False), (ADC[0], 2, True), (0xFFFFF808, 2, False)]:
        try:
            if writing: t.write(address, 0, size)
            else: t.read(address, size)
        except ValueError: counts['rejected'] += 1
        else: raise AssertionError('unsupported MMIO accepted')
    out = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), counts=counts, retained=rows)
    (ROOT/'tcu-output-handoff-verification.json').write_text(json.dumps(out, indent=2)+'\n')
    print(counts, flush=True)


if __name__ == '__main__': main()
