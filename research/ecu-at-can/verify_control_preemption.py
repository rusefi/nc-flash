"""Verify retained preemption, actual task resumption and queue drain evidence."""
import copy
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def check(name, count):
    data = json.loads((ROOT/name).read_text())
    old = json.loads((ROOT/'control-interrupt-timer-prefix10.json').read_text())
    assert data['status'] == 'scheduler idle reached' and data['pc'] == 0x3D0C
    assert len(data['rows']) == len(data['interrupts']) == count
    assert data['requested_selector'] == 2 and len(data['preemptions']) == 1
    assert data['rows'][:4] == old['rows'][:4]
    item = data['preemptions'][0]
    assert item['cycle'] == 4 and item['pc'] == 0xDCBA and item['selector'] == 2
    assert item['before_registers'] == item['after_registers']
    assert item['before_state'] == item['after_state']
    assert item['sr'] == 1 and item['pr'] == 0xDCB0
    assert item['resumed_task'] == 4 and item['higher_priority_task'] == 7
    assert item['epilogue_whole_ram'] is True
    assert item['saved_sp'] == item['before_registers'][15]-156
    assert item['wheel'] == 6 and item['divider'] == 1
    assert [row['target'] for row in item['rte']] == [0xE26C, 0xDCBA]
    events = Counter()
    acquisitions = consumers = 0
    mmio = [['read', 0xFFFFF718, 2, 192], ['write', 0xFFFFF718, 2, 64]]
    for cycle, row in enumerate(data['rows']):
        before_tick = cycle+1+int(cycle > 4)
        assert row['cycle'] == cycle
        assert row['queued'] == dict(wheel=before_tick, divider=before_tick % 5,
            selected=7, queue2=int(before_tick % 5 == 0), queue3=0, pending=0)
        assert row['mmio'] == mmio*(2 if cycle == 4 else 1)
        timer = Counter(v['pc'] for v in row['timer'])
        for pc in [0xF28C, 0x1062E, 0xFA68]:
            assert timer[pc] == 1+int(cycle == 4)
        assert timer[0xFBE8] == timer[0xE5FC] == int(before_tick % 5 == 0)
        acquisitions += sum(v['target'] == 0xE26C for v in row['rte'])
        local = Counter(v['words'][1] for v in row['callbacks'] if v['target'] == 0x2BCE6)
        assert local[1] == int(before_tick % 4 == 3)
        assert local[2] == int(before_tick % 5 == 0)
        events.update(local)
        assert len(row['consumed']) == len(row['callbacks'])
        for check_row in row['consumed']:
            assert check_row['return_pc'] == 0xDCA4 and check_row['result'] == 0
            consumers += 1
        assert row['final'] == dict(queue2=0, queue3=0, pending=0,
            task3_available=2, task4_available=2, task7_available=2)
    assert acquisitions == count+1
    assert events[1] == (count+2)//4 and events[2] == (count+1)//5
    assert len(data['queue2_checks']) == len(data['queue2_callbacks']) == (count+1)//5
    assert all(v['return_pc'] == 0xDC50 and v['result'] == 0 for v in data['queue2_checks'])
    return data, dict(outer_idle_interrupts=count, extra_nonidle_interrupts=1,
        acquisitions=acquisitions, event1=events[1], event2=events[2],
        queue3_whole_ram_returns=consumers, queue2_whole_ram_returns=len(data['queue2_checks']),
        exact_unaffected_first4=True, exact_interrupted_register_restoration=True,
        decode_checks=len(data['decode']), activity_checks=len(data['activity']),
        qualification_observations=len(data['qualification']))


def main():
    data, summary = check('control-preemption-prefix10.json', 10)
    before = json.loads((ROOT/'control-preemption-selector2-before-options10.json').read_text())
    normalized = copy.deepcopy(data)
    del normalized['requested_selector']
    del normalized['preemptions'][0]['selector']
    assert normalized == before
    result = dict(status='PASS', scope=__doc__, prefix10=summary,
        exact_default_after_reproduction_options=True,
        limits='Explicit arrival atDCBA/selector2, entrySRF0, syntheticstack and suppliedperipherals. No physicalclock/admission/remoteDSC proof.')
    full = ROOT/'control-preemption-probe.json'
    if full.exists():
        longer, summary = check(full.name, 600)
        assert longer['rows'][:10] == data['rows']
        assert longer['preemptions'] == data['preemptions']
        prior = json.loads((ROOT/'control-interrupt-timer-probe.json').read_text())
        def event_fields(trace):
            return [row['fields'] for row in trace['rows'] if any(
                v['target'] == 0x2BCE6 and v['words'][1] == 2 for v in row['callbacks'])]
        current_fields, prior_fields = event_fields(longer), event_fields(prior)
        assert len(current_fields) == len(prior_fields) == 120
        assert current_fields == prior_fields
        assert longer['rows'][-1]['fields'] == prior['rows'][-1]['fields']
        result.update(full600=summary, exact_initial10=True,
            exact_120_event2_monitored_fields=True, exact_final_monitored_fields=True)
    (ROOT/'control-preemption-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
