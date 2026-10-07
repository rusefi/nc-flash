"""Independently enumerate arrivals and replay per-interrupt wheel/hold models.

Runtime application/capture prefix checks are differential; wheel and hold
replays below use separate arithmetic RAM models. No physical timing claim.
"""
import copy
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_cmt0_wheel import model as clock_model
from probe_tcu_cmt0_delivery import state as clock_state
from verify_tcu_reference_hold import model as hold_model,state as hold_state

ROOT = Path(__file__).resolve().parent


def check_timeline_boundaries():
    from probe_tcu_capture_timeline import Timeline
    end = 320*81920
    expected = sorted([(n*20000,0) for n in range(1,end//20000+1)] +
                      [(n*40960,1) for n in range(1,end//40960+1)] +
                      [(t,r) for t,r,_ in expected_captures()])
    assert list(Timeline().through(end)) == expected
    # Splitting exactly before/on/after rate changes, loss, and a timer tie
    # must neither duplicate nor omit an arrival; copied cursors are independent.
    cuts = sorted({0,end,5120000} | {n*81920+d for n in [48,80,128,280] for d in [-1,0,1]})
    timeline = Timeline()
    observed = []
    for cut in cuts:
        clone = copy.deepcopy(timeline)
        part = list(timeline.through(cut))
        assert list(clone.through(cut)) == part
        assert list(timeline.through(cut)) == []
        observed.extend(part)
    assert observed == expected
    return dict(arrivals=len(expected),split_and_deepcopy_boundaries=len(cuts))


def expected_captures():
    # Closed-form enumeration independent of the runtime heap/cursor merge.
    a = [(n*24320,2) for n in range(1,(280*81920-1)//24320+1)]
    b = []
    for lo,hi,p in [(0,48,11780),(48,80,12980),(80,128,8860),(128,280,18240)]:
        b += [(lo*81920+n*p,3) for n in range(1,((hi-lo)*81920-1)//p+1)]
    return [[time,rank,n] for n,(time,rank) in enumerate(sorted(a+b),1)]


def check_clock(edge):
    t = SHRotate(TCU)
    before = edge['before']
    for a,n in [(0x800A,1),(0x84D0,4),(0x84D4,1),(0x84D5,1),(0x84D6,1),(0x91AC,2)]:
        w(t,a,before[hex(a)],n)
    for i,v in enumerate(before['countdown_8410_8491']):
        w(t,0x8410+i,v)
    clock_model(t)
    w(t,0x800A,3)
    w(t,0x84D0,(before['0x84d0']+1)&0xFFFFFFFF,4)
    w(t,0x91AC,min(65535,before['0x91ac']+1),2)
    assert clock_state(t) == edge['after']
    event = edge['interrupt']
    assert event['active'] and event['tick'] == edge['number']
    assert event['mode'] == (1 if edge['number'] == 1 else 3)


def check_hold(gate):
    assert gate['whole_application_ram_checked'] and gate['return_pc'] == 0x209D0
    t = SHRotate(TCU)
    before = gate['before']
    for a,n in [(0x91A6,1),(0x9194,1),(0x8158,1),(0x91AC,2),(0x91B4,1),
                (0x809A,2),(0x8080,1),(0x8081,1),(0x92C6,1),(0xAC87,1)]:
        w(t,a,before[hex(a)],n)
    for i,v in enumerate(before['history']):
        w(t,0x91CC+4*i,v,4)
    expected = hold_model(t)
    assert expected == gate['expected'] and hold_state(t) == gate['after']
    return expected


def verify(name,count,diagnostic=False):
    data = json.loads((ROOT/name).read_text())
    assert data['rom_sha256'] == '8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rows = data['rows']
    assert len(rows) == count and all(row['status'] == 'returned' for row in rows)
    captures = expected_captures()
    previous_capture = {'A':0,'B':0}
    capture_counts = {'A':0,'B':0}
    hold_events,transitions = [],[]
    previous = None
    hold_count = 0
    for call,row in enumerate(rows):
        assert row['call'] == call
        start,end = call*81920,(call+1)*81920
        extra = row['extra']
        c0 = [[n*20000,0,n] for n in range(start//20000+1,end//20000+1)]
        c1 = [[n*40960,1,n] for n in range(start//40960+1,end//40960+1)]
        cap = [e for e in captures if start < e[0] <= end]
        diag = ([[n*500000,4,n] for n in range(start//500000+1,end//500000+1)]
                if diagnostic else [])
        assert extra['arrival_order'] == sorted(c0+c1+cap+diag+[[end,5 if diagnostic else 4,call+1]])
        assert extra['clock_order'] == sorted(c0+c1+[[end,2,call+1]])
        assert extra['capture_schedule'] == dict(counter_epoch=0,counter_divisor=2,
            loss_time=280*81920,b_phase_restart=True,zero_service_latency=True)
        assert len(extra['cmt0_edges']) == len(c0)
        for edge,(time,_,n) in zip(extra['cmt0_edges'],c0):
            assert (edge['time'],edge['number']) == (time,n)
            check_clock(edge)
        assert len(extra['cmt1_interrupts']) == len(c1)
        for event,(time,_,n) in zip(extra['cmt1_interrupts'],c1):
            assert event['number'] == n and event['peripheral_match_time'] == time
            assert event['phases'] == [n%16,n//16%16,n//256%2]
            assert event['active'] and event['armed']
            assert event['independent_application_ram_checked'] and event['registers_and_mmio_checked']
        assert len(extra['capture_interrupts']) == len(cap)
        for event,(time,rank,n) in zip(extra['capture_interrupts'],cap):
            channel = 'A' if rank == 2 else 'B'
            mask,address,callback,stop = ((1,0xFFFFF434,'0x179a8','0x16cca') if rank == 2
                                         else (2,0xFFFFF438,'0x17a58','0x16b92'))
            captured = (time//2)&0xFFFFFFFF
            assert event['channel'] == channel and event['number'] == n
            assert event['peripheral_edge_time'] == time and event['captured'] == captured
            assert event['previous'] == previous_capture[channel]
            previous_capture[channel] = captured
            capture_counts[channel] += 1
            assert event['callback'] and event['status'] == event['second_status'] == mask
            assert event['profile_duration'] == 10 and event['stopped_before_rte'] == stop
            assert event['differential_application_ram_checked'] and event['registers_checked']
            assert event['accesses'] == [['read',0xFFFFF6C0,4,n*1000],
                ['read',0xFFFFF42C,2,mask],['read',0xFFFFF42C,2,mask],
                ['write',0xFFFFF42C,2,0],['read',address,4,captured],
                ['read',0xFFFFF6C0,4,n*1000+100]]
            assert event['source_boundaries'][0]['entry'] == callback
            assert all('after' in e for e in event['source_boundaries'])
        app = extra['application_interrupt']
        assert app['armed'] and app['latency'] == 0 and app['mode_after'] == 3
        assert app['phase'] == call%8 and app['index'] == [0,1,2,3,0,1,2,4][call%8]
        assert app['differential_application_ram_checked'] and app['registers_and_mmio_checked']
        assert app['independent_command_pin_boundaries'] == 2
        n = call+1
        compare = (n*2560)&65535
        assert app['duration'] == 10 and app['stage_after'] == 2 and app['phase_after'] == n&255
        assert app['entries'] == ['0x1220a','0x126ec','0x1e5f6']
        assert app['accesses'] == [['read',0xFFFFF454,2,compare],['read',0xFFFFF442,2,compare],
            ['read',0xFFFFF6C0,4,n*1000],['read',0xFFFFF460,2,1],
            ['read',0xFFFFF460,2,1],['write',0xFFFFF460,2,0],
            ['read',0xFFFFF454,2,compare],['write',0xFFFFF454,2,(compare+2560)&65535],
            ['read',0xFFFFF6C0,4,n*1000+100]]
        assert len(extra['hold_checks']) == int(call%4 == 0)
        for gate in extra['hold_checks']:
            expected = check_hold(gate)
            hold_count += 1
            if expected['held'] or expected['history_reset']:
                hold_events.append(dict(call=call,elapsed=gate['before']['0x91ac'],**expected))
        diag = extra['post_application_diagnostic_state' if diagnostic else 'after_diagnostic']
        current = {k:diag[k] for k in ['0xa939','0xa722','0xa98e','0x9415','0x80e8','0x9454']}
        current.update(phases=row['after']['phases'],managed=row['after']['managed'])
        if current != previous:
            transitions.append(dict(call=call,**current))
            previous = current
    return rows,dict(task_pairs=count,application_prefixes=count,cmt0_prefixes=end//20000,
        independent_per_interrupt_wheel_replays=end//20000,cmt1_prefixes=end//40960,
        capture_prefixes=capture_counts,actual_hold_whole_ram_checks=hold_count,
        independent_command_pin_boundaries=2*count,
        creations=sum(len(r['creations']) for r in rows),acks=sum(len(r['acks']) for r in rows),
        hold_events=hold_events,transitions=transitions,final=rows[-1]['after'])


def remove_recorded_next_interval_duplicates(rows):
    """Validate then remove the old observer's proven cross-row list alias.

No firmware values, interrupt records or current-application observations
are changed. Raw320 remains preserved, including this logging defect.
"""
    clean = copy.deepcopy(rows)
    removed = 0
    for n,row in enumerate(clean[:-1]):
        following = rows[n+1]['extra']['capture_interrupts']
        tail = [b for event in following for b in event['source_boundaries']]
        source = row['extra']['source_boundaries']
        if tail and source[-len(tail):] == tail:
            del source[-len(tail):]
            removed += len(tail)
        assert all(e['entry'] not in ['0x179a8','0x17a58'] for e in source)
    return clean,removed


def main():
    rows,prefix = verify('tcu-capture-timeline-prefix8.json',8)
    result = dict(status='PASS',scope=__doc__,prefix8=prefix,
                  timeline_boundary_checks=check_timeline_boundaries())
    full = ROOT/'tcu-capture-timeline-probe.json'
    if full.exists():
        longer,verified = verify(full.name,320)
        clean,removed = remove_recorded_next_interval_duplicates(longer)
        assert clean[:8] == rows
        result.update(full320=verified,exact_first8_after_verified_observer_normalization=True,
            duplicate_next_interval_observations_removed_for_comparison=removed)
    corrected = ROOT/'tcu-capture-timeline-observer-fix9.json'
    if corrected.exists():
        nine,_ = verify(corrected.name,9)
        assert nine[:8] == rows
        assert remove_recorded_next_interval_duplicates(nine)[1] == 0
        if full.exists():
            assert clean[:9] == nine
        result['corrected_observer_exact_prefix9'] = True
    (ROOT/'tcu-capture-timeline-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a not in ['transitions','hold_events','final']}
                      for k,v in result.items() if k in ['prefix8','full320']},indent=2))


if __name__ == '__main__':
    main()
