"""Original1F3CE source1 inhibit/release and five command outputs.

Independent complete application-RAM oracle at direct and real task call
boundaries. Explicit control/input samples; no physicaldriver identity or
claim that arbitrary slot bytes are reachable during normal operation.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_tcu_application_order as order
from verify_tcu_application_order import pins,w,r,TCU

ROOT=Path(__file__).resolve().parent
ENABLED=[1,1,1,1,0,1,0,1,1,1,1]
assert list(TCU[0x5CCE8:0x5CCE8+11])==ENABLED
ROWS=[list(TCU[0x70014+6*i:0x70014+6*i+6]) for i in range(256)]
assert [row[0] for row in ROWS[:12]]==list(range(12))


def fixture(seed=0):
    t=order.fixture();rng=random.Random(seed)
    for a in [0x9415,0x9C58,0x9AE8,0x910C,0x8087,0xA5A2]:w(t,a,rng.randrange(256))
    for i in range(11):w(t,0x910D+i,rng.choice(list(range(12))+[255]))
    for i in range(5):w(t,0xA5C5+i,rng.randrange(256))
    return t


def prefix_model(t):
    inhibit=r(t,0x9C58)&1
    if r(t,0x9415)==1 and not inhibit:w(t,0xA5A2,0)
    if inhibit:w(t,0xA5A2,1);w(t,0x8087,4);return None
    for i,enabled in enumerate(ENABLED):
        if not enabled:w(t,0x910D+i,255)
    selection=4
    for i in range(11):
        value=r(t,0x910D+i)
        if value!=255:selection=value
    w(t,0x8087,selection);return selection


def model(t):
    selection=prefix_model(t)
    if selection is None:outputs=[0]*5
    else:
        row=next((row for row in ROWS if row[0]==selection),None)
        if row is None:raise ValueError('No match in wrapping byte-index search')
        outputs=[int(v==1) for v in row[1:]]
    for i,value in enumerate(outputs):w(t,0xA5C5+i,value)
    w(t,0x910C,(r(t,0x910C)&254)|int(bool(r(t,0x9AE8)&64)))


def equal(t,ref):
    pins.setup.equal(t,ref)
    assert (t.mcr,t.gsr,t.hcan_trace,t.digital_trace)==(ref.mcr,ref.gsr,ref.hcan_trace,ref.digital_trace)


def check(t):
    ref=copy.deepcopy(t);model(ref);pins.execute(t,0x1F3CE);equal(t,ref)


OUTPUTS=[(0xF738,6),(0xF738,7),(0xF73E,4),(0xF738,5),(0xF738,4)]
FEEDBACK_BITS=[4,5,9,12,7]


def publish_model(t):
    for i in range(5):
        value=r(t,0xA5CA+i) if r(t,0xA5CF+i)==1 else r(t,0xA5C5+i)
        if r(t,0x84A0) in [1,4]:value=0
        w(t,0x8A1C+i,value);w(t,0xA5C0+i,value)


def drive_model(t):
    for i,(address,bit) in enumerate(OUTPUTS):
        value=1<<bit if r(t,0x8A1C+i)==1 else 0
        pins.modify(t,address,65535^(1<<bit),value)


def feedback_model(t):
    for i,((address,bit),feedback) in enumerate(zip(OUTPUTS,FEEDBACK_BITS)):
        value=t.configuration[address]
        t.configuration_trace.append(('read',address,2,value));w(t,0x8A21+i,(value>>bit)&1)
        sample=t.digital_inputs[0xFFFFF726];t.digital_trace.append((0xFFFFF726,sample))
        w(t,0x8A26+i,(sample>>feedback)&1)


MODELS={0x1F3CE:model,0x52D8C:publish_model,0x186A4:drive_model,0x186EA:feedback_model}


def output_direct():
    rng=random.Random(0x52D8C);counts=dict(publish=0,drive=0,feedback=0)
    for mode,case in itertools.product([0,1,3,4,255],range(64)):
        t=fixture(case);w(t,0x84A0,mode)
        for i in range(5):
            w(t,0xA5CF+i,rng.choice([0,1,2,255]));w(t,0xA5CA+i,rng.randrange(256))
        ref=copy.deepcopy(t);publish_model(ref);pins.execute(t,0x52D8C);equal(t,ref);counts['publish']+=1
    for value in range(256):
        t=fixture(value)
        for i in range(5):w(t,0x8A1C+i,value)
        for a in [0xF738,0xF73E]:t.configuration[a]=rng.randrange(65536)
        ref=copy.deepcopy(t);drive_model(ref);pins.execute(t,0x186A4);equal(t,ref);counts['drive']+=1
    for bits in range(32):
        t=fixture(bits)
        for i in range(5):w(t,0x8A1C+i,(bits>>i)&1)
        ref=copy.deepcopy(t);drive_model(ref);pins.execute(t,0x186A4);equal(t,ref);counts['drive']+=1
        for feedback in [bits,31^bits]:
            t.digital_inputs[0xFFFFF726]=sum(((feedback>>i)&1)<<bit for i,bit in enumerate(FEEDBACK_BITS))
            ref=copy.deepcopy(t);feedback_model(ref);pins.execute(t,0x186EA);equal(t,ref);counts['feedback']+=1
    return counts


def direct():
    counts=dict(flags=0,priority=0,random=0,helpers=0,outside_table_returns=0,missing_key_bounded=0)
    for gate,inhibit in itertools.product(range(256),[0,1,2,255]):
        t=fixture(gate+inhibit);w(t,0x9415,gate);w(t,0x9C58,inhibit);check(t);counts['flags']+=1
    for slot,value in itertools.product(range(11),list(range(12))+[255]):
        t=fixture(slot+value);w(t,0x9C58,0)
        for i in range(11):w(t,0x910D+i,255)
        w(t,0x910D+slot,value);check(t);counts['priority']+=1
    for seed in range(256):
        t=fixture(seed);w(t,0x9C58,0);check(t);counts['random']+=1
    for seed in range(16):
        t=fixture(seed);ref=copy.deepcopy(t);w(ref,0x8087,4)
        for i in range(11):w(ref,0x910D+i,255)
        pins.execute(t,0x1F3A8);equal(t,ref);counts['helpers']+=1
    for slot,value in itertools.product(range(11),[0,1,4,11,255,0x1234]):
        t=fixture(slot+value);ref=copy.deepcopy(t);w(ref,0x910D+slot,value&255);t.r[5]=value
        pins.execute(t,0x1F3B6,slot);equal(t,ref);counts['helpers']+=1
        ref=copy.deepcopy(t);w(ref,0x910D+slot,255);pins.execute(t,0x1F3C2,slot);equal(t,ref);counts['helpers']+=1
    for key in sorted({row[0] for row in ROWS}-set(range(12))-{255}):
        t=fixture(key);w(t,0x9C58,0)
        for i in range(11):w(t,0x910D+i,255)
        w(t,0x910D+10,key);check(t);counts['outside_table_returns']+=1
    for key in [31,127,254]:
        assert not any(row[0]==key for row in ROWS)
        t=fixture(key);w(t,0x9C58,0)
        for i in range(11):w(t,0x910D+i,255)
        w(t,0x910D+10,key);ref=copy.deepcopy(t);assert prefix_model(ref)==key
        try:t.run(0x1F3CE,limit=10000)
        except RuntimeError:
            assert 0x1F4A0<=t.pc<=0x1F4B6;equal(t,ref);counts['missing_key_bounded']+=1
        else:raise AssertionError('missing key unexpectedly returned')
    return counts


class ObservedSource(order.ObservedTask):
    def finish_source(self,pc):
        if self.source_pending is not None and self.source_pending[0]==pc:
            _,ref,inputs,entry=self.source_pending;self.source_pending=None;equal(self,ref)
            self.source_records.append(dict(entry=entry,inputs=inputs,source=r(self,0xA5A2),selection=r(self,0x8087),
                                            outputs=[r(self,0xA5C5+i) for i in range(5)]))
    def instruction(self,pc):
        self.finish_source(pc)
        if pc in MODELS:
            assert self.source_pending is None
            inputs={hex(a):r(self,a) for a in [0x9415,0x9C58,0x9AE8,0x910C,0xA5A2]}
            ref=copy.deepcopy(self);MODELS[pc](ref);self.source_pending=(self.pr,ref,inputs,pc)
        return super().instruction(pc)


def task_fixture():
    t=order.fixture();t.__class__=ObservedSource;t.source_pending=None;t.source_records=[];return t


def task_call(t):
    phase=r(t,0x84F4)&7;t.source_records=[];result=order.run(t)
    assert t.source_pending is None
    assert [x['entry'] for x in t.source_records]==([0x1F3CE] if phase in [3,7] else [])+[0x52D8C,0x186A4,0x186EA]
    return dict(task=result,source_checks=t.source_records.copy())


def full_tasks():
    rows=[]
    for phase,gate,inhibit in itertools.product(range(8),[0,1,2,255],[0,1]):
        t=task_fixture();w(t,0x84F4,phase);w(t,0x9415,gate);w(t,0x9C58,inhibit)
        rows.append(task_call(t))
    t=task_fixture();retained=[]
    for call in range(40):
        w(t,0x9415,1 if call>=24 else 0)
        w(t,0x9C58,1 if 4<=call<12 else 0)
        retained.append(task_call(t))
    return rows,retained


def main():
    counts=direct();output_counts=output_direct();rows,retained=full_tasks()
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,output_counts=output_counts,task_cases=len(rows),
        retained_calls=len(retained),source_boundary_checks=sum(sum(y['entry']==0x1F3CE for y in x['source_checks']) for x in rows+retained),
        output_boundary_checks=3*(len(rows)+len(retained)),
        rows=rows,retained=retained,
        limits='All slot/key tests direct fixtures; normalcaller domain not proved. Fulltask nested sourcebody independentlyoracled, othernestedsemantics limitedasapplication-order. Nophysicaloutput/clock/remotecontroller proof.')
    (ROOT/'tcu-source-inhibit-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts,output_counts,'tasks',len(rows),'retained',len(retained),'boundaries',result['source_boundary_checks'],flush=True)


if __name__=='__main__':main()
