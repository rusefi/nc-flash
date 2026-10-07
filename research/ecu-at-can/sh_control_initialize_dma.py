"""Bounded channel0 RAM-fill DMA fixture, without CPU/bus timing simulation.

SH7058 REJ09B0046-0300H sections10.1.3,10.2,10.3: big-endian halfword
access, fixed source/incrementing destination, longword auto-request burst.
Other modes, channels, traps and zero-count maximum transfers are rejected.
An enabled burst completes before the next CPU instruction; progress=False
deliberately withholds service to test the original firmware wait.
"""
from probe_control_initialize_timer import TimerStartup

DMAOR, SAR, DAR, COUNT, CONTROL = 0xFFFFECB0, 0xFFFFECC0, 0xFFFFECC4, 0xFFFFECC8, 0xFFFFECCC


class RamFillStartup(TimerStartup):
    def __init__(self):
        super().__init__()
        self.dma = {DMAOR:0, SAR:0, DAR:0, COUNT:0, CONTROL:0}
        self.dma_observed = {DMAOR:0, CONTROL:0}
        self.dma_progress = True
        self.dma_transfers = []

    def _location(self, address, size):
        if address == DMAOR and size == 2:
            return DMAOR, 0, 0xFFFF
        for base in [SAR, DAR, COUNT, CONTROL]:
            if address == base and size == 4:
                return base, 0, 0xFFFFFFFF
            if address in (base, base+2) and size == 2:
                return base, (2-(address-base))*8, 0xFFFF
        raise ValueError(f'Unsupported DMA register access {address:08X}/{size}')

    def read(self, address, size):
        address &= 0xFFFFFFFF
        if DMAOR <= address < CONTROL+4:
            base, shift, mask = self._location(address,size)
            value = (self.dma[base] >> shift) & mask
            if base in self.dma_observed:
                self.dma_observed[base] |= self.dma[base] & (mask << shift) & (6 if base==DMAOR else 2)
            self.accesses.append(('read',address,value,size))
            return value
        return super().read(address,size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if not DMAOR <= address < CONTROL+4:
            return super().write(address,value,size)
        base, shift, mask = self._location(address,size)
        value &= mask
        old = self.dma[base]
        combined = (old & ~(mask << shift)) | value << shift
        allowed = {DMAOR:7, SAR:0xFFFFFFFF, DAR:0xFFFFFFFF, COUNT:0xFFFFFF, CONTROL:0x1F333F}[base]
        if combined & ~allowed:
            raise ValueError('Reserved DMA bits outside bounded fixture')
        if base in self.dma_observed:
            flags = 6 if base==DMAOR else 2
            if combined & flags & ~old:
                raise ValueError('Software cannot set DMA status flags')
            clearing = old & flags & ~combined
            if clearing & ~self.dma_observed[base]:
                raise ValueError('DMA status clear requires prior observed one')
            self.dma_observed[base] &= ~clearing
        self.dma[base] = combined
        self.accesses.append(('write',address,value,size))
        self._service()

    def _service(self):
        control = self.dma[CONTROL]
        if self.dma[DMAOR] != 1 or control & 3 != 1:
            return
        if control & ~3 != 0x1F0128:
            raise NotImplementedError('Only channel0 fixed-source longword auto-request burst supported')
        source, destination, count = self.dma[SAR], self.dma[DAR], self.dma[COUNT]
        if not 1 <= count <= 8192:
            raise NotImplementedError('DMA count outside bounded fixture; zero means 16777216')
        if source % 4 or destination % 4:
            raise NotImplementedError('DMA alignment/address-error handling not simulated')
        if not (0xFFFF0000 <= source <= 0xFFFFBFFC and 0xFFFF0000 <= destination and destination+4*count <= 0xFFFFC000):
            raise NotImplementedError('DMA transfer outside bounded application RAM')
        if not self.dma_progress:
            return
        # Burst transfer: re-read the fixed source each unit, including overlap.
        for _ in range(count):
            value = super().read(source,4)
            super().write(self.dma[DAR],value,4)
            self.dma[DAR] += 4
            self.dma[COUNT] -= 1
        self.dma[CONTROL] |= 2
        self.dma_transfers.append(dict(source=source,destination=destination,count=count,
                                      final_destination=self.dma[DAR],final_count=self.dma[COUNT]))
