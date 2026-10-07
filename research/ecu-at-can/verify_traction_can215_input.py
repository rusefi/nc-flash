"""Shared CAN arbitration -> ECU control publication -> CAN215 -> TCU809A.

Retains the six-step traction-candidate fixture, original firmware calls and
protected writes. Adds original CAN215 encoding and whole TCU paired caller.
No physical DSC attribution, actuator response or full task timing claim.
"""
import hashlib
import json
from fractions import Fraction

from verify_throttle_candidate import (
    setup, paired, publish, local_consumers, angle, selected, pack, f, rf,
)
from verify_tcu_paired_input import ECU, TCU, w, r, ObservedPair
from verify_can215_feedback import receive


def main():
    e=setup();t=ObservedPair();t.run(0x170D4)
    for a,v in [(0x6DC4,100),(0x6D40,20),(0x71D8,3),(0x71D0,4),(0x71C4,32),
                (0x7154,Fraction(1,2)),(0x6DB4,2000),(0x7E0C,40),(0x72F8,50),(0x6D00,0)]:
        f(e,a,v)
    rows=[]
    for active,alternate,override in [(0,0,0),(1,0,0),(1,1,0),(1,0,1),(1,0,2),(0,0,0)]:
        _,e=paired(3200,1600,10040,10060,active,e=e)
        w(e,0x718C,active);e.run(0xA477E,limit=100000)
        publish(e,alternate);local_consumers(e);angle(e)
        w(e,0x566E,override);f(e,0x5520,30)
        branch=selected(e);word=pack(e)
        w(e,0x734A,0x80)
        e.run(0x369D6);e.run(0x36A28)
        payload=bytes(r(e,0x6B50+i) for i in range(8))
        expected_byte=255 if r(e,0xA3A4)==1 else min(200,max(0,int(rf(e,0x6CD4)*2+Fraction(1,2))))
        assert payload[6]==expected_byte
        old=r(t,0x880C,2)
        receive(t,payload);t.run(0x22F3C,limit=1000000)
        expected_value=old if expected_byte==255 else expected_byte*5
        assert r(t,0x880C,2)==expected_value
        assert r(t,0x809A,2)==min(25600,expected_value*256//10)
        rows.append(dict(active=active,substitute=alternate,override=override,
            selected72fc=float(rf(e,0x72FC)),published6cd4=float(rf(e,0x6CD4)),
            branch=branch,final_command=float(rf(e,0x56A0)),outgoing_word=word,
            can215=payload.hex(' '),decoded880c=r(t,0x880C,2),validity880e=r(t,0x880E),
            primary809a=r(t,0x809A,2),published_status=r(t,0xA502)))
    assert [x['primary809a'] for x in rows]==[2176,2048,2048,2048,2048,2176]
    assert [x['validity880e'] for x in rows]==[2,2,1,2,2,2]
    assert rows[3]['can215']==rows[4]['can215']
    assert rows[3]['final_command']!=rows[4]['final_command']
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),
        tcu_sha256=hashlib.sha256(TCU).hexdigest(),rows=rows,
        primary_checks=t.primary_checks,comparison_checks=t.comparison_checks)
    path='research/ecu-at-can/traction-can215-input-verification.json'
    with open(path,'w') as out:json.dump(result,out,indent=2);out.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
