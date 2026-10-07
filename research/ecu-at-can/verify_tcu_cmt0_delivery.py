"""Check native CMT0 joined traces with the independent mixed-wheel model.

Clock boundary fields are independently replayed; the runtime prefix assertion
compares whole application RAM differentially. Neither proves real cadence.
"""
import copy
from collections import Counter
import json
from pathlib import Path
from probe_tcu_cmt0_delivery import state
from verify_tcu_cmt0_wheel import model
from verify_can201_byte6 import TCU,w
from sh_rotate import SHRotate

ROOT=Path(__file__).resolve().parent


def difference_summary(rows,prior):
    changed={}
    def visit(a,b,path,call):
        if isinstance(a,dict) and isinstance(b,dict):
            for key in sorted(a.keys()|b.keys()):
                visit(a.get(key),b.get(key),path+'/'+key,call)
        elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
            for x,y in zip(a,b):visit(x,y,path+'/*',call)
        elif a!=b:
            changed.setdefault(path,[]).append((call,a,b))
    for a,b in zip(rows,prior):visit(a,b,'',a['call'])
    return {path:dict(count=len(values),first=values[:4],last=values[-4:])
            for path,values in sorted(changed.items())}


def account_hold_differences(rows,prior):
    """Account only for the observed new hold bit and its known propagation.

    This is exact trace comparison, not a raw-history oracle for call280.
    """
    adjusted=copy.deepcopy(rows);counts=Counter()
    for row,old in zip(adjusted,prior):
        actual=row['extra']['reference_checks'];previous=old['extra']['reference_checks']
        assert len(actual)==len(previous)
        for a,b in zip(actual,previous):
            assert (a['entry'],a['return_pc'])==(b['entry'],b['return_pc'])
            for name in ['before','after','branch_inputs']:
                if name not in a or a[name]['0x91a6']==b[name]['0x91a6']:continue
                assert row['call']>=280 and not b[name]['0x91a6']&1
                assert a[name]['0x91a6']==b[name]['0x91a6']|1
                a[name]['0x91a6']=b[name]['0x91a6'];counts[name]+=1
            if isinstance(a.get('expected'),dict):
                if a['expected'].get('flags')!=b['expected'].get('flags'):
                    assert row['call']>=280 and not b['expected']['flags']&1
                    assert a['expected']['flags']==b['expected']['flags']|1
                    a['expected']['flags']=b['expected']['flags'];counts['expected_flags']+=1
                if a['expected'].get('branch')!=b['expected'].get('branch'):
                    assert row['call']==280 and a['entry']=='0x209b4'
                    assert a['expected']['branch']=='hold' and b['expected']['branch']=='history'
                    a['expected']['branch']='history';counts['selected_branch']+=1
            if a.get('returned')!=b.get('returned'):
                assert row['call']>=280 and a['entry']=='0x20fac'
                assert a['returned']==b['returned']|1 and not b['returned']&1
                a['returned']=b['returned'];counts['discrepancy_return_flags']+=1
    assert adjusted==prior
    return dict(counts)


