"""TCU request records -> original aggregation -> CAN216 -> ECU spark.

Uses the unchanged ROM and complete original helpers. Record values, local
phase and timer samples are fixtures; no physical units or scheduler model.
"""
import hashlib
import itertools
import json

from verify_can201_byte6 import ECU, TCU, w, r
from sh_software_arithmetic import SHSoftwareArithmetic
from sh_subset import signed
from verify_spark_interaction import paired


def initialized():
    t = SHSoftwareArithmetic(TCU)
    t.run(0x1FB18)
    assert [r(t, 0x915C+2*i, 2) for i in range(5)] == [32767]*5
    assert [r(t, 0x9166+i) for i in range(5)] == [255]*5
    assert r(t, 0x915A, 2) == 32767 and r(t, 0x80BE, 2) == 0
    return t


def put(t, index, value, flag):
    t.r[5] = value & 65535
    t.r[6] = flag
    t.run(0x1FB4A, index)


def reference(values, flags, base):
    # Stock enables only records1/2. Selection walks in index order and
    # independently retains the last nonsentinel value and flag.
    values, flags = list(values), list(flags)
    for i in [0, 3, 4]:
        values[i], flags[i] = 32767, 255
    v, b = list(values), list(flags)
    if v[2] == 0 and v[1] != 32767:
        v[2], b[2] = 32767, 255
    selected_value = next((signed(x, 16) for x in reversed(v) if x != 32767), 0)
    selected_flag = next((x for x in reversed(b) if x != 255), 0)
    result = max(signed((base-selected_value) & 65535, 16), 0) if selected_flag == 1 else 32767
    return values, flags, selected_value, selected_flag, result


def admitted(class_, accepted, code, inhibit):
    return (class_ not in [0, 255] and not inhibit and code not in [10, 17]
            and ((accepted == 0 and class_ != 1) or (accepted == 1 and class_ not in [1, 2])))


def ramp_fixture(accepted=1, class_=6, elapsed=0, duration=10, start=320, timer=0):
    t = initialized()
    for a, v, size in [(0x8080, class_, 1), (0x8081, accepted, 1),
                       (0x9530, 1, 1), (0x953F, 3, 1), (0x953C, start, 2),
                       (0x953E, duration, 1), (0x8170, elapsed, 1),
                       (0x8171, timer, 1), (0x9542, 1, 1), (0x80B4, 250, 2)]:
        w(t, a, v, size)
    t.run(0x216D8)
    assert r(t, 0x92E4, 2) == 800
    return t


