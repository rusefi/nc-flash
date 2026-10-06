"""Execute local-input diagnostics, original caller order, and CAN231 output.

Serial samples are bounded fixtures from verify_local_inputs. ROM functions
are never stubbed. Reporting executes its real RAM cache; stock dispatch masks reject both
groups even with the global gate enabled. This does not claim stored DTCs.
"""
import itertools
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from sh_exact_float import SHExactFloat, exact_bits, exact_value
from verify_local_inputs import InputSamples
from verify_mt_can231 import ECU, ROOT, w, r, payload

THRESHOLD_BITS = int.from_bytes(ECU[0xE02A8:0xE02AC], "big")
THRESHOLD = exact_value(THRESHOLD_BITS)
TOLERANCE_BITS = int.from_bytes(ECU[0x6C9FC:0x6CA00], "big")
TOLERANCE = exact_value(TOLERANCE_BITS)


class EndOfSegment(Exception):
    pass


class DiagnosticInputs(InputSamples, SHExactFloat):
    def __init__(self):
        super().__init__()
        self.in_segment = False
        self.calls = []
        self.reports = []
        self.mapping_reads = []

    def instruction(self, pc):
        if self.in_segment and pc == 0x1B970:
            raise EndOfSegment
        if pc in (0x6BF3A, 0x6BFAA, 0x6C0CC, 0x6C110, 0x6C1E4):
            self.calls.append(pc)
        if pc == 0x8FAC8:
            self.reports.append((self.r[4], self.r[5]))
        return super().instruction(pc)

    def read(self, address, size):
        value = super().read(address, size)
        if address in (0xE130E, 0xE1310) and size == 2:
            self.mapping_reads.append((address, value))
        return value

    def segment(self):
        self.calls.clear()
        self.reports.clear()
        self.in_segment = True
        try:
            self.run(0x1B952)
        except EndOfSegment:
            pass
        else:
            raise AssertionError("Caller segment missed its explicit end")
        finally:
            self.in_segment = False
        assert self.calls == [0x6BF3A, 0x6BFAA, 0x6C0CC, 0x6C110, 0x6C1E4]
        assert self.r[15] == 0xFFFED000


def protected(e, address, value):
    w(e, address, (value << 8) | (value ^ 255), 2)


def float_input(e, bits):
    w(e, 0x6D5C, bits, 4)


def activity_cases():
    cases = 0
    for reset, snapshot, current, latch, held, gate, bits in itertools.product(
        [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2],
        [0, 1], [0, THRESHOLD_BITS - 1, THRESHOLD_BITS, THRESHOLD_BITS + 1]
    ):
        e = DiagnosticInputs()
        protected(e, 0x9462, reset)
        protected(e, 0x7244, current)
        for a, v in [(0x8EB7, snapshot), (0x8EB6, latch), (0x8EB9, held), (0x8EDC, gate)]:
            w(e, a, v)
        float_input(e, bits)
        e.run(0x6BF3A)
        above = exact_value(bits) > THRESHOLD
        expected_latch = 0 if reset == 1 else 1 if snapshot != current else latch
        assert r(e, 0x8EB6) == expected_latch
        assert r(e, 0x8EB8) == above
        assert r(e, 0x8EB9) == (int(above) or held if gate else 0)
        cases += 1
    return cases


