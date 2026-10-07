"""Independent timer wheel/callback selection with all original callees executed.

Checks F28C status clear,1062E counters and exact selected callbacks/admissions.
No independently modeled RAM oracle for every nested task/queue body; no task
drain or hardware interrupt entry here. Nonzero maskF0 prevents inline dispatch.
"""
import json
from pathlib import Path
from probe_control_timer_event2 import TimerEvent
from verify_control_contributions import ECU,r,w


def main():
    combinations={(counter,divider) for counter in range(1024) for divider in [0,4,255]}
    combinations.update((counter,divider) for counter in [65534,65535] for divider in range(256))
    callbacks=events=0
    wheel_indices=[1,2,4,5,6,7,8,9,10]
    wheel_tasks=[8,9,10,11,12,13,14,15,16]
    for counter,divider in sorted(combinations):
        e=TimerEvent();e.r[15]=0xFFFED000;e.sr=0xF0
        w(e,0x12B1,0);w(e,0x12C0,0xB0,4)
        e.run(0x38C4,0xFFFF12B0);e.run(0x3F40,0xFFFF12B0)
        w(e,0x51E0,counter,2);w(e,0x51E2,divider)
        nxt=(counter+1)&65535;d=(divider+1)&255
        indices=[0];tasks=[7]
        # Closed-form lowest set bit, independently from firmware's shift loop.
        bits=(nxt>>1)&511 if nxt&1 else 0
        if bits:
            bit=(bits&-bits).bit_length()-1
            indices.append(wheel_indices[bit]);tasks.append(wheel_tasks[bit])
        if d>=5:indices.append(13);tasks.append(3)
        expected=[int.from_bytes(ECU[0x1138C+i*4:0x11390+i*4],'big') for i in indices]
        status=(counter*37+divider)&65535;e.cmt_samples=[status];e.cmt_io=[]
        saved=e.r[8:16].copy();gbr=e.gbr;e.queue_entries=[];e.cmt_active=True
        try:e.run(0xF28C,limit=30000)
        finally:e.cmt_active=False
        assert e.cmt_io==[['read',0xFFFFF718,2,status],['write',0xFFFFF718,2,status&0xFF7F]]
        assert not e.cmt_samples
        assert [v['target'] for v in e.timer_callbacks]==expected
        assert all(v['argument']==0 for v in e.timer_callbacks)
        assert [v['argument'] for v in e.queue_entries if v['pc']==0x35E0]==tasks
        assert r(e,0x51E0,2)==nxt and r(e,0x51E2)==(0 if d>=5 else d)
        assert r(e,0x45D8)==int(d>=5) and r(e,0x45DB)==0
        assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0
        assert not e.rte_transfers and 0x2BCE6 not in e.visited
        callbacks+=len(expected);events+=int(d>=5)
    result=dict(status='PASS',scope=__doc__,cases=len(combinations),callback_calls=callbacks,
        upstream_event2_requests=events,periodic_divider=5,acquisition_requests_per_invocation=1,
        counter_wrap_checked=True,divider_byte_wrap_checked=True,
        status_bit_is_cleared_but_not_a_callback_admission_gate=True)
    Path(__file__).with_name('control-timer-event-admission-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
