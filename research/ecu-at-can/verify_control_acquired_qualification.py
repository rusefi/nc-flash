"""Verify executed changing-ADC -> periodic publication -> qualification data.

Explicit120paired low-level queue requests/event deliveries. Physical cadence,
real interrupt admission and generic downstream DTC lifecycle are unproved.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    d=json.loads((ROOT/'control-acquired-qualification-probe.json').read_text())
    assert d['status']=='scheduler idle reached' and d['sci0_status_fixture']==0xC0 and d['sci0_input_samples']==1024
    assert len(d['cycles'])==len(d['events'])==len(d['rte'])==120
    old=json.loads((ROOT/'control-acquired-qualification-sci-limit.json').read_text())
    assert d['events'][:48]==old['events'] and d['cycles'][:49]==old['cycles']
    assert 0<d['sci0_remaining']<1024
    expected_calls=[5,25,45,65,85,105]
    assert [int(v['stage'].split('-')[1]) for v in d['decode']]==expected_calls
    reports=[v for v in d['qualification'] if v['entry']==0x6CFD8]
    assert len(reports)==6
    for c in d['cycles']:
        i=c['cycle'];f=c['fields']
        assert f['0x4040']==(0 if i<64 else 32000)
        assert f['0x400a']==(0 if i==0 else 32768)
        assert f['0x40e8']==f['0x6cb4']==(0 if i==0 else 0x41200000)
    for n,(dec,rep) in enumerate(zip(d['decode'],reports)):
        cycle=expected_calls[n];fresh=0 if n<3 else 500
        assert dec['return']==0x1B136 and dec['raw'][0]==fresh<<6
        assert dec['after']['0x6c92']==fresh
        before=rep['before']
        assert rep['stage']==f'event2-{cycle}' and before['0x6c92']==fresh and before['0x914b']==1
        assert before['0x8ef4']==(49-n if n<3 else 50)
        assert before['0x8ef6']==(2-n if n<3 else 3)
        assert before['0x8ef8']==int(n==2)
        assert before['0x8eff']==int(n>=3)
        assert rep['reports']==([] if n<3 else [[31,2],[32,2]])
        assert rep['selected']==rep['reports']
        group=[v for v in d['qualification'] if v['stage']==rep['stage']]
        assert [v['entry'] for v in group]==[0x6CD96,0x6CE24,0x6CF06,0x6CFD8]
        for a,b in zip(group,group[1:]):assert a['after']==b['before']
    assert len(d['activity'])==121
    result=dict(status='PASS',scope=__doc__,paired_cycles=120,periodic_full_ram_decodes=6,
        activity_full_ram_boundaries=121,qualification_groups=6,
        low_fallback_at=45,recovery_copied_at=64,recovery_consumed_at=65,
        selected_reports=[v['reports'] for v in reports],
        report_cache_oracles=[v['cache_oracle'] for v in reports],
        downstream_report_ram_not_independently_verified=True)
    (ROOT/'control-acquired-qualification-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
