"""Verify actual diagnostic prefixes and shared-clock arrival/interleaving records.

Reuse independent capture/time/wheel/hold checks; preserve original task-body
differential comparisons and diagnostic admission whole-RAM runtime oracles.
"""
import copy
import hashlib
import json

from verify_tcu_capture_timeline import ROOT,verify as verify_shared,expected_captures
from probe_tcu_capture_timeline import Timeline


def verify(name,count):
    rows,result = verify_shared(name,count,diagnostic=True)
    number = checks = wraps = 0
    changes = []
    for call,row in enumerate(rows):
        extra = row['extra']
        events = extra['diagnostic_interrupts']
        start,end = call*81920,(call+1)*81920
        assert len(events) == end//500000-start//500000
        assert extra['diagnostic_schedule'] == dict(period=500000,epoch=0,total=end//500000,
            suppressed_once_application_calls=call+1,zero_service_latency=True)
        boundaries = []
        for event in events:
            number += 1
            n = number
            compare = (15625*n)&65535
            assert event['number'] == n and event['peripheral_match_time'] == n*500000
            assert event['armed'] and event['latency'] == 0 and event['duration'] == 10
            assert event['mode_after'] == 3
            assert event['differential_application_ram_checked'] and event['registers_checked']
            assert event['entries'] == ['0x1218e','0x12682','0x57002','0x56f80']
            assert event['accesses'] == [['read',0xFFFFF4A2,2,compare],
                ['read',0xFFFFF4A0,2,compare],['read',0xFFFFF6C0,4,n*1000],
                ['read',0xFFFFF480,2,1],['read',0xFFFFF480,2,1],
                ['write',0xFFFFF480,2,0],['read',0xFFFFF4A2,2,compare],
                ['write',0xFFFFF4A2,2,(compare+15625)&65535],
                ['read',0xFFFFF6C0,4,n*1000+100]]
            assert event['before']['0x84d0'] == event['after']['0x84d0'] == n*25
            assert event['before']['0x8006'] == event['after']['0x8006'] == 3
            for boundary in event['boundaries']:
                assert 'after' in boundary and 'expected_ram' not in boundary
                if boundary['entry'] == '0x56b06':
                    assert boundary['whole_application_ram_checked']
                    checks += 1
            assert event['boundaries'][-1]['entry'] == '0x56f80'
            assert event['boundaries'][-1]['return_pc'] == 0x16872
            boundaries.extend(event['boundaries'])
            wraps += compare+15625 > 65535
            change = {k:[event['before'][k],event['after'][k]] for k in event['before']
                      if event['before'][k] != event['after'][k]}
            if change:
                changes.append(dict(number=n,call=call,time=n*500000,changes=change))
        # CAN receipt/application code also calls the shared diagnostic helpers.
        # ISR observations precede that work; they are not the entire interval.
        assert extra['diagnostic_boundaries'][:len(boundaries)] == boundaries
        for boundary in extra['diagnostic_boundaries'][len(boundaries):]:
            assert boundary['entry'] in ['0x1a598','0x56b06']
            assert 'after' in boundary and 'expected_ram' not in boundary
            if boundary['entry'] == '0x56b06':
                assert boundary['whole_application_ram_checked']
                assert boundary['return_pc'] == 0x1E89C
                checks += 1
        assert 'before_diagnostic' not in extra and 'after_diagnostic' not in extra
    result.update(diagnostic_prefixes=number,diagnostic_admission_ram_boundaries=checks,
                  diagnostic_compare_wraps=wraps,diagnostic_changes=changes)
    return rows,result


def timeline_checks():
    end = 320*81920
    wanted = sorted([(n*20000,0) for n in range(1,end//20000+1)] +
                    [(n*40960,1) for n in range(1,end//40960+1)] +
                    [(time,rank) for time,rank,_ in expected_captures()] +
                    [(n*500000,4) for n in range(1,end//500000+1)])
    assert list(Timeline([(4,500000)]).through(end)) == wanted
    t = Timeline([(4,500000)])
    observed = []
    for cut in [499999,500000,500001,999999,1000000,1000001,end]:
        clone = copy.deepcopy(t)
        part = list(t.through(cut))
        assert list(clone.through(cut)) == part
        assert not list(t.through(cut))
        observed.extend(part)
    assert observed == wanted
    return dict(arrivals=len(wanted),split_and_copy_boundaries=7,
                diagnostic_cmt0_ties=end//500000)


def main():
    rows,prefix = verify('tcu-diagnostic-timeline-prefix8.json',8)
    old = (ROOT/'tcu-capture-timeline-prefix8.json').read_bytes()
    assert old == (ROOT/'tcu-diagnostic-hook-reuse-prefix8.json').read_bytes()
    result = dict(status='PASS',scope=__doc__,prefix8=prefix,
        default_hooks_byte_identical=True,default_prefix_sha256=hashlib.sha256(old).hexdigest(),
        timeline_checks=timeline_checks())
    full = ROOT/'tcu-diagnostic-timeline-probe.json'
    if full.exists():
        longer,verified = verify(full.name,320)
        assert longer[:8] == rows
        prior = json.loads((ROOT/'tcu-capture-timeline-probe.json').read_text())['rows']
        assert len(prior) == len(longer)
        result.update(full320=verified,exact_first8=True,
            same_all320_recorded_request_snapshots_as_once_application_diagnostics=
                all(a['after'] == b['after'] for a,b in zip(prior,longer)),
            same_all320_creation_ack_retirement_records=
                all(all(a[k] == b[k] for k in ['creations','acks','retired'])
                    for a,b in zip(prior,longer)))
    (ROOT/'tcu-diagnostic-timeline-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a not in
        ['transitions','hold_events','final','diagnostic_changes']}
        for k,v in result.items() if k in ['prefix8','full320']},indent=2))


if __name__ == '__main__':
    main()
