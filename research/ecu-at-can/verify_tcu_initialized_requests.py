"""Verify natural request overlap and actual acknowledgement RAM boundaries.

Direct31C18 bitmap tests include all application RAM and callback effects.
Saved complete-task trace checks allocation, phase records, payload and event
ordering; no whole-task semantic or physical cadence claim.
"""
import itertools
import json
from pathlib import Path

import verify_tcu_phase_retirement as retire
from verify_can201_byte6 import TCU, w, r
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent


def direct():
    cases = 0
    for index, phase, bitmap in itertools.product([0, 15], [0, 3], range(1024)):
        t = retire.RetirementTCU()
        retire.seed(t, index, [7], phase)
        for j in range(10):
            w(t, 0x95D4+15*index+j, int(bool(bitmap & (1 << j))))
        for a, value, size in [(0x95C2, 2, 1), (0x95C4, 7, 2),
                               (0x95BE, 2, 1), (0x95BF, 7, 1), (0x95D0, 2, 1)]:
            w(t, a, value, size)
        ref = SHRotate(TCU)
        ref.ram = dict(t.ram)
        expected, callbacks = retire.ack_model(ref, index, 0xFFFF)
        t.r[5] = 0xFFFF
        result = t.run(0x31C18, index)
        assert result == expected and ram(t) == ram(ref)
        assert t.retired == callbacks
        cases += 1
    # Non-binary ack bytes and latch values distinguish truthy group completion
    # from the exact1 retirement latch, using the original function.
    for ack_value, latch, code in itertools.product([1, 2, 255], [0, 1, 2, 255], [0, 7, 11]):
        t = retire.RetirementTCU()
        retire.seed(t, 15, [code], 0)
        for j in range(10):
            w(t, 0x95D4+15*15+j, ack_value)
        w(t, 0x95D4+15*15+14, latch)
        ref = SHRotate(TCU)
        ref.ram = dict(t.ram)
        expected, callbacks = retire.ack_model(ref, 15, 0xFFFF)
        t.r[5] = 0xFFFF
        assert t.run(0x31C18, 15) == expected
        assert ram(t) == ram(ref) and t.retired == callbacks
        cases += 1
    return cases


def baseline():
    data = json.loads((ROOT/'tcu-initialized-requests-probe.json').read_text())
    rows = data['rows']
    assert len(rows) == 32 and not data['explicit_timer_before_each_task']
    assert all(row['status'] == 'returned' for row in rows)
    payloads = [[0, 0, 0], [1, 2, 0], [2, 2, 0]]
    creations = []
    acks = []
    for row in rows:
        call = row['call']
        expected_count = sum(call >= first for first in [1, 5, 9])
        after = row['after']
        assert after['0xa2ba'] == after['0x96c5'] == expected_count
        assert after['0xa1ac'] == 0 and not row['retired']
        assert len(row['acks']) == len(row['ack_checks'])
        assert [v['arguments'] for v in row['ack_checks']] == row['acks']
        acks.extend(row['acks'])
        assert all(not v['retired'] for v in row['ack_checks'])
        for event in row['creations']:
            index = len(creations)
            assert call == [1, 5, 9][index]
            assert event['return_pc'] == 0x48FAC and event['payload'] == payloads[index]
            before, completed = event['before'], event['after']
            assert before['0xa2ba'] == before['0x96c5'] == index
            assert completed['0xa2ba'] == completed['0x96c5'] == index+1
            assert completed['0xa1ac'] == 0
            assert completed['0xa2b8'] == (2 if index == 0 else 3)
            phase = completed['phases'][-1]
            assert phase['index'] == index and phase['bytes'][10:13] == payloads[index]
            record = completed['managed'][-1]
            assert record['index'] == index
            assert int.from_bytes(bytes(record['entry'][4:6]), 'big') == 7
            assert record['record'][:2] == [2, index]
            pointers = [v['pointer'] for v in completed['managed']]
            assert len(set(pointers)) == index+1
            creations.append(dict(call=call, payload=event['payload'],
                                  pointer=record['pointer'], count=index+1))
        assert [v['record'][:2] for v in after['managed']] == [[2, i] for i in range(expected_count)]
    assert len(creations) == 3 and len(acks) == 25
    assert all(0 <= index < 3 and group in retire.GROUPS for index, group in acks)
    return dict(task_calls=32, whole_ram_ack_boundaries=25,
                prior_whole_ram_command_boundaries=64,
                selected_gate_boundaries=sum(len(row['checks']) for row in rows),
                creations=creations, acks=acks, retired=0)


