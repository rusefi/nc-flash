"""Full ECU serial application service with independent receipt/feedback checks.

SCI1 reply bytes are synthetic. No remote firmware, physical timing or actuator.
"""
from fractions import Fraction
import hashlib
import itertools
import json
import random

from verify_control_serial import ControlSerial, framed, ECU, TCU, w, r, f, rf, protected, paired, publish, angle, selected
from verify_model_sources import rounded as q, number


class ControlApplication(ControlSerial):
    WIDTHS={**ControlSerial.WIDTHS,0xFFFFF754:2,0xFFFFF75E:2}
    def write(self,a,v,size):
        if a & 0xFFFFFFFF == 0xFFFFF75E:
            raise ValueError('Application pin sample is read-only')
        super().write(a,v,size)


def fixture():
    e=ControlApplication()
    w(e,0x9462,1)  # explicit local mode;6DF8=0 avoids separateC260 reset branch
    w(e,0x55EC,0x9001,2)
    return e


def payload(header=0x9001,complement=True,seed=1):
    rng=random.Random(seed)
    p=bytearray(rng.randrange(256) for _ in range(38))
    p[:2]=header.to_bytes(2,'big')
    p[2:4]=((~header & 65535) ^ (0 if complement else 1)).to_bytes(2,'big')
    return bytes(p)


def feedback_expected(e,p):
    word=lambda i:int.from_bytes(p[i:i+2],'big')
    a,b=q(word(8)*number(0x229B8)),q(word(10)*number(0x229B8))
    if r(e,0x55DF)==1:
        def convert(v,offset,scale):
            return max(0,q(q(q(q(v-offset)*scale)*125)/5))
        x,y=convert(a,number(0xBB1E4),number(0xBB1E8)),convert(b,number(0xBB1EC),number(0xBB1F0))
    else:x,y=q(word(4)*number(0x22C44)),q(word(6)*number(0x22C44))
    return {0x5534:x,0x5540:y,0x5544:a,0x5548:b,
            0x554C:q(word(12)*number(0x229B8)),0x5550:q(p[14]*number(0x22C58)),
            0x5554:q((p[15]-256 if p[15]>=128 else p[15])*number(0x22C64))}


def verify_numeric(e,want):
    assert all(rf(e,a)==v for a,v in want.items()),[(hex(a),rf(e,a),v) for a,v in want.items() if rf(e,a)!=v]
    bits=r(e,0x5534,4);cs=~((bits>>16)+(bits&65535)) & 65535
    assert r(e,0x5538,2)==r(e,0x553A,2)==cs


def appcheck(e,p,status,inject=True):
    header=int.from_bytes(p[:2],'big')
    complement=int.from_bytes(p[2:4],'big')==(header^65535)
    accepted=status==1 and complement
    decoded=accepted and (header==0x8000 or 0x9001<=header<=0x9080)
    oldraw=bytes(r(e,0x55B8+i) for i in range(38))
    oldnumeric={a:rf(e,a) for a in feedback_expected(e,p)}
    want=feedback_expected(e,p) if decoded else oldnumeric
    oldseq=r(e,0x55EC,2);counter=r(e,0x55E7)
    pin=bool(e.registers[0xFFFFF75E]&4)
    newcounter=min(255,counter+1) if pin else 0
    send=status in [1,2] or newcounter>ECU[0xB8100]
    if inject:
        w(e,0x43A7,status)
        for i,v in enumerate(p):w(e,0x4352+i,v)
    else:
        assert r(e,0x43A7)==status
        assert bytes(r(e,0x4352+i) for i in range(38))==p
    e.visited.clear();stack=e.r[15]
    e.run(0x22224,limit=100000)
    assert e.r[15]==stack and 0x2256A in e.visited
    assert (0x2291A in e.visited)==decoded and (0x23748 in e.visited)==accepted
    assert r(e,0x5578)==int(decoded)
    raw=p if accepted else p[:4]+oldraw[4:] if status==1 else oldraw
    assert bytes(r(e,0x55B8+i) for i in range(38))==raw
    # Invalid replies hold numeric feedback; protectedchecksum checked onlywhenwritten.
    if decoded:verify_numeric(e,want)
    else:assert all(rf(e,a)==v for a,v in want.items())
    assert r(e,0x55E7)==newcounter and (0xC350 in e.visited)==send
    assert r(e,0x43A7)==0
    if send:
        expectedheader=0x8000 if pin else oldseq
        assert r(e,0x437A,2)==expectedheader and r(e,0x437C,2)==expectedheader^65535
        assert r(e,0x43A9)==1
        assert bytes(r(e,0x437A+i) for i in range(38))==bytes(r(e,0x5592+i) for i in range(38))
    assert r(e,0x55EC,2)==(oldseq if not send or pin else 0x9001 if oldseq>=0x9034 else oldseq+1)
    if accepted and 0x9001<=header<=0x9080:
        assert bytes(r(e,0xBB70+8*(header-0x9001)+i) for i in range(8))==p[30:38]
    return dict(status=status,header=hex(header),complement=complement,decoded=decoded,
                sent=send,next_sequence=hex(r(e,0x55EC,2)),feedback=float(rf(e,0x5534)))