def main():
    assert TCU[0x5CD0C:0x5CD11] == bytes([0, 1, 1, 0, 0])
    base_cases = 0
    for raw in sorted(set(range(0, 65536, 257)) | {0, 1, 9, 10, 249, 250, 10239, 10240, 10241, 32767, 32768, 55295, 55296, 55297, 65535}):
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x80B4, raw, 2)
        t.run(0x216D8)
        value = signed(raw, 16)*32
        quotient = (abs(value)//10) * (-1 if value < 0 else 1)
        expected = min(32767, max(-32768, quotient)) & 65535
        assert r(t, 0x92E2, 2) == r(t, 0x92E4, 2) == expected
        base_cases += 1
    setter_cases = 0
    for i, value, flag in itertools.product(range(5), [0, 1, 320, 32766, 32767, 32768, 65535], [0, 1, 2, 128, 255]):
        t = initialized()
        put(t, i, value, flag)
        assert [r(t, 0x915C+2*j, 2) for j in range(5)] == [value if j == i else 32767 for j in range(5)]
        assert [r(t, 0x9166+j) for j in range(5)] == [flag if j == i else 255 for j in range(5)]
        t.run(0x1FB6E, i)
        assert r(t, 0x915C+2*i, 2) == 32767 and r(t, 0x9166+i) == 255
        setter_cases += 1

    aggregate_cases = 0
    priority_examples = []
    for a, b, fa, fb, base in itertools.product(
            [0, 320, 640, 32766, 32767, 32768, 65535],
            [0, 320, 640, 32766, 32767, 32768, 65535],
            [0, 1, 2, 128, 255], [0, 1, 2, 128, 255], [0, 800, 32767, 32768]):
        t = initialized()
        values, flags = [123, a, b, 234, 345], [1, fa, fb, 1, 1]
        for i in range(5):
            put(t, i, values[i], flags[i])
        w(t, 0x92E4, base, 2); w(t, 0x9158, 0xA6)
        t.sr = 0xA0
        t.run(0x1FB8C)
        after_values, after_flags, selected, mode, expected = reference(values, flags, base)
        assert r(t, 0x915A, 2) == expected
        assert r(t, 0x80BE, 2) == (-selected) & 65535
        assert r(t, 0x9158) == 0xA6 | int(mode != 0)
        assert t.sr & 0xF0 == 0xA0
        assert [r(t, 0x915C+2*i, 2) for i in range(5)] == after_values
        assert [r(t, 0x9166+i) for i in range(5)] == after_flags
        if base == 800 and a in [320, 640] and b in [0, 320, 640, 32767] and fa == fb == 1:
            priority_examples.append({'record1': a, 'record2': b, 'selected': selected, 'source915a': expected})
        aggregate_cases += 1

    admission_cases = 0
    for class_, accepted, code, inhibit in itertools.product(
            [0, 1, 2, 3, 6, 127, 128, 255], [0, 1, 2, 3, 4, 5, 6, 255], [0, 10, 17, 255], range(2)):
        t = SHSoftwareArithmetic(TCU)
        for addr, val in [(0x8080, class_), (0x8081, accepted), (0x9B40, code), (0x916F, inhibit)]:
            w(t, addr, val)
        assert t.run(0x2C30C) == int(admitted(class_, accepted, code, inhibit))
        admission_cases += 1

    ramp_cases = 0
    for accepted, class_, duration, elapsed, start, timer in itertools.product(
            [0, 1, 2, 5], [0, 1, 2, 6, 255], [10], [0, 1, 5, 9, 10],
            [0, 320, 640], [0, 121, 122]):
        t = ramp_fixture(accepted, class_, elapsed, duration, start, timer)
        t.run(0x2C234)
        value = start*(duration-elapsed)//duration
        live = admitted(class_, accepted, 0, 0) and timer < TCU[0x76FF6] and value > 0
        assert r(t, 0x915E, 2) == (value if live else 32767)
        assert r(t, 0x9167) == (1 if live else 255)
        assert r(t, 0x9530) & 1 == int(live)
        if not live:
            assert r(t, 0x953F) == 0 and r(t, 0x9542) & 1 == 0
        t.run(0x1FB8C)
        assert r(t, 0x915A, 2) == (800-value if live else 32767)
        ramp_cases += 1

    lifecycle = []
    t = ramp_fixture()
    for elapsed in [0, 1, 5, 9, 10]:
        w(t, 0x8170, elapsed)
        t.run(0x2C234); t.run(0x1FB8C)
        source = r(t, 0x915A, 2)
        row = paired(source, 16, 1, 1, 0, t=t)
        lifecycle.append({'timer8170': elapsed, 'record1_value': r(t, 0x915E, 2),
                          'record1_flag': r(t, 0x9167), **row})
    competition = []
    for record2 in [0, 320, 640, 32767]:
        t = ramp_fixture()
        t.run(0x2C234)
        put(t, 2, record2, 1 if record2 != 32767 else 255)
        t.run(0x1FB8C)
        competition.append({'record2': record2, **paired(r(t, 0x915A, 2), 16, 1, 1, 1, t=t)})

    print(json.dumps({'scope': __doc__.strip(),
                      'rom_sha256': {'ECU': hashlib.sha256(ECU).hexdigest(), 'TCU': hashlib.sha256(TCU).hexdigest()},
                      'base_scaling_cases': base_cases, 'setter_reset_cases': setter_cases, 'aggregate_cases': aggregate_cases,
                      'admission_cases': admission_cases, 'complete_ramp_caller_cases': ramp_cases,
                      'priority_examples': priority_examples, 'producer_to_ecu_lifecycle': lifecycle,
                      'competing_record_to_ecu_cases': competition,
                      'limits': 'Phase3 starts active by fixture; phase1/2 entry, upstream source80B4, record2 policy4C7AC, timer scheduling and physical roles remain open.'}, indent=2))


if __name__ == '__main__':
    main()
