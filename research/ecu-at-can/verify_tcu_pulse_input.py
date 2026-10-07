"""Verify TCU pulse-input publication and its ordering in the application task.

Original instructions execute without helper stubs. Independent models compare
all application RAM and admitted peripheral traces. Raw input and diagnostics
are explicit fixtures; no physical timing, board identity or boot claim.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

import verify_tcu_inhibit_writers as writers
from verify_tcu_inhibit_writers import TCU, pins, r, source, w

ROOT = Path(__file__).resolve().parent
FALLBACK = TCU[0x5FD38]
assert FALLBACK == 0


def raw_model(t):
    w(t, 0x88CC, (r(t, 0x8F33) >> 1) & 1)
    w(t, 0x88CD, 2)


def publication_model(t):
    value = r(t, 0xA520)
    flags = r(t, 0xA991)
    if r(t, 0x88CD) == 2 and flags & 1:
        value, status = r(t, 0x88CC), 1
    elif flags & 4:
        value, status = FALLBACK, 4
    elif flags & 2:
        status = 3
    else:
        status = 2
    w(t, 0xA520, value)
    w(t, 0xA521, status)


def check(t, entry, model):
    ref = copy.deepcopy(t)
    model(ref)
    pins.execute(t, entry)
    source.equal(t, ref)


def direct():
    counts = dict(raw=0, publication=0, initialization=0)
    for bits in range(256):
        t = writers.fixture(bits)
        w(t, 0x8F33, bits)
        check(t, 0x17670, raw_model)
        counts['raw'] += 1
    for flags, status, value in itertools.product(range(256), [0, 2, 255], [0, 1, 255]):
        t = writers.fixture(flags + value)
        for address, byte in [(0xA991, flags), (0x88CD, status), (0x88CC, value)]:
            w(t, address, byte)
        check(t, 0x51314, publication_model)
        counts['publication'] += 1
    for seed, entry in itertools.product(range(8), [0x17664, 0x51308]):
        t = writers.fixture(seed)
        addresses = [0x88CC, 0x88CD] if entry == 0x17664 else [0xA520, 0xA521]
        for address in addresses:
            w(t, address, (seed * 31 + 1) & 255)
        ref = copy.deepcopy(t)
        for address in addresses:
            w(ref, address, 0)
        pins.execute(t, entry)
        source.equal(t, ref)
        counts['initialization'] += 1
    return counts


class ObservedInput(writers.ObservedWriters):
    def instruction(self, pc):
        if self.input_pending is not None and pc == self.input_pending[0]:
            _, ref, inputs = self.input_pending
            self.input_pending = None
            source.equal(self, ref)
            self.input_records.append(dict(inputs=inputs, value=r(self, 0xA520), status=r(self, 0xA521)))
        if pc == 0x51314:
            assert self.input_pending is None
            inputs = {hex(a): r(self, a) for a in [0xA520, 0x88CC, 0x88CD, 0xA991]}
            ref = copy.deepcopy(self)
            publication_model(ref)
            self.input_pending = (self.pr, ref, inputs)
        if pc in [0x23DD0, 0x51314]:
            self.input_order.append(pc)
        return super().instruction(pc)


def task_fixture():
    t = writers.task_fixture()
    t.__class__ = ObservedInput
    t.input_pending = None
    t.input_records = []
    t.input_order = []
    return t


def task_call(t):
    phase = r(t, 0x84F4) & 7
    previous = r(t, 0xA520)
    t.input_records = []
    t.input_order = []
    row = writers.task_call(t)
    assert t.input_pending is None
    expected = [0x23DD0, 0x51314] if phase in [0, 4] else []
    assert t.input_order == expected
    if expected:
        assert row['writers'][0]['inputs']['0xa520'] == previous
        assert r(t, 0x941A) == previous
    row.update(phase=phase, order=t.input_order.copy(), publication=t.input_records.copy(),
               sample=r(t, 0xA520), previous=r(t, 0x941A), pulse=r(t, 0x9414))
    return row


def tasks():
    standalone = []
    for phase, flags in itertools.product(range(8), [0, 1, 4, 7]):
        t = task_fixture()
        for address, byte in [(0x84F4, phase), (0xA991, flags), (0x88CC, 1), (0x88CD, 2)]:
            w(t, address, byte)
        standalone.append(task_call(t))
    scenarios = []
    # A separate original raw-reader call precedes each complete application
    # task by explicit harness choice. This is not its proved scheduler cadence.
    # Counter is held at the selected value to isolate the edge boundary.
    for counter in [91, 92]:
        t = task_fixture()
        for entry in [0x17664, 0x51308, 0x23D94]:
            pins.execute(t, entry)
        w(t, 0x8280, counter)
        retained = []
        for call in range(24):
            bits = 2 if call < 8 or call >= 16 else 0
            flags = 1 if call < 8 or call >= 16 else 0 if call < 12 else 4
            w(t, 0x8F33, bits)
            w(t, 0xA991, flags)
            check(t, 0x17670, raw_model)
            row = task_call(t)
            row.update(call=call, raw=bits, flags=flags)
            retained.append(row)
        # New high is published on call0, consumed on call4. Missing-validity
        # flags retain it at8; fallback clears it at12, observed at16. The
        # second rising publication16 is observed at20.
        assert [row['sample'] for row in retained[::4]] == [1, 1, 1, 0, 1, 1]
        assert [row['previous'] for row in retained[::4]] == [0, 1, 1, 1, 0, 1]
        assert [row['call'] for row in retained if row['order'] and row['pulse']] == ([4, 20] if counter == 91 else [])
        scenarios.append(dict(counter=counter, retained=retained))
    return standalone, scenarios


def main():
    counts = direct()
    standalone, scenarios = tasks()
    rows = standalone + [row for scenario in scenarios for row in scenario['retained']]
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
                  counts=counts, standalone=standalone, scenarios=scenarios,
                  publication_boundaries=sum(len(row['publication']) for row in rows),
                  full_application_tasks=len(rows), explicit_raw_reader_calls=48,
                  limits='Raw8F33/A991 fixtures; raw-reader/task ratio and held counter explicit. No physical units, startup, real cadence, controller or board proof.')
    (ROOT / 'tcu-pulse-input-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(counts, 'tasks', len(rows), 'publication boundaries', result['publication_boundaries'])


if __name__ == '__main__':
    main()
