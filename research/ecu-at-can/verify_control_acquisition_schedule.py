"""Execute periodic ADC copy/configuration with explicit register latches.

Six control/status bytes retain software writes; no analog conversion,
interrupt, completion or hardware timing is simulated. Results are supplied
explicitly. SR-zero cases use an explicit task descriptor that avoids a
scheduler dispatch. Original ROM helpers execute without stubs or ISA edits.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_control_acquisition as prior
from verify_control_acquisition import ECU, TCU, w, r, rf, run, REGISTERS

ROOT = Path(__file__).resolve().parent
CONTROL = [0xFFFFF818, 0xFFFFF838, 0xFFFFF858]
COPIERS = [0x4E32, 0x4EE8, 0x4F78]
STARTERS = [0x5018, 0x50E2, 0x527A]


class ScheduledAcquisition(prior.Acquisition):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address in self.adc_control:
            if size != 1:
                raise ValueError('ADC control requires byte access')
            value = self.adc_control[address]
            self.adc_io.append(('read', address, value))
            return value
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address in self.adc_control:
            if size != 1:
                raise ValueError('ADC control requires byte access')
            value &= 255
            self.adc_control[address] = value
            self.adc_io.append(('write', address, value))
            return
        super().write(address, value, size)


def attach(e):
    assert type(e) is prior.Acquisition
    e.__class__ = ScheduledAcquisition
    e.adc_control = {a + offset: 0 for a in CONTROL for offset in [0, 1]}
    e.adc_io = []
    # A synthetic, explicit task descriptor for original3894's SR-zero path.
    w(e, 0x12C8, 0xFFFF1300, 4)
    w(e, 0x1301, 1)
    return e


def setup():
    e = attach(prior.setup())
    e.sr = 0x40
    return e


def ram(e):
    return {a: v for a, v in e.ram.items() if a >= 0xFFFF0000 and v}


def equal(e, ref):
    aa, bb = ram(e), ram(ref)
    assert aa == bb, {hex(a): (aa.get(a, 0), bb.get(a, 0))
                      for a in set(aa) | set(bb) if aa.get(a, 0) != bb.get(a, 0)}
    assert e.adc_control == ref.adc_control
    assert e.adc_reads == ref.adc_reads
    assert e.adc_io == ref.adc_io


def copy_model(e, bank):
    count = r(e, 0x404F + bank * 3)
    if count:
        w(e, 0x404D + bank * 3, 0)
        w(e, 0x404E + bank * 3, 0)
    if count not in ([1, 4, 8, 12] if bank < 2 else [1, 4, 8]):
        return
    for index in reversed(range(bank * 12, bank * 12 + count)):
        address = REGISTERS[index]
        e.adc_reads.append(address)
        w(e, 0x4008 + 2 * index, e.adc_samples[address], 2)


def start_model(e, bank):
    count = r(e, 0x404F + bank * 3)
    config = ({1: 0x10, 4: 0x13, 8: 0x23, 12: 0x33} if bank < 2
              else {1: 0x18, 4: 0x1B, 8: 0x2B}).get(count)
    if config is None:
        return
    if bank == 1 and r(e, 0x4049) == 1:
        config |= 0x40
    a = CONTROL[bank]
    old, status = e.adc_control[a], e.adc_control[a + 1]
    e.adc_io.extend([('read', a + 1, status), ('write', a + 1, status & 0xDF),
                     ('read', a, old), ('write', a, config),
                     ('read', a + 1, status & 0xDF),
                     ('write', a + 1, (status & 0x0F) | 0x20)])
    e.adc_control[a] = config
    e.adc_control[a + 1] = (status & 0x0F) | 0x20


def schedule_model(e):
    for bank in range(3):
        copy_model(e, bank)
    old = r(e, 0x404C)
    if old <= 2:
        for i in range(old + 1):
            w(e, 0x4004 + i, r(e, 0x4004 + i) + 1)
    phase = (r(e, 0x4048) + 1) & 255
    w(e, 0x4048, phase)
    w(e, 0x4049, 0)
    if phase % 16 == 0:
        mode, counts = 2, [12, 12, 8]
        slow = (r(e, 0x404A) + 1) & 255
        if slow >= 4:
            slow = 0
            w(e, 0x4049, 1)
        w(e, 0x404A, slow)
    else:
        mode, counts = (1 if phase % 4 == 0 else 0), [12, 8, 0]
    w(e, 0x404C, mode)
    for bank, count in enumerate(counts):
        w(e, 0x404F + 3 * bank, count)
    start_model(e, 0)
    w(e, 0x404B, 0)
    start_model(e, 1)
    if counts[2]:
        start_model(e, 2)


def execute_slice(e, start, stop):
    pc = start
    for _ in range(10000):
        if pc == stop:
            return
        nxt, delay = e.instruction(pc)
        if delay:
            _, nested = e.instruction(pc + 2)
            assert not nested
        pc = nxt
    raise AssertionError('slice bound')


def schedule(e, values, caller=False):
    e.adc_samples = dict(zip(REGISTERS, values))
    e.adc_reads, e.adc_io = [], []
    ref = copy.deepcopy(e)
    schedule_model(ref)
    sp, mask = e.r[15], e.sr & 0xF0
    if caller:
        # Original E26C task's manager+scaler pair, excluding unrelated calls.
        raw = r(ref, 0x400A, 2)
        w(ref, 0x40EC, raw, 2)
        prior.f(ref, 0x40E8, prior.q(prior.q(raw / prior.number(0x676C)) * prior.number(0xDC480)))
        execute_slice(e, 0xE276, 0xE282)
    else:
        run(e, 0x4CE2)
    assert e.r[15] == sp and (e.sr & 0xF0) == mask
    equal(e, ref)


def seed(e, rng):
    for a in range(0x4004, 0x4056):
        w(e, a, rng.randrange(256))
    e.adc_control = {a: rng.randrange(256) for a in e.adc_control}
    e.adc_samples = {a: rng.randrange(65536) for a in REGISTERS}


def direct():
    rng = random.Random(0x4CE2)
    counts = dict(copy=0, start=0, schedule=0, caller=0, rejected=0)
    for bank, count in itertools.product(range(3), range(256)):
        e = setup(); seed(e, rng); w(e, 0x404F + 3 * bank, count)
        ref = copy.deepcopy(e); copy_model(ref, bank)
        run(e, COPIERS[bank]); equal(e, ref); counts['copy'] += 1
        for flag in [0, 1, 2, 255]:
            e = setup(); seed(e, rng); w(e, 0x404F + 3 * bank, count); w(e, 0x4049, flag)
            ref = copy.deepcopy(e); start_model(ref, bank)
            run(e, STARTERS[bank]); equal(e, ref); counts['start'] += 1
    for phase, slow in itertools.product(range(256), [0, 1, 2, 3, 4, 254, 255]):
        e = setup(); seed(e, rng)
        w(e, 0x4048, phase); w(e, 0x404A, slow); w(e, 0x404C, phase)
        e.sr = (phase % 16) << 4
        for bank in range(3):
            w(e, 0x404F + bank * 3, [0, 1, 4, 8, 12, 255][(phase + bank) % 6])
        schedule(e, list(e.adc_samples.values())); counts['schedule'] += 1
    # All possible status byte values, with recognized start counts.
    for status in range(256):
        e = setup(); seed(e, rng); w(e, 0x4048, 63); w(e, 0x404A, 3)
        for a in CONTROL: e.adc_control[a + 1] = status
        schedule(e, list(e.adc_samples.values())); counts['schedule'] += 1
    for phase in range(32):
        e = setup(); seed(e, rng); w(e, 0x4048, phase)
        schedule(e, list(e.adc_samples.values()), True); counts['caller'] += 1
    e = setup()
    for address, size, writing in [(CONTROL[0], 2, False), (CONTROL[1], 2, True),
                                   (0xFFFFF81A, 1, False), (REGISTERS[0], 2, True)]:
        try:
            if writing: e.write(address, 0, size)
            else: e.read(address, size)
        except ValueError: counts['rejected'] += 1
        else: raise AssertionError('unsupported ADC access accepted')
    return counts


def retained():
    e = setup(); rows = []
    for call in range(1, 321):
        values = [((call * 7 + i) % 1024) << 6 for i in range(32)]
        schedule(e, values, True)
        prior.decode(e); prior.publish(e, call == 1)
        rows.append(dict(call=call, phase=r(e, 0x4048), slow=r(e, 0x404A), flag=r(e, 0x4049),
                         counters=[r(e, 0x4004 + i) for i in range(3)],
                         selected=[r(e, 0x404F + i * 3) for i in range(3)],
                         copied=[REGISTERS.index(a) for a in e.adc_reads],
                         bank=[r(e, 0x4008 + 2 * i, 2) >> 6 for i in range(32)],
                         value6cac=r(e, 0x6CAC), value6cb4=float(rf(e, 0x6CB4))))
    assert rows[0]['copied'] == []
    assert rows[15]['bank'][28] == 0 and rows[16]['bank'][28] == (17 * 7 + 28) % 1024
    assert rows[17]['bank'][28] == rows[16]['bank'][28]
    assert [row['call'] for row in rows if row['flag']] == [64, 128, 192, 256, 320]
    assert rows[255]['phase'] == 0
    assert rows[-1]['counters'] == [64, 79, 19]
    return rows


def prepare(e):
    prior.prepare(e)
    attach(e)


def mode_step(e, call):
    prior.prior.prior.mode_step(e, call)
    w(e, 0x70F0, 1 if 40 <= call <= 60 else 2)
    w(e, 0x9462, 1 if 201 <= call <= 210 else 0)
    values = [0] * 32
    values[1] = (410 if call <= 160 else 600 if call <= 220 else 350) << 6
    values[8] = (0 if call <= 100 else 480 if call <= 160 else 1023) << 6
    schedule(e, values, True)
    prior.decode(e, True)
    prior.publish(e)
    prior.prior.group(e)


def step(e, call):
    row = prior.prior.prior.source.followers.step(
        e, call, input_producer=prior.prior.input_step, mode_producer=mode_step)
    row.update(adc1=r(e, 0x400A, 2) >> 6, adc8=r(e, 0x4018, 2) >> 6,
               produced6cac=r(e, 0x6CAC), produced6cb4=float(rf(e, 0x6CB4)),
               acquisition_phase=r(e, 0x4048), extended_bank=r(e, 0x4049))
    return row


def main():
    counts = direct(); rows = retained()
    print('Direct', counts, 'retained', len(rows), flush=True)
    lifecycle, boundaries = prior.prior.prior.source.followers.adjustment.upstream.secondary.prior.lifecycle(
        prepare=prepare, upstream=step, checkpoints={1, 2, 16, 17, 64, 65, 100, 101, 160, 161, 162, 220, 221, 222, 255, 256, 257, 320})
    out = dict(scope=__doc__, ecu_sha256=hashlib.sha256(ECU).hexdigest(),
               tcu_sha256=hashlib.sha256(TCU).hexdigest(), counts=counts, retained=rows,
               serial_cycles=320, paired_can_updates=len(boundaries), can211_latch_updates=320,
               lifecycle=lifecycle)
    (ROOT / 'control-acquisition-schedule-verification.json').write_text(json.dumps(out, indent=2) + '\n')
    print('Integrated', 320, len(boundaries), flush=True)


if __name__ == '__main__': main()
