"""Verify recorded exact-ratio clock delivery without assuming old lifecycle dates."""
import copy
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_reference_hold import model as hold_model,state as hold_state
from verify_tcu_cmt0_wheel import model as clock_model
from probe_tcu_cmt0_delivery import state as clock_state
from verify_tcu_cmt0_delivery import difference_summary

ROOT=Path(__file__).resolve().parent


def check(name,count,application=False):
    data=json.loads((ROOT/name).read_text())
    assert data['rom_sha256']=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rows=data['rows']
    assert len(rows)==count and all(row['status']=='returned' for row in rows)
    number=hold_checks=capture_checks=ties=0
    hold_events=[];transitions=[];previous=None
    for call,row in enumerate(rows):
        assert row['call']==call
        extra=row['extra'];period=81920 if application else 2000000
        start=call*period;end=(call+1)*period
        clock_count=end//20000-start//20000
        # Independent closed-form enumeration, not the runtime merge loop.
        wanted=[[n*20000,0,n] for n in range(start//20000+1,end//20000+1)]
        wanted += [[n*40960,1,n] for n in range(start//40960+1,end//40960+1)]
        if application:wanted.append([end,2,call+1])
        assert extra['clock_order']==sorted(wanted)
        ties += sum(1 for time,channel,n in wanted if channel==1 and time%20000==0)
        schedule=extra['clock_schedule']
        expected_schedule=dict(peripheral_time=end,cmt0_total=end//20000,
            cmt1_total=end//40960,initial_offset=0)
        if application:expected_schedule.update(application_total=call+1,zero_compare_latency=True)
        else:expected_schedule.update(superseded_primary_requests=(call+1)*8,cmt0_before_cmt1_on_ties=True)
        assert schedule==expected_schedule
        events=extra['cmt1_interrupts']
        assert len(events)==end//40960-start//40960
        for event in events:
            number+=1;n=number;stamp=n*1000
            assert event['number']==n and event['peripheral_match_time']==n*40960
            assert event['active'] and event['armed'] and event['mode']==(1 if n==1 else 3)
            assert event['entries']==['0x12386','0x12886','0x11014']
            assert event['phases']==[n%16,(n//16)%16,(n//256)%2]
            assert event['profile_duration']==10
            assert event['independent_application_ram_checked'] and event['registers_and_mmio_checked']
            assert event['accesses']==[['read',0xFFFFF6C0,4,stamp],
                ['read',0xFFFFF718,2,193],['read',0xFFFFF718,2,193],
                ['write',0xFFFFF718,2,65],['read',0xFFFFF6C0,4,stamp+100]]
        c=extra['cmt0'];before=c['before'];t=SHRotate(TCU)
        assert c['count']==c['differential_application_ram_checks']==c['registers_and_finite_ordered_mmio_checks']==clock_count
        assert c['total']==end//20000
        for a,size in [(0x800A,1),(0x84D0,4),(0x84D4,1),(0x84D5,1),(0x84D6,1),(0x91AC,2)]:
            w(t,a,before[hex(a)],size)
        for i,value in enumerate(before['countdown_8410_8491']):w(t,0x8410+i,value)
        for _ in range(clock_count):clock_model(t)
        w(t,0x800A,3);w(t,0x84D0,(before['0x84d0']+clock_count)&0xFFFFFFFF,4)
        w(t,0x91AC,min(65535,before['0x91ac']+clock_count),2)
        assert clock_state(t)==c['after']
        captures=extra['capture_interrupts']
        assert len(captures)==(2 if call<280 else 0)
        assert all(e['differential_application_ram_checked'] and e['registers_checked'] for e in captures)
        capture_checks+=len(captures)
        assert len(extra['hold_checks'])==int(call%4==0)
        for gate in extra['hold_checks']:
            assert gate['whole_application_ram_checked'] and gate['return_pc']==0x209D0
            before=gate['before'];t=SHRotate(TCU)
            for a,n in [(0x91A6,1),(0x9194,1),(0x8158,1),(0x91AC,2),(0x91B4,1),
                        (0x809A,2),(0x8080,1),(0x8081,1),(0x92C6,1),(0xAC87,1)]:
                w(t,a,before[hex(a)],n)
            for i,value in enumerate(before['history']):w(t,0x91CC+4*i,value,4)
            expected=hold_model(t)
            assert expected==gate['expected'] and hold_state(t)==gate['after']
            if expected['held'] or expected['history_reset']:
                hold_events.append(dict(call=call,head=before['0x91b4'],elapsed=before['0x91ac'],**expected))
            hold_checks+=1
        diag=extra['after_diagnostic']
        current={k:diag[k] for k in ['0xa939','0xa722','0xa98e','0x9415','0x80e8','0x9454']}
        current.update(phases=row['after']['phases'],managed=row['after']['managed'])
        if current!=previous:transitions.append(dict(call=call,**current));previous=current
    old=json.loads((ROOT/'tcu-cmt1-delivery-probe.json').read_text())['rows'][:count]
    a,b=copy.deepcopy(rows),copy.deepcopy(old)
    for row in a:
        for key in ['clock_order','clock_schedule','cmt1_interrupts']:row['extra'].pop(key)
        if application:row['extra'].pop('application_interrupt')
    for row in b:row['extra'].pop('cmt1_interrupts')
    return rows,dict(task_pairs=count,cmt0_prefixes=end//20000,cmt1_prefixes=number,
        capture_prefixes=capture_checks,actual_hold_whole_ram_checks=hold_checks,
        simultaneous_match_times=ties,independent_clock_boundary_replays=count,
        same_recorded_behavior_as_prior_100_to_8_after_clock_observations_removed=a==b,
        changes=difference_summary(a,b),hold_events=hold_events,transitions=transitions,
        final=rows[-1]['after'])


def main():
    rows,prefix=check('tcu-clock-ratio-prefix8.json',8)
    result=dict(status='PASS',scope=__doc__,prefix8=prefix)
    full=ROOT/'tcu-clock-ratio-probe.json'
    if full.exists():
        longer,verified=check(full.name,320)
        assert longer[:8]==rows
        result.update(full320=verified,exact_first8=True)
    (ROOT/'tcu-clock-ratio-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{x:v[x] for x in ['task_pairs','cmt0_prefixes','cmt1_prefixes',
        'capture_prefixes','actual_hold_whole_ram_checks','simultaneous_match_times',
        'same_recorded_behavior_as_prior_100_to_8_after_clock_observations_removed']}
        for k,v in result.items() if k in ['prefix8','full320']},indent=2))


if __name__=='__main__':main()
