"""CAN201/CAN4EC source arbitration and complete comparison-input producer.

Original bodies and helpers execute. CAN4EC bytes are explicit received-buffer
fixtures: sender, physical meaning, transport admission and task cadence open.
"""
import hashlib
import itertools
import json
import random

from sh_subset import signed
from verify_can201_byte6 import ECU,TCU,w,r,ecu_payload,receive
from verify_tcu_qualification_lifecycle import ObservedLifecycle,retained
from verify_tcu_qualification_limit import phase_for_code
from verify_tcu_transition_classification import pending_model

HISTORY=[0x934E+2*i for i in range(4)]
LONG_HISTORY=[0x9358+2*i for i in range(25)]
WORDS=[0x89B0,0x8808,0x809C,0x9340,0x9342,0xA4D8,*HISTORY,*LONG_HISTORY]
BYTES=[0x88C4,0x88C5,0x880A,0x89B2,0x92D5,0x8199,0x9339,0x9338,0x9344,0x9356,0x8089,0xA4DA]
OUTPUT_WORDS=[0x809C,0x9340,0x9342,0xA4D8,*HISTORY,*LONG_HISTORY]
OUTPUT_BYTES=[0x8199,0x9339,0x9338,0x9344,0x9356,0xA4DA]


def snap(t):
    return {**{a:r(t,a,2) for a in WORDS},**{a:r(t,a) for a in BYTES}}


def source_model(d,raw):
    value,status=d[0x89B0],1
    if d[0x88C4]==1 and d[0x88C5]==2:
        if raw!=255:
            value=raw*5
            if d[0x880A]==2:value=max(value,d[0x8808])
            status=2
    else:
        status=d[0x880A]
        if status==2:value=d[0x8808]
    return value,status


