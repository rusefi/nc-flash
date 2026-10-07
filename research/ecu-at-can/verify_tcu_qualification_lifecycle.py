"""Selector-produced progress reset and timed CAN215 qualification lifecycle.

Original bodies execute; peripheral samples and scheduling remain explicit
fixtures. No physical selector names, tick duration or whole-task claim.
"""
import hashlib
import itertools
import json

from verify_can201_byte6 import ECU,TCU,w,r
from verify_tcu_qualification_limit import ObservedLimit,can_inputs,selection_then_limit,full_fixture
from verify_tcu_transition_progress import initialize_segment,SegmentEnd,PROGRESS,RATES
from verify_tcu_source_selection import sample
from verify_tcu_ascending_map import lifecycle
from verify_tcu_request_admission import paired_snapshot


TIMERS=[0x8159,0x815A,0x815B]


def class_flags(klass):
    return {255:1,0:2,1:128,2:64,3:32,4:16,5:8}.get(klass&255,4)


class ObservedLifecycle(ObservedLimit):
    def __init__(self):
        super().__init__()
        self.class_expected=self.timer_expected=None
        self.class_checks=self.timer_checks=0
    def instruction(self,pc):
        if pc==0x226CC:
            self.class_expected=class_flags(self.read(self.r[15]+12,1))
        elif pc==0x227D2:
            assert r(self,0x9315)==self.class_expected,(r(self,0x9315),self.class_expected)
            self.class_checks+=1;self.class_expected=None
        elif pc==0x11014:
            due=r(self,0x8494,4)%4==1
            self.timer_expected=[min(r(self,a)+int(due),255) for a in TIMERS]
        elif pc==0x11042:
            assert [r(self,a) for a in TIMERS]==self.timer_expected
            self.timer_checks+=1;self.timer_expected=None
        return super().instruction(pc)


def selector_sample(t,mask,adc=500):
    t.samples[0xFFFFF778]=(15^mask)<<2
    t.samples[0xFFFFF810]=t.samples[0xFFFFF812]=adc<<6
    for fn in [0x17250,0x174A0,0x17D60,0x22416]:t.run(fn)


def direct_cases():
    t=ObservedLifecycle();counts=dict(class_encoding=0,timer_steps=0,selector_transitions=0,adc_hold_recovery=0)
    for klass,old in itertools.product(range(256),[0,3,0xA5,255]):
        t.r[12]=1;t.r[13]=0;t.r[14]=0xFFFF9314
        t.write(t.r[15]+12,klass,1);w(t,0x9315,old)
        sp=t.r[15];t.stop_before=0x227D2
        try:t.run(0x226BC)
        except SegmentEnd:pass
        else:raise AssertionError('class segment did not stop')
        finally:t.stop_before=None
        assert t.r[15]==sp and r(t,0x9315)==class_flags(klass)
        counts['class_encoding']+=1
    for phase,first,second in itertools.product(range(16),[0,11,12,17,18,48,49,254,255],[0,254,255]):
        w(t,0x8494,phase,4);w(t,0x8498,0,4);w(t,0x849C,0,4)
        for a,value in zip(TIMERS,[first,second,255-first]):w(t,a,value)
        t.run(0x11014)
        counts['timer_steps']+=1
    base=full_fixture().ram
    for old,new in itertools.product(range(16),repeat=2):
        t=ObservedLifecycle();t.ram=dict(base)
        t.run(0x17230);t.run(0x17D54)
        selector_sample(t,old);selector_sample(t,old)
        for nth in [1,2]:
            for a,value in zip(PROGRESS,[12345,23456,3456]):w(t,a,value,2)
            for a,value in zip(RATES,[105,-256,105]):w(t,a,value,4)
            selector_sample(t,new)
            assert sum(r(t,0x88B4+i)<<i for i in range(4))==(old if nth==1 else new)
            assert r(t,0x9315)==class_flags(r(t,0x8080))
            t.run(0x32348)
            if r(t,0x8080) in [0,255]:
                assert all(r(t,a,2)==0 for a in PROGRESS)
                assert all(r(t,a,4)==0 for a in RATES)
            else:assert any(r(t,a,2)!=0 for a in PROGRESS)
        counts['selector_transitions']+=1
    # ADC rejection retains old selector/progress-reset class until two healthy
    # samples complete release; diagnostic fault promotion is outside this test.
    held=[]
    for old in [1,2,4]:
        t=ObservedLifecycle();t.ram=dict(base);t.run(0x17230);t.run(0x17D54)
        selector_sample(t,old);selector_sample(t,old)
        rows=[]
        for adc in [374,374,500,500]:
            for a in PROGRESS:w(t,a,12345,2)
            selector_sample(t,8,adc)
            t.run(0x32348)
            rows.append(dict(adc=adc,klass=r(t,0x8080),gate=r(t,0x9315),
                             progress=[r(t,a,2) for a in PROGRESS]))
        assert [x['klass'] for x in rows]==([255]*3+[6] if old==2 else [0]*3+[6])
        assert all(x['progress']==[0,0,0] for x in rows[:3])
        assert any(rows[-1]['progress'])
        held.append(dict(old_mask=old,new_mask=8,rows=rows));counts['adc_hold_recovery']+=1
    return counts,held

