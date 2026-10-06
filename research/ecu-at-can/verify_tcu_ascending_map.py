"""Execute group7 constructor, numeric map, permission and paired ECU path.

Map/callback boundary cases use explicit records and upstream inputs. Two
retained manager traces use original creation and dispatch; sampled inputs and
task calls are fixtures, not a physical shift or timing model.
"""
import hashlib
import itertools
import json

from verify_can201_byte6 import TCU, w, r
from verify_tcu_slot2 import fixture, allocate, BANKS
from verify_tcu_request_maps import table, lookup
from verify_tcu_request_dispatch import curve
from verify_tcu_request_admission import gate_model, paired_snapshot
from verify_tcu_phase_retirement import RetirementTCU, full_fixture

RECORD = 0xA900  # Isolated callback fixture, not manager-owned memory.


def candidate(code, x, y, captured, flags, timer):
    bank = code if code in range(5) else 0
    value = lookup(0x76805 + 50*bank, x, y) >> 2
    threshold = int.from_bytes(TCU[0x76738+2*bank:0x7673A+2*bank], 'big')
    if not flags & 0x10 and captured >= threshold:
        factor = curve(0x76913+9*bank, timer << 8) >> 8
        value = value*factor >> 4
    return value


def setup(t, handle, code, x, y, captured, flags, timer):
    for a, v, size in [(RECORD+1, code, 1), (RECORD+2, handle, 1),
                       (RECORD+8, flags, 1), (RECORD+16, captured, 2),
                       (RECORD+18, y, 2), (0x80F8, x, 2), (0x8276, timer, 1)]:
        w(t, a, v, size)


def publish(t, handle, expected, flags):
    t.r[5] = 0xFFFF0000+RECORD
    t.run(0x4E036)
    assert r(t, RECORD+4, 2) == expected
    assert r(t, RECORD+8) == (flags & 127) | (128 if expected else 0)
    assert r(t, BANKS[0]['base']+4*handle+2, 2) == expected
    assert r(t, BANKS[0]['flags']+handle) == int(expected > 0)
    t.run(0x4C7AC)
    assert (r(t, 0x9160, 2), r(t, 0x9168)) == (expected, int(expected > 0))
    t.run(0x1FB8C)
    source = max(800-expected, 0) if expected else 32767
    assert r(t, 0x915A, 2) == source
    return source


class ObservedAscending(RetirementTCU):
    def __init__(self):
        super().__init__()
        self.numeric_entries = []

    def instruction(self, pc):
        if pc == 0x4E036:
            p = self.r[5] & 65535
            self.numeric_entries.append(dict(code=r(self, p+1),
                permission=r(self, 0x9410), inhibit=r(self, 0x92D5),
                x=r(self, 0x80F8, 2), y=r(self, p+18, 2),
                captured=r(self, p+16, 2), flags=r(self, p+8),
                timer=r(self, 0x8276)))
        return super().instruction(pc)


def lifecycle(measured_a, samples=None, t=None, calls=111, rearm_input=None, map_samples=None, upstream=None, observe=None, prepare=None, require_ascending=True):
    t = ObservedAscending() if t is None else t
    samples = {80: 5000} if samples is None else samples
    map_samples = {} if map_samples is None else map_samples
    t.ram = dict(full_fixture().ram)
    w(t, 0x606F, 1); t.run(0x48BC0)
    for a, v in [(0x8080, 6), (0x8084, 2), (0x92D0, 4), (0xA93A, 1)]:
        w(t, a, v)
    for a, v in [(0x80EA, 4672), (0x80F6, 4224), (0x809C, 20000),
                 (0x809A, measured_a), (0x80EE, 1000), (0x80F8, 14080)]:
        w(t, a, v, 2)
    if prepare is not None:
        prepare(t)
    t.run(0x48C08, limit=1000000)
    record = r(t, 0xA2BC, 4) & 65535
    assert r(t, record+1) == 1 and r(t, record) == 2
    if rearm_input is not None:
        w(t, 0x8081, rearm_input)  # Explicit post-creation perturbation only.
    w(t, 0x9220, 5000, 4)  # Explicit target reference, not a producer claim.
    rows = []
    previous = None
    for call in range(1, calls+1):
        if call in samples:
            w(t, 0x80EE, samples[call], 2)
        if call in map_samples:
            w(t, 0x80F8, map_samples[call], 2)
        if upstream is not None:
            upstream(t, call)
        t.run(0x11014)
        t.run(0x31524, 2, limit=1000000)
        for subcall in range(2):
            t.r[5] = 0
            t.run(0x31524, 4, limit=1000000)
            t.run(0x4C7AC); t.run(0x1FB8C)
            if observe is not None:
                observe(t, call, subcall)
            state = (r(t, record), r(t, record+8), r(t, record+4, 2),
                     r(t, 0x915A, 2), r(t, 0x95E1))
            if state != previous:
                rows.append(dict(call=call, subcall=subcall, state=state[0],
                    flags=state[1], request=state[2], phase=state[4],
                    permission=r(t, 0x9410), **paired_snapshot(t)))
                previous = state
    assert r(t, 0x96C5) == 0 and r(t, 0x8088) == 1
    if require_ascending:
        assert t.numeric_entries
    if require_ascending and samples == {80: 5000}:
        assert len(t.numeric_entries) == 1
    entry = t.numeric_entries[0] if t.numeric_entries else None
    raw = (candidate(entry['code'], entry['x'], entry['y'], entry['captured'],
                     entry['flags'], entry['timer']) if entry else None)
    return dict(measured_a=measured_a, numeric_entry=entry,
                independently_calculated_candidate=raw, checkpoints=rows)


