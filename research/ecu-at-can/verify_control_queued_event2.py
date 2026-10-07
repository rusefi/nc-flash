"""Verify retained native event2 queue dispatch, preserving observed differences."""
import copy
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    data=json.loads((ROOT/'control-queued-event2-probe.json').read_text())
    old=json.loads((ROOT/'control-acquired-qualification-probe.json').read_text())
    prefix=json.loads((ROOT/'control-queued-event2-prefix8.json').read_text())
    assert data['rom_sha256']==old['rom_sha256']=='7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08'
    rows=data['event_queue'];assert len(rows)==len(data['cycles'])==120
    assert data['status']=='scheduler idle reached' and data['pc']==0x3D0C
    count=wraps=0;changed=[];targets=Counter()
    for cycle,row in enumerate(rows):
        assert row['cycle']==cycle
        assert row['admission']==dict(pending=1,count=1,task=4,availability=1,priority=1)
        entries=row['entries']
        assert [v['pc'] for v in entries[:7]]==[0x215C6,0x1826E,0x2BC8C,0xDAE8,0xF5A0,0x35E0,0x391A]
        events=[v for v in entries if v['pc']==0x2BCE6]
        assert len(events)==1 and events[0]['pr']==0xDCBE
        assert all(v['target']==0xDC80 and v['sp']==0xFFFECFF8 and v['status']==0 for v in row['rte'])
        consumers=row['consumed'];callbacks=row['callbacks']
        assert len(consumers)==len(callbacks)>0
        assert callbacks[0]['target']==0x2BCE6 and callbacks[0]['words'][:2]==[0x2BCE6,2]
        initial=consumers[0]['head']
        for i,(consumer,callback) in enumerate(zip(consumers,callbacks)):
            assert consumer['stage']==callback['stage']==f'queued-event2-{cycle}'
            assert consumer['return_pc']==0xDCA4 and consumer['result']==0
            assert 1<=consumer['count']<=100 and consumer['head']==(initial+i)%100
            assert callback['target']==callback['words'][0]
            targets[hex(callback['target'])]+=1;count+=1;wraps+=int(consumer['head']==99)
        assert row['head']==row['tail']==(initial+len(consumers))%100
        if row['fields']!=old['events'][cycle]['fields']:
            changed.append(dict(cycle=cycle,fields={k:[old['events'][cycle]['fields'].get(k),v]
                for k,v in row['fields'].items() if old['events'][cycle]['fields'].get(k)!=v}))
    first=copy.deepcopy(rows[:8])
    for row in first:
        row.pop('consumed');row.pop('callbacks')
    assert first==prefix['event_queue']
    result=dict(status='PASS',scope=__doc__,task_pairs=120,actual_event2_callbacks=120,
        independent_consumer_ram_returns=count,queue_wraps=wraps,callback_targets=targets,
        identical_first8_before_added_consumer_observations=True,
        monitored_fields_identical_to_prior_direct_event2=not changed,
        monitored_field_differences=changed,decode_checks=len(data['decode']),
        activity_checks=len(data['activity']),qualification_observations=len(data['qualification']),
        rte_transfers=len(data['rte']),final_fields=data['fields'],
        limits='Supplied task7/event2 ratio, ADC/SCI samples, maskF0 and event stackFFFED000. Additional callbacks execute; only F6A0 and existing decode/activity/qualification oracles are independent. No complete all-RAM differential versus prior direct callback trace or native producer cadence.')
    (ROOT/'control-queued-event2-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['monitored_field_differences','scope','limits','final_fields']},indent=2))


if __name__=='__main__':main()
