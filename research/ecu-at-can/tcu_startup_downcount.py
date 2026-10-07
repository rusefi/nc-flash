"""Bounded DSTR reads/zero writes with no counter or terminate events.

Compatible SH7055S section11.2.11: only ones writable; zeros do not clear
existing DST bits. Nonzero writes require DCNT/reload state and are rejected.
Initial values are explicit sampled inputs, not proof of full hardware reset.
"""


class Registers:
    ADDRESS=0xFFFFF666

    def __init__(self,initial=0):
        if not 0<=initial<=65535:raise ValueError('Unsupported DSTR initial state')
        self.values={self.ADDRESS:initial}
        self.accesses=[]

    def read(self,address,size):
        if address!=self.ADDRESS or size!=2:raise ValueError('Unsupported DSTR read')
        value=self.values[address]
        self.accesses.append(['read',address,size,value])
        return value

    def write(self,address,value,size):
        if address!=self.ADDRESS or size!=2:raise ValueError('Unsupported DSTR write')
        value&=65535
        if value:raise ValueError('DSTR start requires unprovided counter/reload state')
        self.accesses.append(['write',address,size,value])