def counter_cases():
    cases = 0
    for reset, neutral_changed, clutch_changed, previous, current, activity, old_activity, above, count in itertools.product(
        [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1], [0, 1],
        [0, 1, 2], [0, 1, 2], [0, 1], [0, 1, 8, 255]
    ):
        e = DiagnosticInputs()
        protected(e, 0x9462, reset)
        protected(e, 0x723E, current)
        for a, v in [(0x8EB6, neutral_changed), (0x8EBA, clutch_changed),
                     (0x8EBB, previous), (0x8EB9, activity), (0x8EC0, old_activity),
                     (0x8EB8, above), (0x8EB4, count), (0x8EB5, count)]:
            w(e, a, v)
        e.run(0x6BFAA)
        changed = 0 if reset == 1 else 1 if previous != current else clutch_changed
        neutral_count = 10 if reset == 1 or neutral_changed == 1 else max(0, count - 1) if above == 1 and previous != current else count
        clutch_count = 8 if reset == 1 or changed == 1 else max(0, count - 1) if activity == 0 and old_activity == 1 else count
        assert (r(e, 0x8EBA), r(e, 0x8EB4), r(e, 0x8EB5), r(e, 0x8EC0)) == (changed, neutral_count, clutch_count, activity)
        cases += 1
    return cases


def qualification_cases():
    cases = 0
    for mode, reset, enabled, count_a, count_b, changed_a, changed_b, old in itertools.product(
        [0, 0x40, 0x80, 0xC0], [0, 1, 2], [0, 1, 2], [0, 1, 255],
        [0, 1, 255], [0, 1, 2], [0, 1, 2], [(0, 0, 0, 0), (1, 1, 1, 1), (2, 3, 4, 5)]
    ):
        e = DiagnosticInputs()
        protected(e, 0x9462, reset)
        for a, v in [(0x734A, mode), (0x911A, enabled), (0x8EB5, count_a),
                     (0x8EB4, count_b), (0x8EBA, changed_a), (0x8EB6, changed_b)]:
            w(e, a, v)
        for a, v in zip(range(0x8EBC, 0x8EC0), old):
            w(e, a, v)
        e.run(0x6C110)
        expected = old
        if reset == 1:
            expected = (0, 0, 0, 0)
        elif mode & 0x40 and enabled == 1:
            expected = ((1, 0) if count_a == 0 else (0, 1) if changed_a == 1 else old[:2]) + ((1, 0) if count_b == 0 else (0, 1) if changed_b == 1 else old[2:])
        assert tuple(r(e, a) for a in range(0x8EBC, 0x8EC0)) == expected
        cases += 1
    return cases


def reporting_cases():
    cases = 0
    for flags, reset, suppress in itertools.product(itertools.product([0, 1, 2], repeat=4), [0, 1, 2], [0, 1, 2]):
        e = DiagnosticInputs()
        protected(e, 0x9462, reset)
        w(e, 0x9A28, suppress)
        for a, v in zip(range(0x8EBC, 0x8EC0), flags):
            w(e, a, v)
        for group in (0x43, 0x44):
            w(e, 0x971E + group, 0xA5)
        e.run(0x6C1E4)  # Real8FAC8->8FB52->8FC94; global99D5=0.
        expected = []
        for group, fault, passed in [(0x43, flags[0], flags[1]), (0x44, flags[2], flags[3])]:
            report = 2 if passed == 1 else 1 if fault == 1 else None
            if report is not None:
                expected.append((group, report))
            cached = report if report is not None and reset != 1 and suppress != 1 else 0xA5
            assert r(e, 0x971E + group) == cached
        assert e.reports == expected
        assert e.mapping_reads == [(0xE1288 + 2*g, g) for g, _ in expected]
        cases += 1
    return cases


def gate_cases():
    cases = 0
    for bits, reset, remaining, old_active, old_latch in itertools.product(
        [0, TOLERANCE_BITS - 1, TOLERANCE_BITS, TOLERANCE_BITS + 1,
         TOLERANCE_BITS | 0x80000000, (TOLERANCE_BITS + 1) | 0x80000000,
         THRESHOLD_BITS, THRESHOLD_BITS + 1], [0, 1, 2], [0, 1, 2, 30, 255], [0, 1], [0, 1]
    ):
        e = DiagnosticInputs()
        protected(e, 0x9462, reset)
        float_input(e, bits)
        w(e, 0x8EDC, remaining)
        w(e, 0x8EE0, old_active)
        w(e, 0x8EE1, old_latch)
        w(e, 0x8ED8, exact_bits(0), 4)
        e.run(0x6C91E)
        value = exact_value(bits)
        expected = 30 if abs(value) > TOLERANCE or reset == 1 else max(0, remaining - 1)
        assert r(e, 0x8EDC) == expected
        assert r(e, 0x8EE0) == (0 if expected == 0 or reset == 1 else 1 if value > THRESHOLD else old_active)
        cases += 1
    return cases


