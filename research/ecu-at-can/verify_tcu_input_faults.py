"""Produced CAN201/CAN215 validity faults through all three TCU inputs.

Original encoder, receive, diagnostic and application routines execute.
Tick order, diagnostic admission and numeric ECU sources are fixtures.
Separate invalid flags model independent received-message histories; shared
invalidity is also covered. No physical time or whole-task claim.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from functools import lru_cache

from sh_exact_float import exact_bits
from sh_control_float import SHControlFloat
from verify_tcu_paired_input import ECU, TCU, w, r, ObservedPair
from verify_can215_feedback import receive as receive215
from verify_can201_byte6 import receive as receive201
from verify_tcu_qualification_lifecycle import retained


@lru_cache(None)
def packets(invalid201=False,invalid215=False,source215=60,primary=25):
    e=SHControlFloat(ECU)
    for a,v in [(0x6CF8,78),(0x6718,78),(0x6CD4,source215),(0x6DB4,4000),
                (0x71EC,primary),(0x71B4,30),(0x71C4,0)]:
        w(e,a,exact_bits(v),4)
    w(e,0x734A,0x80);w(e,0xA3A4,int(invalid201))
    for fn in [0x3663E,0x366EC,0x366D4,0x368A2,0x365D0]:e.run(fn)
    p201=bytes(r(e,0x6B2C+i) for i in range(8))
    # Different flags deliberately represent a change between publications,
    # not two independent A3A4 fields in one ECU at the same instant.
    w(e,0xA3A4,int(invalid215))
    e.run(0x369D6);e.run(0x36A28)
    p215=bytes(r(e,0x6B50+i) for i in range(8))
    assert p201[6]==(255 if invalid201 else 156)
    assert p215[6]==(255 if invalid215 else min(200,max(0,int(source215*2+Fraction(1,2)))))
    return p201,p215


def initial(recovery_gate=0):
    t=ObservedPair();t.run(0x5327C)
    for a,v,n in [(0xA936,1,1),(0xA939,1,1),(0x8464,200,2),
                  (0x868C,1,1),(0x80A4,recovery_gate,2)]:w(t,a,v,n)
    return t


def refresh(t,tick,p201,p215,unready=False):
    receive201(t,p201);receive215(t,p215)
    if unready:w(t,0x880E,3)  # Explicit dependency state, not an on-wire byte.
    w(t,0x84D0,tick,4)
    for fn in [0x583DC,0x56658,0x57F50,0x570F6,0x57258,0x21C1C,
               0x1ADD0,0x21500,0x22F3C]:t.run(fn,limit=1000000)


def step(t,tick,invalid201=False,invalid215=False,unready=False):
    refresh(t,tick,*packets(invalid201,invalid215),unready)
    fault=bool(r(t,0xA98D)&8 or r(t,0xA98F)&8)
    assert r(t,0x92D5)&0x88==(0x88 if fault else 0)
    assert r(t,0x8098,2)==(0 if fault else 19968)
    assert r(t,0x809A,2)==(25600 if fault else 15360)
    assert r(t,0x809C,2)==(3200 if fault else 19968)
    count=t.run(0x558CC,0xFFFFB000)
    t.run(0x5329A);t.run(0x19414,1)
    report=bytes(r(t,0xB000+i) for i in range(count*3)).hex(' ')
    assert not report and not r(t,0x8F04)&2 and not r(t,0x8EEE)&0x40
    return dict(tick=tick,invalid201=invalid201,invalid215=invalid215,unready=unready,
        validity=[r(t,0x880A),r(t,0x880E)],decoded=[r(t,0x8808,2),r(t,0x880C,2)],
        raw_groups=[r(t,0xA772),r(t,0xA773)],active_groups=[r(t,0xA728),r(t,0xA729)],
        deadlines=[r(t,0xA870,4),r(t,0xA874,4)],counts=[r(t,0xA91C,2),r(t,0xA91E,2)],
        mapped=[r(t,0xA97E),r(t,0xA97F)],aggregates=[r(t,0xA98D),r(t,0xA98F)],
        fault=fault,flags92d5=r(t,0x92D5),inputs=[r(t,a,2) for a in [0x8098,0x809A,0x809C]],
        statuses=[r(t,a) for a in [0xA4D6,0xA502,0xA4DA]],
        primary_fault_timer=r(t,0x82C4),stored_report=report)


def direct_cases():
    assert TCU[0x5EF48:0x5EF58].hex()=='000101f4000111000000000029002700'
    assert TCU[0x5F120:0x5F128].hex()=='2900010001f40001'
    count=0
    for status,admitted,dep35,dep36 in itertools.product(range(256),[0,1,2],[0,8],[0,8]):
        t=initial()
        for a,v in [(0x880E,status),(0xA939,admitted),(0xA977,dep35),(0xA978,dep36)]:w(t,a,v)
        t.run(0x583DC)
        enabled=admitted==1 and not dep35 and not dep36
        assert r(t,0xA773)==((3 if status==1 else 1) if enabled else 0)
        count+=1
    mapping=0
    for group,state in itertools.product(range(0x49),[0,2,4,16]):
        t=initial()
        receive201(t,packets()[0]);receive215(t,packets()[1])
        w(t,0xA6EC+group,state)
        for fn in [0x570F6,0x57258,0x21C1C,0x1ADD0,0x21500,0x22F3C]:t.run(fn,limit=1000000)
        fault=group in [0x35,0x36,0x3C,0x3D] and state in [2,4]
        assert r(t,0x92D5)&0x88==(0x88 if fault else 0)
        assert [r(t,a,2) for a in [0x8098,0x809A,0x809C]]==([0,25600,3200] if fault else [19968,15360,19968])
        mapping+=1
    return dict(group3d_producer=count,group_to_three_inputs=mapping)


def retained_profile(fault_enabled=True,t=None):
    t=ObservedPair() if t is None else t;rows=[]
    def update(t,call):
        t.application_call=call
        if call==0:
            t.run(0x5327C)
            for a,v,n in [(0xA936,1,1),(0xA939,1,1),(0x8464,200,2),(0x868C,1,1),(0x80A4,0,2)]:w(t,a,v,n)
        bad=fault_enabled and 100<=call<160
        primary=100 if 100<=call<170 else 25
        refresh(t,call*10,*packets(False,bad,Fraction(195,2),primary))
        assert r(t,0x880C,2)==975  # Invalid reception must hold the last real frame.
        t.run(0x516E6);t.run(0x216D8)
        if call in [0,99,100,149,150,151,159,160,162,163,170,209,210,211,212,320]:
            rows.append(dict(call=call,tick=call*10,active=r(t,0xA729),summary=r(t,0xA98F),
                flags=r(t,0x92D5),inputs=[r(t,a,2) for a in [0x8098,0x809A,0x809C]],
                history_change=r(t,0x933E,2)))
    def check_transitions(t,states):
        # Discovery profile: per-instruction source, classification, progress,
        # limit and paired input models remain active for every original call.
        # Ring output is recorded without assuming healthy-case phase dates.
        assert t.creation_calls[0]==[1,0,0]
        assert states[-1]['count']==0
        assert all(d['count']==len(d['records']) for d in states)
        assert all(0<=x['phase']<=3 and 0<=x['code']<12 for d in states for x in d['records'])
    # The hook owns every CAN215 update. Passing changes to the older helper
    # would first deliver its own valid byte6=0 frame and defeat invalid hold.
    trace=retained(25,t=t,comparison_update=update,transition_checks=check_transitions)
    assert t.primary_checks==t.comparison_checks==t.input_source_checks==321
    by_call={d['call']:d for d in rows}
    assert by_call[149]['flags']&0x88==0
    assert by_call[100]['inputs']==[19968,24960,19968]
    if fault_enabled:
        assert by_call[150]['inputs']==[0,25600,3200]
        assert by_call[210]['flags']&0x88==0x88 and by_call[211]['flags']&0x88==0
    else:
        assert all(d['flags']&0x88==0 for d in rows)
    result=dict(scope='Each manager call advances the supplied diagnostic tick by10; not a physical cadence.',
                fault_enabled=fault_enabled,rows=rows,trace=trace,primary_checks=t.primary_checks,
                comparison_checks=t.comparison_checks,source_checks=t.input_source_checks)
    verify_retained_result(result)
    return result


def verify_retained_result(result):
    """Preserve the observed profile sequence in addition to instruction oracles."""
    fault=result['fault_enabled'];trace=result['trace'];states=trace['checkpoints']
    expected=[(1,6,0),(80,6,1),(100,6,1),(130,6,2)]
    expected+=([(150,1,0),(170,1,0),(211,6,1),(261,6,2),(290,None,None)] if fault
               else [(162,None,None),(163,None,None),(170,None,None)])
    assert [(s['call'],s['records'][0]['code'] if s['records'] else None,
             s['records'][0]['phase'] if s['records'] else None) for s in states]==expected
    assert trace['creation_calls']==([[1,0,0],[6,8,0],[1,1,0],[6,8,0]] if fault else [[1,0,0],[6,8,0]])
    assert all(s['at_correction']==0 and s['tcu_source915a']==32767 for s in states)


def main():
    counts=direct_cases();print('Direct cases:',counts,flush=True)
    profiles=[]
    for bad201,bad215,gate in itertools.product([False,True],[False,True],[0,1]):
        if not (bad201 or bad215):continue
        t=initial(gate);rows=[]
        for tick in [0,100,599,600,601,1100,1101,1101,1102]:
            bad=100<=tick<=600
            d=step(t,tick,bad201 and bad,bad215 and bad)
            expected=tick>=600 and (tick<1101 or gate==1 or len(rows)==6)
            assert d['fault']==expected,(tick,d,expected)
            assert d['decoded']==[780,600]
            if tick in [100,599]:
                assert d['statuses']==[2 if bad201 else 1,2 if bad215 else 1,2 if bad201 else 1]
            if expected:assert d['statuses']==[4,4,4]
            rows.append(d)
        profiles.append(dict(invalid201=bad201,invalid215=bad215,recovery_gate=gate,rows=rows))
    # A switch between invalid sources preserves the shared application fault
    # while each group has its own qualification/recovery state and deadline.
    t=initial();switched=[]
    for tick,a,b in [(0,False,False),(100,False,True),(600,False,True),
                     (601,True,False),(1100,True,False),(1101,True,False),
                     (1101,True,False),(1102,False,False),(1602,False,False),(1602,False,False)]:
        switched.append(step(t,tick,a,b))
    assert [x['fault'] for x in switched]==[False,False,True,True,True,True,True,True,True,False]
    interrupted=[]
    for unready in [False,True]:
        t=initial();rows=[]
        for tick in [0,100,600,601,1100,1101,1601,1601]:
            bad=tick in [100,600] or (tick==1100 and not unready)
            rows.append(step(t,tick,False,bad,unready and tick==1100))
        assert [x['fault'] for x in rows]==[False,False,True,True,True,True,True,False]
        interrupted.append(dict(unready=unready,rows=rows))
    t=initial();qualification=[]
    for tick,bad in [(0,False),(100,True),(598,True),(599,False),(600,True),(1099,True),(1100,True)]:
        qualification.append(step(t,tick,False,bad))
    assert [x['fault'] for x in qualification]==[False]*6+[True]
    gates=[]
    for a in [0xA977,0xA978]:
        t=initial();rows=[]
        for tick,value in [(100,0),(599,8),(600,0),(1099,0),(1100,0)]:
            receive215(t,packets(False,True)[1]);w(t,0x84D0,tick,4);w(t,a,value)
            t.run(0x583DC);t.run(0x566E0,0x3D)
            assert r(t,0xA773)==(0 if value else 3)
            assert bool(r(t,0xA729)&4)==(tick==1100)
            if tick>=600:assert r(t,0xA874,4)==1100
            rows.append(dict(tick=tick,gate=value,raw=r(t,0xA773),active=r(t,0xA729),deadline=r(t,0xA874,4)))
        gates.append(dict(address=hex(a),rows=rows))
    result=dict(scope=__doc__,ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        direct_cases=counts,packets=[dict(invalid201=a,invalid215=b,can201=packets(a,b)[0].hex(' '),can215=packets(a,b)[1].hex(' '))
                                  for a,b in itertools.product([False,True],repeat=2)],
        profiles=profiles,switched_sources=switched,interrupted_recovery=interrupted,
        interrupted_qualification=qualification,dependency_gates=gates,
        retained_profile=retained_profile(),healthy_control=retained_profile(False))
    previous=json.load(open('research/ecu-at-can/tcu-qualification-lifecycle-verification.json'))
    assert json.loads(json.dumps(retained(25)))==previous['retained_traces'][0]
    result['default_lifecycle_regression']='320-call primary25 profile exactly matches prior saved JSON'
    path='research/ecu-at-can/tcu-input-faults-verification.json'
    with open(path,'w') as out:json.dump(result,out,indent=2);out.write('\n')
    print(path,flush=True)


if __name__=='__main__':main()
