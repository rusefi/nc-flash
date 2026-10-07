"""Verify recorded original timer-driven acquisition/event queues and limits."""
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def check(name,count):
    data=json.loads((ROOT/name).read_text());rows=data['rows']
    assert data['status']=='scheduler idle reached' and data['pc']==0x3D0C and len(rows)==count
    assert data['rom_sha256']=='7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08'
    events=Counter();targets=Counter();consumed=0;event2_fields=[]
    for cycle,row in enumerate(rows):
        n=cycle+1;assert row['cycle']==cycle
        assert row['queued']==dict(wheel=n&65535,divider=n%5,selected=7,
            queue2=int(n%5==0),queue3=0,pending=0)
        assert row['final']==dict(queue2=0,queue3=0,pending=0,
            task3_available=2,task4_available=2,task7_available=2)
        assert row['mmio']==[['read',0xFFFFF718,2,192],['write',0xFFFFF718,2,64]]
        timer=[v['pc'] for v in row['timer']]
        assert timer.count(0xF28C)==timer.count(0x1062E)==timer.count(0xFA68)==1
        assert timer.count(0xFBE8)==timer.count(0xE5FC)==int(n%5==0)
        assert sum(t['target']==0xE26C for t in row['rte'])==1
        assert all(t['sp']==0xFFFECFF8 and t['status']==0 for t in row['rte'])
        callbacks=row['callbacks'];local=Counter(v['words'][1] for v in callbacks if v['target']==0x2BCE6)
        assert local[1]==int(n%4==3) and local[2]==int(n%5==0)
        events.update(local);targets.update(hex(v['target']) for v in callbacks)
        assert len(row['consumed'])==len(callbacks)
        for item in row['consumed']:
            assert item['return_pc']==0xDCA4 and item['result']==0 and 1<=item['count']<=100
            consumed+=1
        if n%5==0:event2_fields.append(dict(tick=n,fields=row['fields']))
    old=json.loads((ROOT/'control-acquired-qualification-probe.json').read_text())['events']
    changed=[dict(event2_index=i,tick=v['tick'],fields={k:[old[i]['fields'].get(k),x]
        for k,x in v['fields'].items() if old[i]['fields'].get(k)!=x})
        for i,v in enumerate(event2_fields[:120]) if v['fields']!=old[i]['fields']]
    return rows,dict(timer_invocations=count,acquisition_requests=count,
        callback_events={str(k):v for k,v in events.items()},callback_targets=targets,
        actual_queue3_consumer_ram_checks=consumed,decode_checks=len(data['decode']),
        activity_checks=len(data['activity']),qualification_observations=len(data['qualification']),
        sci4_transmitted_bytes=len(data['sci4_transmitted']),sci4_received_bytes=4096-data['sci4_remaining'],
        same_monitored_fields_as_prior_one_to_one=not changed,monitored_differences=changed,
        final_fields=rows[-1]['fields'])


def main():
    rows,prefix=check('control-timer-event2-prefix10.json',10)
    result=dict(status='PASS',scope=__doc__,prefix10=prefix)
    if (ROOT/'control-timer-event2-probe.json').exists():
        full,longer=check('control-timer-event2-probe.json',600)
        assert full[:10]==rows
        result.update(full600=longer,exact_first10=True)
    (ROOT/'control-timer-event2-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{a:b for a,b in v.items() if a not in ['monitored_differences','final_fields']}
        for k,v in result.items() if k in ['prefix10','full600']},indent=2))


if __name__=='__main__':main()
