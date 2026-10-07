"""Recompute selected actual-return models and verify captured-task trace prefixes."""
import json
from collections import Counter
from pathlib import Path

from verify_tcu_captured_requests import verify
from verify_tcu_ascending_map import candidate
from verify_tcu_ascending_release import release
from verify_tcu_ascending_phase import model
from verify_tcu_spark_requests import reference

ROOT = Path(__file__).resolve().parent


def check(name, count, approach=False):
    interval = (lambda call: 5890 if call < 48 else 6490 if call < 256 else 4430) if approach else None
    summary = verify(name, count, True, interval)
    rows = json.loads((ROOT/name).read_text())['rows']
    counts = Counter()
    successes, changes, active = [], [], []
    prior = None
    for row in rows:
        for boundary in row['extra']['numeric_checks']:
            entry, args, actual = boundary['entry'], boundary['inputs'], boundary['actual']
            counts[hex(entry)] += 1
            if entry == 0x32614:
                expected = list(model(*args))
                if expected[0]:
                    successes.append(dict(call=row['call'], index=boundary['index'], inputs=args))
            elif entry == 0x4E036:
                value = candidate(*args) if boundary['permission'] & 1 and not boundary['inhibit'] & 1 else 0
                expected = [value, (args[4] & 127) | (128 if value else 0)]
                active.append(dict(call=row['call'], inputs=args, request=value))
            elif entry == 0x4E0EE:
                expected = list(release(*args)[:3])
            else:
                assert entry == 0x1FB8C
                values, flags, selected, flag, result = reference(*args)
                # Other9158 bits are outside the selected saved-input oracle.
                assert actual[:3] == [values, flags, (-selected) & 65535]
                assert actual[3] & 1 == int(flag != 0) and actual[4] == result
                continue
            assert actual == expected
        after = row['after']
        state = ([r['record'][0] for r in after['managed']],
                 after['request_word_915a'], [r['bytes'][13] for r in after['phases']])
        if state != prior:
            changes.append(dict(call=row['call'], managed_states=state[0],
                                source=state[1], phases=state[2]))
            prior = state
    summary.update(boundary_checks=dict(counts), phase_successes=successes,
                   numeric_candidates=active, state_changes=changes,
                   final_state=rows[-1]['after'])
    return summary, rows


def main():
    baseline, rows = check('tcu-captured-phase-probe.json', 256)
    previous = json.loads((ROOT/'tcu-received-captured-requests-extended.json').read_text())['rows']
    for current, old in zip(rows, previous):
        trimmed = dict(current, extra={k: v for k, v in current['extra'].items() if k != 'numeric_checks'})
        assert trimmed == old
    approach, next_rows = check('tcu-captured-phase-approach.json', 512, True)
    assert rows == next_rows[:256]
    assert approach['numeric_candidates'] == [dict(call=167,
        inputs=[0, 7984, 39444, 19722, 0, 0], request=494)]
    assert approach['phase_successes'] == [dict(call=280, index=0,
        inputs=[0, 0, 7, 0, 14446, 14327, 14583, 0, 92, 0])]
    assert approach['boundary_checks'] == {'0x1fb8c': 256, '0x32614': 93,
                                           '0x4e036': 1, '0x4e0ee': 71}
    assert next_rows[310]['after']['phases'][0]['bytes'][13] == 3
    assert next_rows[311]['acks'] == [[0, 5]]
    assert next_rows[311]['retired'] == [['0x30b82', 0], ['0x30a9e', 0], ['0x31168', 0]]
    for row in next_rows[311:]:
        state = row['after']
        assert state['managed'] == state['phases'] == []
        assert state['0xa2b8'] == state['0x8088'] == 1
        assert state['0xa2ba'] == state['0x96c5'] == state['0x96c6'] == state['0xa1ac'] == 0
        assert state['first_list_count_a202'] == 0
        assert state['heap_first_header_9f3c'] == 0x007FFFFF
        assert state['request_word_915a'] == 32767
    approach['retirement_call'] = 311
    approach['further_idle_tasks'] = 200
    result = dict(status='PASS', scope=__doc__, baseline=baseline, approach=approach,
                  baseline_prior_256_prefix_identical=True, approach_256_prefix_identical=True)
    (ROOT/'tcu-captured-phase-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: {q: v[q] for q in ['task_calls', 'boundary_checks', 'state_changes']}
                      for k, v in [('baseline', baseline), ('approach', approach)]}, indent=2))


if __name__ == '__main__':
    main()
