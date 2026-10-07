"""Original74D62 activity-hold producer, including protected-read side effects.

Independent whole-application-RAM oracle; physical meanings are unassigned.
"""
import hashlib
import itertools
import json
from pathlib import Path
from probe_control_activity_hooks import Hooks
from verify_control_contributions import ECU,r,w
from verify_control_raw_inputs import application,expected_write

ROOT=Path(__file__).resolve().parent
FIELDS=[0x914E,0xA556,0x914D,0x925E,0xA55C,0x2B84,0xA562,0x900A,0x915C]


def expected_timer(e):
    reload=min(65535,sum(int.from_bytes(ECU[a:a+2],'big') for a in [0xE0862,0xE0864,0xE0866]))
    value=reload if not r(e,0x735A)&128 else 0 if r(e,0x8FD8)==0 else max(0,r(e,0x8FD4,2)-1)
    want=application(e);expected_write(want,0x8FD4,value,2)
    return want,value


def expected(e):
    want=application(e)
    previous,current=r(e,0x914E),r(e,0xA556)
    latch=1 if previous!=0 and current==0 else r(e,0x914D)
    expected_write(want,0x914D,latch,1)
    helper=r(e,0x8FD4,2)==0 and r(e,0x925E)!=1
    predicate=r(e,0xA55C)!=1 and r(e,0x2B84)==1
    protected=helper and predicate and latch==0 and r(e,0xA562)==0 and r(e,0x900A)==0
    value=r(e,0x282C)
    invalid=protected and (value^r(e,0x282D))!=255
    if invalid:
        value=0;expected_write(want,0x534C,0xFFFF282C,4);expected_write(want,0x5354,1,1)
    flag=int(not helper or (protected and value==0) or r(e,0x915C)==1)
    expected_write(want,0x9149,flag,1);expected_write(want,0x914E,current,1)
    return want,dict(helper=helper,protected=protected,invalid=invalid,flag=flag,latch=latch)


class Hold(Hooks):
    def __init__(self):
        super().__init__();self.readers=[]
    def instruction(self,pc):
        if pc in [0x14450,0x15146,0x157F0]:self.readers.append(pc)
        return super().instruction(pc)


def check(e):
    want,detail=expected(e);saved=e.r[8:16].copy();gbr=e.gbr
    e.run(0x74D62)
    assert application(e)==want
    assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==0xF0 and not e.accesses
    targets=([0x14450] if detail['helper'] else [])+([0x15146] if detail['protected'] else [])+([0x157F0] if detail['invalid'] else [])
    assert e.readers==targets,(e.readers,targets)
    return detail


def main():
    counts=dict(helper=0,boolean_gates=0,byte_sweeps=0,timer=0)
    outcomes=dict(set=0,clear=0,invalid=0)
    for a,b in itertools.product(range(256),[0,1,2,255]):
        e=Hold();w(e,0xA55C,a);w(e,0x2B84,b);want=application(e);saved=e.r[8:16].copy()
        assert e.run(0x14450)==int(a!=1 and b==1)
        assert application(e)==want and e.r[8:16]==saved
        counts['helper']+=1
    for values,timer,pair in itertools.product(itertools.product([0,1],repeat=len(FIELDS)),[0,1,65535],[0x00FF,0x01FE,0xFF00,0x0000,0x0101]):
        e=Hold()
        for a,v in zip(FIELDS,values):w(e,a,v)
        w(e,0x8FD4,timer,2);w(e,0x282C,pair,2)
        d=check(e);outcomes['set' if d['flag'] else 'clear']+=1;outcomes['invalid']+=int(d['invalid'])
        counts['boolean_gates']+=1
    for field,value in itertools.product(FIELDS,range(256)):
        e=Hold();w(e,0x2B84,1);w(e,0x282C,0x00FF,2);w(e,field,value)
        check(e);counts['byte_sweeps']+=1
    for mode,enabled,old in itertools.product(range(256),[0,1,2,255],[0,1,2,639,640,65535]):
        e=Hold();w(e,0x735A,mode);w(e,0x8FD8,enabled);w(e,0x8FD4,old,2)
        want,value=expected_timer(e);saved=e.r[8:16].copy();gbr=e.gbr
        e.run(0x6F422)
        assert application(e)==want and e.r[8:16]==saved and e.gbr==gbr
        assert e.sr&0xF0==0xF0 and not e.accesses
        counts['timer']+=1
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,counts=counts,total=sum(counts.values()),gate_outcomes=outcomes)
    (ROOT/'control-activity-hold-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts,outcomes)

if __name__=='__main__':main()
