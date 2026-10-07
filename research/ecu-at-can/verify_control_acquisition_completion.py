"""Execute ECU alternate ADC arming, completion callbacks and timer writes.

Explicit ADC words, software register latches and injected callback entries;
no analog conversion, interrupt delivery, elapsed time or plant simulation.
Original ROM helpers execute. Shared verifiers, interpreter and ROM unchanged.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_control_acquisition_schedule as prior
from verify_control_acquisition_schedule import ECU, w, r, rf, run, REGISTERS
from verify_control_acquisition import f, q

ROOT = Path(__file__).resolve().parent
BYTES = [0xFFFFF72E, 0xFFFFF76E]
WORDS = [0xFFFFF440, 0xFFFFF44E, 0xFFFFF450, 0xFFFFF452,
         0xFFFFF64A, 0xFFFFF64C, 0xFFFFF64E]


class Completion(prior.ScheduledAcquisition):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address in self.extra:
            if size != (1 if address in BYTES else 2):
                raise ValueError('Wrong peripheral width')
            value = self.extra[address]
            self.extra_io.append(('read', address, value))
            return value
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address in self.extra:
            if size != (1 if address in BYTES else 2):
                raise ValueError('Wrong peripheral width')
            value &= 255 if size == 1 else 65535
            self.extra[address] = value
            self.extra_io.append(('write', address, value))
            return
        super().write(address, value, size)


def setup():
    e = prior.setup(); e.__class__ = Completion
    e.extra = dict.fromkeys(BYTES + WORDS, 0); e.extra_io = []
    return e


def seed(e, rng):
    prior.seed(e, rng)
    for a in range(0x4078, 0x40A4): w(e, a, rng.randrange(256))
    f(e, 0x4068, rng.choice([999, 1000, 1025, 1050, 1051]))
    e.extra = {a: rng.randrange(256 if a in BYTES else 65536) for a in e.extra}


def get(e, a):
    d, log = (e.extra, e.extra_io) if a in e.extra else (e.adc_control, e.adc_io)
    log.append(('read', a, d[a])); return d[a]


def put(e, a, v):
    d, log = (e.extra, e.extra_io) if a in e.extra else (e.adc_control, e.adc_io)
    v &= 65535 if a in WORDS else 255
    d[a] = v; log.append(('write', a, v))


def sample(e, a):
    e.adc_reads.append(a); return e.adc_samples[a]


def arm_model(e, argument):
    for config, trigger in [(0xFFFFF818, 0xFFFFF76E), (0xFFFFF838, 0xFFFFF72E)]:
        control = config + 1
        put(e, control, get(e, control) & 0xDF)
        get(e, config)
        put(e, config, (0x0B if argument == 0 else 0x0A) | (0x40 if config == 0xFFFFF838 else 0))
        put(e, trigger, get(e, trigger) | 0x80)
        put(e, control, (get(e, control) & 0xAF) | 0x80)
    w(e, 0x404B, 1)


def timer_model(e, argument):
    base = get(e, 0xFFFFF440) + 4
    # Only low byte of argument selects the timer branch.
    mode = bool(argument & 255)
    for address, value, twice in [(0xFFFFF64C, 25 if mode else 44, True),
                                  (0xFFFFF450, base if mode else base + 25, False),
                                  (0xFFFFF64E, 14 if mode else 25, True),
                                  (0xFFFFF452, base + 25 if mode else base, False),
                                  (0xFFFFF64A, 1, True), (0xFFFFF44E, base + 20, False)]:
        put(e, address, value)
        if twice: put(e, address, value)
    w(e, 0x40A3, 0)


def alternate_model(e):
    n = (r(e, 0x40A2) + 1) & 255
    if n >= 2: n = 0
    w(e, 0x40A2, n)
    if n: return
    w(e, 0x4096, sample(e, 0xFFFFF836), 2)
    w(e, 0x409A, sample(e, 0xFFFFF816), 2)
    value = rf(e, 0x4068)
    if value <= 1000: w(e, 0x40A0, 1)
    elif value > q(1000 + 50): w(e, 0x40A0, 0)
    arm_model(e, 0)
    timer_model(e, r(e, 0x40A0))
    w(e, 0x40A1, 0)


def capture_model(e):
    if r(e, 0x40A1): return
    w(e, 0x4078, r(e, 0x4096, 2), 2)
    w(e, 0x407A, r(e, 0x409A, 2), 2)
    w(e, 0x4098, sample(e, 0xFFFFF836), 2)
    w(e, 0x409C, sample(e, 0xFFFFF816), 2)
    w(e, 0x409E, 1)


def follow_model(e):
    if r(e, 0x404B):
        capture_model(e); w(e, 0x404B, 0)
    elif r(e, 0x4049) == 1:
        alternate_model(e)


def irq_model(e):
    put(e, 0xFFFFF838, get(e, 0xFFFFF838) & 0x7F)
    follow_model(e)


def checked(e, entry, model, argument=0):
    ref = copy.deepcopy(e); model(ref, argument) if entry in [0x531E, 0x5D62] else model(ref)
    sp, mask = e.r[15], e.sr & 0xF0
    e.run(entry, argument)
    assert e.r[15] == sp and (e.sr & 0xF0) == mask
    prior.equal(e, ref)
    assert e.extra == ref.extra and e.extra_io == ref.extra_io


def main():
    rng = random.Random(0x4DFE); counts = {}
    # Stock calibration asserted independently of formulas above.
    assert [int.from_bytes(ECU[a:a+2], 'big') for a in range(0xDC3D6, 0xDC3DE, 2)] == [25, 44, 14, 20]
    assert prior.prior.number(0xDC3EC) == 1000 and prior.prior.number(0xDC3F0) == 50
    n = 0
    for flag in range(256):
        e = setup(); seed(e, rng); w(e, 0x40A1, flag)
        checked(e, 0x5E38, capture_model); n += 1
    counts['capture'] = n
    n = 0
    for argument, mask in itertools.product([0, 1, 2, 255, 256, 0xFFFFFFFF], range(16)):
        e = setup(); seed(e, rng); e.sr = mask << 4
        checked(e, 0x531E, arm_model, argument); n += 1
    counts['arm'] = n
    n = 0
    for argument, timer in itertools.product([0, 1, 2, 255, 256, 0xFFFFFFFF], [0, 1, 32767, 32768, 65507, 65531, 65535]):
        e = setup(); seed(e, rng); e.extra[0xFFFFF440] = timer
        checked(e, 0x5D62, timer_model, argument); n += 1
    counts['timer'] = n
    n = 0
    for counter, value, oldflag in itertools.product(range(256), [999.9375, 1000, 1000.0625, 1050, 1050.0625], [0, 1, 2, 255]):
        e = setup(); seed(e, rng); w(e, 0x40A2, counter); f(e, 0x4068, value); w(e, 0x40A0, oldflag)
        checked(e, 0x5CF4, alternate_model); n += 1
    counts['alternate'] = n
    n = 0
    for marker, extended, inhibit, count in itertools.product([0, 1, 2, 255], [0, 1, 2, 255], [0, 1, 2, 255], [0, 1, 255]):
        e = setup(); seed(e, rng)
        for a, v in [(0x404B, marker), (0x4049, extended), (0x40A1, inhibit), (0x40A2, count)]: w(e, a, v)
        checked(e, 0x4DFE, follow_model)
        checked(e, 0xF29C, irq_model); n += 1
    counts['follow_and_callback'] = n
    for status in range(256):
        e = setup(); seed(e, rng); w(e, 0x404B, 0); w(e, 0x4049, 0)
        e.adc_control[0xFFFFF838] = status
        checked(e, 0xF29C, irq_model)
    counts['acknowledgement_status_bytes'] = 256
    # Static vector provenance: original VBR load, ADI1 slot and wrapper target.
    assert ECU[0xF758:0xF75C] == bytes.fromhex('d342432e')
    assert int.from_bytes(ECU[0xF864:0xF868], 'big') == 0xFFC50
    assert int.from_bytes(ECU[0xFFC50+0x308:0xFFC50+0x30C], 'big') == 0x2FA8
    assert int.from_bytes(ECU[0x2FB8:0x2FBC], 'big') == 0xF29C
    rows = []; e = setup(); f(e, 0x4068, 1025); callbacks = 0
    for call in range(1, 321):
        values = [((call * 17 + i * 31) & 1023) << 6 for i in range(32)]
        prior.schedule(e, values, caller=True)
        enabled = bool(e.adc_control[0xFFFFF838] & 0x40)
        # Inject completion only when original software enabled ADIE1.
        # Delivery and successful conversion are explicit harness assumptions.
        if enabled:
            e.adc_control[0xFFFFF838] |= 0x80
            checked(e, 0xF29C, irq_model); callbacks += 1
        row = dict(call=call, enabled=enabled, extended=r(e,0x4049),
                   half=r(e,0x40A2), armed=r(e,0x404B))
        if row['armed']:
            assert e.adc_control[0xFFFFF838] & 0x40
            e.adc_samples[0xFFFFF836] = ((call + 100) & 1023) << 6
            e.adc_samples[0xFFFFF816] = ((call + 200) & 1023) << 6
            e.adc_control[0xFFFFF838] |= 0x80
            checked(e, 0xF29C, irq_model); callbacks += 1
            row['captured'] = [r(e,a,2) for a in [0x4078,0x407A,0x4098,0x409C]]
        rows.append(row)
    assert [x['call'] for x in rows if x['enabled']] == [64, 128, 192, 256, 320]
    assert [x['call'] for x in rows if x['armed']] == [128, 256]
    counts['retained_schedule_calls'] = len(rows)
    counts['retained_injected_callbacks'] = callbacks
    counts['rejected'] = 0
    for a, size, writing in [(BYTES[0],2,False), (WORDS[0],1,False), (WORDS[1],4,True), (0xFFFFF454,2,True)]:
        try: e.write(a,0,size) if writing else e.read(a,size)
        except ValueError: counts['rejected'] += 1
        else: raise AssertionError('Unsupported peripheral accepted')
    out = dict(scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),counts=counts,retained=rows)
    (ROOT/'control-acquisition-completion-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(counts,flush=True)


if __name__ == '__main__': main()
