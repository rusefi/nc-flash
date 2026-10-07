"""Check recorded original queue/dispatch/acquisition-to-idle cycles.

Specific explicit result samples and low-level task7/priority3 requests, not
physical cadence or real interrupt/producer admission. Full decoder absent.
"""
import json
from pathlib import Path
from verify_control_acquisition import REGISTERS

ROOT=Path(__file__).resolve().parent


def main():
    d=json.loads((ROOT/'control-queued-acquisition-probe.json').read_text())
    assert d['queued'] and d['status']=='scheduler idle reached' and d['pc']==0x3D0C
    assert len(d['cycles'])==len(d['rte'])==20 and d['sr']==0
    for c,t in zip(d['cycles'],d['rte']):
        i=c['cycle'];f=c['fields']
        assert t==dict(pc=0x3F3C,sp=0xFFFF11A0,target=0xE26C,status=0,restored_sr=0)
        order=[] if i==0 else list(reversed(REGISTERS[:12]))+list(reversed(REGISTERS[12:24 if i==16 else 20]))
        if i==16:order+=list(reversed(REGISTERS[24:]))
        assert c['adc_reads']==order
        assert f['0x400a']==f['0x40ec']==(0 if i==0 else 32768)
        assert f['0x40e8']==f['0x6cb4']==(0 if i==0 else 0x41200000)
        assert f['0x4040']==(0 if i<16 else 32000)
        assert f['0x6c92']==f['0x914b']==0 and f['0x4048']==i+1
        assert c['descriptor']==[0,3,0,i+1,255,255,17,168]
        entries=[e['entry'] for e in d['entries'] if e['stage']==f'queued-task7-{i}']
        assert entries==[0xE26C,0x4CE2,0x6718,0x1DF32]
    assert d['context']=={'0x12b4':65535,'0x12b6':65535,'0x12b8':0x80000000,
        '0x12bc':0xFFFF11A8,'0x12c0':0xB0,'0x12c4':0xFFFF11A8,'0x12c8':0x40D0}
    result=dict(status='PASS',scope=__doc__,queued_cycles=20,rte_entries=20,observed_idle_boundaries=20,
                copied_channel1_at_cycle=1,copied_channel28_at_cycle=16,full_decode_observed=False)
    (ROOT/'control-queued-acquisition-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