def retained(primary,enabled=0,changes=None,t=None,comparison_update=None,transition_checks=None):
    """Run the shared pipeline; optional checks cover a different input profile.

    Independent instruction observers always validate producers and consumers.
    The default additionally checks the original two-transition trace. Profiles
    with produced diagnostic faults may legitimately create other transitions.
    """
    t=ObservedLifecycle() if t is None else t
    rows=[];last=None;source_rows=[];input_rows=[]
    changes={} if changes is None else changes
    def prepare(t):
        initialize_segment(t)
        w(t,0x80E8,1000,2)
        can_inputs(t,primary)
        if comparison_update is not None:comparison_update(t,0)
        t.run(0x23544,limit=1000000)
    def upstream(t,call):
        if call==1:
            t.run(0x17230);t.run(0x17D54)
            w(t,0x921C,6500,4)
        if call in changes:
            input_rows.append(dict(call=call,primary=changes[call],can215=can_inputs(t,changes[call])))
        if comparison_update is not None:comparison_update(t,call)
        sample(t,enabled)
        t.run(0x32348,limit=1000000)
        t.run(0x44CFE,limit=1000000)
        selection_then_limit(t)
        if call in [1,2,79,80,81,99,100,101,130,150,162,163,169,170,171,200,320]:
            source_rows.append(dict(call=call,accepted=r(t,0x8081),code=r(t,0x9C87),
                operation=r(t,0x9C88),progress=[r(t,a,2) for a in PROGRESS],
                gate=r(t,0x9315),limit=r(t,0x939E,2),live_input=r(t,0x80F8,2),
                classification_limit=r(t,0x9C52,2),phase=r(t,0x95E1+15*r(t,0x96C4)),
                timers=[r(t,a) for a in [0x8159,0x815A,0x815B]]))
    def observe(t,call,subcall):
        nonlocal last
        head,count=r(t,0x96C4),r(t,0x96C5)
        state=dict(head=head,count=count,records=[dict(index=i,code=r(t,0x95DE+15*i),phase=r(t,0x95E1+15*i))
                         for i in [(head+j)%16 for j in range(count)]],source915a=r(t,0x915A,2),live_input=r(t,0x80F8,2),limit=r(t,0x939E,2))
        if state!=last:
            rows.append(dict(call=call,subcall=subcall,**state,**paired_snapshot(t)))
            last=state
    trace=lifecycle(25000,t=t,calls=320,samples={80:6500},prepare=prepare,
                    upstream=upstream,observe=observe,require_ascending=False)
    if transition_checks is None:
        assert t.creation_calls==[[1,0,0],[6,8,0]]
        assert [code for _,code in t.retired]==[1]*3+[6]*3
        assert [(x['call'],x['records'][0]['phase'] if x['records'] else None)
                for x in rows if x['call'] in [1,80,130,162]]==[(1,0),(80,1),(130,2),(162,None)]
        assert all(x['at_correction']==0 and x['tcu_source915a']==32767 for x in rows)
    else:
        transition_checks(t,rows)
    assert t.progress_checks==t.class_checks==t.timer_checks==320
    assert t.limit_checks==t.tail_checks==321
    if changes and comparison_update is None:
        by_call={x['call']:x for x in source_rows}
        assert by_call[100]['limit']==12736 and by_call[100]['live_input']==7984
        assert by_call[100]['classification_limit']==9600
        assert by_call[101]['classification_limit']==12736
        assert by_call[162]['live_input']==7984 and by_call[163]['live_input']==12736
        assert by_call[170]['limit']==by_call[170]['live_input']==7984
    return dict(primary=primary,input25=enabled,changed_inputs=input_rows,source_rows=source_rows,checkpoints=rows,
                legacy_record_trace=trace,creation_calls=t.creation_calls,retired=t.retired,
                classification_rows=t.classification_rows,group_calls=t.group_calls,
                limit_checks=t.limit_checks,tail_checks=t.tail_checks,progress_checks=t.progress_checks,
                class_checks=t.class_checks,timer_checks=t.timer_checks)


def main():
    counts,held=direct_cases();print('Direct cases:',counts,flush=True)
    traces=[]
    for primary,changes in [(25,None),(100,None),(25,{100:100,170:25})]:
        traces.append(retained(primary,changes=changes))
        print('Retained trace:',primary,changes,flush=True)
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),
                ecu_sha256=hashlib.sha256(ECU).hexdigest(),direct_cases=counts,
                adc_hold_recovery=held,retained_traces=traces)
    path='research/ecu-at-can/tcu-qualification-lifecycle-verification.json'
    with open(path,'w') as f:json.dump(result,f,indent=2);f.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
