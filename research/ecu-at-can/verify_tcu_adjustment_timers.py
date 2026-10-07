"""TCU timer production and retained adjustment capture/abort observation.

Original110B4/1127E/11292 and12386 wheel, original49B08 lifecycle.
Explicit service-to-application ratios; no milliseconds/hardware timing claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
import verify_tcu_adjustment_lifecycle as life
from verify_tcu_adjustment_lifecycle import TCU,w,r,SHRotate
ROOT=Path(__file__).resolve().parent
BYTE_LO=int.from_bytes(TCU[0x76CCC:0x76CD0],'big')&65535
BYTE_HI=int.from_bytes(TCU[0x76CD0:0x76CD4],'big')&65535
WORD_LO=int.from_bytes(TCU[0x76CFC:0x76D00],'big')&65535
WORD_HI=int.from_bytes(TCU[0x76D00:0x76D04],'big')&65535
TIMERS=[0x81EB,0x822C,0x822D,0x822F]


def direct():
    counts=dict(byte=0,word=0,range=0,wheel=0)
    for value in range(256):
        t=SHRotate(TCU);w(t,0x81EB,value);sp=t.r[15];t.run(0x1127E,0xFFFF81EB)
        assert r(t,0x81EB)==min(255,value+1) and t.r[15]==sp;counts['byte']+=1
    for value in [0,1,127,128,32767,32768,65534,65535]:
        t=SHRotate(TCU);w(t,WORD_LO,value,2);sp=t.r[15];t.run(0x11292,0xFFFF0000+WORD_LO)
        assert r(t,WORD_LO,2)==min(65535,value+1) and t.r[15]==sp;counts['word']+=1
    for seed in [0,1,127,128,254,255]:
        t=SHRotate(TCU);before={a:(a+seed)&255 for a in range(BYTE_LO,BYTE_HI)}
        words={a:(a*17+seed)&65535 for a in range(WORD_LO,WORD_HI,2)}
        for a,v in before.items():w(t,a,v)
        for a,v in words.items():w(t,a,v,2)
        guards={BYTE_LO-1:93,BYTE_HI:94,WORD_LO-1:95,WORD_HI:96}
        for a,v in guards.items():w(t,a,v)
        sp=t.r[15];t.run(0x110B4)
        assert t.r[15]==sp
        assert all(r(t,a)==min(255,v+1) for a,v in before.items())
        assert all(r(t,a,2)==min(65535,v+1) for a,v in words.items())
        assert all(r(t,a)==v for a,v in guards.items());counts['range']+=1
    for phase in range(16):
        t=life.setup();t.run(0x11004);w(t,0x8494,phase,4);w(t,0x8009,1)
        for a in TIMERS:w(t,a,0)
        expect=0
        for tick in range(32):
            if (phase+tick)%16 in [3,11]:expect+=1
            t.run(0x12386)
            assert all(r(t,a)==expect for a in TIMERS)
            assert r(t,0x8494,4)==(phase+tick+1)%16;counts['wheel']+=1
    return counts


RESET_ADDRESSES=[0x8247,0x822C,0x822D,0x822E,0x8160,0x822F,0x8161,0x8230,0x8231]


def reset(t,code):
    armed=r(t,0x95D0);before={a:r(t,a) for a in RESET_ADDRESSES};want=before.copy()
    if armed:
        group=TCU[0x5D446+(code&65535)]
        address={0:0x8247,1:0x822C,2:0x822D,3:0x822F,4:0x8230}.get(group,0x8231)
        want[address]=0
        if group==2 and (code&65535)==1:want[0x822E]=want[0x8160]=0
        if group==3 and (code&65535)==2:want[0x8161]=0
    sp=t.r[15];t.run(0x310F8,code)
    assert all(r(t,a)==v for a,v in want.items()) and t.r[15]==sp
    assert r(t,0x95D0)==(2 if armed else 0)
    return [a for a in RESET_ADDRESSES if before[a]!=want[a]]


def reset_cases():
    count=0
    for code,armed,value in itertools.product([*range(11),0x10001],[0,1,2,255],[0,200,255]):
        t=SHRotate(TCU);w(t,0x95D0,armed)
        for a in RESET_ADDRESSES:w(t,a,value)
        reset(t,code);count+=1
    return count


def fixture(group,phase):
    t=life.setup(group);t.run(0x11004);w(t,0x8494,phase,4);w(t,0x8009,1);w(t,0x8088,0)
    for a in TIMERS:w(t,a,0)
    return t


def tick(t,expected):
    if r(t,0x8494,4) in [3,11]:expected=min(255,expected+1)
    t.run(0x12386)
    assert all(r(t,a)==expected for a in TIMERS)
    return expected


def timed(group,phase,interval,drop):
    t=fixture(group,phase);expected=0;capture_tick=None;drop_observation=None;trace=[];abort_tick=None
    for n in range(1,1801):
        expected=tick(t,expected)
        if expected>=122:w(t,0x8088,2 if expected<drop else 0)
        if n%interval:continue
        row=life.execute(t)
        if row['outcome']=='capture':
            assert expected>=122 and capture_tick is None;capture_tick=n
        if expected>=drop and drop_observation is None:drop_observation=(n,expected)
        if row['outcome']!='hold':trace.append(dict(tick=n,timer=expected,**row))
        if row['outcome']=='abort':abort_tick=n;break
        if expected>=190:break
    assert capture_tick is not None and drop_observation is not None
    should_abort=drop_observation[1]>=183
    assert (abort_tick is not None)==should_abort
    if should_abort:assert abort_tick==drop_observation[0] and r(t,0x9C98)==0
    else:assert r(t,0x9C98)==1 and r(t,0x9CA2)==0
    return dict(group=group,initial_phase=phase,service_interval=interval,queue_drop_timer=drop,
                capture_tick=capture_tick,drop_observation=list(drop_observation),abort_tick=abort_tick,
                final_timer=expected,final_state=r(t,0x9C98),trace=trace)


def early_pending():
    t=fixture(0,0);expected=0;rows=[]
    for n in range(1,1101):
        expected=tick(t,expected)
        if n==1:w(t,0x8088,2)
        if n==1050:w(t,0x8088,0)
        if n==1051:w(t,0x8088,2)
        row=life.execute(t)
        if n<=1050:assert row['state']==0
        if n==1051:assert row['outcome']=='capture' and expected>=122
        if n in [1,971,972,973,1049,1050,1051,1100]:rows.append(dict(tick=n,timer=expected,**row))
    return rows


def main():
    counts=direct();counts['reset']=reset_cases();print('Direct',counts,flush=True)
    rows=[]
    for group,phase,interval,drop in itertools.product([0,1,2],[0,15],[1,7,17],[182,183]):
        rows.append(timed(group,phase,interval,drop))
    early=early_pending()
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),counts=counts,
                byte_range=[BYTE_LO,BYTE_HI],word_range=[WORD_LO,WORD_HI],timed=rows,early_pending=early)
    (ROOT/'tcu-adjustment-timers-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Timed',len(rows),'aborts',sum(x['abort_tick'] is not None for x in rows),flush=True)
if __name__=='__main__':main()
