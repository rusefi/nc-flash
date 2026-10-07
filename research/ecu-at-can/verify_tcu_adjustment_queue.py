"""Original queue creation/reset/phase progression and stored adjustment lifecycle.

62-function initialized fixture, explicit measured sources and service order.
No queue-phase injection in the coupled traces; no full boot/timebase claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
import verify_tcu_adjustment_lifecycle as life
import verify_tcu_adjustment_timers as timers
import verify_tcu_phase_retirement as retirement
import verify_tcu_ascending_phase as ascending
from verify_tcu_adjustment_lifecycle import TCU,w,r,signed
ROOT=Path(__file__).resolve().parent


def expected_reset(t,code):
    values={a:r(t,a) for a in timers.RESET_ADDRESSES}
    armed=r(t,0x95D0)
    if armed:
        group=TCU[0x5D446+(code&65535)]
        values[{0:0x8247,1:0x822C,2:0x822D,3:0x822F,4:0x8230}.get(group,0x8231)]=0
        if group==2 and (code&65535)==1:values[0x822E]=values[0x8160]=0
        if group==3 and (code&65535)==2:values[0x8161]=0
    return values,2 if armed else 0


class QueueTCU(retirement.RetirementTCU):
    def __init__(self):
        super().__init__();self.resets=[];self.pending_reset=None;self.pending_qualification=None;self.qualifications=0;self.pending_initial=None
    def instruction(self,pc):
        if pc==0x310F8:
            code=self.r[4]&65535
            self.pending_reset=(code,expected_reset(self,code))
        elif pc==0x31164:
            code,(values,flag)=self.pending_reset
            assert all(r(self,a)==v for a,v in values.items()) and r(self,0x95D0)==flag
            self.resets.append(dict(code=code,flag=flag,timers={hex(a):v for a,v in values.items()}));self.pending_reset=None
        if pc==0x317E4:self.pending_initial=ascending.initial_model(self,self.r[4]&65535)
        elif pc==0x31972:
            assert self.r[0]==self.pending_initial[0];self.pending_initial=None
        if pc==0x32614:
            index,code,operation=[self.r[i]&65535 for i in [4,5,6]]
            args=ascending.inputs(self,index,code,operation);self.pending_qualification=(index,ascending.model(*args))
        elif pc==0x327A0:
            index,want=self.pending_qualification
            assert (self.r[0],r(self,0x96CF+index),r(self,0x96DF+index),r(self,0x971A))==want
            self.pending_qualification=None;self.qualifications+=1
        return super().instruction(pc)


def setup(base):
    t=QueueTCU();t.ram=dict(base.ram);life.stored.initialize(t)
    for a,v in [(0x8080,4),(0x8081,1),(0x8084,1),(0x9C99,1),(0x9C00,2),(0x92D0,4),(0xA93A,1)]:w(t,a,v)
    for a,v in [(0x809C,23040),(0x80F2,32000),(0x80EA,1000),(0x80EE,15000),(0x80F6,4224)]:w(t,a,v,2)
    for a in [0x916F,0x9330,0x92D9,0x916C,0x9B40,0x9B3D,0x9BFC,0x9ACD,0x92D1,0x9CA4,0x9CA2,0x9C98,0x81EB,0x822C,0x822D,0x822F]:w(t,a,0)
    return t


def create(t,code,operation=0x17):
    for i,v in enumerate([code,operation,0]):w(t,0xA900+2*i,v,2)
    before=len(t.resets);t.r[5]=0xFFFFA900;t.run(0x31524,1,limit=1000000)
    assert len(t.resets)==before+1 and t.resets[-1]['code']==code
    assert r(t,0x8088)==2 and r(t,0x8089)==code
    assert t.pending_reset is None


def callback_cases(base):
    count=0
    for code,armed,seed in itertools.product(range(12),[0,1,2,255],[0,200,255]):
        t=setup(base);w(t,0x95D0,armed)
        for a in timers.RESET_ADDRESSES:w(t,a,seed)
        create(t,code);count+=1
    return count


def coupled(base,code,head,measurement):
    t=setup(base);w(t,0x96C4,head);w(t,0x80EE,measurement,2)
    for _ in range(122):t.run(0x110B4)
    assert r(t,0x81EB)==122
    create(t,code)
    timer=[0x822C,0x822D,0x822F][code]
    assert r(t,timer)==0 and r(t,0x81EB)==122
    first=life.execute(t);assert first['outcome']=='capture'
    captured=r(t,0x9CA0,2);w(t,0x80EA,captured+TCU[0x75E7F+code]*64,2)
    w(t,0x9218+4*TCU[0x5D446+code],measurement,4)
    index=head;rows=[dict(call=0,phase=r(t,0x95E1+15*index),**first)];complete=None
    for call in range(1,101):
        t.run(0x11014);t.r[5]=0;t.run(0x31524,2,limit=1000000)
        row=life.execute(t);phase=r(t,0x95E1+15*index)
        if row['outcome']!='hold' or call in [1,20,40,100]:rows.append(dict(call=call,phase=phase,**row))
        if row['outcome']=='complete':complete=call;assert row['update']['admitted'];break
    assert complete is not None,(code,head,measurement,rows)
    assert phase==1 and t.qualifications>0
    offsets=[signed(r(t,0x6176+2*i,2),16) for i in range(3)]
    # Original event3 accepts ten external group acknowledgements and retires
    # the real created record; these acknowledgements remain explicit inputs.
    for group in retirement.GROUPS:retirement.ack(t,index,group)
    assert r(t,0x96C5)==0 and r(t,0x8088)==1 and r(t,0x95D0)==1
    assert t.retired==[(fn,code) for fn in retirement.CALLBACKS]
    life.execute(t)
    create(t,code);assert r(t,timer)==0 and r(t,0x95D0)==2
    return dict(code=code,head=head,measurement=measurement,completion_call=complete,offsets=offsets,trace=rows,qualification_checks=t.qualifications,resets=t.resets,retirement_callbacks=t.retired)


def accepted_drop(base,active):
    t=setup(base)
    w(t,0x8081,2);w(t,0x8084,2)
    life.execute(t);assert r(t,0x9C99)==2 # Produce previousaccepted via original tail.
    for _ in range(130):t.run(0x110B4)
    create(t,0)
    if active:assert life.execute(t)['outcome']=='capture'
    w(t,0x8081,1);w(t,0x8084,1)
    row=life.execute(t)
    assert row['outcome']==('abort' if active else 'capture') and r(t,0x81EB)==0
    for _ in range(121):t.run(0x110B4)
    assert r(t,0x81EB)==121
    row2=life.execute(t)
    assert row2['outcome']=='hold'
    t.run(0x110B4);row3=life.execute(t)
    assert r(t,0x81EB)==122 and row3['outcome']=='hold'
    return dict(initially_active=active,drop=row,at121=row2,at122=row3,final_state=r(t,0x9C98))


def main():
    base=retirement.full_fixture();assert r(base,0x95D0)==1;cases=callback_cases(base);print('Callbacks',cases,flush=True)
    rows=[]
    for code,head,measurement in itertools.product(range(3),[0,15],[15000,17000]):
        row=coupled(base,code,head,measurement);rows.append(row);print('Coupled',code,head,measurement,row['completion_call'],flush=True)
    drops=[accepted_drop(base,x) for x in [False,True]]
    result=dict(scope=__doc__,tcu_sha256=hashlib.sha256(TCU).hexdigest(),callback_cases=cases,coupled=rows,accepted_drop=drops)
    (ROOT/'tcu-adjustment-queue-verification.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
