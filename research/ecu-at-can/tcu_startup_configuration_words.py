"""Strict owner for explicitly selected fixed-width configuration latches.

No counters, pin outputs, interrupt requests or peripheral timing. Callers
provide documented masks and explicit starting values for their bounded scope.
"""


class ConfigurationWords:
    def __init__(self,initial,masks,*,size=2):
        assert size in (1,2)
        self.size=size
        assert initial.keys()==masks.keys()
        assert all(value>=0 and value & ~masks[a]==0 for a,value in initial.items())
        self.values=initial.copy()
        self.masks=masks.copy()
        self.accesses=[]

    def read(self,address,size):
        if size!=self.size or address not in self.values:
            raise ValueError('Unsupported configuration-word read')
        value=self.values[address]
        self.accesses.append(['read',address,size,value])
        return value

    def write(self,address,value,size):
        if size!=self.size or address not in self.values:
            raise ValueError('Unsupported configuration-word write')
        value &= (1 << (8*self.size))-1
        if value & ~self.masks[address]:
            raise ValueError('Reserved configuration bits must be zero')
        self.values[address]=value
        self.accesses.append(['write',address,size,value])
