"""Execute simultaneous CAN211 and TCU CAN216 spark/cylinder-cut paths.

Original ROM bodies and helpers, synthetic coefficients and explicit call
order. No DSC sender identification, physical units, complete scheduler or
ignition/injector hardware simulation. Shared interpreters are unchanged.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import math

from verify_can201_byte6 import ECU, TCU, w, r
from sh_exact_float import SHExactFloat, exact_bits, exact_value
from sh_software_arithmetic import SHSoftwareArithmetic


def f(e, a, v):
    w(e, a, exact_bits(v), 4)


def rf(e, a):
    return exact_value(r(e, a, 4))


def root(q):
    return Fraction(math.isqrt(max(q, 0)*16), 4)


TRACTION = [0x34B8C, 0x34BB2, 0x349CA, 0x34BBC, 0x34FFA, 0x3F600,
            0x3FF2C, 0x3F97C, 0x3FDCA, 0x3F9EC, 0x3FA3E, 0x53438]
AT = [0x35034, 0x34CEC, 0x3B584, 0x3B5C6, 0x3AE82, 0x3AEEC, 0x5295C]
GATES = {0x6566: 1, 0x65DD: 1, 0x6530: 1, 0x6531: 0, 0x700E: 1,
         0x8EF8: 0, 0x8F30: 0, 0xA3A4: 0, 0x8F4B: 0}


def paired(source, traction, enabled_at, enabled_211, cut, reverse=False, fault=False,
           t=None, e=None, model_offset=0):
    if t is None:
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x915A, source, 2)
    else:
        assert r(t, 0x915A, 2) == source
    w(t, 0x9454, cut)
    w(t, 0x92C6, 0x20)  # Byte4 invalid; unrelated to first-word/bit5 tests.
    t.run(0x18F10, 1); t.run(0x18F8C, 1)
    if e is None:
        e = SHExactFloat(ECU)
        f(e, 0x71C4, model_offset)
    else:
        assert rf(e, 0x71C4) == model_offset
    for a, v in {**GATES, 0x734A: 0x80, 0x734C: 1, 0x6A5D: 1,
                 0x6590: enabled_211, 0x6566: enabled_at, 0x69E2: int(fault),
                 0xA488: 1, 0x6567: 1, 0x65F0: 1}.items():
        w(e, a, v)
    for a, v in [(0x7140, 50), (0x71A8, 1), (0x71B0, 25), (0x71AC, 30),
                 (0x71C0, 50), (0x7A80, 30), (0x7A84, 30), (0x7D38, 100),
                 (0x7F0C, 4), (0x7A7C, -60), (0x7C94, 30), (0x7ACC, 60),
                 (0x73FC, 8), (0x73F4, 4), (0x73F8, 2), (0x7400, 1)]:
        f(e, a, v)
    for i in range(1, 5):
        w(e, 0x749E+i, 0x20)
    for i in range(8):
        w(e, 0x6A40+i, r(t, 0x8EFD+i))
    w(e, 0x6A10, 10000+traction, 2)
    for fn in (TRACTION+AT if reverse else AT+TRACTION):
        e.run(fn)
    value = 65537 if fault else 65022 if source == 32767 else source//32
    at_correction = root(25-value) if enabled_at and value < 50 else 0
    traction_correction = root(25-traction-model_offset) if enabled_211 and traction < 50 else 0
    assert rf(e, 0x6A34) == rf(e, 0x6E04) == value
    assert rf(e, 0x6E08) == 30-root(25-value)
    assert rf(e, 0x7C74) == at_correction
    assert rf(e, 0x7D2C) == traction_correction
    for fn in [0x4FD9C, 0x4FBDA, 0x4FB4E]:
        e.run(fn)
    assert rf(e, 0x7AC4) == 4
    assert rf(e, 0x7AC0) == 4+traction_correction
    assert rf(e, 0x7A94) == 4+at_correction
    assert rf(e, 0x7A90) == 4+at_correction+traction_correction
    outputs = [rf(e, a) for a in [0x7A9C, 0x7AA0, 0x7AA4, 0x7AA8]]
    assert outputs == [26-at_correction-traction_correction]*4
    for fn in [0x3AE52, 0x3B4D4, 0x3AD04, 0x3AC14]:
        e.run(fn)
    for i in range(1, 5):
        w(e, 0x6DF2, ECU[0x4F4F0+4*i+3])
        e.run(0x4D716)
    e.run(0x44E50)
    commands = [rf(e, 0x7408+4*i) for i in range(1, 5)]
    assert commands == ([0]*4 if cut else [1]*4)
    return {'tcu_source915a': source, 'can216': bytes(r(t, 0x8EFD+i) for i in range(8)).hex(' '),
            'can211_word0': 10000+traction, 'enabled_at': enabled_at,
            'enabled_211': enabled_211, 'cut': cut, 'at_network_fault': fault,
            'at_numeric': value, 'at_correction': float(at_correction),
            'traction_correction': float(traction_correction),
            'spark': [float(v) for v in outputs],
            'other_cylinder_commands': [float(v) for v in commands]}


def main():
    gate_cases = 0
    for bits in range(512):
        e = SHExactFloat(ECU)
        for i, (a, wanted) in enumerate(GATES.items()):
            w(e, a, wanted if bits & (1 << i) else 1-wanted)
        e.run(0x3AEEC)
        assert r(e, 0x6E2F) == int(bits == 511)
        gate_cases += 1
    root_cases = 0
    for request, subtract_a, subtract_b, add in itertools.product(
            [-39, 0, 16, 23, 25, 50], [0, 4], [0, 2], [0, 8]):
        e = SHExactFloat(ECU)
        for a, v in [(0x71A8, 1), (0x71B0, 25), (0x71AC, 30), (0x6E04, request),
                     (0x71E0, subtract_a), (0x71CC, subtract_b), (0x71D0, add)]:
            f(e, a, v)
        e.run(0x3B5C6)
        assert rf(e, 0x6E08) == 30-root(25-request-subtract_a-subtract_b+add)
        root_cases += 1
    for curvature in [0, -1, Fraction(1, 2048)]:
        e = SHExactFloat(ECU)
        f(e, 0x71A8, curvature); f(e, 0x6E08, 117)
        e.run(0x3B5C6)
        assert rf(e, 0x6E08) == 117
        root_cases += 1
    cap = exact_value(int.from_bytes(ECU[0xBFAE4:0xBFAE8], 'big'))
    correction_cases = 0
    for gate, enable, difference in itertools.product(range(3), range(3), [-20, 0, 5, 40, 60]):
        e = SHExactFloat(ECU)
        w(e, 0x6E3A, gate); w(e, 0x6E2F, enable)
        f(e, 0x7A80, 30); f(e, 0x6E08, 30-difference)
        e.run(0x5295C)
        assert rf(e, 0x7C74) == (min(difference, cap) if gate == enable == 1 else 0)
        correction_cases += 1
    comparison_cases = 0
    for mt, limit, request in itertools.product(range(2), [-1, 0, 25, 50], [-1, 0, 25, 50, 65537]):
        e = SHExactFloat(ECU)
        w(e, 0x734A, 0x40 if mt else 0x80)
        f(e, 0x71C0, limit); f(e, 0x6E04, request)
        e.run(0x3AE82)
        assert r(e, 0x6E3A) == int(not mt and limit > request)
        comparison_cases += 1
    examples = []
    for source, traction, enabled_at, enabled_211, cut in itertools.product(
            [0, 16*32, 23*32, 25*32, 50*32, 32767], [0, 16, 23, 25, 50], range(2), range(2), range(2)):
        row = paired(source, traction, enabled_at, enabled_211, cut)
        assert paired(source, traction, enabled_at, enabled_211, cut, reverse=True) == row
        examples.append(row)
    fault_examples = [paired(0, traction, 1, 1, cut, fault=True)
                      for traction, cut in itertools.product([0, 16, 25, 50], range(2))]
    print(json.dumps({'scope': __doc__.strip(),
                      'rom_sha256': {'ECU': hashlib.sha256(ECU).hexdigest(), 'TCU': hashlib.sha256(TCU).hexdigest()},
                      'enable_gate_cases': gate_cases, 'model_cases': root_cases,
                      'correction_cases': correction_cases, 'request_comparison_cases': comparison_cases,
                      'stock_cap_bits': ECU[0xBFAE4:0xBFAE8].hex(), 'stock_cap': float(cap),
                      'paired_cases': len(examples)*2, 'both_call_orders_identical': True,
                      'paired_matrix': examples, 'at_fault_examples': fault_examples,
                      'limits': '915A and9454 source fixtures; bounded ordinary final-spark branch with zero trims, inactive rate limit/diagnostic override. Actual task order and physical CAN211 sender/units remain unresolved.'}, indent=2))


if __name__ == '__main__':
    main()