def monitorcheck(e):
    reset,good,gate=r(e,0x9462),r(e,0x5578),r(e,0x57CC)
    bad_count,good_count=r(e,0x57D2,2),r(e,0x57D0,2)
    fault,latch=r(e,0x20A8),r(e,0x57CD)
    loss_threshold=int.from_bytes(ECU[0xE1004:0xE1006],'big')
    good_threshold=int.from_bytes(ECU[0xE1006:0xE1008],'big')
    if reset==1:
        bad_count=good_count=fault=latch=missing=0
    else:
        missing=int(not good)
        if gate!=1:bad_count=good_count=0
        elif not good:
            if bad_count>=loss_threshold:fault=1
            bad_count=min(65535,bad_count+1);good_count=0
        else:
            if good_count>=good_threshold:latch=1
            good_count=min(65535,good_count+1);bad_count=0
    e.run(0x285F0)
    assert (r(e,0x57D2,2),r(e,0x57D0,2),r(e,0x20A8),r(e,0x57CD),r(e,0x57CE))==(bad_count,good_count,fault,latch,missing)


def main():
    numeric=0
    for mode,seed in itertools.product([0,1,2],range(64)):
        e=fixture();p=payload(seed=seed);w(e,0x55DF,mode)
        for i,v in enumerate(p):w(e,0x55B8+i,v)
        want=feedback_expected(e,p);e.run(0x2291A,limit=50000);verify_numeric(e,want)
        assert r(e,0x5558)==p[16]
        numeric+=1
    filtering=0
    for mode,bit,old,previous,current in itertools.product([0,1,2],range(8),[0,1],[0,1],[0,1]):
        e=fixture();p=bytearray(payload());w(e,0x55DF,mode)
        before=[]
        for i in range(6):
            mask=1<<bit
            a=(0xA5&~mask)|(old<<bit);b=(0x5A&~mask)|(previous<<bit);c=(0x96&~mask)|(current<<bit)
            w(e,0x557E+i,a);w(e,0x55E0+i,b);p[17+i]=c
            want=c if mode==1 else sum((sum((v>>j)&1 for v in [a,b,c])>=2)<<j for j in range(8))
            before.append(want)
        for i,v in enumerate(p):w(e,0x55B8+i,v)
        e.run(0x2291A,limit=50000)
        assert [r(e,0x557E+i) for i in range(6)]==before
        assert [r(e,0x55E0+i) for i in range(6)]==list(p[17:23])
        filtering+=1
    headers=0
    for header,complement,status in itertools.product([0,0x7FFF,0x8000,0x8001,0x9000,*range(0x9001,0x9081),0x9081,0xFFFF],[False,True],[0,1,2]):
        e=fixture();f(e,0x5534,12);f(e,0x5540,34)
        appcheck(e,payload(header,complement),status);headers+=1
    scheduling=0
    for status,pin,counter,seq in itertools.product([0,1,2,3],[0,4],[0,1,2,254,255],[0x9001,0x9033,0x9034]):
        e=fixture();e.registers[0xFFFFF75E]=pin;w(e,0x55E7,counter);w(e,0x55EC,seq,2)
        appcheck(e,payload(),status);scheduling+=1
    monitor_cases=0
    for reset,good,gate,bad_count,good_count in itertools.product([0,1,2],[0,1,2],[0,1,2],[0,24,25,65535],[0,249,250,65535]):
        e=fixture()
        for a,v in [(0x9462,reset),(0x5578,good),(0x57CC,gate),(0x57CD,0xA5),(0x20A8,monitor_cases%2)]:w(e,a,v)
        w(e,0x57D2,bad_count,2);w(e,0x57D0,good_count,2)
        monitorcheck(e);monitor_cases+=1
    # True transport -> fullapplication; no directcompletion injection afterbootstrap.
    e=fixture()
    for a,v in [(0x2114,10.5),(0x211C,11),(0x2124,100),(0x212C,12)]:protected(e,a,v)
    for a,v in [(0x6DC4,100),(0x6D40,20),(0x71D8,3),(0x71D0,4),(0x71C4,32),
                (0x7154,Fraction(1,2)),(0x6DB4,2000),(0x7E0C,40),(0x72F8,50)]:f(e,a,v)
    appcheck(e,payload(),2) # Bootstrap receiptfailure triggers firstrealstart.
    lifecycle=[]
    for i,(header,complement,bad,active) in enumerate([(0x9001,True,False,0),(0x9002,False,False,1),(0x9003,True,True,1),(0xFFFF,True,False,1),(0x9004,True,False,0)]):
        p=payload(header,complement,20+i);frame=framed(p)
        if bad:frame=frame[:-1]+bytes([frame[-1]^1])
        previous=rf(e,0x5534);base=len(e.tx);out=bytes(r(e,0x437A+j) for j in range(38))
        e.run(0xE86E)
        for v in frame:e.rdr=v;e.run(0xE86E)
        assert bytes(e.tx[base:])==framed(out)
        status=r(e,0x43A7);assert status==(2 if bad else 1)
        _,e=paired(3200,1600,10040,10060,active,e=e);w(e,0x718C,active)
        e.run(0xA477E,limit=100000);publish(e);angle(e);selected(e)
        # Observe original transport outputs without replacing status orpayload.
        assert bytes(r(e,0x4352+j) for j in range(38))==p
        result=appcheck(e,p,status,inject=False)
        if not result['decoded']:assert rf(e,0x5534)==previous
        result.update(active=active,command_word=r(e,0x437E,2))
        lifecycle.append(result)
    # Originaltransport creates valid-checksum/bad-header failures, thenrecovery.
    #57CC is explicitly held enabled; its upstreamproducer is notmodeled.
    loss=[]
    w(e,0x9462,0);w(e,0x57CC,1)
    for call in range(28):
        p=payload(0x9001,call==27,70+call)
        e.run(0xE86E)
        for v in framed(p):e.rdr=v;e.run(0xE86E)
        appcheck(e,p,r(e,0x43A7),inject=False)
        monitorcheck(e)
        assert r(e,0x20A8)==int(call>=25)
        loss.append(dict(call=call+1,decoded=r(e,0x5578),bad_count=r(e,0x57D2,2),fault=r(e,0x20A8)))
    assert r(e,0x57D2,2)==0 and r(e,0x20A8)==1 #onegoodreplydoesnotclearlatchedfault
    w(e,0x9462,1);monitorcheck(e);assert r(e,0x20A8)==0
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        numeric_cases=numeric,filter_cases=filtering,header_cases=headers,scheduling_cases=scheduling,monitor_cases=monitor_cases,lifecycle=lifecycle,loss_lifecycle=loss,
        limits='Full22224 executed with9462=0/1,6DF8=0 andsampledports. Decoder independentchecks covernamednumeric/filteroutputs,notallflags/faultreporting. Remote reply remains synthetic.'),indent=2))


if __name__=='__main__':main()
