"""Original TCU49B08 stored-adjustment admission/capture/abort/completion.

Independent integer/state models, actual queue readers and update body.
Raw inputs and invocation cadence are fixtures; no physical learning claim.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_tcu_stored_adjustments as stored
from verify_tcu_stored_adjustments import TCU,w,r,word,SHRotate,signed
from verify_tcu_transition_classification import pending_model
ROOT=Path(__file__).resolve().parent


def phase(t,code):
    head,count=r(t,0x96C4),r(t,0x96C5)
    for i in range(count):
        p=0x95D4+15*((head+i)&15)
        if r(t,p+10)==(code&65535):return r(t,p+13)
    return 255


def events(t):
    proposal=r(t,0x8084);old=r(t,0x9CA4)
    a=r(t,0x9BFC)&1;b=r(t,0x9C00)&1
    c=int(bool(r(t,0x9ACD)&16 or r(t,0x9C00)&16 or not r(t,0x9C00)&2))
    out=old
    if proposal>r(t,0x9CA3):
        out=(out&~0x70)|(16 if a and not old&2 else 0)|(32 if b and not old&4 else 0)|(64 if not c and old&8 else 0)
    out=(out&~14)|(a<<1)|(b<<2)|(c<<3)
    w(t,0x9CA4,out);w(t,0x9CA3,proposal)


def transition(t):
    proposed,accepted=r(t,0x8084),r(t,0x8081);flag=r(t,0x9CA4)&128
    if pending_model(t) and proposed!=accepted:flag=128
    if proposed==accepted==r(t,0x9C99):flag=0
    w(t,0x9CA4,(r(t,0x9CA4)&127)|flag)


def admission(t):
    return int(r(t,0x8080) in [4,5,6] and r(t,0x9B40) not in [10,17]
       and signed(r(t,0x809C,2),16)>=word(0x77372) and signed(r(t,0x80F2,2),16)>=word(0x77370)
       and not r(t,0x916F)&16 and not r(t,0x9330)&33 and not r(t,0x92D9)&16 and not r(t,0x916C)&1)


def capture(t):
    group=r(t,0x8089)
    edge=pending_model(t) and r(t,0x9CA2)==0 and group<=2 and not r(t,0x9CA4)&(16<<group)
    return int(edge and r(t,0x8084)==r(t,0x8081) and not r(t,0x9CA4)&128
       and r(t,0x81EB)>=TCU[0x75E7C+group] and r(t,0x9B3D) in [0,1])


def peak(t):
    w(t,0x9C9C,max(signed(r(t,0x9C9C,2),16),signed(r(t,0x80EE,2),16)),2)


def abort(t):
    group=r(t,0x9C9E,2);slot=group if group<=2 else 0
    timer=r(t,{0:0x822C,1:0x822D}.get(group,0x822F))
    qualified=r(t,0x9CA2)!=0 and not pending_model(t) and timer>=TCU[0x70AAD+slot*6+r(t,0x808D)]
    return int(qualified or r(t,0x8081)!=r(t,0x9C99))


def completion(t):
    current=phase(t,r(t,0x9C9E,2));old=signed(r(t,0x9C9A),8)
    done=(current==1 and old<=0) or (r(t,0x92D1)&1 and not r(t,0x9CA4)&1)
    w(t,0x9C9A,current)
    return int(bool(done))


def lifecycle_model(t):
    state,accepted=r(t,0x9C98),r(t,0x8081);events(t);transition(t)
    outcome='hold';update=None
    if not admission(t):state=0;outcome='inhibited'
    elif state==0:
        if capture(t):
            for a,v in [(0x9C9E,signed(r(t,0x8089),8)),(0x9CA0,r(t,0x80EA,2)),(0x9C9C,r(t,0x80EE,2))]:w(t,a,v,2)
            w(t,0x9C9A,phase(t,r(t,0x9C9E,2)));state=1;outcome='capture'
    elif state==1:
        peak(t)
        if abort(t):state=0;outcome='abort'
        elif completion(t):
            update=stored.model(t)
            if update['admitted']:w(t,0x616A+2*update['index'],update['new'],2)
            state=0;outcome='complete'
    if r(t,0x9C99)>accepted:w(t,0x81EB,0)
    w(t,0x9C98,state);w(t,0x9C99,accepted);w(t,0x9CA2,pending_model(t))
    w(t,0x9CA4,(r(t,0x9CA4)&254)|(r(t,0x92D1)&1))
    return outcome,update


def execute(t):
    other=copy.deepcopy(t);outcome,update=lifecycle_model(other)
    regs=t.r[8:16].copy();sr=t.sr&~0x301;t.visited.clear();t.run(0x49B08,limit=100000)
    assert t.r[8:16]==regs and t.sr&~0x301==sr
    for a in [*range(0x9C98,0x9CA5),0x81EB,*range(0x616A,0x6188)]:
        assert r(t,a)==r(other,a),(hex(a),r(t,a),r(other,a),outcome)
    assert (0x49FE0 in t.visited)==(outcome=='complete')
    assert (0x2456E in t.visited)==bool(update and update['admitted'])
    return dict(outcome=outcome,state=r(t,0x9C98),flags=r(t,0x9CA4),peak=signed(r(t,0x9C9C,2),16),update=update)


def setup(group=0):
    t=SHRotate(TCU)
    for a,v in [(0x8080,4),(0x8081,1),(0x8084,1),(0x8088,2),(0x8089,group),(0x9C99,1),(0x81EB,122),(0x9C00,2)]:w(t,a,v)
    for a,v in [(0x809C,23040),(0x80F2,32000),(0x80EA,1000),(0x80EE,15000)]:w(t,a,v,2)
    w(t,0x96C4,0);w(t,0x96C5,1)
    for i in range(10):w(t,0x95D4+i,1)
    w(t,0x95DE,group);w(t,0x95E1,0)
    return t


def check_helper(t,address,model):
    other=copy.deepcopy(t);want=model(other);saved=t.r[8:16].copy();t.visited.clear();got=t.run(address,limit=100000)
    assert t.r[8:16]==saved
    if want is not None:assert got==want,(hex(address),got,want)
    for a in [0x9CA3,0x9CA4,0x9C9A,0x9C9C,0x9C9D]:assert r(t,a)==r(other,a),(hex(address),hex(a),r(t,a),r(other,a))


def direct():
    counts=dict(events=0,transition=0,admission=0,capture=0,peak=0,abort=0,completion=0,lifecycle=0);outcomes={}
    for old,a,b,c,rise in itertools.product(range(256),[0,1],[0,1],[0,1],[0,1]):
        t=setup();w(t,0x9CA4,old);w(t,0x9BFC,a);w(t,0x9C00,b|(0 if c else 2));w(t,0x9CA3,0 if rise else 1)
        check_helper(t,0x49BE8,events);counts['events']+=1
    for old,pending,proposal,accepted,previous in itertools.product([0,128,255],[0,1],[0,1,255],[0,1,255],[0,1,255]):
        t=setup();w(t,0x9CA4,old);w(t,0x8088,2 if pending else 0);w(t,0x8084,proposal);w(t,0x8081,accepted);w(t,0x9C99,previous)
        check_helper(t,0x49D00,transition);counts['transition']+=1
    for address,values,size in [(0x8080,range(256),1),(0x9B40,range(256),1),(0x809C,[0,23039,23040,23041,32767,32768,65535],2),(0x80F2,[0,31999,32000,32001,32767,32768,65535],2)]+[(a,range(256),1) for a in [0x916F,0x9330,0x92D9,0x916C]]:
        for v in values:
            t=setup();w(t,address,v,size);check_helper(t,0x49D66,admission);counts['admission']+=1
    for group,flags,pending,previous,timer,operation in itertools.product([0,1,2,3,255],[0,16,32,64,128,255],[0,1],[0,1],[121,122,123],[0,1,2]):
        t=setup(group);w(t,0x9CA4,flags);w(t,0x8088,2 if pending else 0);w(t,0x9CA2,previous);w(t,0x81EB,timer);w(t,0x9B3D,operation)
        check_helper(t,0x49E10,capture);counts['capture']+=1
    for old,new in itertools.product([-32768,-1,0,15000,15616,32767],repeat=2):
        t=setup();w(t,0x9C9C,old,2);w(t,0x80EE,new,2);check_helper(t,0x49F66,peak);counts['peak']+=1
    for group,timer,pending,previous,changed,axis in itertools.product([0,1,2,3,65535],[182,183,184],[0,1],[0,1],[0,1],range(6)):
        t=setup();w(t,0x9C9E,group,2);w(t,0x8088,2 if pending else 0);w(t,0x9CA2,previous);w(t,0x9C99,0 if changed else 1);w(t,0x808D,axis)
        for a in [0x822C,0x822D,0x822F]:w(t,a,timer)
        check_helper(t,0x49EE0,abort);counts['abort']+=1
    for current,old,flag,prior in itertools.product([0,1,2,127,128,255],[0,1,2,127,128,255],[0,1],[0,1]):
        t=setup();w(t,0x95E1,current);w(t,0x9C9A,old);w(t,0x92D1,flag);w(t,0x9CA4,prior)
        check_helper(t,0x49F7A,completion);counts['completion']+=1
    rng=random.Random(0x49B08)
    for _ in range(1200):
        t=setup(rng.randrange(3))
        for a in [0x9C98,0x9C99,0x9CA2,0x8081,0x8084]:w(t,a,rng.choice([0,1,2,255]))
        for a in [0x9CA3,0x9CA4,0x9BFC,0x9C00,0x9ACD,0x92D1]:w(t,a,rng.randrange(256))
        w(t,0x8080,rng.choice([3,4,5,6]));w(t,0x9C9E,rng.randrange(4),2);w(t,0x95E1,rng.choice([0,1,2,3,255]));w(t,0x9C9A,rng.choice([0,1,255]));w(t,0x9C9C,rng.randrange(65536),2)
        row=execute(t);outcomes[row['outcome']]=outcomes.get(row['outcome'],0)+1;counts['lifecycle']+=1
    return counts,outcomes


def retained():
    rows=[]
    for group,measurement in itertools.product(range(3),[15000,15600,17000]):
        t=setup(group);stored.initialize(t);w(t,0x80EE,measurement,2)
        trace=[execute(t)];assert trace[-1]['outcome']=='capture'
        w(t,0x80EE,measurement-100,2);trace.append(execute(t));assert trace[-1]['outcome']=='hold' and trace[-1]['peak']==measurement
        w(t,0x80EA,1000+TCU[0x75E7F+group]*64,2);w(t,0x95E1,1)
        trace.append(execute(t));assert trace[-1]['outcome']=='complete' and trace[-1]['update']['admitted']
        trace.append(execute(t));assert trace[-1]['outcome']=='hold'
        rows.append(dict(group=group,measurement=measurement,trace=trace,offsets=[signed(r(t,0x6176+2*i,2),16) for i in range(3)]))
    for cause in ['accepted_change','queue_expiry','inhibit','flag_completion']:
        t=setup();stored.initialize(t);trace=[execute(t)];assert trace[-1]['outcome']=='capture'
        if cause=='accepted_change':w(t,0x8081,2)
        elif cause=='queue_expiry':w(t,0x8088,0);w(t,0x822C,183)
        elif cause=='inhibit':w(t,0x8080,3)
        else:w(t,0x92D1,1);w(t,0x80EA,1320,2)
        trace.append(execute(t))
        want='inhibited' if cause=='inhibit' else 'complete' if cause=='flag_completion' else 'abort'
        assert trace[-1]['outcome']==want and trace[-1]['state']==0
        rows.append(dict(cause=cause,trace=trace))
    return rows


def produce_offsets(t,measurement):
    stored.initialize(t);events_seen=[]
    # Establish raw upstream fixtures; state9C98 starts idle as in local setup.
    w(t,0x9C98,0);w(t,0x9CA4,0);w(t,0x9CA2,0);w(t,0x9CA3,1)
    for a,v in [(0x8080,4),(0x8081,1),(0x8084,1),(0x9C99,1),(0x9C00,2),(0x81EB,122)]:w(t,a,v)
    for a in [0x916F,0x9330,0x92D9,0x916C,0x9B40,0x9B3D,0x9BFC,0x9ACD,0x92D1]:w(t,a,0)
    w(t,0x809C,23040,2);w(t,0x80F2,32000,2);w(t,0x96C4,0);w(t,0x96C5,1)
    for i in range(10):w(t,0x95D4+i,1)
    for group in range(3):
        w(t,0x8089,group);w(t,0x95DE,group)
        for _ in range(8):
            w(t,0x8088,0);events_seen.append(execute(t)['outcome']) # observed no-pending state before new event
            w(t,0x8088,2);w(t,0x95E1,0);w(t,0x80EA,1000,2);w(t,0x80EE,measurement,2)
            row=execute(t);assert row['outcome']=='capture';events_seen.append(row['outcome'])
            w(t,0x95E1,1);w(t,0x80EA,1000+TCU[0x75E7F+group]*64,2)
            row=execute(t);assert row['outcome']=='complete' and row['update']['admitted'];events_seen.append(row['outcome'])
    offsets=[signed(r(t,0x6176+2*i,2),16) for i in range(3)]
    assert offsets==([192,256,320] if measurement==15000 else [-512,-512,-512])
    return offsets,events_seen


def replays():
    raw=(ROOT/'tcu-fault-selection-snapshots.json').read_bytes();snapshots=json.loads(raw);rows=[]
    for call,measurement,full in itertools.product([150,211],[15000,17000],[False,True]):
        t=stored.restore(snapshots[str(call)]);t.application_call=call
        # configure() writes stored offsets: it must precede their production.
        stored.configure(t,1,3,0,23040)
        offsets,events_seen=produce_offsets(t,measurement)
        consumed_offsets=[signed(r(t,0x6176+2*i,2),16) for i in range(3)]
        assert consumed_offsets==offsets
        if full:
            t.run(0x44CFE,limit=1000000);stored.selection_then_limit(t)
            outcome=dict(proposed=r(t,0x8084),accepted=r(t,0x8081),creations=t.creation_calls)
        else:
            t.run(0x4530C,limit=1000000);pair=stored.proposal_model(t)
            t.r[5]=0xFFFEC000;t.run(0x4508A,0xFFFEC004)
            assert [t.read(0xFFFEC004,1),t.read(0xFFFEC000,1)]==list(pair)
            outcome=dict(scan=list(pair))
        assert not t.optional_pending and len(t.threshold_rows)==10
        rows.append(dict(call=call,measurement=measurement,full=full,offsets=offsets,consumed_offsets=consumed_offsets,events=events_seen,thresholds=t.threshold_rows,**outcome))
    return hashlib.sha256(raw).hexdigest(),rows


def main():
    counts,outcomes=direct();print('Direct',counts,outcomes,flush=True)
    rows=retained();sha,replayed=replays()
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,outcomes=outcomes,retained=rows,snapshots_sha256=sha,replays=replayed)
    (ROOT/'tcu-adjustment-lifecycle-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('Retained',len(rows),'replays',len(replayed),flush=True)
if __name__=='__main__':main()
