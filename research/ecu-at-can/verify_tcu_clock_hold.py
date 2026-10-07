"""Verify actual20CBC inputs/returns in the short native-clock loss experiment."""
import copy
import json
from pathlib import Path
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_reference_hold import model,state

ROOT=Path(__file__).resolve().parent


def main():
    rows=json.loads((ROOT/'tcu-clock-hold-probe.json').read_text())['rows']
    prior=json.loads((ROOT/'tcu-cmt0-delivery-probe.json').read_text())['rows']
    assert len(rows)==32 and all(row['status']=='returned' for row in rows)
    initial=copy.deepcopy(rows[:20])
    for row in initial:del row['extra']['hold_checks']
    assert initial==prior[:20]
    events=[];checks=0
    for row in rows:
        call=row['call'];hold=row['extra']['hold_checks']
        assert len(hold)==int(call%4==0)
        assert len(row['extra']['capture_interrupts'])==(2 if call<20 else 0)
        assert row['extra']['cmt0']['count']==100
        for boundary in hold:
            assert boundary['return_pc']==0x209D0 and boundary['whole_application_ram_checked']
            before=boundary['before'];t=SHRotate(TCU)
            for a,n in [(0x91A6,1),(0x9194,1),(0x8158,1),(0x91AC,2),(0x91B4,1),
                        (0x809A,2),(0x8080,1),(0x8081,1),(0x92C6,1),(0xAC87,1)]:
                w(t,a,before[hex(a)],n)
            for i,value in enumerate(before['history']):w(t,0x91CC+4*i,value,4)
            expected=model(t)
            assert expected==boundary['expected'] and state(t)==boundary['after']
            assert expected['held']==(call>=20) and not expected['history_reset']
            ref=next(b for b in row['extra']['reference_checks'] if b['entry']=='0x209b4')
            if call>=20:
                assert before['history']==[1216]*18 and before['0x91b4']==1
                assert before['0x91ac']==100*(call-19)
                assert before['0x8158']==2*(call-16)
                assert expected['total']==21888 and expected['period']==1216
                assert expected['ratio']==(100*(call-19)<<16)//304
                assert ref['expected']==dict(branch='hold',result=1145,reference=1145,period=134144,flags=1)
            events.append(dict(call=call,elapsed=before['0x91ac'],timer_before=before['0x8158'],
                **expected,selected_reference=ref['expected']))
            checks+=1
    result=dict(status='PASS',scope=__doc__,task_pairs=32,cmt0_prefixes=3200,
                capture_prefixes=40,actual_hold_whole_application_ram_checks=checks,
                exact_prior_first20=True,events=events,
                limits='Early captureloss fixture, not a raw-entry replay of the original320-pair call280.')
    (ROOT/'tcu-clock-hold-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
