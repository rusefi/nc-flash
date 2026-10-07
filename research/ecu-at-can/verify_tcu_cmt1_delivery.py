"""Verify exact recovery behavior through native CMT1 delivery and hold gates."""
import copy
import json
from pathlib import Path
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_tcu_reference_hold import model,state

ROOT=Path(__file__).resolve().parent


def check(name,count):
    data=json.loads((ROOT/name).read_text())
    assert data['rom_sha256']=='8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    rows=data['rows'];prior=json.loads((ROOT/'tcu-cmt0-delivery-probe.json').read_text())['rows'][:count]
    assert len(rows)==count and all(row['status']=='returned' for row in rows)
    normalized=copy.deepcopy(rows);primary=hold_count=0;held=[]
    for row in normalized:
        call=row['call'];events=row['extra'].pop('cmt1_interrupts')
        assert len(events)==8
        for event in events:
            primary+=1;n=event['number'];start=1000*n
            assert n==primary and event['armed'] and event['active']
            assert event['mode']==(1 if n==1 else 3)
            assert event['entries']==['0x12386','0x12886','0x11014']
            assert event['phases']==[n%16,(n//16)%16,(n//256)%2]
            assert event['profile_duration']==10
            assert event['independent_application_ram_checked'] and event['registers_and_mmio_checked']
            assert event['accesses']==[['read',0xFFFFF6C0,4,start],
                ['read',0xFFFFF718,2,128],['read',0xFFFFF718,2,128],
                ['write',0xFFFFF718,2,0],['read',0xFFFFF6C0,4,start+100]]
        gates=row['extra'].pop('hold_checks');assert len(gates)==int(call%4==0)
        for gate in gates:
            assert gate['whole_application_ram_checked'] and gate['return_pc']==0x209D0
            before=gate['before'];t=SHRotate(TCU)
            for a,n in [(0x91A6,1),(0x9194,1),(0x8158,1),(0x91AC,2),(0x91B4,1),
                        (0x809A,2),(0x8080,1),(0x8081,1),(0x92C6,1),(0xAC87,1)]:
                w(t,a,before[hex(a)],n)
            for i,value in enumerate(before['history']):w(t,0x91CC+4*i,value,4)
            expected=model(t)
            assert expected==gate['expected'] and state(t)==gate['after']
            assert expected['held']==(call>=280)
            if call>=280:
                assert before['history']==[1216]*18
                assert before['0x91ac']==100*(call-279)
                assert before['0x8158']==2*(call-276)
                assert expected['total']==21888 and expected['period']==1216
                assert expected['ratio']==(100*(call-279)<<16)//304
                held.append(dict(call=call,head=before['0x91b4'],elapsed=before['0x91ac'],
                                 timer_before=before['0x8158'],**expected))
            hold_count+=1
    assert normalized==prior
    return rows,dict(task_pairs=count,cmt1_independent_whole_ram_prefixes=primary,
                cmt0_differential_whole_ram_prefixes=count*100,
                actual_hold_whole_ram_returns=hold_count,held_entries=held,
                exact_prior_rows_after_only_new_cmt1_and_hold_observations_removed=True,
                final=rows[-1]['after'])


def main():
    prefix,small=check('tcu-cmt1-delivery-prefix8.json',8)
    result=dict(status='PASS',scope=__doc__,prefix8=small)
    if (ROOT/'tcu-cmt1-delivery-probe.json').exists():
        rows,full=check('tcu-cmt1-delivery-probe.json',320)
        assert rows[:8]==prefix
        result.update(full320=full,exact_initial8=True)
    (ROOT/'tcu-cmt1-delivery-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
