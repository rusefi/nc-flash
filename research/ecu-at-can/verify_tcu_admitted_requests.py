"""Verify native receive/capture/fulltask traces with saved independent models."""
import json
from collections import Counter
from pathlib import Path
from tcu_receive_fixture import watchdog_state_model
from verify_tcu_captured_requests import verify

ROOT = Path(__file__).resolve().parent


def check(name, count, expiry=False):
    summary = verify(name, count, interval=lambda call: 5890 if call < 48 else 6490 if call < 256 else 4430)
    rows = json.loads((ROOT/name).read_text())['rows']
    changes = []
    old = None
    for call, row in enumerate(rows):
        e = row['extra']
        omitted = expiry and 96 <= call < 112
        assert [r['index'] for r in e['receive_prefixes']] == ([6, 1] if omitted else [8, 6, 1])
        for prefix in e['receive_prefixes']:
            assert prefix['whole_application_ram_checked'] and prefix['admitted']
            assert prefix['stopped_before_rte'] == '0x1b7d4'
        callbacks = ['0x1c10e', '0x1c20a']+([] if omitted else ['0x1c264'])
        assert e['receive_callbacks'] == callbacks
        boundaries = e['receive_boundaries']
        assert [b['entry'] for b in boundaries] == ['0x1bd10', '0x19af0']
        dispatch, watchdog = boundaries
        assert dispatch['return_pc'] == 0x1BD0C and watchdog['return_pc'] == 0x1E60A
        assert dispatch['before']['pending'] == 1
        assert dispatch['before']['bitmap'] == [66, 0 if omitted else 1]
        assert dispatch['after']['pending'] == 0 and dispatch['after']['bitmap'] == [0, 0]
        expected = watchdog_state_model(watchdog['before'])
        for actual, predicted in [('deadlines', 'expected_deadlines'), ('fresh', 'expected_fresh'), ('faults', 'expected_faults')]:
            assert watchdog['after'][actual] == expected[predicted]
        s = e['final_receive_state']
        assert s['tick'] == (call+1 if expiry else 0)
        assert s['faults'] == (0x2787 if expiry and 105 <= call < 112 else 0x2785)
        sources = e['final_sources']
        assert sources['0x809a'] == 24960
        assert sources['0x809c'] == (0 if call < 4 else 19968)
        assert sources['0x89b0'] == (0 if call == 0 else 780)
        assert [v['entry'] for v in e['input_checks']] == (['0x22f46', '0x230f0'] if call % 4 == 0 else [])
        state = ([r['record'][0] for r in row['after']['managed']],
                 sources['0x915a'], [r['bytes'][13] for r in row['after']['phases']], s['faults'])
        if state != old:
            changes.append(dict(call=call, managed=state[0], source=state[1], phases=state[2], faults=state[3]))
            old = state
    summary.update(whole_ram_receive_prefixes=sum(len(r['extra']['receive_prefixes']) for r in rows),
                   native_dispatch_calls=count, native_watchdog_checks=count,
                   input_producer_checks=sum(len(r['extra']['input_checks']) for r in rows),
                   transitions=changes, final=rows[-1]['after'])
    summary['actual_numeric_boundary_checks'] = dict(Counter(
        hex(b['entry']) for row in rows for b in row['extra']['numeric_checks']))
    return summary, rows


def main():
    initial, first = check('tcu-admitted-requests-probe.json', 32)
    extended, rows = check('tcu-admitted-requests-extended.json', 352)
    assert first == rows[:32]
    assert extended['creations'] == [dict(call=93, payload=[0, 0, 0])]
    assert extended['admitted_numeric_requests'] == [
        dict(call=i, source=306, word=521, normalized=9.0) for i in [167, 168]]
    assert rows[280]['after']['phases'][0]['bytes'][13] == 2
    assert rows[310]['after']['phases'][0]['bytes'][13] == 3
    assert rows[311]['acks'] == [[0, 5]]
    for row in rows[311:]:
        state = row['after']
        assert state['managed'] == state['phases'] == []
        assert state['0xa2b8'] == state['0x8088'] == 1
        assert state['0xa2ba'] == state['0x96c5'] == state['0x96c6'] == state['0xa1ac'] == 0
        assert state['first_list_count_a202'] == 0
        assert state['heap_first_header_9f3c'] == 0x007FFFFF
    extended['further_idle_tasks'] = 40
    expiry, _ = check('tcu-admitted-requests-expiry.json', 192, True)
    result = dict(status='PASS', scope=__doc__, initial=initial, extended=extended,
                  expiry=expiry, identical_initial32_prefix=True)
    (ROOT/'tcu-admitted-requests-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: {q: v[q] for q in ['task_calls', 'whole_ram_receive_prefixes', 'transitions']}
                      for k, v in [('extended', extended), ('expiry', expiry)]}, indent=2))


if __name__ == '__main__':
    main()
