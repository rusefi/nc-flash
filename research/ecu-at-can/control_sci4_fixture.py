"""Explicit SCI4 byte samples and configuration latches; no serial peer.

SH7058 manual table15.2 (PDF509): F020..F026. SSR reads use an explicit
constant sample and writes only log. Each RDR read consumes a supplied byte.
SDCR fixed bits follow the documented F2 reset pattern, DIR is bit3.
"""
from collections import deque


class Serial4:
    def __init__(self,status,received):
        assert 0<=status<=255 and all(0<=v<=255 for v in received)
        self.status=status;self.rx=deque(received);self.tx=[];self.accesses=[]
        self.config={0xFFFFF020:0,0xFFFFF021:255,0xFFFFF022:0,0xFFFFF023:255,0xFFFFF026:0xF2}
    def read(self,address,size):
        if size!=1 or not 0xFFFFF020<=address<=0xFFFFF026:raise ValueError('SCI4 fixture requires mapped byte read')
        if address==0xFFFFF024:value=self.status
        elif address==0xFFFFF025:
            if not self.rx:raise ValueError('SCI4 explicit receive samples exhausted')
            value=self.rx.popleft()
        else:value=self.config[address]
        self.accesses.append(['read',address,1,value]);return value
    def write(self,address,value,size):
        if size!=1 or not 0xFFFFF020<=address<=0xFFFFF026 or address==0xFFFFF025:
            raise ValueError('SCI4 fixture requires mapped writable byte')
        value &= 255
        self.accesses.append(['write',address,1,value])
        if address==0xFFFFF024:return
        self.config[address]=(value&8)|0xF2 if address==0xFFFFF026 else value
        if address==0xFFFFF023:self.tx.append(value)
