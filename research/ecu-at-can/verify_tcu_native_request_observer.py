"""Compare all retained original observer fields; reject unexpected additions."""
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXTRA={'first_list_count_a202','heap_first_header_9f3c','primary_timer_phase_8494',
       'ramp_timers_8115','request_word_915a'}


def compare(old,new,path='root',additions=None):
    if additions is None:
        additions=[]
    if isinstance(old,dict):
        assert isinstance(new,dict) and old.keys()<=new.keys(),path
        extra=new.keys()-old.keys()
        assert not extra or (extra==EXTRA and '0x8007' in old),(path,extra)
        if extra:
            additions.append(path)
        for key in old:
            compare(old[key],new[key],path+'/'+key,additions)
    elif isinstance(old,list):
        assert isinstance(new,list) and len(old)==len(new),path
        for i,(a,b) in enumerate(zip(old,new)):
            compare(a,b,path+'/'+str(i),additions)
    else:
        assert old==new,(path,old,new)
    return additions


def main():
    names=['tcu-initialized-requests-probe.json','tcu-native-request-observer-regression.json']
    data=[json.loads((ROOT/n).read_text()) for n in names]
    additions=compare(*data)
    assert len(data[1]['rows'])==32 and all(r['status']=='returned' for r in data[1]['rows'])
    checks=sum(len(r['ack_checks']) for r in data[1]['rows'])
    assert checks==25
    result=dict(status='PASS',all_original_fields_equal=True,byte_identical=False,
        reason='Retained baseline predates five snapshot observation fields; these are the only allowed additions.',
        added_snapshot_fields=sorted(EXTRA),addition_paths=additions,application_calls=32,
        whole_ram_ack_checks=checks,creations=sum(len(r['creations']) for r in data[1]['rows']),
        sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names})
    (ROOT/'tcu-native-request-observer-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS32 original task calls/25 ack RAM boundaries/all original fields; five prior snapshot additions')


if __name__=='__main__':
    main()
