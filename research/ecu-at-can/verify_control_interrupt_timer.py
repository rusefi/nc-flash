"""Verify original idle IRQ delivery records against prior direct timer traces."""
import copy
import json
from pathlib import Path
from verify_control_timer_event2 import check as timer_check

ROOT=Path(__file__).resolve().parent


def check(name,count,previous):
    data=json.loads((ROOT/name).read_text());old=json.loads((ROOT/previous).read_text())
    rows,summary=timer_check(name,count)
    assert len(data['interrupts'])==count
    normalized=copy.deepcopy(rows)
    for cycle,(irq,row) in enumerate(zip(data['interrupts'],normalized)):
        assert irq['cycle']==cycle and irq['selected']==7
        assert irq['after_callback_stack']==0xFFFF1144 and irq['after_idle_stack']==0xFFFF11A8
        assert irq['nesting']==0x80000001 and irq['final_nesting']==0x80000000
        assert irq['queue2_checks']==(cycle+1)//5
        for item in row['timer']:
            if item['pc'] in [0xF28C,0x1062E]:
                assert item['argument']==0xFFFF12B0;item['argument']=0
            if item['pc'] in [0xF28C,0x1062E,0xFBE8]:
                assert item['pr']==0x32D8;item['pr']=0xFFFFFFF0
    assert normalized==old['rows']
    assert len(data['queue2_checks'])==len(data['queue2_callbacks'])==count//5
    for i,(item,callback) in enumerate(zip(data['queue2_checks'],data['queue2_callbacks'])):
        assert item==dict(stage=f'queued-event2-timer-{5*i+4}',return_pc=0xDC50,
            result=0,count=1,head=i%30)
        assert callback['stage']==item['stage'] and callback['target']==callback['words'][0]==0xE5FC
    summary.update(actual_queue2_consumer_ram_checks=len(data['queue2_checks']),
        exact_prior_rows_after_explicit_entry_argument_and_return_pc_accounting=True)
    return data,summary


def main():
    prefix,summary=check('control-interrupt-timer-prefix10.json',10,'control-timer-event2-prefix10.json')
    result=dict(status='PASS',scope=__doc__,prefix10=summary)
    full=ROOT/'control-interrupt-timer-probe.json'
    if full.exists():
        data,summary=check(full.name,600,'control-timer-event2-probe.json')
        assert data['rows'][:10]==prefix['rows'] and data['interrupts'][:10]==prefix['interrupts']
        result.update(full600=summary,exact_first10=True)
    (ROOT/'control-interrupt-timer-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a not in ['final_fields','monitored_differences']}
        for k,v in result.items() if k in ['prefix10','full600']},indent=2))


if __name__=='__main__':main()
