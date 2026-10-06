"""Original reference production and two-sample error -> request release -> CAN.

Measured80EE and reference-source80EC are explicit input samples. Reference
words9218, capture95C0 and output80D8 are produced by original firmware.
No physical units or full application-task schedule are inferred.
"""
import hashlib
import itertools
import json
import random

from sh_rotate import SHRotate
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_phase_retirement import full_fixture, RetirementTCU, GROUPS
from verify_tcu_request_admission import periodic, paired_snapshot

COEFFICIENTS = [14492, 8438, 5755, 4096, 2920, 2384, 12976]
CAPTURE_INDEX = {3: 3, 4: 4, 8: 3, 9: 4, 11: 3}


def error(measured, reference):
    difference = signed(signed(measured, 16)-signed(reference, 32), 32)
    return min(16319, max(-16319, difference))


def main():
    assert [int.from_bytes(TCU[a:a+2], 'big', signed=True) for a in range(0x70000, 0x7000E, 2)] == COEFFICIENTS
    rng = random.Random(0x30C20)
    samples = [0, 1, 63, 64, 4095, 4096, 7014, 16383, 16384, 32767, 32768, 32769, 65534, 65535]
    samples += [rng.randrange(65536) for _ in range(512)]
    t = SHRotate(TCU)
    for sample in samples:
        t.macl = 0x12345678
        w(t, 0x80EC, sample, 2)
        t.run(0x2117C)
        assert t.macl == 0x12345678
        assert [signed(r(t, 0x9218+4*i, 4), 32) for i in range(7)] == [signed(sample, 16)*c//4096 for c in COEFFICIENTS]

    raw_cases = 0
    for index, reference in itertools.product(range(7), [-2147483648, -16320, -1, 0, 1, 5000, 16320, 2147483647]):
        values = {-32768, -16320, -16319, -1, 0, 1, 16319, 16320, 32767}
        values |= {v for v in [reference-16320, reference-16319, reference-16318,
                               reference+16318, reference+16319, reference+16320] if -32768 <= v <= 32767}
        w(t, 0x95C6, index)
        w(t, 0x9218+4*index, reference, 4)
        for measured in values:
            w(t, 0x80EE, measured, 2)
            assert signed(t.run(0x30C20), 32) == error(measured, reference)
            raw_cases += 1

    capture_cases = 0
    for state, code in itertools.product([0, 1, 2, 255], list(range(256))+[256, 65535]):
        for address, value, size in [(0x95C2, state, 1), (0x95C4, 77, 2),
                                     (0x95C6, 2, 1), (0x95C0, 123, 2), (0x80D8, 456, 2),
                                     (0x80EE, 1234, 2)]:
            w(t, address, value, size)
        for index in range(7):
            w(t, 0x9218+4*index, 1000*index, 4)
        t.run(0x30B28, code)
        if state and code in CAPTURE_INDEX:
            index = CAPTURE_INDEX[code]
            expected = error(1234, 1000*index) & 65535
            assert r(t, 0x95C2) == 2 and r(t, 0x95C4, 2) == code and r(t, 0x95C6) == index
            assert r(t, 0x95C0, 2) == r(t, 0x80D8, 2) == expected
        else:
            assert [r(t, a, n) for a, n in [(0x95C2, 1), (0x95C4, 2), (0x95C6, 1), (0x95C0, 2), (0x80D8, 2)]] == [state, 77, 2, 123, 456]
        capture_cases += 1

    filter_cases = 0
    for prior, reference, measured in itertools.product(
            [-32768, -16319, -1, 0, 1, 16319, 32767], [-20000, 0, 5000, 20000],
            [-32768, -16320, -1, 0, 1, 63, 64, 127, 128, 32767]):
        w(t, 0x95C2, 2)
        w(t, 0x95C6, 4)
        w(t, 0x9218+16, reference, 4)
        w(t, 0x80EE, measured, 2)
        w(t, 0x95C0, prior, 2)
        t.run(0x30B9E)
        raw = error(measured, reference)
        assert signed(r(t, 0x95C0, 2), 16) == raw
        assert signed(r(t, 0x80D8, 2), 16) == (prior+raw)//2
        filter_cases += 1
    reset_cases = 0
    for state, old in itertools.product([v for v in range(256) if v != 2], [0, 0x7FFF, 0x8000, 0xFFFF]):
        w(t, 0x95C2, state)
        w(t, 0x95C0, old, 2)
        w(t, 0x80D8, old, 2)
        t.run(0x30B9E)
        assert r(t, 0x95C0, 2) == r(t, 0x80D8, 2) == 0
        assert r(t, 0x95C2) == state
        reset_cases += 1

    sequence = []
    w(t, 0x95C2, 2)
    w(t, 0x95C6, 4)
    w(t, 0x9218+16, 0, 4)
    previous = 3000
    w(t, 0x95C0, previous, 2)
    for measured in [1000, 1000, 128, 0, 127, 0, -1, 0]:
        w(t, 0x80EE, measured, 2)
        t.run(0x30B9E)
        expected = (previous+measured)//2
        assert signed(r(t, 0x80D8, 2), 16) == expected
        sequence.append({'previous_raw': previous, 'new_raw': measured, 'output': expected})
        previous = measured

    base = full_fixture()
    lifecycles, paired_checks = [], 0
    cases = [(5, delta, head) for delta, head in itertools.product([1000, 128, 127], [0, 15])]
    cases += [(3, 1000, 0), (4, 1000, 0)]
    for old, delta, head in cases:
        t = RetirementTCU()
        t.ram = dict(base.ram)
        w(t, 0x96C4, head)
        w(t, 0x80EC, 7014, 2)
        t.run(0x2117C)
        references = [signed(r(t, 0x9218+4*i, 4), 32) for i in range(7)]
        assert references == [24816, 14449, 9854, 7014, 5000, 4082, 22220]
        target = references[old-1]
        w(t, 0x606F, old)
        t.run(0x48BC0)
        for address, value in [(0x8080, 6), (0x8084, old-1), (0x92D0, 4), (0xA93A, 1)]:
            w(t, address, value)
        for address, value in [(0x80EA, 4672), (0x80F6, 4224), (0x809C, 20000), (0x80EE, target+delta)]:
            w(t, address, value, 2)
        t.run(0x48C08, limit=1000000)
        record = r(t, 0xA2BC, 4) & 65535
        phase = 0x95D4+15*head
        if old == 5:
            assert signed(r(t, 0x80D8, 2), 16) == delta
        rows, last, release_started = [], None, None
        for call in range(201):
            if call:
                if call == 80:
                    w(t, 0x80EE, target, 2)
                t.run(0x11014)
                t.run(0x2117C)
                t.run(0x30B9E)
                t.run(0x31524, 2, limit=1000000)
                periodic(t)
            else:
                t.run(0x4C7AC)
                t.run(0x1FB8C)
            state = (r(t, phase+13), r(t, record), r(t, 0x96C5))
            if old == 5 and state[1] == 5 and release_started is None:
                release_started = call
            if state != last or call in [79, 80, 81]:
                rows.append({'call': call, 'phase_state': state[0], 'request_state': state[1],
                             'phase_count': state[2], 'measured': signed(r(t, 0x80EE, 2), 16),
                             'raw_error': signed(r(t, 0x95C0, 2), 16),
                             'filtered_error': signed(r(t, 0x80D8, 2), 16), **paired_snapshot(t)})
                paired_checks += 1
                last = state
            if not state[2]:
                break
        assert call < 200 and r(t, 0x8088) == 1 and r(t, 0xA2BA) == 0
        assert r(t, 0x915A, 2) == 0x7FFF
        assert {group for index, group in t.acks if index == head} == set(GROUPS)
        if old == 5:
            assert release_started == (80 if delta == 127 else 81)
        # Retirement callback returns capture state to1; next producer clears history.
        t.run(0x30B9E)
        assert r(t, 0x95C0, 2) == r(t, 0x80D8, 2) == 0
        lifecycles.append({'old': old, 'code': old+4, 'head': head, 'initial_difference': delta,
                           'produced_references': references, 'release_started': release_started,
                           'retired_at': call, 'checkpoints': rows})
    print(json.dumps({'scope': __doc__.strip(), 'tcu_sha256': hashlib.sha256(TCU).hexdigest(),
                      'reference_source_cases': len(samples), 'reference_word_checks': len(samples)*7,
                      'clipped_difference_cases': raw_cases, 'creation_capture_cases': capture_cases,
                      'two_sample_filter_cases': filter_cases, 'inactive_reset_cases': reset_cases,
                      'sample_sequence': sequence, 'lifecycles': lifecycles,
                      'paired_can216_ecu_checks': paired_checks,
                      'limits': 'Input80EC/80EE sensor production, units and real task order remain unproved. Explicit producer schedule and input step, original reference/error/phase/request/queue/CAN bodies. No direct80D8 or9218 injection in integrated cases. Full ascending/overlap/composite, traction and OEM roof goals remain open.'}, indent=2))


if __name__ == '__main__':
    main()