def stock_dispatch_cases():
    mask_cases = 0
    for group in (0x43, 0x44):
        assert ECU[0xAC008 + 2*group:0xAC00A + 2*group] == b'\0\0'
        e = DiagnosticInputs()
        for mask in range(65536):
            e.r[5] = mask
            assert e.run(0x9034E, group) == 1  # Every runtime mask rejects.
            mask_cases += 1
    reports = 0
    for flags, active, mask in itertools.product(
            itertools.product([0, 1, 2], repeat=4), [0, 1, 2], [0, 1, 0x40, 0x80, 65535]):
        e = DiagnosticInputs()
        w(e, 0x99D5, active)
        w(e, 0x99D8, mask, 2)
        for a, v in zip(range(0x8EBC, 0x8EC0), flags):
            w(e, a, v)
        e.run(0x6C1E4)
        for group, fault, passed in [(0x43, flags[0], flags[1]), (0x44, flags[2], flags[3])]:
            expected = 2 if passed == 1 else int(fault == 1)
            assert r(e, 0x971E + group) == expected
        assert not {0x8FCB8, 0x8FE4E, 0xDAE8} & e.visited
        assert (0x9034E in e.visited) == (active == 1 and bool(e.reports))
        reports += 1
    return {'exhaustive_mask_cases': mask_cases, 'full_report_cases': reports,
            'groups_43_44_dispatch_masks': ['0000', '0000'],
            'cache_updates_but_downstream_dispatch_rejected': True}


def initialize():
    e = DiagnosticInputs()
    e.banks = [0, 255, 255]
    e.run(0xCA94)
    e.run(0x744C6)  # Stock E0CC2=0 ->911A=1; whole ROM function runs.
    assert r(e, 0x911A) == 1
    w(e, 0x734A, 0x40)
    w(e, 0x734C, 0)  # Explicit MT/local source selection, not stock AT startup.
    protected(e, 0x7002, 0)
    w(e, 0x99D5, 0)  # Full enabled-report cases are tested separately.
    for entry in (0x411F0, 0x412A2, 0x6BF20):
        e.run(entry)
    assert (r(e, 0x8EB4), r(e, 0x8EB5)) == (10, 8)
    return e


def cycle(e, sample, bits, reset=0):
    e.banks[1] = sample
    protected(e, 0x9462, reset)
    float_input(e, bits)
    for entry in (0xCADE, 0x411F0, 0x412A2, 0x6C91E):
        e.run(entry)
    e.segment()
    e.run(0x35BAA)
    e.run(0x36DB0)
    flags = 4*(r(e, 0x723A) == 1) + 2*(r(e, 0x723E) == 1) + int(r(e, 0x8EBC) == 1 or r(e, 0x8EBE) == 1)
    assert payload(e, 0x6B64) == bytes([255, flags, 255, 255, 0, 0, 0, 0])
    return {"sample": sample, "counter_clutch": r(e, 0x8EB5), "counter_neutral": r(e, 0x8EB4),
            "fault_clutch": r(e, 0x8EBC), "fault_neutral": r(e, 0x8EBE),
            "activity_hold": r(e, 0x8EDC), "can231": payload(e, 0x6B64).hex(), "reports": list(e.reports)}