def timed():
    data = json.loads((ROOT/'tcu-initialized-requests-timer-completion.json').read_text())
    rows = data['rows']
    assert data['explicit_timer_before_each_task'] and len(rows) == 352
    assert all(row['status'] == 'returned' for row in rows)
    additions = {'request_word_915a', 'first_list_count_a202', 'ramp_timers_8115',
                 'primary_timer_phase_8494', 'heap_first_header_9f3c'}

    def common(value):
        if isinstance(value, dict):
            return {k: common(v) for k, v in value.items() if k not in additions}
        if isinstance(value, list):
            return [common(v) for v in value]
        return value

    for name, count in [('tcu-initialized-requests-timer-probe.json', 160),
                        ('tcu-initialized-requests-timer-final.json', 256)]:
        earlier = json.loads((ROOT/name).read_text())
        assert common(rows[:count]) == common(earlier['rows'])
    creations = [(row['call'], event['payload']) for row in rows for event in row['creations']]
    assert creations == [(1, [0, 0, 0]), (5, [1, 2, 0]), (9, [2, 2, 0]),
                         (29, [7, 10, 0]), (105, [6, 0, 0]), (109, [5, 1, 0])]
    retired = [(row['call'], code) for row in rows for fn, code in row['retired']
               if fn == '0x30b82']
    assert retired == [(29, 0), (29, 1), (29, 2), (102, 7), (149, 6), (321, 5)]
    acknowledgements = 0
    for row in rows:
        assert len(row['acks']) == len(row['ack_checks'])
        assert row['acks'] == [v['arguments'] for v in row['ack_checks']]
        assert row['retired'] == [[hex(fn), code] for v in row['ack_checks']
                                 for fn, code in v['retired']]
        assert row['after']['0xa1ac'] == 0
        assert row['after']['request_word_915a'] == 0x7FFF
        acknowledgements += len(row['acks'])
        if 151 <= row['call'] <= 320:
            # State5 entry resets at151. Even timer phases increment before
            # even-numbered task calls; no service observes expiry until321.
            count = (row['call']-150)//2
            assert row['after']['ramp_timers_8115'][4] == count
            assert row['after']['managed'][-1]['record'][0] == 5
        if row['call'] >= 321:
            after = row['after']
            assert after['0xa2b8'] == after['0x8088'] == 1
            assert after['0xa2ba'] == after['0x96c5'] == after['first_list_count_a202'] == 0
            assert after['0x96c4'] == 6 and after['0x96c6'] == 0
            assert not after['managed'] and not after['phases']
            assert after['heap_first_header_9f3c'] == data['initial']['heap_first_header_9f3c'] == 0x007FFFFF
    assert TCU[0x763FC] == 85
    assert rows[320]['after']['ramp_timers_8115'][4] == 85
    assert rows[321]['acks'] == [[5, 5]]
    assert acknowledgements == 60
    return dict(timer_task_pairs=352, original_creations=creations,
                retired_records=retired, whole_ram_ack_boundaries=acknowledgements,
                prior_whole_ram_command_boundaries=704,
                selected_gate_boundaries=sum(len(row['checks']) for row in rows),
                timer_expiry_call=320, final_release_call=321,
                subsequent_idle_tasks=30, prefixes_compared=[160, 256],
                nonzero_request_observed=False)


def main():
    result = dict(status='PASS', scope=__doc__, direct_whole_ram_cases=direct(),
                  baseline=baseline(), timed=timed())
    (ROOT/'tcu-initialized-requests-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS', result['direct_whole_ram_cases'], 'direct; baseline', result['baseline']['task_calls'])


if __name__ == '__main__':
    main()
