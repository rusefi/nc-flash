"""Bounded SYSCR2 access and an explicit SH7058 SDSR word sample.

SYSCR2: read F70B byte; write F70A word keyed3C; reserved bits rejected.
FPU-stop bit1 is sticky until a new machine/reset fixture. FPU operations
while stopped are rejected, not executed. No clock-rate, AUD, UBC, or TAP
simulation. SDSR 0B01 follows manual table19.2/TRST state, not measured hardware.
"""
from sh_control_initialize_dma import RamFillStartup, DMAOR, CONTROL


class SystemStartup(RamFillStartup):
    def __init__(self):
        super().__init__()
        self.syscr2 = 1
        self.sdsr_sample = 0x0B01

    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address in [0xFFFFF70A,0xFFFFF70B]:
            if address != 0xFFFFF70B or size != 1:
                raise ValueError('SYSCR2 requires byte read at F70B')
            value = self.syscr2
        elif 0xFFFFF7C2 <= address < 0xFFFFF7C4:
            if address != 0xFFFFF7C2 or size != 2:
                raise ValueError('Only SDSR word sample implemented')
            if self.syscr2 & 4:
                raise NotImplementedError('H-UDI access while module clock stopped')
            if self.sdsr_sample not in [0x0B00,0x0B01]:
                raise ValueError('SDSR sample outside documented SH7058 values')
            value = self.sdsr_sample
        else:
            return super().read(address,size)
        self.accesses.append(('read',address,value,size))
        return value

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address in [0xFFFFF70A,0xFFFFF70B]:
            if address != 0xFFFFF70A or size != 2:
                raise ValueError('SYSCR2 requires keyed word write at F70A')
            value &= 65535
            if value >> 8 != 0x3C or value & 0x70:
                raise ValueError('Unsupported SYSCR2 key or reserved bits')
            if (value ^ self.syscr2) & 128 and self.dma[DMAOR] & 1 and self.dma[CONTROL] & 3 == 1:
                raise NotImplementedError('Clock switching during enabled DMA not modeled')
            self.syscr2 = (value & 0x8F) | (self.syscr2 & 2)
            self.accesses.append(('write',address,value,size))
            return
        if 0xFFFFF7C2 <= address < 0xFFFFF7C4:
            raise NotImplementedError('SDSR writes/TAP state not modeled')
        return super().write(address,value,size)

    def instruction(self, pc):
        if self.syscr2 & 2 and self.read(pc,2) >> 12 == 15:
            raise NotImplementedError('FPU instruction while SYSCR2 stops FPU clock')
        return super().instruction(pc)
