"""Stock admission versus conditional class-adjustment behavior.

Execute untouched TCU code, including its original getters and full outer
369A4 caller. No ROM patch, predicate stub or direct output-state injection.
"""
import hashlib
import itertools
import json
from pathlib import Path
from verify_tcu_class_adjustments import fixture, execute, slots, flags, TCU, w, r

ROOT = Path(__file__).resolve().parent


def admitted_fixture():
    t = fixture()
    for a, v, size in [(0x9922,1,1),(0x9870,1,1),(0x9390,11000,2),
            (0x98DE,0,2),(0x98E0,0,1),(0x92C5,0,1),(0x92D1,4,1),
            (0x993E,0,2),(0x80F2,12800,2)]:
        w(t,a,v,size)
    return t


def main():
    assert TCU[0x77142:0x77146] == bytes.fromhex('32003200')
    t = admitted_fixture(); low_branch=high_branch=0
    for raw in range(65536):
        w(t,0x80F2,raw,2); w(t,0x821E,61)
        assert execute(t,0x36BDA) == 0
        assert r(t,0x821E) == 0
        assert 0x36C2E in t.visited
        if raw < 12800 or raw >= 32768:
            assert 0x36C38 not in t.visited
            low_branch += 1
        else:
            assert 0x36C38 in t.visited and 0x36C3C not in t.visited
            high_branch += 1
    print('Exhaustive signed-word admission passed',low_branch,high_branch,flush=True)
    cases=0
    for state, counter, mode, raw in itertools.product([0,1,2,3,255],
            [0,14,15,255],[0,1,2,3,4,5,6,255],[12799,12800,12801]):
        t=admitted_fixture(); w(t,0x985C,state); w(t,0x985D,counter)
        w(t,0x9870,mode); w(t,0x80F2,raw,2); w(t,0x821E,255)
        before=slots(t); seen=flags(t); error=r(t,0x98DC,2)
        execute(t,0x369A4)
        want=0 if state in [1,2] and mode in [2,3,4,6] else 1 if state==2 else state
        assert r(t,0x985C)==want and r(t,0x985D)==0
        assert 0x36D1A not in t.visited
        assert slots(t)==before and flags(t)==seen and r(t,0x98DC,2)==error
        if state in [1,2]: assert r(t,0x821E)==0
        cases+=1
    # Retain state through the original start helper and complete outer body.
    t=admitted_fixture(); w(t,0x985C,0); w(t,0x985D,14)
    execute(t,0x369EC)
    assert r(t,0x985C)==1 and r(t,0x821E)==0
    rows=[]
    for call in range(1,121):
        w(t,0x80F2,[12799,12800,12801][call%3],2)
        w(t,0x821E,61)  # favorable externally supplied timer, not a scheduler claim
        execute(t,0x369A4)
        assert r(t,0x985C)==1 and r(t,0x985D)==0 and r(t,0x821E)==0
        assert 0x36D1A not in t.visited and slots(t)==[0]*15 and flags(t)==[0]*3
        rows.append(dict(call=call,state=r(t,0x985C),counter=r(t,0x985D),timer=r(t,0x821E)))
    output=dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        calibration_addresses=['77142','77144'],calibration_values=[12800,12800],
        exhaustive_admission_cases=65536,rejected_below_signed_lower=low_branch,
        rejected_at_or_above_signed_upper=high_branch,full_outer_cases=cases,
        retained=rows,scope_limit='Stock 36BDA always rejects under immutable ROM; 369A4 cannot sustain state 2 or call 36D1A. Other direct callers/state writers not globally excluded. Earlier updater traces explicitly fixture admission and remain conditional behavior, not stock reachability.')
    (ROOT/'tcu-class-admission-verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print('Verified stock admission:',65536,'full callers:',cases,'retained:',len(rows),flush=True)


if __name__=='__main__': main()
