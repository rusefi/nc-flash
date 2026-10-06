"""CAN215 shared invalid-data diagnostic -> TCU base substitution -> ECU spark.

Original functions with explicit task/tick order. Selected fields can be
replaced by FFFF to isolate receiver policy; those cases do not claim that
the ECU normally produces isolated invalid words. Active phase3 and ECU model
coefficients remain fixtures. No physical time, sender identity or actuator claim.
"""
import hashlib
import itertools
import json

from verify_can215_feedback import sender, receive, clamp
from verify_can201_byte6 import ECU, TCU, w, r
from verify_tcu_spark_requests import ramp_fixture
from verify_spark_interaction import paired
from sh_software_arithmetic import SHSoftwareArithmetic
from sh_subset import signed


def initial(recovery_gate=0):
    t = ramp_fixture()
    t.run(0x5327C)
    for a, v, n in [(0xA936, 1, 1), (0xA939, 1, 1), (0x8464, 200, 2),
                    (0x868C, 1, 1), (0x80A4, recovery_gate, 2)]:
        w(t, a, v, n)
    return t


def step(t, tick, invalid=None, unready=False):
    e, payload = sender(25, 0, invalid=int(invalid == 'all'))
    payload = bytearray(payload)
    if isinstance(invalid, int):
        payload[invalid:invalid+2] = bytes.fromhex('ffff')
    w(t, 0x84D0, tick, 4)
    receive(t, payload)
    if unready:
        # A separate dependency fixture, not a decoded on-wire state.
        w(t, 0x88EE, 3)
    for fn in [0x583DC, 0x56658, 0x57F50, 0x570F6, 0x57258,
               0x516E6, 0x517B2, 0x216D8, 0x2C234, 0x1FB8C]:
        t.run(fn)
    row = paired(r(t, 0x915A, 2), 16, 1, 1, 0, t=t, e=e)
    count = t.run(0x558CC, 0xFFFFB000)
    t.run(0x5329A); t.run(0x19414, 1)
    report = bytes(r(t, 0xB000+i) for i in range(count*3)).hex(' ')
    assert not report and r(t, 0x8F04) & 2 == 0 and r(t, 0x8EEE) & 0x40 == 0
    return {'tick': tick, 'invalid_field_byte_offset': invalid, 'unready_fixture': unready,
            'can215': payload.hex(' '), 'validity_first': r(t, 0x88EA),
            'validity_second': r(t, 0x88EE), 'combined_validity': r(t, 0xAC7A),
            'converted_first': signed(r(t, 0x88E8, 2), 16),
            'converted_second': signed(r(t, 0x88EC, 2), 16),
            'raw_group3b': r(t, 0xA771), 'active_group3b': r(t, 0xA727),
            'deadline': r(t, 0xA86C, 4), 'qualification_count': r(t, 0xA91A, 2),
            'mapped_summary': r(t, 0xA97D), 'summary': r(t, 0xA98C),
            'selected_first': signed(r(t, 0x80B4, 2), 16),
            'selected_second': signed(r(t, 0x80B2, 2), 16),
            'first_status': r(t, 0xA538), 'second_status': r(t, 0xA53C),
            'scaled_second': signed(r(t, 0x92E6, 2), 16),
            'stored_report': report, 'can216_report_bit': r(t, 0x8F04) & 2,
            'can231_report_bit': r(t, 0x8EEE) & 0x40, **row}


