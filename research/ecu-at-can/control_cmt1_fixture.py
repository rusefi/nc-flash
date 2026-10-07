"""Bounded CMT1 configuration/status latches, without clock or interrupt events.

SH7058 manual14.2: reserved bits0; CMF clears only after read1/write0.
Initial register values explicit; only word accesses used by original startup.
"""
class Cmt1:
    def __init__(self):
        self.values={0xFFFFF710:0,0xFFFFF718:0,0xFFFFF71A:0,0xFFFFF71C:65535}
        self.seen_flag=False;self.accesses=[]
    def read(self,address,size):
        if address not in self.values or size!=2:raise ValueError('unsupported CMT1 word read')
        value=self.values[address]
        if address==0xFFFFF718 and value&128:self.seen_flag=True
        self.accesses.append(['read',address,size,value]);return value
    def write(self,address,value,size):
        if address not in self.values or size!=2:raise ValueError('unsupported CMT1 word write')
        value &= 65535
        if address==0xFFFFF710 and value&~3:raise ValueError('reserved CMSTR bits')
        if address==0xFFFFF718:
            if value&~0xC3:raise ValueError('reserved CMCSR1 bits')
            flag=self.values[address]&128
            if self.seen_flag and not value&128:flag=0;self.seen_flag=False
            self.values[address]=(value&0x43)|flag
        else:self.values[address]=value
        self.accesses.append(['write',address,size,value])
