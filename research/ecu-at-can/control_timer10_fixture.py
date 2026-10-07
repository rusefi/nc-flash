"""Bounded TSR10/TIER10 latches, without events or interrupt delivery.

SH7058 REJ09B0046-0300H table11.3 (PDF259), section11.2.26 (PDF398..402).
TSR10 low4 flags clear on zero after a read; TIER10 low5 bits latch. No event
arrives between accesses in this fixture. Unsupported widths/reserved writes
are rejected, not treated as a claim about hardware exception behavior.
"""


class Timer10:
    def __init__(self,status=0,enable=0):
        assert 0<=status<16 and 0<=enable<32
        self.status=status;self.enable=enable;self.seen=0;self.accesses=[]
    def read(self,address,size):
        if size!=2 or address not in [0xFFFFF6E8,0xFFFFF6EA]:raise ValueError('Timer10 requires mapped word read')
        if address==0xFFFFF6E8:
            value=self.status;self.seen|=value
        else:value=self.enable
        self.accesses.append(['read',address,size,value]);return value
    def write(self,address,value,size):
        if size!=2 or address not in [0xFFFFF6E8,0xFFFFF6EA]:raise ValueError('Timer10 requires mapped word write')
        mask=15 if address==0xFFFFF6E8 else 31
        if value&~mask:raise ValueError('Timer10 reserved bit write outside fixture')
        if address==0xFFFFF6E8:
            cleared=self.seen&~value;self.status&=~cleared;self.seen&=~cleared
        else:self.enable=value
        self.accesses.append(['write',address,size,value])