def main():
    record = TCU[0x5EF28:0x5EF38]
    assert record.hex() == '000101f4000111000000000025002500'
    assert TCU[0x5C81E:0x5C822].hex() == '0101fe00'
    assert TCU[0x5C5BC:0x5C5C0].hex() == '010a0000'
    assert TCU[0x5FD58:0x5FD60].hex() == '241824182418fc18'
    t = SHSoftwareArithmetic(TCU)
    for fn in [0x178EC, 0x517A4]:
        t.run(fn)
    assert r(t, 0x88EC, 2) == r(t, 0x80B2, 2) == 9240
    assert r(t, 0x88EE) == r(t, 0xA53C) == 0

    conversions = 0
    values = [0, 1, 511, 512, 537, 1000, 3788, 3789, 65534, 65535]
    for raw, offset, old_value, old_offset in itertools.product(values, values, [-1234, 300], [-5120, 123]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x88EC, old_value, 2); w(t, 0x88E4, old_offset, 2)
        receive(t, bytes.fromhex('0219')+raw.to_bytes(2, 'big')+offset.to_bytes(2, 'big')+bytes(2))
        valid = raw != 65535 and offset != 65535
        expected = clamp((raw-512)*10-clamp((offset-512)*10)) if valid else old_value
        assert signed(r(t, 0x88EC, 2), 16) == expected
        assert r(t, 0x88EE) == (2 if valid else 1)
        conversions += 1

    dependencies = 0
    for raw, status in itertools.product([0, 512, 537, 65535], [0, 1, 2, 3, 255]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x8F2E, raw, 2); w(t, 0x88E6, status)
        w(t, 0x88E4, 50, 2); w(t, 0x88EC, 123, 2)
        t.run(0x178FC)
        valid = raw != 65535 and status == 2
        assert signed(r(t, 0x88EC, 2), 16) == (clamp((raw-512)*10-50) if valid else 123)
        assert r(t, 0x88EE) == (2 if valid else 1 if raw == 65535 or status == 1 else 3)
        dependencies += 1

    policy_cases = 0
    for summary, validity, value in itertools.product(range(256), range(4), [-32768, -1001, 300, 10000]):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0xA98C, summary); w(t, 0x88EE, validity); w(t, 0x88EC, value, 2)
        w(t, 0x80B2, -1200, 2)
        t.run(0x517B2)
        if validity == 2 and summary & 1:
            expected, status = value, 1
        elif summary & 4:
            expected, status = 9240, 4
        elif summary & 2:
            expected, status = 9240, 3
        else:
            expected, status = -1200, 2
        expected = clamp(expected, -1000, 9240)
        assert signed(r(t, 0x80B2, 2), 16) == expected and r(t, 0xA53C) == status
        t.run(0x216D8)
        scaled = (abs(expected*32)//10)*(-1 if expected < 0 else 1)
        assert signed(r(t, 0x92E6, 2), 16) == clamp(scaled)
        policy_cases += 1

    lifecycles = []
    for field, recovery_gate in itertools.product([0, 2, 4, 'all'], range(2)):
        t = initial(recovery_gate)
        rows = []
        for tick in [0, 100, 599, 600, 601, 602, 1101, 1102, 1103]:
            invalid = field if 100 <= tick <= 600 else None
            d = step(t, tick, invalid)
            active = tick >= 600 and (tick <= 1101 or recovery_gate != 0)
            assert bool(d['summary'] & 8) == active
            assert (d['selected_first'], d['selected_second']) == ((9240, 9240) if active else (250, 300))
            assert d['first_status'] == (4 if active else 2 if invalid in [0, 4, 'all'] else 1)
            assert d['second_status'] == (4 if active else 2 if invalid in [2, 4, 'all'] else 1)
            assert d['spark'] == ([23.0]*4 if active else [20.0]*4)
            assert d['at_numeric'] == (914 if active else 15)
            assert bool(d['mapped_summary'] & 16) == (tick >= 600)
            rows.append(d)
        lifecycles.append({'invalid_field': field, 'recovery_gate': recovery_gate, 'timeline': rows})

    # Alternating which word is invalid never yields a healthy aggregate sample.
    t = initial()
    switched = []
    for tick, field in [(0, None), (100, 0), (300, 2), (599, 4), (600, 2)]:
        d = step(t, tick, field)
        assert bool(d['summary'] & 8) == (tick == 600)
        if tick >= 100:
            assert d['deadline'] == 600 and d['combined_validity'] == 1
        switched.append(d)

    interrupted = []
    t = initial()
    for tick, field in [(0, None), (100, 2), (599, None), (600, 0), (1099, 4), (1100, 2)]:
        d = step(t, tick, field)
        assert bool(d['summary'] & 8) == (tick == 1100)
        if tick >= 600:
            assert d['deadline'] == 1100
        interrupted.append(d)

    recovery_interruptions = []
    for unready in [False, True]:
        t = initial()
        rows = []
        for tick in [0, 100, 600, 601, 1100, 1101, 1601, 1602]:
            field = 2 if tick in [100, 600] or (tick == 1100 and not unready) else None
            d = step(t, tick, field, unready=unready and tick == 1100)
            assert bool(d['summary'] & 8) == (600 <= tick <= 1601)
            if tick == 1100:
                assert d['combined_validity'] == (3 if unready else 1)
            rows.append(d)
        recovery_interruptions.append({'unready_instead_of_invalid': unready, 'timeline': rows})

    # The healthy helper runs after group processing: deadline readiness and
    # fault clearing take separate passes, not an additional clock tick.
    t = initial()
    same_tick_recovery = []
    for tick in [0, 100, 600, 601, 1100, 1101, 1101]:
        d = step(t, tick, 2 if tick in [100, 600] else None)
        same_tick_recovery.append(d)
    assert [d['active_group3b'] for d in same_tick_recovery] == [0, 1, 5, 68, 68, 68, 0]
    assert TCU[0x5F100:0x5F108].hex() == '2500010001f40001'

    gates = []
    for gate in [0, 1, 2]:
        t = initial(); w(t, 0xA936, gate)
        rows = [step(t, tick, 2) for tick in [100, 599, 600]]
        assert bool(rows[-1]['summary'] & 8) == (gate == 1)
        gates.append({'processing_gate': gate, 'timeline': rows})

    dependencies_gate = []
    for gate in [0xA977, 0xA978]:
        t = initial(); rows = []
        for tick, fault in [(100, 0), (599, 8), (600, 0), (1099, 0), (1100, 0)]:
            e, payload = sender(25, 0, 1)
            receive(t, payload); w(t, 0x84D0, tick, 4); w(t, gate, fault)
            t.run(0x583DC); t.run(0x566E0, 0x3B)
            assert r(t, 0xA771) == (0 if fault else 3)
            assert bool(r(t, 0xA727) & 4) == (tick == 1100)
            if tick >= 600:
                assert r(t, 0xA86C, 4) == 1100
            rows.append({'tick': tick, 'gate_value': fault, 'active': r(t, 0xA727), 'deadline': r(t, 0xA86C, 4)})
        dependencies_gate.append({'summary_address': hex(gate), 'timeline': rows})

    print(json.dumps({'scope': __doc__.strip(),
                      'rom_sha256': {'ECU': hashlib.sha256(ECU).hexdigest(), 'TCU': hashlib.sha256(TCU).hexdigest()},
                      'record3b': record.hex(' '), 'initialization_cases': 2,
                      'conversion_cases': conversions, 'dependency_cases': dependencies,
                      'policy_and_scaling_cases': policy_cases, 'lifecycles': lifecycles,
                      'switching_invalid_field': switched, 'interrupted_qualification': interrupted,
                      'interrupted_recovery': recovery_interruptions, 'same_tick_recovery': same_tick_recovery,
                      'processing_gates': gates,
                      'dependency_gate_interruptions': dependencies_gate,
                      'limits': 'Explicit software task/tick fixtures; no real scheduler or time units. Only all-invalid lifecycle uses original ECU invalid flag; isolated field invalidity is receiver injection. Report absence applies to tested outputs, not every diagnostic service. Traction sender/model origin and PRHT integration remain open.'}, indent=2))


if __name__ == '__main__':
    main()
