"""Original descending phase gates, qualification and selector-to-ECU lifecycle.

All firmware bodies execute. Sources, references and interleaving are explicit
fixtures; call counts are not physical time. Other group acknowledgements and
ascending/composite phase policy are outside this verifier.
"""
import hashlib
import itertools
import json

from sh_relative_branch import SHRelativeBranch
from sh_subset import signed
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_dispatch import fixture
from verify_tcu_request_admission import periodic, paired_snapshot


def family(code):
    return code-5  # Descending codes5..11 only.


def word(address):
    return int.from_bytes(TCU[address:address+2], 'big', signed=True)


def initial_delay_model(code, bank, operation, timer):
    assert code in range(5, 12) and bank in range(5)
    delay = 0 if operation else TCU[0x70A8A+5*family(code)+bank]
    return int(signed(timer, 16) >= 2*delay), delay


def phase_fixture(code, index=0, operation=0):
    t = SHRelativeBranch(TCU)
    w(t, 0x96C4, index)
    w(t, 0x96C5, 1)
    w(t, 0x95DE+15*index, code)
    w(t, 0x95DF+15*index, operation)
    return t


def selector_fixture(old):
    t = fixture()
    t.run(0x31524, 0)
    w(t, 0x606F, old)
    t.run(0x48BC0)
    for address, value in [(0x8080, 6), (0x8084, old-1), (0x92D0, 4), (0xA93A, 1)]:
        w(t, address, value)
    for address, value in [(0x80EA, 4672), (0x80F6, 4224),
                           (0x809C, 20000), (0x80EE, 1000)]:
        w(t, address, value, 2)
    t.run(0x48C08, limit=1000000)
    w(t, 0x9218+4*(old-1), 5000, 4)
    return t


