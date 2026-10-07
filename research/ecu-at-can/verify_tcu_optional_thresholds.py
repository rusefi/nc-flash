"""Execute optional4530C threshold modifiers and whole selection replays.

Stock ROM only. Explicit stored adjustment words and admission inputs remain
fixtures; no EEPROM identity, real scheduling or physical response asserted.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_rotate import SHRotate
from sh_subset import signed
from verify_tcu_release_thresholds import ObservedRelease, TCU, w, r
from verify_tcu_curve_sources import curve
from verify_tcu_request_dispatch import curve as byte_curve
from verify_tcu_transition_classification import proposal_model
from verify_tcu_qualification_limit import selection_then_limit

ROOT = Path(__file__).resolve().parent


def word(a): return int.from_bytes(TCU[a:a+2], 'big')


def adjust(t, slot, value, axis):
    value &= 65535
    if slot < 5:
        delta = signed(r(t, 0x616A+2*word(0x73BEE+2*slot), 2), 16)
        bound = min(32767, max(0, curve(t, r(t, 0x9AEC+4*slot, 4), axis) + delta))
        result = bound if signed(r(t, 0x809C, 2), 16) >= signed(word(0x77372), 16) else min(value, bound)
        return result, bound
    bound = max(0, signed(signed(r(t, 0x9B42+2*(slot-5), 2), 16) - TCU[0x73BE8+slot-5]*64, 16))
    return min(value, bound), None


def floor(slot, value, axis, mode):
    mode &= 255
    bound = 0 if mode == 2 else TCU[0x73BEB+slot-2]*64
    if mode != 1 and slot != 2:
        bound = max(bound, byte_curve(0x73C02+7*(slot-3), axis) >> 2)
    return max(value & 65535, bound)


def admitted(t):
    return (signed(r(t, 0x80F2, 2), 16) >= signed(word(0x77370), 16)
            and not r(t, 0x916F)&16 and not r(t, 0x92D9)&16
            and r(t, 0x8080) != 255 and not r(t, 0x916C)&1)


def direct():
    t = SHRotate(TCU); counts = dict(getter=0, upper=0, lower=0, floor=0)
    for index, value in itertools.product([0, 6, 7, 8], [0, 1, 32767, 32768, 65535]):
        w(t, 0x616A+2*index, value, 2)
        assert signed(t.run(0x24584, index), 32) == signed(value, 16)
        counts['getter'] += 1
    # Synthetic constant curves exercise original lookup and both clamp edges.
    p = 0xFFFFA900
    for j, v in enumerate([2, 0, 0, 65535, 0, 0]): t.write(p+2*j, v, 2)
    for slot, delta, base, incoming, comparison in itertools.product(range(5),
            [-32768, -1, 0, 1, 32767], [0, 1000, 32767, 65535],
            [0, 1, 1000, 32767, 65535], [0, 23039, 23040, 32767, 32768]):
        w(t, 0x9AEC+4*slot, p, 4)
        t.write(p+8, base, 2); t.write(p+10, base, 2)
        w(t, 0x616A+2*word(0x73BEE+2*slot), delta, 2); w(t, 0x809C, comparison, 2)
        want, cached = adjust(t, slot, incoming, 46080)
        t.r[5] = incoming; t.r[6] = 46080; sp = t.r[15]
        assert t.run(0x44E14, slot) & 65535 == want
        assert r(t, 0x9B42+2*slot, 2) == cached and t.r[15] == sp
        counts['upper'] += 1
    for slot, cache, incoming in itertools.product(range(5, 10),
            [0, 511, 512, 513, 32767, 32768, 65535], [0, 1, 1000, 32767, 65535]):
        w(t, 0x9B42+2*(slot-5), cache, 2)
        want, _ = adjust(t, slot, incoming, 46080)
        t.r[5] = incoming; t.r[6] = 46080; sp = t.r[15]
        assert t.run(0x44E14, slot) & 65535 == want
        assert r(t, 0x9B42+2*(slot-5), 2) == cache and t.r[15] == sp
        counts['lower'] += 1
    for slot, mode, axis, incoming in itertools.product([2, 3, 4], [0, 1, 2, 3],
            [0, 8191, 8192, 8193, 10240, 12288, 65535], [0, 1, 511, 512, 1000, 32767, 65535]):
        t.r[5] = incoming; t.r[6] = axis; t.r[7] = mode; sp = t.r[15]
        assert t.run(0x44F5A, slot) & 65535 == floor(slot, incoming, axis, mode) == incoming
        assert t.r[15] == sp; counts['floor'] += 1
    return counts


class ObservedOptional(ObservedRelease):
    def __init__(self):
        super().__init__(); self.optional_pending = []; self.optional_rows = []
        self.threshold_rows = []; self.capture = None; self.threshold_expected = None

    def instruction(self, pc):
        while self.optional_pending and self.optional_pending[-1]['return_pc'] == pc:
            entry = self.optional_pending.pop()
            assert self.r[0] & 65535 == entry['expected'], entry
            if entry['cached'] is not None:
                assert r(self, 0x9B42+2*entry['slot'], 2) == entry['cached']
            self.optional_rows.append(entry)
        if pc == 0x4530C:
            self.capture = dict(axis=r(self, 0x941E if r(self, 0x9B40) in [13, 14] else 0x9B3E, 2),
                                alternate=(word(0x77372)*2)&65535,
                                floor_axis=(r(self, 0x92F0, 2)*8)&65535,
                                mode_high=2 if r(self, 0x92D1)&8 else 0)
        if pc == 0x453CA:
            slot = self.r[14]
            value = curve(self, r(self, 0x9AEC+4*slot, 4), self.capture['axis'])
            use_adjust = admitted(self) and r(self, 0x9B32+slot) in [0, 1] and slot in [0, 1, 2, 5, 6, 7]
            mode = (r(self, 0x9AE9)&1) + self.capture['mode_high']
            use_floor = slot in [2, 3, 4] and mode != 0
            if use_adjust: value, _ = adjust(self, slot, value, self.capture['alternate'])
            if use_floor: value = floor(slot, value, self.capture['floor_axis'], mode)
            self.threshold_expected = dict(slot=slot, expected=value, adjust=use_adjust, floor=use_floor)
        if pc in [0x44E14, 0x44F5A]:
            slot, value, axis = self.r[4], self.r[5], self.r[6]
            if pc == 0x44E14: expected, cached = adjust(self, slot, value, axis)
            else: expected, cached = floor(slot, value, axis, self.r[7]), None
            self.optional_pending.append(dict(function=f'{pc:05x}', slot=slot, incoming=value&65535,
                                              axis=axis&65535, expected=expected, cached=cached, return_pc=self.pr))
        if pc == 0x45436:
            row = self.threshold_expected
            assert self.r[13] & 65535 == row['expected'], (row, self.r[13]&65535)
            self.threshold_rows.append(row); self.threshold_expected = None
        return super().instruction(pc)


def restore(snapshot):
    t = ObservedOptional(); t.ram = {int(a, 16): v for a, v in snapshot['ram'].items()}
    t.samples = {int(a, 16): v for a, v in snapshot['samples'].items()}
    return t


def configure(t, gate, mode, offset, comparison, dynamic=0):
    for a, v in [(0x8080, 0), (0x9C12, 0), (0x9B40, 0), (0x9C7C, 0),
                 (0x9E88, dynamic), (0x9B5C, 0), (0x916F, 0), (0x92D7, 0),
                 (0x9AE9, mode&1), (0x92D1, 8 if mode&2 else 0),
                 (0x92D9, 0), (0x916C, 0)]: w(t, a, v)
    for a, v in [(0x80F2, 32000 if gate else 31999), (0x9B3E, 6400),
                 (0x809C, comparison), (0x92F0, 1280)]: w(t, a, v, 2)
    for index in [0, 6, 7, 8]: w(t, 0x616A+2*index, offset, 2)


def replays(snapshots):
    rows = []
    for gate, mode, offset, comparison in itertools.product([0, 1], range(4), [-1000, 0, 1000], [3200, 23040]):
        t = restore(snapshots['150']); configure(t, gate, mode, offset, comparison)
        sp = t.r[15]; t.run(0x4530C, limit=1000000)
        assert t.r[15] == sp and not t.optional_pending and len(t.threshold_rows) == 10
        assert len(t.optional_rows) == (6 if gate else 0) + (3 if mode else 0)
        assert [r(t, 0x9B1E+2*i, 2) for i in range(10)] == [x['expected'] for x in t.threshold_rows]
        pair = proposal_model(t); t.r[5] = 0xFFFEC000; t.run(0x4508A, 0xFFFEC004)
        assert [t.read(0xFFFEC004, 1), t.read(0xFFFEC000, 1)] == list(pair)
        rows.append(dict(gate=gate, mode=mode, offset=offset, comparison=comparison,
                         thresholds=t.threshold_rows, optional=t.optional_rows, proposal=list(pair)))
    return rows


def full_replays(snapshots):
    rows = []
    for call, gate, mode, offset in itertools.product([150, 211], [0, 1], [0, 3], [-1000, 1000]):
        t = restore(snapshots[str(call)]); t.application_call = call
        configure(t, gate, mode, offset, 23040)
        sp = t.r[15]; t.run(0x44CFE, limit=1000000); selection_then_limit(t)
        assert t.r[15] == sp and not t.optional_pending and len(t.threshold_rows) == 10
        rows.append(dict(call=call, gate=gate, mode=mode, offset=offset,
                         optional=t.optional_rows, thresholds=t.threshold_rows,
                         proposed=r(t, 0x8084), accepted=r(t, 0x8081), creations=t.creation_calls))
    return rows


def admission_cases(snapshot):
    rows = []
    for measurement, flags, source in itertools.product([31999, 32000, 32767, 32768],
            [(0, 0, 0, 0), (16, 0, 0, 0), (0, 16, 0, 0),
             (0, 0, 1, 0), (0, 0, 0, 255), (32, 32, 2, 0)], ['normal', 'dynamic', 'fixed']):
        t = restore(snapshot); configure(t, 1, 3, 1000, 23040, int(source == 'dynamic'))
        w(t, 0x9B5C, int(source == 'fixed')); w(t, 0x80F2, measurement, 2)
        for a, v in zip([0x916F, 0x92D9, 0x916C, 0x8080], flags): w(t, a, v)
        w(t, 0x9C12, flags[3])
        t.run(0x4530C, limit=1000000)
        wanted = sum(row['adjust'] for row in t.threshold_rows)
        actual = sum(row['function'] == '44e14' for row in t.optional_rows)
        assert len(t.threshold_rows) == 10 and wanted == actual
        assert sum(row['function'] == '44f5a' for row in t.optional_rows) == 3
        rows.append(dict(measurement=measurement, flags=flags, source=source, adjust_calls=actual,
                         kinds=[r(t, 0x9B32+i) for i in range(10)]))
    return rows


def main():
    raw = (ROOT/'tcu-fault-selection-snapshots.json').read_bytes(); snapshots = json.loads(raw)
    result = dict(scope=__doc__, tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                  snapshots_sha256=hashlib.sha256(raw).hexdigest(), direct=direct())
    print('Direct:', result['direct'], flush=True)
    result['replays'] = replays(snapshots); result['full_replays'] = full_replays(snapshots)
    result['admission'] = admission_cases(snapshots['150'])
    (ROOT/'tcu-optional-thresholds-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Threshold/scan:', len(result['replays']), 'full:', len(result['full_replays']), flush=True)


if __name__ == '__main__': main()
