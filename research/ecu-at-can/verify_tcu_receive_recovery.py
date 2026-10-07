"""Verify restored native receipt, selected diagnostic policy and task lag.

Recompute the watchdog model at each saved entry; compare pre-restoration
execution with the prior qualified-fault trace. Whole-RAM admission checks
execute in the probe; downstream diagnostic checks cover selected policy.
"""
import copy
import json
from pathlib import Path
from tcu_receive_fixture import CALLBACKS, watchdog_state_model
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w
from verify_tcu_base_publication import ram

ROOT = Path(__file__).resolve().parent
RECEIPT_MASKS = {0: {0: 3}, 1: {0: 0xFC, 1: 0xFF, 2: 3},
                 4: {2: 0x80}, 5: {3: 0x7F},
                 6: {3: 0x80, 4: 0xFF, 5: 3}, 8: {5: 0x30}, 9: {5: 0x40}}


def recovery_predicate_cases():
    assert TCU[0x5EB78+16*0x36+6] & 1
    count = 0
    for state in range(256):
        for value in [0, 1, 65535]:
            t = SHRotate(TCU)
            w(t, 0xA722, state)
            w(t, 0x80A4, value, 2)
            before = ram(t)
            expected = int(bool(state & 0x80) and ((state & 6) == 2 or value == 0))
            assert t.run(0x56A4A, 0x36) == expected
            assert ram(t) == before
            count += 1
    return count


def check(name, stopped=False):
    rows = json.loads((ROOT/name).read_text())['rows']
    prior = json.loads((ROOT/'tcu-qualified-receive-wheel8.json').read_text())['rows']
    assert len(rows) == 160 and all(row['status'] == 'returned' for row in rows)
    prefix = copy.deepcopy(rows[:64])
    for row in prefix:
        del row['extra']['recovery']
        row['extra'].pop('motion_checks', None)
        row['extra'].pop('motion_entries', None)
    assert prefix == prior[:64]
    if stopped:
        base = json.loads((ROOT/'tcu-receive-recovery-probe.json').read_text())['rows'][:120]
        prefix = copy.deepcopy(rows[:120])
        for row in prefix+base:
            row['extra'].pop('motion_checks', None)
            row['extra'].pop('motion_entries', None)
        assert prefix == base
    counts = dict(prefixes=0, admission=0, acknowledgements=0, scaling=0)
    transitions, last = [], None
    for call, row in enumerate(rows):
        e = row['extra']
        indices = [8, 6, 1]+([0, 4, 5, 9] if call >= 64 else [])
        assert [p['index'] for p in e['receive_prefixes']] == indices
        assert all(p['whole_application_ram_checked'] and p['admitted'] for p in e['receive_prefixes'])
        assert e['receive_callbacks'] == [hex(CALLBACKS[i]) for i in sorted(indices)]
        counts['prefixes'] += len(indices)
        dispatch, watchdog = e['receive_boundaries']
        assert dispatch['entry'] == '0x1bd10' and watchdog['entry'] == '0x19af0'
        assert dispatch['before']['bitmap'] == ([115, 3] if call >= 64 else [66, 1])
        assert dispatch['after']['bitmap'] == [0, 0] and dispatch['after']['pending'] == 0
        for field in ['fresh', 'consumer_fresh']:
            expected_flags = list(dispatch['before'][field])
            for index in indices:
                for offset, mask in RECEIPT_MASKS[index].items():
                    expected_flags[offset] |= mask
            assert dispatch['after'][field] == expected_flags
        predicted = watchdog_state_model(watchdog['before'])
        for field in ['deadlines', 'fresh', 'faults']:
            assert watchdog['after'][field] == predicted['expected_'+field]
        assert watchdog['after']['faults'] == (0x604 if call >= 64 else 0x2785)
        assert e['recovery']['0x868c'] == 1
        d = e['after_diagnostic']
        assert d['0x84d0'] == 100*(call+1)
        assert d['0xa76c'] == (0 if call < 37 else 1 if call < 42 else
                               7 if call < 65 else 1 if call < 116 else 0x81)
        assert d['0xa722'] == (0 if call < 42 else 4 if call < 116 else 0x84)
        assert d['0xa978'] == d['0xa98e'] == (1 if call < 42 else 0x1C)
        assert d['0x80e8'] == (10240 if call < 46 else 20480)
        assert d['0x9454'] == int(call < 46)
        if call >= 20:
            raw = 8430 if stopped and call >= 124 else 19269
            assert e['recovery']['0x932c'] == raw
            assert e['recovery']['0x80a4'] == raw*10//256
        if stopped:
            scaling = e['motion_checks']
            assert len(scaling) == len(e['motion_entries']) == int(call % 4 == 0)
            for b in scaling:
                assert b['whole_application_ram_checked']
                a, c, flag = b['before']
                assert b['after'] == [a*10//256, c*10//256, flag]
            counts['scaling'] += len(scaling)
            callbacks = [b for b in e['source_boundaries'] if b['entry'] in ['0x179a8', '0x17a58']]
            assert len(callbacks) == (2 if call < 120 else 0)
            if call >= 120:
                sources = e['final_sources']
                assert sources['0x810c'] == sources['0x810d'] == 4*(call-119)
                assert sources['0x80ee'] == (9861 if call < 124 else 0)
                assert sources['0x80ea'] == (7017 if call < 124 else 3070)
        assert e['recovery']['0xa99b'] == int(call >= 40)
        gates = [b for b in e['diagnostic_boundaries'] if b['entry'] == '0x56b06']
        assert len(gates) == int(call % 4 == 0)
        assert all(b['whole_application_ram_checked'] for b in gates)
        counts['admission'] += len(gates)
        assert row['acks'] == [b['arguments'] for b in row['ack_checks']]
        counts['acknowledgements'] += len(row['acks'])
        assert bool(e['wire']['payload'][7] & 32) == bool(d['0x9454'])
        state = {k: d[k] for k in ['0xa76c', '0xa722', '0xa978', '0xa98e', '0x92c9', '0x80e8', '0x9454', '0x8ee2']}
        state.update(e['recovery'])
        if state != last:
            transitions.append(dict(call=call, tick=d['0x84d0'], state=state))
            last = state
    return dict(task_pairs=len(rows), checks=counts, identical_pre_restoration64=True,
                  identical_pre_stop120=stopped,
                  transitions=transitions, final_operational_state=rows[-1]['after'])


def main():
    result = dict(status='PASS', scope=__doc__,
                  recovery_predicate_whole_ram_cases=recovery_predicate_cases(),
                  continuous=check('tcu-receive-recovery-probe.json'),
                  stopped=check('tcu-receive-recovery-stopped-captures.json', True))
    (ROOT/'tcu-receive-recovery-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
