"""Original event2 dispatch, decrement, phase advance and activity-hook checks.

Explicit event delivery and peripheral samples; no actual queue cadence.
"""
import hashlib
import itertools
import json
from pathlib import Path
from probe_control_outer_event import Outer
from verify_control_contributions import ECU,r,w

ROOT=Path(__file__).resolve().parent
TARGETS=[0x18DC8,0x1CAE8,0x1CAF0,0x1CB04,0x1CB0C]


def setup():
    e=Outer();e.registers[0xFFFFF74E]=1;e.run(0xCA94)
    e.write(0xFFFFD800,2,4)
    return e


def execute(e,fresh=False):
    phase=r(e,0x651C);pending=r(e,0x652D)
    before=[r(e,a) for a in [0x660E,0x660F,0x6610,0x6611]]
    preserved=e.r[8:16].copy();gbr=e.gbr;start=len(e.outer_entries)
    e.run(0x2BCE6,0xFFFFD800,limit=1000000)
    expected=[0x18282,0x16172]+([TARGETS[phase]] if phase<5 else [])+([0x1616C] if phase==0 else [])
    actual=[x['pc'] for x in e.outer_entries[start:]]
    major=[pc for pc in actual if pc not in [0x1616C,0x16172,0x16178,0x1617E]]
    expected_major=[0x18282]+([TARGETS[phase]] if phase<5 else [])
    if major!=expected_major or (fresh and actual!=expected):
        (ROOT/'control-outer-event-oracle-limit.json').write_text(json.dumps(dict(
            phase=phase,actual=actual,expected=expected,pending=pending,
            counters_before=before,counters_after=[r(e,a) for a in [0x660E,0x660F,0x6610,0x6611]],
            entries=e.outer_entries,tail=e.tail),indent=2)+'\n')
        raise AssertionError((phase,actual,expected))
    assert r(e,0x651C)==(phase+1 if phase<4 else 0)
    assert r(e,0x652D)==max(0,pending-1)
    after=[r(e,a) for a in [0x660E,0x660F,0x6610,0x6611]]
    if fresh:
        assert after==[(before[0]+int(phase==0))%256,before[1],(before[2]+1)%256,before[3]]
    assert e.r[8:16]==preserved and e.gbr==gbr and e.sr&0xF0==0xF0
    return dict(initial_phase=phase,phase=r(e,0x651C),pending_before=pending,pending=r(e,0x652D),entries=actual,counters_before=before,counters_after=after)


def main():
    isolated=[]
    for phase,pending in itertools.product([0,1,2,3,4,5,255],[0,1,255]):
        e=setup();w(e,0x651C,phase);w(e,0x652D,pending)
        for a in [0x660E,0x660F,0x6610,0x6611]:w(e,a,255)
        isolated.append(execute(e,fresh=True))
    e=setup();w(e,0x652D,3)
    retained=[execute(e) for _ in range(10)]
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,complete_outer_calls=len(isolated)+len(retained),retained_hook_status='Observed only; fresh-case hook oracle does not generalize to retained state',isolated=isolated,retained=retained)
    (ROOT/'control-outer-event-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('31 complete outer calls;phase/decrement/order verified;21 fresh hook-counter cases;retained hooks observed only')


if __name__=='__main__':main()
