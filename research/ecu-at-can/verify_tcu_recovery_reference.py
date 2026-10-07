"""Check actual reference/discrepancy/phase boundaries and unchanged prefixes."""
import copy
import json
from collections import Counter
from pathlib import Path

from verify_tcu_motion_conversion import converted

ROOT = Path(__file__).resolve().parent


def check(name, count, approach=False, second_approach=False):
    rows = json.loads((ROOT/name).read_text())['rows']
    assert len(rows) == count and all(r['status'] == 'returned' for r in rows)
    totals, branches = Counter(), Counter()
    changes, last = [], None
    history, head, timestamp = [18*4096]*24, 0, 0
    stop = 280 if second_approach else 220 if approach else 120
    for row in rows:
        e = row['extra']
        call = row['call']
        delta = (5890 if call < 48 else 9120 if second_approach and call >= 128
                 else 4430 if approach and call >= 80 else 6490)
        captures = [b for b in e['source_boundaries'] if b['entry'] in ['0x179a8','0x17a58']]
        if call < stop:
            timestamp += delta
            assert [b['argument'] for b in captures] == [12160*(call+1), timestamp]
            if call:
                head = (head+1)%24
                history[head] = delta//10
        else:
            assert not captures
        stale = call == 0 or call >= stop+4
        period = 0x7FFFFFFF if stale else sum(history)
        measured = 0 if stale else min(32767,153600000//period)
        assert e['final_sources']['0x80ee'] == measured
        assert e['final_sources']['0x9238'] == period
        checks = e['reference_checks']
        for b in checks:
            totals[b['entry']] += 1
            if b['entry'] == '0x31720':
                assert b['predicate_checked'] and b['returned'] == b['expected']
            elif b['entry'] == '0x20fac':
                assert b['discrepancy_checked']
                for address, key in [('0x91a6','flags'),('0x91c6','count'),('0x91c4','cache'),('0x91c9','index')]:
                    assert b['after'][address] == b['expected'][key]
            elif b['entry'] == '0x209b4':
                assert b['reference_checked'] and b['returned'] == b['expected']['result']
                assert b['after']['0x80ec'] == b['expected']['reference']
                assert b['after']['0x9198'] == b['expected']['period'] & 0xFFFFFFFF
                assert b['after']['0x91a6'] == b['expected']['flags']
                branches[b['expected']['branch']] += 1
        assert sum(b['entry']=='0x209b4' for b in checks) == int(row['call']%4==0)
        assert len(e['motion_checks']) == int(row['call']%4==0)
        assert len(e['motion_entries']) == len(e['motion_checks'])
        for entry, boundary in zip(e['motion_entries'], e['motion_checks']):
            assert boundary['whole_application_ram_checked']
            a,b = [converted(entry[key]) for key in ['source_80ea','source_91a2']]
            assert boundary['before'][:2] == [a,b]
            assert boundary['after'][:2] == [a*10//256,b*10//256]
        assert all(p['whole_application_ram_checked'] for p in e['receive_prefixes'])
        refs = [b for b in checks if b['entry']=='0x209b4']
        if refs:
            b = refs[0]
            pending = [p for p in checks if p['entry']=='0x31720' and p['return_pc']==0x209DA]
            assert len(pending)==1
            active = bool(pending[0]['returned'])
            before = b['before']
            timer = 0 if active else before['0x8196']
            refresh = not active and 4*timer >= 37
            cache = ((before['0x80ee'] if before['0x810c'] < 5 else 0)
                     if refresh else before['0x91a8'])
            index = before['0x8081'] if refresh else before['0x91c7']
            assert [b['after'][a] for a in ['0x8196','0x91a8','0x91c7']] == [timer,cache,index]
            assert b['selected_registers']['5']==int(not refresh)
            signed_cache = cache if cache < 32768 else cache-65536
            assert b['selected_registers']['9']==signed_cache & 0xFFFFFFFF
            state = dict(branch=b['expected']['branch'], source=b['returned'],
                         cache=b['branch_inputs']['0x91a8'], index=b['branch_inputs']['0x91c7'],
                         settle=b['branch_inputs']['0x8196'], flags=b['branch_inputs']['0x91a6'],
                         gate=b['branch_inputs']['0x9194'], phase=b['branch_inputs']['head_phase'],
                         phase_count=b['branch_inputs']['0x96c5'],
                         active=e['after_diagnostic']['0xa722'], scaled=e['recovery']['0x80a4'])
            if state != last:
                changes.append(dict(call=row['call'], **state));last=state
    return rows, dict(task_pairs=count,
                     receive_prefix_checks=sum(len(r['extra']['receive_prefixes']) for r in rows),
                     motion_checks=sum(len(r['extra']['motion_checks']) for r in rows),
                     ack_checks=sum(len(r['ack_checks']) for r in rows),
                     creations=[dict(call=r['call'], payload=c['payload']) for r in rows for c in r['creations']],
                     retirements=[dict(call=r['call'], callbacks=r['retired']) for r in rows if r['retired']],
                     actual_boundary_checks=dict(totals),
                     branches=dict(branches), transitions=changes,
                     final=rows[-1]['after'])


def main():
    rows, baseline = check('tcu-recovery-reference-probe.json',160)
    old = json.loads((ROOT/'tcu-receive-recovery-stopped-captures.json').read_text())['rows']
    stripped = copy.deepcopy(rows)
    for row in stripped:
        del row['extra']['reference_checks']
    assert stripped == old
    for row in rows:
        call = row['call']
        checks = row['extra']['reference_checks']
        if call % 4 == 0:
            pending = [b for b in checks if b['entry']=='0x31720' and b['return_pc']==0x209DA]
            assert len(pending)==1 and pending[0]['returned']==int(call>=36)
            b = next(b for b in checks if b['entry']=='0x209b4')
            if call >= 36:
                g = b['branch_inputs']
                assert (g['0x91a8'],g['0x91c7'],g['0x8196']) == (10865,0,0)
            if call >= 124:
                assert b['expected']['branch']=='fallback'
                assert b['returned']==10865*4096//14492==3070
                assert b['branch_inputs']['0x91a6']==16
    result = dict(status='PASS', scope=__doc__, baseline=baseline,
                  identical_baseline160=True)
    path = ROOT/'tcu-recovery-reference-target-approach.json'
    if path.exists():
        approach_rows, approach = check(path.name,256,True)
        assert approach_rows[:80] == rows[:80]
        assert [(r['call'],c['payload']) for r in approach_rows for c in r['creations']] == [(33,[0,0,0]),(113,[2,0,0])]
        assert [r['call'] for r in approach_rows if r['retired']] == [108]
        assert approach_rows[108]['acks'] == [[0,2],[0,0x25]]
        for row in approach_rows[108:113]:
            a = row['after']
            assert a['phases'] == [] and a['managed'] == []
            assert a['heap_first_header_9f3c'] == 0x007FFFFF
        for row in approach_rows[116:]:
            assert row['extra']['after_diagnostic']['0xa722'] == 0x84
        for call, timer in [(108,4),(112,8),(116,0)]:
            b = next(b for b in approach_rows[call]['extra']['reference_checks'] if b['entry']=='0x209b4')
            assert b['branch_inputs']['0x8196'] == timer
            assert b['branch_inputs']['0x91a8'] == 10865 and b['branch_inputs']['0x91c7'] == 0
        b = next(b for b in approach_rows[224]['extra']['reference_checks'] if b['entry']=='0x209b4')
        assert b['expected']['branch']=='fallback' and b['returned']==3070
        assert approach_rows[224]['extra']['recovery']['0x80a4']==329
        result.update(approach=approach,identical_approach80=True)
        second_path = ROOT/'tcu-recovery-reference-second-approach.json'
        if second_path.exists():
            second_rows, second = check(second_path.name,320,True,True)
            assert second_rows[:128] == approach_rows[:128]
            assert [(r['call'],c['payload']) for r in second_rows for c in r['creations']] == [(33,[0,0,0]),(113,[2,0,0])]
            assert [r['call'] for r in second_rows if r['retired']] == [108,194]
            assert second_rows[194]['acks'] == [[1,2],[1,0x25]]
            qualifier = next(b for b in second_rows[190]['extra']['numeric_checks'] if b['entry']==0x32614)
            assert qualifier['inputs'] == [2,0,7,0,7017,6889,7145,19,0,2]
            assert qualifier['actual'] == qualifier['expected'] == [1,20,0,0]
            for row in second_rows[194:]:
                a = row['after']
                assert a['phases']==[] and a['managed']==[]
                assert a['0x96c5']==a['0xa2ba']==a['first_list_count_a202']==0
                assert a['heap_first_header_9f3c']==0x007FFFFF
            for call,cache,timer in [(204,7017,12),(284,0,92)]:
                b = next(b for b in second_rows[call]['extra']['reference_checks'] if b['entry']=='0x209b4')
                assert [b['after'][a] for a in ['0x91a8','0x91c7','0x8196']] == [cache,3,timer]
                assert b['selected_registers']['5']==0 and b['selected_registers']['9']==cache
            policy_transitions,last = [],None
            for row in second_rows:
                call,e=row['call'],row['extra']
                d=e['after_diagnostic']
                assert d['0xa722']==(0 if call<42 or call>=284 else 4 if call<116 else 0x84)
                assert d['0xa978']==d['0xa98e']==(1 if call<42 else 0x11 if call>=284 else 0x1C)
                assert d['0xa76c']==(0 if call<37 else 1 if call<42 or 65<=call<116 or call>=285 else 7 if call<65 else 0x81)
                assert bool(d['0x92c9']&64)==(44<=call<288)
                assert d['0x80e8']==(20480 if 46<=call<290 else 10240)
                assert d['0x9454']==int(call<46)
                assert bool(e['wire']['payload'][7]&32)==bool(d['0x9454'])
                if call>=284:
                    assert e['recovery']['0x80a4']==e['recovery']['0x932c']==0
                    assert e['final_sources']['0x80ea']==e['final_sources']['0x80ec']==0
                state={a:d[a] for a in ['0xa76c','0xa722','0xa978','0xa98e','0x92c9','0x92d5','0x80e8','0x9454']}
                state.update(e['recovery'])
                if state!=last:
                    policy_transitions.append(dict(call=call,state=state));last=state
            second['policy_transitions']=policy_transitions
            second['continuous_empty_phase_and_free_heap_pairs']=len(second_rows)-194
            second['cut_request_reassertion_proved']=False
            result.update(second_approach=second,identical_second128=True)
    (ROOT/'tcu-recovery-reference-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