def selected(d):
    return 3200 if d[0x92D5]&0x88 else min(25600,d[0x89B0]*256//10)


def word_magnitude(delta):
    return signed(-delta if signed(delta,16)<0 else delta,16)


def producer_model(d,pending,phase):
    value=selected(d)
    history=[d[0x809C],*[d[a] for a in HISTORY[:3]]]
    for a,v in zip(HISTORY,history):d[a]=v
    d[0x809C]=value;d[0xA4D8]=value*10//256
    d[0xA4DA]=4 if d[0x92D5]&0x88 else (1 if d[0x89B2]==2 else 2)
    bounds=[128*x for x in TCU[0x5CD1C:0x5CD29]]
    category=12 if value>=bounds[12] else next(i for i,v in enumerate(bounds) if value<v)
    if category<signed(d[0x9339],8) and value>=signed(bounds[category]-640,16):category+=1
    d[0x9339]=category;d[0x9338]=category//2 if category<10 else category-5
    short=value-signed(history[0],16);long=value-signed(history[3],16)
    if word_magnitude(short)>=25600:
        d[0x8199]=0
        if word_magnitude(long)>=2560:d[0x9344]|=2
    if word_magnitude(long)<2560 and d[0x8199]>=6:d[0x9344]&=253
    change=0 if d[0x9344]&2 else long
    d[0x9340]=change&65535
    values=[change&65535,*[d[a] for a in LONG_HISTORY[:24]]]
    for a,v in zip(LONG_HISTORY,values):d[a]=v
    if pending and d[0x8089]==d[0x9356]:
        chosen=signed(d[0x9342],16)
        if phase<1:chosen=max(chosen,signed(change,16))
    else:
        chosen=change
        if d[0x8089]!=d[0x9356]:chosen=max([signed(change,16),*[signed(x,16) for x in values[1:19]]])
    d[0x9356]=d[0x8089];d[0x9342]=chosen&65535


class ObservedComparison(ObservedLifecycle):
    def __init__(self):
        super().__init__()
        self.source_expected=self.comparison_expected=None
        self.input_source_checks=self.comparison_checks=0
        self.application_call=None;self.comparison_rows=[]
    def instruction(self,pc):
        if pc==0x17E74:self.source_expected=source_model(snap(self),r(self,0x8F0F))
        elif pc==0x17EEC:
            assert (r(self,0x89B0,2),r(self,0x89B2))==self.source_expected
            self.input_source_checks+=1;self.source_expected=None
        elif pc==0x230F0:
            d=snap(self);producer_model(d,pending_model(self),phase_for_code(self,d[0x8089]));self.comparison_expected=d
        elif pc==0x23366:
            for a in OUTPUT_WORDS+OUTPUT_BYTES:
                size=1 if a in OUTPUT_BYTES else 2
                assert r(self,a,size)==self.comparison_expected[a],(hex(a),r(self,a,size),self.comparison_expected[a])
            self.comparison_checks+=1;self.comparison_expected=None
        result=super().instruction(pc)
        if pc==0x2399E and self.application_call in [0,1,2,99,100,101,109,110,111,114,118,130,162,163,170,171,320]:
            self.comparison_rows.append(dict(call=self.application_call,source=r(self,0x89B0,2),
                comparison=r(self,0x809C,2),change=r(self,0x9340,2),retained_change=r(self,0x9342,2),
                limit=r(self,0x939E,2),live_input=r(self,0x80F8,2),
                classification_limit=r(self,0x9C52,2),timers=[r(self,a) for a in [0x8159,0x815A,0x815B]]))
        return result


def direct_cases():
    t=ObservedComparison();rng=random.Random(0x230F0)
    counts=dict(flag=0,source=0,selection=0,producer=0)
    for byte in range(256):
        w(t,0x8F0D,byte);w(t,0x88C4,0xA5);w(t,0x88C5,0xA5);t.run(0x175EC)
        assert r(t,0x88C4)==int(bool(byte&4)) and r(t,0x88C5)==2
        counts['flag']+=1
    for raw,gate,valid,local in itertools.product(range(256),[(0,2),(1,2),(1,3)],[0,1,2,255],[0,780,65535]):
        for a,v in [(0x88C4,gate[0]),(0x88C5,gate[1]),(0x880A,valid),(0x8F0F,raw)]:w(t,a,v)
        w(t,0x8808,local,2);w(t,0x89B0,12345,2);t.run(0x17E74)
        counts['source']+=1
    for flags,value in itertools.product(range(256),[0,1,124,125,780,1000,1001,1270,32767,32768,65535]):
        w(t,0x92D5,flags);w(t,0x89B0,value,2)
        assert t.run(0x23380)==selected(snap(t))
        counts['selection']+=1
    for n in range(1600):
        for a in WORDS:w(t,a,rng.randrange(65536),2)
        for a in BYTES:w(t,a,rng.randrange(256))
        w(t,0x89B0,rng.choice([0,1,125,780,1000,1270,65535]),2)
        w(t,0x92D5,rng.choice([0,8,128,136]))
        code=rng.randrange(12);w(t,0x8089,code);w(t,0x9356,rng.choice([code,(code+1)%12,255]))
        w(t,0x8088,rng.choice([1,2]));w(t,0x96C4,0);w(t,0x96C5,1)
        w(t,0x95DE,code);w(t,0x95E1,rng.randrange(4));w(t,0x95D5,0)
        t.run(0x230F0,limit=1000000);counts['producer']+=1
    return counts


def input_lifecycle(remote_change=False):
    t=ObservedComparison();payload=ecu_payload(78,78,0)
    assert payload[6]==156
    def update(t,call):
        t.application_call=call
        if call==0:
            receive(t,payload)
            for i in range(7):w(t,0x8F0D+i,0)
        if remote_change and call in [110,170]:
            w(t,0x8F0D,4 if call==110 else 0);w(t,0x8F0F,200)
        # Full original acquisition wrapper refreshes the CAN4EC flag and
        # arbitration, including its other original callees. Then230F0.
        t.run(0x1ADD0,limit=1000000);t.run(0x230F0,limit=1000000)
    trace=retained(25,changes={100:100,170:25},t=t,comparison_update=update)
    assert t.comparison_checks==t.input_source_checks==321,(t.comparison_checks,t.input_source_checks)
    by_call={x['call']:x for x in t.comparison_rows}
    assert by_call[0]['comparison']==19968
    assert by_call[100]['limit']==12736 and by_call[100]['live_input']==7984
    if remote_change:
        assert by_call[110]['comparison']==25600 and by_call[110]['live_input']==12736
        assert by_call[110]['timers'][2]==0
    else:
        assert by_call[110]['comparison']==19968 and by_call[110]['live_input']==7984
        assert by_call[162]['live_input']==7984 and by_call[163]['live_input']==12736
    return dict(can201=payload.hex(' '),remote_change=remote_change,comparison_rows=t.comparison_rows,
                source_checks=t.input_source_checks,comparison_checks=t.comparison_checks,trace=trace)


def main():
    counts=direct_cases();print('Direct cases:',counts,flush=True)
    profiles=[]
    for remote in [False,True]:
        profiles.append(input_lifecycle(remote));print('Profile:',remote,flush=True)
    previous=json.load(open('research/ecu-at-can/tcu-qualification-lifecycle-verification.json'))
    regression=retained(25)
    assert json.loads(json.dumps(regression))==previous['retained_traces'][0]
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                ecu_sha256=hashlib.sha256(ECU).hexdigest(),direct_cases=counts,
                total_direct_cases=sum(counts.values()),profiles=profiles,
                default_lifecycle_regression='320-call primary25 result exactly matches prior saved JSON')
    path='research/ecu-at-can/tcu-comparison-input-verification.json'
    with open(path,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
