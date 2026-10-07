"""Bounded DMAOR: DME control, seeded error flags and read-one/write-zero clear.

No DMA transfers, new NMI/address-error events or channel state. Writes with
one in a status flag are rejected; their hardware behavior is not simulated.
"""


class Registers:
    ADDRESS=0xFFFFECB0

    def __init__(self,initial=0):
        if not 0<=initial<=7:raise ValueError('Unsupported DMAOR initial state')
        self.values={self.ADDRESS:initial}
        self.read_flags=0
        self.accesses=[]

    def read(self,address,size):
        if address!=self.ADDRESS or size!=2:raise ValueError('Unsupported DMAOR read')
        value=self.values[address];self.read_flags|=value&6
        self.accesses.append(['read',address,size,value])
        return value

    def write(self,address,value,size):
        if address!=self.ADDRESS or size!=2:raise ValueError('Unsupported DMAOR write')
        value&=65535
        if value&~1:raise ValueError('Unsupported DMAOR reserved/status-one write')
        self.values[address]=(self.values[address]&6&~self.read_flags)|(value&1)
        self.read_flags=0
        self.accesses.append(['write',address,size,value])
