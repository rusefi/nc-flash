"""Original SCI1 command/reply state machine with bounded register samples.

No serial peer, clock or interrupt model. Each byte-ready call and RDR byte is
an explicit fixture. Peripheral status writes are logged, not treated as RAM.
"""
import hashlib
import itertools
import json
import random

from sh_control_float import SHControlFloat
from verify_throttle_candidate import ECU, TCU, f, rf, w, r, protected, angle, selected, pack
from verify_control_conversion import publish
from verify_numeric_arbitration import paired
from fractions import Fraction


class ControlSerial(SHControlFloat):
    WIDTHS = {**{0xFFFFF008+i:1 for i in range(7)}, 0xFFFFF746:2, 0xFFFFED1A:2}
    def __init__(self):
        super().__init__(ECU)
        self.sr=0xF0
        self.registers=dict.fromkeys(self.WIDTHS,0)
        self.ssr=0xC0
        self.rdr=None
        self.accesses=[]
        self.tx=[]
    def read(self,a,size):
        a &= 0xFFFFFFFF
        if a >= 0xFFFFE000:
            if self.WIDTHS.get(a)!=size:raise ValueError(f'Unsupported read {a:08X}/{size}')
            v=self.registers[a]
            if a==0xFFFFF00C:v=self.ssr
            if a==0xFFFFF00D:
                if self.rdr is None:raise ValueError('Missing explicit SCI1 RDR sample')
                v=self.rdr;self.rdr=None
            self.accesses.append(('read',a,v,size))
            return v
        return super().read(a,size)
    def write(self,a,v,size):
        a &= 0xFFFFFFFF
        if a>=0xFFFFE000:
            if self.WIDTHS.get(a)!=size or a==0xFFFFF00D:raise ValueError(f'Unsupported write {a:08X}/{size}')
            v &= (1<<(8*size))-1
            self.accesses.append(('write',a,v,size))
            if a!=0xFFFFF00C:self.registers[a]=v
            if a==0xFFFFF00B:self.tx.append(v)
            return
        super().write(a,v,size)


def framed(payload):
    assert len(payload)==38
    return payload+((0x5AA5-sum(payload)) & 65535).to_bytes(2,'big')


def start(e,payload):
    assert len(payload)==38
    for i,v in enumerate(payload):w(e,0x437A+i,v)
    before=len(e.tx)
    port=e.registers[0xFFFFF746]
    e.run(0xC00A)
    assert len(e.tx)==before
    assert r(e,0x43A9)==1 and all(r(e,a)==0 for a in [0x43A6,0x43A7,0x43A8])
    assert r(e,0x43A2,2)==r(e,0x43A4,2)==0
    assert e.registers[0xFFFFF746]==port & ~1
    assert e.registers[0xFFFFF00A] & 0xF4 == 0x30
    assert e.registers[0xFFFFED1A]==0xBF


def transfer(e,tx_payload,rx_frame,gaps=0):
    start(e,tx_payload)
    base=len(e.tx)
    e.run(0xE86E)
    assert r(e,0x43A6)==1 and e.tx[base:]==list(tx_payload[:1])
    for i,v in enumerate(rx_frame):
        for _ in range(gaps):e.run(0xBF38)
        assert r(e,0x43A9)==1
        e.rdr=v
        e.run(0xE86E)
        assert e.rdr is None
        assert r(e,0x43A6)==i+2
    assert len(rx_frame)==40
    assert bytes(e.tx[base:])==framed(tx_payload)
    assert bytes(r(e,0x4352+i) for i in range(40))==rx_frame
    for i in range(19):
        e.run(0xC200,i)
        assert e.r[0] & 65535 == int.from_bytes(rx_frame[2*i:2*i+2],'big')
    assert 0xE86E in e.visited and e.registers[0xFFFFED1A]==0xBF
    valid=((sum(rx_frame[:38])+int.from_bytes(rx_frame[38:],'big')) & 65535)==0x5AA5
    assert r(e,0x43A9)==0 and r(e,0x43A7)==(1 if valid else 2)
    assert e.registers[0xFFFFF746]&1
    assert r(e,0x43A2,2)==sum(tx_payload) and r(e,0x43A4,2)==sum(rx_frame[:38])
    e.run(0xC20A)
    assert e.r[0] & 255 == (1 if valid else 2) and r(e,0x43A7)==0
    e.run(0xC20A)
    assert e.r[0]==0
    return valid