def check(name,count):
    rows=json.loads((ROOT/name).read_text())['rows']
    assert len(rows)==count and all(row['status']=='returned' for row in rows)
    prior=json.loads((ROOT/'tcu-capture-delivery-probe.json').read_text())['rows'][:count]
    normalized=copy.deepcopy(rows)
    phase_previous=None;transitions=[]
    for row,old in zip(rows,prior):
        call=row['call'];c=row['extra']['cmt0']
        assert c['count']==c['differential_application_ram_checks']==c['registers_and_finite_ordered_mmio_checks']==100
        assert c['total']==100*(call+1)
        before=c['before'];t=SHRotate(TCU)
        for a,size in [(0x800A,1),(0x84D0,4),(0x84D4,1),(0x84D5,1),(0x84D6,1),(0x91AC,2)]:
            w(t,a,before[hex(a)],size)
        for i,value in enumerate(before['countdown_8410_8491']):w(t,0x8410+i,value)
        assert before['0x800a']==(1 if call==0 else 3)
        for _ in range(100):model(t)
        w(t,0x800A,3);w(t,0x84D0,(before['0x84d0']+100)&0xFFFFFFFF,4)
        w(t,0x91AC,min(65535,before['0x91ac']+100),2)
        assert state(t)==c['after'],('independent wheel/clock boundary',call)
        for which,number in [('first',call*100+1),('last',(call+1)*100)]:
            e=c[which]
            assert e['entries']==['0x123c2','0x128b6','0x11864','0x1e506','0x11a64']
            assert e['tick']==number and e['armed'] and e['active']
            assert e['mode']==(1 if number==1 else 3)
        assert c['after']['0x84d0']==100*(call+1)
        assert [c['after'][a] for a in ['0x84d4','0x84d5','0x84d6']]==[0,0,(call+1)%10]
        assert c['after_tasks']['0x91ac']==(0 if call<280 else 100*(call-279))
        # The external capture event schedule and strict MMIO remain identical.
        assert row['extra']['capture_interrupts']==old['extra']['capture_interrupts']
        assert len(row['extra']['cut_checks'])==(2 if call%2==0 else 0)
        assert all(b['whole_application_ram_checked'] for b in row['extra']['cut_checks'])
        diag=row['extra']['after_diagnostic'];out=row['after']
        key=(diag['0xa722'],diag['0xa98e'],diag['0x92c9'],diag['0x9454'],
             out['0x96c5'],out['first_list_count_a202'],out['0xa2ba'])
        if key!=phase_previous:
            transitions.append(dict(call=call,active_a722=key[0],summary_a98e=key[1],
                inhibit_92c9=key[2],cut_9454=key[3],phase_count=key[4],list_count=key[5],managed_count=key[6]))
            phase_previous=key
        # Account only for new clock observations and the independently checked
        # timer8464 value at its existing diagnostic snapshot locations.
        adjusted=normalized[call];del adjusted['extra']['cmt0']
        states=[adjusted['extra'][key] for key in ['before_diagnostic','after_diagnostic']]
        states += [b[key] for b in adjusted['extra']['diagnostic_boundaries'] for key in ['before','after']]
        for snapshot in states:
            assert snapshot['0x8464']==10*(call+1)
            snapshot['0x8464']=0
    if count==320:
        (ROOT/'tcu-cmt0-delivery-differences.json').write_text(
            json.dumps(difference_summary(normalized,prior),indent=2)+'\n')
    differences=account_hold_differences(normalized,prior)
    return rows,dict(task_pairs=count,original_cmt0_prefixes=100*count,
            independent_clock_and_mixed_wheel_boundaries=count,
            capture_prefixes=sum(len(row['extra']['capture_interrupts']) for row in rows),
            cut_whole_ram_checks=sum(len(row['extra']['cut_checks']) for row in rows),
            creations=sum(len(row['creations']) for row in rows),
            acknowledgements=sum(len(row['acks']) for row in rows),
            exact_prior_rows_after_only_clock_observations_and_timer8464_accounted=normalized==prior,
            exact_other_recorded_behavior_after_hold_bit_changes_accounted=True,
            observed_hold_difference_counts=differences,
            transitions=transitions,final=rows[-1]['after'],
            final_diagnostic=rows[-1]['extra']['after_diagnostic'])


def main():
    prefix,summary=check('tcu-cmt0-delivery-prefix8.json',8)
    result=dict(status='PASS',scope=__doc__,prefix8=summary)
    if (ROOT/'tcu-cmt0-delivery-probe.json').exists():
        rows,full=check('tcu-cmt0-delivery-probe.json',320)
        assert rows[:8]==prefix
        result.update(full320=full,exact_initial8=True)
    (ROOT/'tcu-cmt0-delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