def lifecycles():
    neutral = []
    e = initialize()
    sample = 255
    for transition in range(1, 11):
        sample ^= 64
        first = cycle(e, sample, THRESHOLD_BITS + 1)
        assert first['counter_neutral'] == 11 - transition
        point = cycle(e, sample, THRESHOLD_BITS + 1)
        assert point['counter_neutral'] == 10 - transition
        assert point['fault_neutral'] == (transition == 10)
        neutral.append(point)
    sample ^= 1
    neutral.append(cycle(e, sample, THRESHOLD_BITS + 1))
    assert neutral[-1]['fault_neutral'] == 1
    neutral.append(cycle(e, sample, THRESHOLD_BITS + 1))
    assert neutral[-1]['fault_neutral'] == 0 and neutral[-1]['counter_neutral'] == 10
    neutral.append(cycle(e, sample, 0, reset=1))
    assert (r(e, 0x8EB6), r(e, 0x8EBA), r(e, 0x8EBC), r(e, 0x8EBE)) == (0, 0, 0, 0)

    clutch = []
    e = initialize()
    for event in range(1, 9):
        cycle(e, 255, THRESHOLD_BITS + 1)
        for tick in range(1, 31):
            point = cycle(e, 255, 0)
            assert point['activity_hold'] == 30 - tick
            assert point['counter_clutch'] == 8 - event + int(tick < 30)
            assert point['fault_clutch'] == (event == 8 and tick == 30)
        clutch.append(point)
    clutch.append(cycle(e, 191, 0))
    assert clutch[-1]['fault_clutch'] == 1
    clutch.append(cycle(e, 191, 0))
    assert clutch[-1]['fault_clutch'] == 0 and clutch[-1]['counter_clutch'] == 8
    return neutral, clutch


def main():
    assert ECU[0xE0294:0xE0296] == bytes([8, 10])
    assert ECU[0xE02A4] == 30 and ECU[0xE0CC2] == 0
    mappings = []
    xml = ET.parse(ROOT / 'research/ecu-at-can/sources/lffeee.xml')
    for group, dtc in [(0x43, 0x0704), (0x44, 0x0850)]:
        e = DiagnosticInputs()
        assert e.run(0x902DC, group) & 65535 == dtc
        assert e.run(0x902F0, dtc) == group
        e.r[5] = 1
        assert e.run(0x9033C, group) == 0
        address = 0xE1A90 + group
        names = [node.attrib['name'].strip() for node in xml.iter('table') if node.attrib.get('address', '').lower() == f'{address:x}']
        assert len(names) == 1 and f'P{dtc:04X}' in names[0]
        mappings.append({'group': f'{group:02X}', 'dtc': f'P{dtc:04X}', 'enable_address': f'{address:X}', 'definition': names[0]})
    initializers = 0
    for neutral, clutch in itertools.product([0, 1, 2, 255], repeat=2):
        e = DiagnosticInputs()
        protected(e, 0x7244, neutral)
        protected(e, 0x723E, clutch)
        e.run(0x6BF20)
        assert (r(e, 0x8EB7), r(e, 0x8EBB), r(e, 0x8EB4), r(e, 0x8EB5)) == (int(neutral != 0), int(clutch != 0), 10, 8)
        initializers += 1
    result = {'mapping': mappings, 'initializer_cases': initializers,
              'activity_cases': activity_cases(), 'counter_cases': counter_cases(),
              'qualification_cases': qualification_cases(), 'reporting_cases': reporting_cases(),
              'activity_hold_cases': gate_cases(), 'stock_dispatch': stock_dispatch_cases()}
    result['neutral_lifecycle'], result['clutch_lifecycle'] = lifecycles()
    result['scope'] = 'Original caller segment and functions; bounded serial samples, explicit surrounding call order, real report cache; stock downstream rejection tested with global dispatch enabled and disabled. No stored DTC or OEM PRHT reception claim.'
    Path(__file__).with_name('local-input-faults-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if not k.endswith('lifecycle')}, indent=2))


if __name__ == '__main__':
    main()