def main():
    constructors = 0
    for code, bank in itertools.product([0, 1, 2, 3, 4, 255], [0, 5, 255]):
        t = fixture()
        for a, v, size in [(0x808D, bank, 1), (0x808C, 77, 1),
                           (0x80C8, 0x1234, 2), (0x80D2, 0xABCD, 2),
                           (0x80D4, 0xFEDC, 2), (RECORD+8, 0x65, 1)]:
            w(t, a, v, size)
        t.r[5], t.r[6], t.r[7] = code, 0x17, 0xFFFF0000+RECORD
        assert t.run(0x4DCA4, 9) == 2
        assert [r(t, RECORD+i) for i in [1, 2, 8, 12]] == [code, 2, 0x65, bank]
        assert [r(t, RECORD+i, 2) for i in [4, 14, 16, 18]] == [0, 0x1234, 0xABCD, 0xFEDC]
        constructors += 1
    t = fixture()
    handle = allocate(t, BANKS[0])
    maps = 0
    for code in range(5):
        address = 0x76805+50*code
        xs, ys, _ = table(address)
        xx = sorted({0, 65535, *xs, *((a+b)//2 for a, b in zip(xs, xs[1:]))})
        yy = sorted({0, 65535, *ys, *((a+b)//2 for a, b in zip(ys, ys[1:]))})
        for x, y in itertools.product(xx, yy):
            setup(t, handle, code, x, y, 0, 0, 0)
            assert t.run(0x4E3A8, 0xFFFF0000+RECORD) == lookup(address, x, y) >> 2
            maps += 1
    scaled = 0
    for code, flags, timer in itertools.product([0, 1, 2, 3, 4, 5, 255],
                                               [0, 0x10, 0x80, 0xEF, 0xFF],
                                               [0, 1, 2, 3, 4, 5, 6, 11, 12, 13, 255]):
        bank = code if code in range(5) else 0
        threshold = int.from_bytes(TCU[0x76738+2*bank:0x7673A+2*bank], 'big')
        for captured in [0, threshold-1, threshold, threshold+1, 65535]:
            setup(t, handle, code, 14080, 40000, captured, flags, timer)
            expected = candidate(code, 14080, 40000, captured, flags, timer)
            assert t.run(0x4E3A8, 0xFFFF0000+RECORD) == expected
            scaled += 1
    gates = 0
    pairs = []
    for code, inhibit, enable in itertools.product(range(5), [0, 1, 0xFE, 0xFF],
                                                  [0, 1, 6, 7, 0xFE, 0xFF]):
        setup(t, handle, code, 14080, 40000, 0, 0x25, 0)
        w(t, 0x92D5, inhibit); w(t, 0x9410, enable)
        expected = candidate(code, 14080, 40000, 0, 0x25, 0) if enable & 1 and not inhibit & 1 else 0
        publish(t, handle, expected, 0x25)
        gates += 1
        if inhibit == 0 and enable in [0, 1]:
            pairs.append(dict(code=code, reduction=expected, **paired_snapshot(t)))
    # Permission transitions execute the original producer, including hysteresis.
    permissions = []
    w(t, 0x9410, 6); w(t, 0x916D, 0); w(t, 0x92D5, 0)
    for a, v, size in [(0x80F6, 4224, 2), (0x809C, 20000, 2),
                       (0x80EE, 1000, 2), (0x80C8, 16000, 2),
                       (0x8081, 2, 1), (0x80C4, 18688, 2)]:
        w(t, a, v, size)
    for a, b in [(0, 20000), (25000, 20000), (0, 20000), (0, 0), (25000, 0)]:
        old = r(t, 0x9410)
        w(t, 0x809A, a, 2); w(t, 0x809C, b, 2)
        expected = gate_model(old, 0, 4224, a, b, 1000, 16000, 2, 18688)
        t.run(0x23BF6)
        assert r(t, 0x9410) == expected
        setup(t, handle, 1, 14080, 40000, 0, 0, 0)
        value = candidate(1, 14080, 40000, 0, 0, 0) if expected & 1 else 0
        publish(t, handle, value, 0)
        permissions.append(dict(measured_a=a, measured_b=b, old=old,
            produced_permission=expected, reduction=value, **paired_snapshot(t)))
    assert [row['produced_permission'] & 1 for row in permissions] == [0, 1, 1, 0, 1]
    traces = [lifecycle(a) for a in [0, 25000]]
    assert not traces[0]['numeric_entry']['permission'] & 1
    assert traces[1]['numeric_entry']['permission'] & 1
    assert [row['request'] for row in traces[0]['checkpoints']] == [0]*7
    assert [row['request'] for row in traces[1]['checkpoints']] == [0, 0, 1280, 1280, 0, 0, 0]
    print(json.dumps(dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        constructor_cases=constructors, map_cases=maps, scaling_cases=scaled,
        callback_gate_cases=gates, paired_callbacks=pairs,
        produced_permission_sequence=permissions, retained_manager_traces=traces,
        limits='Original helpers execute; no substituted opcodes. Inputs, cadence, references and ECU coefficients remain fixtures. Release numeric policy 4E0EE and map-input physical provenance remain separate open work.'), indent=2))


if __name__ == '__main__':
    main()