def main():
    counts = {}
    timer_cases = 0
    for code, bank, op, index in itertools.product(range(5, 12), range(5), [0, 1, 0x17], [0, 15]):
        t = phase_fixture(code, index, op)
        w(t, 0x808C, bank)
        # Original software conversion of +0.5 truncates to zero for nonzero op.
        threshold = 0 if op else 2*TCU[0x70A8A+5*family(code)+bank]
        for timer in sorted({0, 1, max(0, threshold-1), threshold, threshold+1,
                             32767, 32768, 65535}):
            w(t, 0x8380+2*index, timer, 2)
            got = t.run(0x317E4, index)
            assert got == initial_delay_model(code, bank, op, timer)[0], (code, bank, op, index, timer, got)
            timer_cases += 1
    counts['descending_timer_gate'] = timer_cases

    initial_cases = 0
    for code, reference, ready, flags in itertools.product(range(5, 12), [-1000, 0, 1000],
                                                           [False, True], [0, 2, 16, 18, 4, 32, 128]):
        t = phase_fixture(code)
        threshold = word(0x70AEE+2*(family(code)+5))
        timer = 2*TCU[0x70A8A+5*family(code)]-int(not ready)
        w(t, 0x8380, timer, 2)
        w(t, 0x9218+4*TCU[0x5D428+code], reference, 4)
        w(t, 0x92C6, flags)
        for measured in [-32768, reference+threshold-1, reference+threshold,
                         reference+threshold+1, 32767]:
            w(t, 0x80EE, measured, 2)
            t.r[5] = code
            got = signed(t.run(0x3241C, 0), 32)
            expected = 1 if not flags & 0x12 and ready and measured >= reference+threshold else -1
            assert got == expected, (code, reference, ready, flags, measured, got)
            initial_cases += 1
    counts['initial_phase_predicate'] = initial_cases

    qualified_cases = 0
    for code, enable, global_op, reference, flags in itertools.product(
            range(5, 12), [0, 1], [0, 5], [0, 1000], [0, 2, 16]):
        threshold = TCU[0x70B14+2*family(code)+enable]
        if global_op == 5 and enable and code in [8, 9]:
            threshold = TCU[0x70B22+code-8]
        for measured, prior in itertools.product(
                [reference-129, reference-128, reference+127, reference+128, 127],
                [0, max(0, threshold-2), threshold-1, 254, 255]):
            t = phase_fixture(code)
            w(t, 0x9410, enable*2)
            w(t, 0x9C88, global_op)
            w(t, 0x9218+4*TCU[0x5D446+code], reference, 4)
            w(t, 0x80EE, measured, 2)
            w(t, 0x96EF, prior)
            w(t, 0x971A, 0xA7)
            w(t, 0x92C6, flags)
            # A sentinel makes the disabled path's lack of writes observable.
            w(t, 0x9700, 12345, 4)
            w(t, 0x9704, 54321, 4)
            t.r[5], t.r[6] = code, 0
            got = signed(t.run(0x324CE, 0), 32)
            if flags & 0x12:
                expected_count, expected = prior, -1
                assert [r(t, 0x9700, 4), r(t, 0x9704, 4), r(t, 0x971A)] == [12345, 54321, 0xA7]
            else:
                assert r(t, 0x9700, 4) == (reference+128) & 0xFFFFFFFF
                assert r(t, 0x9704, 4) == (reference-128) & 0xFFFFFFFF
                assert r(t, 0x971A) == 0xA5
                qualified = (measured >= reference-128 if code == 11 else
                             reference-128 <= measured < reference+128 or
                             code in [8, 9, 10] and measured < 128)
                expected_count = min(prior+1, 255) if qualified else 0
                expected = 2 if qualified and expected_count >= threshold else -1
            assert r(t, 0x96EF) == expected_count
            assert got == expected, (code, enable, global_op, reference, flags, measured, prior, got, expected)
            qualified_cases += 1
    counts['target_band_and_counter'] = qualified_cases

    bypass_cases = 0
    for measured, extra in itertools.product([871, 872, 1127, 1128], [0x47FF, 0x4800, 0x4801, 0x8000, 0xFFFF]):
        t = phase_fixture(11)
        w(t, 0x9218+4*TCU[0x5D446+11], 1000, 4)
        w(t, 0x80EE, measured, 2)
        w(t, 0x96CC, extra, 2)
        t.r[5], t.r[6] = 11, 0
        got = signed(t.run(0x324CE), 32)
        expected = 2 if measured >= 872 and signed(extra, 16) >= word(0x770C2) else -1
        assert got == expected
        bypass_cases += 1
    counts['code11_counter_bypass'] = bypass_cases

    dispatch_cases = 0
    for code, state, qualifies in itertools.product(range(5, 12), [0, 1], [False, True]):
        t = phase_fixture(code)
        w(t, 0x9218+4*TCU[0x5D446+code], 1000, 4)
        w(t, 0x9218+4*TCU[0x5D428+code], 5000, 4)
        w(t, 0x80EE, 1000, 2)
        w(t, 0x96EF, TCU[0x70B14+2*family(code)]-(1 if qualifies else 2))
        t.r[5], t.r[6], t.r[7] = 0, code, 0
        t.write(t.r[15], 0, 4)
        got = signed(t.run(0x321AE, state), 32)
        assert got == (state+1 if qualifies else -1)
        assert 0x324CE in t.visited
        assert (0x3241C in t.visited) == (state == 0)
        dispatch_cases += 1
    counts['initial_target_route_and_state_dispatch'] = dispatch_cases

    completion_cases = 0
    for index, timer in itertools.product(range(16), [0, 7, 8, 9, 32767, 32768, 65535]):
        t = SHRelativeBranch(TCU)
        w(t, 0x83C0+2*index, timer, 2)
        got = signed(t.run(0x325DA, index), 32)
        assert got == (3 if signed(timer, 16) >= word(0x770C0) else -1)
        assert signed(t.run(0x325F2, index), 32) == -1
        completion_cases += 1
    counts['completion_timer'] = completion_cases

    lifecycles = []
    expected_milestones = {
        3: [(46, 1, 2), (80, 1, 3), (81, 1, 4), (100, 1, 5), (129, 2, 5), (135, 2, 0), (158, 3, 0)],
        4: [(22, 1, 2), (80, 1, 3), (81, 1, 5), (109, 2, 5), (111, 2, 0), (138, 3, 0)],
        5: [(22, 1, 2), (80, 1, 3), (81, 1, 5), (111, 2, 5), (117, 2, 0), (142, 3, 0)],
    }
    paired_checks = 0
    for old in [3, 4, 5]:
        t = selector_fixture(old)
        rows, milestones = [], []
        last = None
        for call in range(201):
            if call:
                if call == 80:
                    w(t, 0x80EE, 5000, 2)
                t.run(0x11014)
                t.run(0x31524, 2, limit=1000000)
                periodic(t)
            else:
                t.run(0x4C7AC)
                t.run(0x1FB8C)
            state = r(t, 0x95E1), r(t, 0x9F40)
            if state != last:
                if call:
                    milestones.append((call, *state))
                rows.append({'primary_timer_calls': call, 'phase': state[0], 'request': state[1],
                             'phase_timer': r(t, 0x8380, 2), 'completion_timer': r(t, 0x83C0, 2),
                             'qualification_count': r(t, 0x96EF),
                             'managed_request_count': r(t, 0xA2BA), **paired_snapshot(t)})
                paired_checks += 1
                last = state
            if state == (3, 0):
                break
        assert milestones == expected_milestones[old], (old, milestones)
        assert r(t, 0xA2BA) == 0 and r(t, 0xA202, 2) == 0
        assert r(t, 0x915A, 2) == 0x7FFF
        assert r(t, 0x96C5) == 1  # Other group acknowledgements are not simulated.
        lifecycles.append({'old': old, 'requested': old-1, 'transition_code': old+4, 'checkpoints': rows})
    counts['selector_to_phase_completion_lifecycles'] = len(lifecycles)
    counts['paired_can216_ecu_checks'] = paired_checks
    print(json.dumps({'scope': __doc__.strip(), 'tcu_sha256': hashlib.sha256(TCU).hexdigest(),
                      'checks': counts, 'lifecycles': lifecycles,
                      'limits': 'Original code with synthetic source/reference changes and interleaving. Phase completion is not ring retirement: other request groups are not initialized or acknowledged. Upward/overlapping/composite policy, source identities, units, actual task timebase, DSC and OEM PRHT reception remain open.'}, indent=2))


if __name__ == '__main__':
    main()
