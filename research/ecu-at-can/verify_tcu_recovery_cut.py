"""Verify actual cut boundaries and exact unchanged320-pair recovery trace."""
import copy
import hashlib
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU,w
from verify_can201_cut_loop import reference
from verify_software_lookup import expected_curve

ROOT=Path(__file__).resolve().parent


def main():
    rows=json.loads((ROOT/'tcu-recovery-cut-probe.json').read_text())['rows']
    prior=json.loads((ROOT/'tcu-recovery-reference-second-approach.json').read_text())['rows']
    assert len(rows)==320 and all(r['status']=='returned' for r in rows)
    normalized=copy.deepcopy(rows)
    for row in normalized:del row['extra']['cut_checks']
    assert normalized==prior
    counts={'cut':0,'admission':0};transitions=[];last=None
    for row in rows:
        checks=row['extra']['cut_checks']
        cut=[b for b in checks if b['entry']=='0x24fa0']
        assert len(cut)==int(row['call']%2==0)
        assert len(checks)==2*len(cut)
        for b in checks:
            assert b['whole_application_ram_checked']
            g=b['before'];enabled=not(g['0x92c9']&64 or g['0x9317']&1 or g['0x92c6']&2)
            if b['entry']=='0x2513e':
                assert b['returned']==b['expected']==int(enabled)
                assert b['before']==b['after'];counts['admission']+=1
                continue
            assert b['entry']=='0x24fa0';counts['cut']+=1
            t=SHRotate(TCU)
            for a,v in g.items():w(t,int(a,16),v,2 if a in ['0x9334','0x80e8'] else 1)
            value,history,timers=reference(t)
            assert b['expected']==[value,history,timers]
            assert [b['after'][a] for a in ['0x9454','0x9455','0x82a5','0x82a6','0x82a7']]==[value,history,*timers]
            call=row['call']
            assert timers==[call//2+1]*3 and g['0x828b']==call//2+1
            assert enabled==(call<46 or call>=290)
            assert value==int(call<46) and history==0
            threshold=expected_curve(g['0x9334']);assert b['threshold']==threshold
            assert threshold==(8960 if call==0 else 7168)
            if call>=290:
                assert g['0x800e']==0 and g['0x80e8']==10240
                assert not g['0x9317']&9 and not g['0x94f4']&1
                assert g['0x828b']>=61 and timers[2]>=61
            flags=dict(admitted=enabled,
                       timer_force_off=g['0x828b']>=61 and timers[2]>=61,
                       selector_force_off=bool(g['0x9317']&8),
                       below_threshold=g['0x80e8']<threshold,
                       set_window=g['0x828b']<=31 or timers[2]<=31,
                       set_threshold=g['0x80e8']>=threshold+1280,
                       set_motion=g['0x800e']<11 or timers[0]<=31 or timers[1]<=31,
                       set_flag_clear=not bool(g['0x94f4']&1),output=value)
            if flags!=last:
                transitions.append(dict(call=row['call'],conditions=flags,inputs=g,threshold=threshold))
                last=flags
    result=dict(status='PASS',scope=__doc__,task_pairs=len(rows),exact_prior320=True,
                whole_application_ram_checks=counts,condition_transitions=transitions,
                rom_sha256=hashlib.sha256(TCU).hexdigest())
    (ROOT/'tcu-recovery-cut-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