def main():
    init=0
    for v in range(256):
        e=ControlSerial()
        for a in e.registers:e.registers[a]=v
        before=e.registers.copy()
        e.run(0xBE92)
        assert e.registers[0xFFFFF008]==0x80 and e.registers[0xFFFFF009]==4
        assert e.registers[0xFFFFF00A]==v & 0xFC
        assert e.registers[0xFFFFF00E]==(0xF2 if v&8 else v)
        assert e.registers[0xFFFFF746]==before[0xFFFFF746]
        init+=1
    rng=random.Random(0xC350)
    exchanges=0
    for pattern,bad,gap in itertools.product(range(20),[False,True],[0,1,4]):
        tx=(bytes(38) if pattern==0 else bytes([255])*38 if pattern==1 else bytes(rng.randrange(256) for _ in range(38)))
        rx=framed(bytes(rng.randrange(256) for _ in range(38)))
        if bad:rx=rx[:-1]+bytes([rx[-1]^1])
        e=ControlSerial();e.registers[0xFFFFF746]=0xA55B
        assert transfer(e,tx,rx,gap)==(not bad)
        # Inactive callback cannot consume an RDR sample or write anotherbyte.
        n=len(e.tx);e.run(0xBFB4);assert len(e.tx)==n
        exchanges+=1
    timeout=[]
    for position in [0,1,20,39,40]:
        e=ControlSerial();tx=bytes(range(38));start(e,tx)
        for i in range(position):
            if i:e.rdr=i
            e.run(0xBFB4)
        for call in range(1,6):
            e.run(0xBF38)
            assert r(e,0x43A9)==int(call<5)
            assert r(e,0x43A7)==(0 if call<5 else 2)
            assert r(e,0x43A8)==min(call,4)
        assert e.registers[0xFFFFF746]&1
        # No partial reply accepted; a newstart resets sums,index,status.
        assert transfer(e,tx,framed(tx))
        timeout.append(dict(byte_callbacks=position,abort_service_call=5,recovery=True))
    monitor=0
    for enabled,old,threshold in itertools.product([0,1,2],[0,1,254,255],[0,1,254,255]):
        e=ControlSerial();w(e,0x43AB,enabled);w(e,0x43AA,old);w(e,0x4351,threshold)
        w(e,0x4350,0xA5);e.run(0xBF38)
        assert r(e,0x43AA)==(min(255,old+1) if enabled else old)
        # MOV.B sign extension affects the unsigned comparison of two bytes
        # equally; ordering remains their byte ordering.
        assert r(e,0x4350)==(1 if enabled and old>=threshold else 0xA5)
        monitor+=1
    rejections=0
    for op,a,size in [('r',0xFFFFF00A,2),('w',0xFFFFF00D,1),('r',0xFFFFF010,1),('r',0xFFFFF00D,1)]:
        e=ControlSerial()
        try:e.read(a,size) if op=='r' else e.write(a,0,size)
        except ValueError:rejections+=1
        else:raise AssertionError('Expected bounded-model rejection')
    paired_sequence=[]
    e=ControlSerial()
    for a,v in [(0x2114,10.5),(0x211C,11),(0x2124,100),(0x212C,12)]:protected(e,a,v)
    for a,v in [(0x6DC4,100),(0x6D40,20),(0x71D8,3),(0x71D0,4),(0x71C4,32),
                (0x7154,Fraction(1,2)),(0x6DB4,2000),(0x7E0C,40),(0x72F8,50)]:f(e,a,v)
    for active,bad in [(0,False),(1,False),(1,True),(1,False),(0,False)]:
        _,e=paired(3200,1600,10040,10060,active,e=e);w(e,0x718C,active)
        e.run(0xA477E,limit=100000);publish(e);angle(e);selected(e);word=pack(e)
        data=bytes(r(e,0x437A+i) for i in range(38))
        # Explicit arbitrary reply, NOT the missing physical controller's reply.
        reply=framed(bytes([0x55])*38)
        if bad:reply=reply[:-1]+bytes([reply[-1]^1])
        good=transfer(e,data,reply,1)
        paired_sequence.append(dict(active=active,word=word,tx_frame=framed(data).hex(),reply_valid=good))
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(),tcu_sha256=hashlib.sha256(TCU).hexdigest(),
        initialization_cases=init,exchange_cases=exchanges,monitor_cases=monitor,
        expected_rejections=rejections,timeout_recovery=timeout,paired_sequence=paired_sequence,
        limits='Sampled MMIO, explicit callbacks and arbitrary synthetic replies; no wire, interrupt timing or external receiver model.'),indent=2))


if __name__=='__main__':main()
