"""Independent whole-RAM oracle for original39926 periodic bank2 publication.

Raw ADC RAM samples only; no analog units, physical cadence or CAN sender claim.
"""
import hashlib,json,random
from pathlib import Path
from sh_control_task_dispatch import TaskDispatch
from verify_control_contributions import ECU,w,r
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent


def expected(e):
    want=application(e)
    for a,v,n in [(0x6C92,r(e,0x4040,2)>>6,2),(0x6CAE,r(e,0x4042,2)>>8,1),(0x6C98,r(e,0x4046,2),2)]:
        expected_write(want,a,v,n)
    return want


def stack_reproduction():
    from verify_control_activity_conditions import expected as activity_expected
    e=TaskDispatch();e.r[15]=0xFFFF11A8;e.sr=0
    want=activity_expected(e,0x74ED2);e.run(0x74ED2);actual=application(e)
    difference={hex(a):[want.get(a,0),actual.get(a,0)] for a in sorted(set(want)|set(actual)) if want.get(a,0)!=actual.get(a,0)}
    assert set(difference)=={hex(a) for a in [0xFFFF119D,0xFFFF11A0,0xFFFF11A1,0xFFFF11A2,0xFFFF11A3]}
    return difference


def main():
    rng=random.Random(0x39926);count=0
    samples=[(v<<6,((v*7)&1023)<<6,((v*13)&1023)<<6) for v in range(1024)]
    samples += [tuple(rng.randrange(65536) for _ in range(3)) for _ in range(2048)]
    for values in samples:
        e=TaskDispatch();e.sr=0xF0
        for a in range(0x6C90,0x6CB0):w(e,a,rng.randrange(256))
        for a,value in zip([0x4040,0x4042,0x4046],values):w(e,a,value,2)
        want=expected(e);saved=e.r[8:16].copy();gbr=e.gbr;sr=e.sr
        e.run(0x39926)
        assert application(e)==want and e.r[8:16]==saved and e.gbr==gbr and e.sr==sr
        count+=1
    stack_difference=stack_reproduction()
    result=dict(stack_mismatch_reproduced=stack_difference,status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),whole_ram_cases=count,
                outputs={'6c92':'word4040>>6','6cae':'word4042>>8','6c98':'word4046'})
    (ROOT/'control-periodic-raw-decode-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
