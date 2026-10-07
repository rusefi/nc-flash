"""Verify exact recovery trace through original capture ISR delivery."""
import copy
import json
from pathlib import Path

from verify_tcu_capture_interrupts import CHANNELS

ROOT=Path(__file__).resolve().parent


def check(path,count):
    rows=json.loads((ROOT/path).read_text())['rows']
    prior=json.loads((ROOT/'tcu-recovery-cut-probe.json').read_text())['rows'][:count]
    assert len(rows)==count and all(r['status']=='returned' for r in rows)
    normalized=copy.deepcopy(rows);events=0
    timestamps={'A':0,'B':0}
    for row in normalized:
        call=row['call'];observed=row['extra'].pop('capture_interrupts')
        assert len(observed)==(2 if call<280 else 0)
        for channel,event in zip(['A','B'],observed):
            cfg=CHANNELS[channel]
            delta=(12160 if channel=='A' else 5890 if call<48 else 6490 if call<80 else 4430 if call<128 else 9120)
            previous=timestamps[channel];timestamps[channel]=(previous+delta)&0xFFFFFFFF
            assert event['channel']==channel and event['previous']==previous
            assert event['captured']==timestamps[channel]
            assert event['status']==event['second_status']==cfg['mask']
            assert event['callback'] and event['differential_application_ram_checked'] and event['registers_checked']
            assert event['stopped_before_rte']==hex(cfg['stop']) and event['profile_duration']==10
            events+=1;start=1000*events
            assert event['accesses']==[
                ['read',0xFFFFF6C0,4,start],['read',0xFFFFF42C,2,cfg['mask']],
                ['read',0xFFFFF42C,2,cfg['mask']],['write',0xFFFFF42C,2,0],
                ['read',cfg['capture'],4,timestamps[channel]],['read',0xFFFFF6C0,4,start+100]]
        callbacks=[b for b in row['extra']['source_boundaries'] if b['entry'] in ['0x179a8','0x17a58']]
        assert len(callbacks)==len(observed)
        for b in callbacks:
            assert b['return_pc']=={'0x179a8':0x16CB2,'0x17a58':0x16B7A}[b['entry']]
            b['return_pc']=0xFFFFFFF0
    assert normalized==prior
    return rows,dict(task_pairs=count,capture_prefix_differential_ram_checks=events,
                     exact_prior_rows_after_only_capture_observations_and_return_pc_normalized=True,
                     final=rows[-1]['after'])


def main():
    prefix,small=check('tcu-capture-delivery-prefix8.json',8)
    result=dict(status='PASS',scope=__doc__,prefix8=small)
    if (ROOT/'tcu-capture-delivery-probe.json').exists():
        rows,full=check('tcu-capture-delivery-probe.json',320)
        assert rows[:8]==prefix
        assert full['capture_prefix_differential_ram_checks']==560
        result.update(full320=full,exact_initial8=True)
    (ROOT/'tcu-capture-delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
