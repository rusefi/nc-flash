"""Original inhibit-latch writer and mode-pulse producer, including task boundaries.

Independent full applicationRAM and return-value models; peripheral samples
and call/timer ordering explicit. No physicalunits, boot or realtimer claim.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path
import verify_tcu_source_inhibit as source
from verify_tcu_source_inhibit import pins,w,r,TCU
from sh_subset import signed
from verify_tcu_request_timing import RANGES

ROOT=Path(__file__).resolve().parent
LOW=int.from_bytes(TCU[0x77350:0x77352],'big');HIGH=int.from_bytes(TCU[0x7734E:0x77350],'big')
EDGE_LIMIT=TCU[0x76EA0]
assert (LOW,HIGH,EDGE_LIMIT)==(7424,16640,92)


def fixture(seed=0):
    t=source.fixture(seed);rng=random.Random(seed)
    for a in list(range(0x9414,0x941B))+[0x8280,0x82B9,0x82BA,0xA520,0xA735,0x92C8,0x92C7,0x9C58,0x9C60]:w(t,a,rng.randrange(256))
    w(t,0x80EA,rng.randrange(65536),2);return t


def latch_model(t,argument):
    result=argument&0xFFFFFFFF;latch=r(t,0x9C58)&1;fault=r(t,0xA735)
    value=signed(r(t,0x80EA,2),16);gate=r(t,0x9415)
    if fault and not r(t,0x92C8)&32:
        if result&255==5:result=4
        if not latch and value<(LOW if r(t,0x92C7)&8 else HIGH):latch=1
    auxiliary=r(t,0x9C60)
    if r(t,0x92C7)&128 and not auxiliary&4 and value<HIGH:auxiliary|=4
    if gate==1:
        auxiliary &= 251
        if fault==0:latch=0
    if latch or auxiliary&4:result=3
    w(t,0x9C60,auxiliary);w(t,0x9C58,(r(t,0x9C58)&254)|latch)
    return result


def pulse_model(t):
    sample=r(t,0xA520)
    counter=signed(r(t,0x8280),8)&0xFFFFFFFF
    limit=signed(EDGE_LIMIT,8)&0xFFFFFFFF
    edge=counter<limit and r(t,0x941A)==0 and sample==1
    w(t,0x941A,sample)
    fired=r(t,0x9417)==1 or edge
    w(t,0x9414,int(fired))
    if fired:w(t,0x9417,0)
    state=r(t,0x9415)
    if r(t,0x9418)==1 or edge:state=1;w(t,0x9418,0);w(t,0x82B9,0)
    if state==1 and r(t,0x82B9)>=15:state=0
    w(t,0x9415,state)
    state=r(t,0x9416)
    if r(t,0x9419)==1:state=1;w(t,0x9419,0);w(t,0x82BA,0)
    if state==1 and r(t,0x82BA)>=15:state=0
    w(t,0x9416,state)


def direct():
    counts=dict(latch=0,pulse=0,initialize=0,requests=0)
    for fault,block,gate,old,aux,value,flags in itertools.product([0,1,255],[0,32],[0,1,2],[0,1],[0,4],[-32768,LOW-1,LOW,HIGH-1,HIGH,32767],[0,8,128,136]):
        t=fixture(value&65535)
        for a,v in [(0xA735,fault),(0x92C8,block),(0x9415,gate),(0x9C58,0xA4|old),(0x9C60,0xA1|aux),(0x92C7,flags)]:w(t,a,v)
        w(t,0x80EA,value,2);argument=[0,3,5,0x105,0xFFFFFFFF][counts['latch']%5]
        ref=copy.deepcopy(t);expected=latch_model(ref,argument);actual=pins.execute(t,0x47C9C,argument)
        assert actual==expected;source.equal(t,ref);counts['latch']+=1
    for counter,sample,previous in itertools.product(range(256),[0,1,2,255],[0,1]):
        t=fixture(counter+sample);w(t,0x8280,counter);w(t,0xA520,sample);w(t,0x941A,previous)
        for a in [0x9417,0x9418,0x9419]:w(t,a,0)
        ref=copy.deepcopy(t);pulse_model(ref);pins.execute(t,0x23DD0);source.equal(t,ref);counts['pulse']+=1
    for state,timer,request in itertools.product([0,1,2,255],[0,14,15,16,255],[0,1,2,255]):
        t=fixture(timer);w(t,0xA520,0)
        for a in [0x9415,0x9416]:w(t,a,state)
        for a in [0x9417,0x9418,0x9419]:w(t,a,request)
        for a in [0x82B9,0x82BA]:w(t,a,timer)
        ref=copy.deepcopy(t);pulse_model(ref);pins.execute(t,0x23DD0);source.equal(t,ref);counts['pulse']+=1
    for seed in range(16):
        t=fixture(seed);ref=copy.deepcopy(t)
        for a in list(range(0x9414,0x941B))+[0x8280]:w(ref,a,0)
        pins.execute(t,0x23D94);source.equal(t,ref);counts['initialize']+=1
        for entry,address in [(0x23DB8,0x9417),(0x23DC0,0x9418),(0x23DC8,0x9419)]:
            ref=copy.deepcopy(t);w(ref,address,1);pins.execute(t,entry);source.equal(t,ref);counts['requests']+=1
    return counts


class ObservedWriters(source.ObservedSource):
    def finish_writer(self,pc):
        if self.writer_pending is not None and self.writer_pending[0]==pc:
            _,ref,entry,expected,inputs=self.writer_pending;self.writer_pending=None
            source.equal(self,ref)
            if entry==0x47C9C:assert self.r[0]==expected
            self.writer_records.append(dict(entry=entry,inputs=inputs,result=self.r[0],
                outputs={hex(a):r(self,a) for a in [0x9414,0x9415,0x9416,0x9C58,0x9C60]}))
    def instruction(self,pc):
        self.finish_writer(pc)
        if pc in [0x47C9C,0x23DD0]:
            assert self.writer_pending is None
            inputs={hex(a):r(self,a) for a in [0x9415,0x9418,0xA735,0x92C7,0x92C8,0x9C58,0x9C60,0x82B9,0xA520]}
            inputs['80EA_word']=r(self,0x80EA,2)
            ref=copy.deepcopy(self)
            expected=latch_model(ref,self.r[4]) if pc==0x47C9C else pulse_model(ref)
            self.writer_pending=(self.pr,ref,pc,expected,inputs)
        return super().instruction(pc)


def task_fixture():
    t=source.task_fixture();t.__class__=ObservedWriters;t.writer_pending=None;t.writer_records=[];return t


def task_call(t):
    phase=r(t,0x84F4)&7;t.writer_records=[];result=source.task_call(t)
    assert t.writer_pending is None
    expected=[0x23DD0] if phase in [0,4] else [0x47C9C] if phase in [1,5] else []
    assert [row['entry'] for row in t.writer_records]==expected
    return dict(task=result,writers=t.writer_records.copy(),mode=r(t,0x9415),inhibit=r(t,0x9C58),source=r(t,0xA5A2),command=r(t,0xA5A0))


def wheel(t):
    ref=copy.deepcopy(t)
    low,mid,high=[r(t,a,4) for a in [0x8494,0x8498,0x849C]]
    assert low<16 and mid<16 and high<2
    tick=low+16*mid+256*high
    for begin,end,size,cap,period,positions in RANGES:
        if tick%period in positions:
            for a in range(begin,end,size):
                old=r(ref,a,size)
                if old!=cap:w(ref,a,(old+1)&((1<<(8*size))-1),size)
    if low%2==0:w(ref,0x90C8,(r(ref,0x90C8,2)+1)&65535,2)
    tick=(tick+1)%512
    for a,v in [(0x8494,tick%16),(0x8498,(tick//16)%16),(0x849C,tick//256)]:w(ref,a,v,4)
    pins.execute(t,0x11014);source.equal(t,ref)


def tasks():
    rows=[]
    for phase,fault,request in itertools.product(range(8),[0,1],[0,1]):
        t=task_fixture();w(t,0x84F4,phase);w(t,0xA735,fault);w(t,0x9418,request)
        rows.append(task_call(t))
    t=task_fixture();pins.execute(t,0x12880);retained=[]
    for call in range(64):
        w(t,0xA735,int(0<=call<16))
        # Eight wheelcalls perapplicationcall is an explicit fixture ratio,
        # not measuredscheduler cadence. Each wheelcall has fullRAM oracle.
        for _ in range(8):wheel(t)
        if call==24:pins.execute(t,0x23DC0)
        row=task_call(t);row['timers']=[r(t,a) for a in [0x8280,0x82B9,0x82BA]]
        retained.append(row)
    return rows,retained


def main():
    counts=direct();rows,retained=tasks()
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,rows=rows,retained=retained,
        timer_wheel_calls=512,writer_boundaries=sum(len(row['writers']) for row in rows+retained),
        limits='InputsA735/92C7/92C8/80EA/A520 andtimebase upstream stillopen; recordedfulltaskvalues atboundary. Producedtimerwheel with explicit8:1 callratio, no realtiming orboard/remotecontroller proof.')
    (ROOT/'tcu-inhibit-writers-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(counts,'tasks',len(rows),'retained',len(retained),'writerboundaries',result['writer_boundaries'],flush=True)


if __name__=='__main__':main()
