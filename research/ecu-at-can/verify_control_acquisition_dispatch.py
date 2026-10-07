"""Independent whole-RAM dispatch-prefix and bounded RTE instruction checks."""
import itertools,json,random
from pathlib import Path
from probe_control_acquisition_dispatch import DispatchPrefix,RteBoundary
from sh_control_task_dispatch import TaskDispatch
from verify_control_raw_inputs import application,expected_write
from verify_control_contributions import w

ROOT=Path(__file__).resolve().parent


def main():
    prefixes=0
    for context,stack,sr,seed in itertools.product([0x12B0],[0xFFFF11A8,0xFFFFB000],[0,1,0xB0,0xF0],range(8)):
        e=DispatchPrefix();rng=random.Random(seed);e.sr=sr
        for a in range(0x11A0,0x1350):w(e,a,rng.randrange(256))
        w(e,0x11E0,0);w(e,context+12,stack,4)
        before=application(e);want=before.copy()
        for a,v,n in [(context+4,7,2),(context+8,0,4),(context+20,0xFFFF11E0,4),
                      (context+24,0x4140,4),(0x11E1,3,1),(0x11E4,stack,4),(0x45CC,7,2),
                      (stack-0xFFFF0000-8,0xE26C,4),(stack-0xFFFF0000-4,0,4)]:
            expected_write(want,a,v,n)
        e.r[5]=7
        try:e.run(0x3D10,0xFFFF0000+context)
        except RteBoundary:pass
        else:raise AssertionError('missed RTE boundary')
        actual=application(e)
        if actual!=want:
            difference={hex(a):[want.get(a,0),actual.get(a,0)] for a in sorted(set(actual)|set(want)) if actual.get(a,0)!=want.get(a,0)}
            (ROOT/'control-acquisition-dispatch-oracle-limit.json').write_text(json.dumps(dict(context=context,stack=stack,sr=sr,seed=seed,difference=difference),indent=2)+'\n')
        assert actual==want,(context,stack,sr,seed,difference if actual!=want else None)
        assert e.r[15]==stack-8 and e.r[4]==0xE26C and e.r[5]==stack and e.r[6]==0
        assert e.sr==sr|1 and e.pr==0xFFFFFFF0
        prefixes+=1
    rte=0
    for sp,target,sr in itertools.product([0xFFFE8000,0xFFFF11A0,0xFFFFBFF8],[0,0xE26C,0x3D0C,0x1B17E],
            [0,1,0xF0,0x3F3,0xFFFFFFFF,0xF000F000]+[1<<b for b in range(32)]):
        e=TaskDispatch();e.r=[(i*0x1020304)&0xFFFFFFFF for i in range(16)];e.r[15]=sp
        e.write(0xFFFE2000,0x002B0009,4);e.write(sp,target,4);e.write(sp+4,sr,4)
        old=e.r.copy();memory=e.ram.copy();gbr=e.gbr;pr=e.pr
        nxt,delay=e.instruction(0xFFFE2000)
        assert delay and nxt==target and e.r==old[:15]+[sp+8]
        assert e.sr==sr&0x0FFF0FFF and e.ram==memory and e.gbr==gbr and e.pr==pr
        _,nested=e.instruction(0xFFFE2002);assert not nested
        rte+=1
    rejects=0
    for sp,target,slot in [(0xFFFF11A1,0xE26C,9),(0,0xE26C,9),
                           (0xFFFFBFFC,0xE26C,9),(0xFFFF11A0,0xE26D,9),
                           (0xFFFF11A0,0xFFFFFFF0,9),(0xFFFF11A0,0xE26C,0x000B),
                           (0xFFFF11A0,0xE26C,0x7E08)]:
        e=TaskDispatch();e.write(0xFFFE2000,(0x2B<<16)|slot,4);e.r[15]=sp
        if sp>=0xFFFE0000:e.write(sp,target,4);e.write(sp+4,0,4)
        before=(e.r.copy(),e.sr,e.ram.copy())
        try:e.instruction(0xFFFE2000)
        except (ValueError,NotImplementedError):rejects+=1
        else:raise AssertionError('missing rejection')
        assert (e.r,e.sr,e.ram)==before
    result=dict(status='PASS',scope=__doc__,original_dispatch_prefix_cases=prefixes,
                rte_cases=rte,expected_rejections=rejects,physical_interrupts=False)
    (ROOT/'control-acquisition-dispatch-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
