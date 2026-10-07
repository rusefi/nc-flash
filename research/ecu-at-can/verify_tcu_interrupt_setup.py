"""Original TCU vector-base and INTC priority startup slices.

Local LDC register-form extension only; strict software INTC latches.
This does not deliver hardware interrupts, execute RTE or complete reset.
"""
import hashlib
import json
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT = Path(__file__).resolve().parent
PRIORITIES = [0,0,13,0x30,0xC00,0x2040,0x50C0,0xF00,0,0x980,6,0xA00]


class InterruptRegisters:
    def __init__(self, seed, *, nmi_level=None, irq_status=None):
        # Optional ICR fixture: constant externally supplied NMI pin level.
        # No IRQ/NMI arrivals or exception acceptance are simulated.
        self.values = {0xFFFFED00+2*i:(seed*1709+i*8191)&65535 for i in range(12)}
        if nmi_level is not None:
            if nmi_level not in (0,1):
                raise ValueError("NMI level must be0 or1")
            self.values[0xFFFFED18] = nmi_level << 15
        if irq_status is not None:
            if irq_status != 0:
                raise ValueError("Only explicit zero IRQ status is supported")
            self.values[0xFFFFED1A] = 0
        self.accesses = []

    def read(self, address, size):
        if address not in self.values or size != 2:
            raise ValueError('Unsupported INTC read')
        value = self.values[address]
        self.accesses.append(['read',address,size,value])
        return value

    def write(self, address, value, size):
        if address not in self.values or size != 2:
            raise ValueError('Unsupported INTC write')
        value &= 65535
        if address == 0xFFFFED18:
            if value & 0x7E00:
                raise ValueError("Reserved ICR bits must be zero")
            self.values[address] = (self.values[address] & 0x8000) | (value & 0x1FF)
        elif address == 0xFFFFED1A:
            # Bounded zero-status input: no pending flags/pin assertions.
            # Nonzero status and read-one/write-zero clearing remain outside.
            if value != 0:
                raise ValueError("Only zero IRQ-status command is supported")
        else:
            self.values[address] = value
        self.accesses.append(['write',address,size,value])


class Machine(SHRotate):
    def __init__(self, rom=TCU, seed=0):
        super().__init__(rom)
        self.vbr = 0xA55A0000
        self.intc = InterruptRegisters(seed)

    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.intc.read(address,size)
        return super().read(address,size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.intc.write(address,value,size)
        return super().write(address,value,size)

    def instruction(self, pc):
        opcode = self.read(pc,2)
        operation = opcode & 0xF0FF
        # Renesas SH-2E software manual section7.2.26: Rm -> GBR/VBR,
        # no condition-bit update. Existing shared interpreter is unchanged.
        if operation in (0x401E,0x402E):
            self._pending_slot = None
            self.visited.add(pc)
            value = self.r[(opcode>>8)&15] & 0xFFFFFFFF
            if operation == 0x401E:
                self.gbr = value
            else:
                self.vbr = value
            return pc+2,False
        return super().instruction(pc)


def main():
    rom_sha = hashlib.sha256(TCU).hexdigest()
    assert rom_sha == '8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    counts = dict(ldc_register_cases=0, boot_prefix_cases=0,
                  priority_leaf_cases=0, priority_caller_cases=0, rejected=0)
    for op in [0x401E,0x402E]:
        for n in range(16):
            for value in [0,1,0xFFFF,0x10000,0x7FFFFFFF,0x80000000,0xFFFFFFFE,0xFFFFFFFF]:
                for status in [0,0x3F1]:
                    t = Machine((op|(n<<8)).to_bytes(2,'big'))
                    t.r = [0x12345000+i for i in range(16)]
                    t.r[n] = value
                    t.sr = status
                    before = (t.r.copy(),t.sr,t.pr,t.macl,t.gbr,t.vbr,dict(t.ram))
                    assert t.instruction(0) == (2,False)
                    assert (t.r,t.sr,t.pr,t.macl,t.ram) == (before[0],before[1],before[2],before[3],before[6])
                    assert t.gbr == (value if op==0x401E else before[4])
                    assert t.vbr == (value if op==0x402E else before[5])
                    assert t.visited == {0} and not t.intc.accesses
                    counts['ldc_register_cases'] += 1
    assert int.from_bytes(TCU[0x76C84:0x76C88],'big') == 0xFFFF8000
    for status in range(0x400):
        # Only documented SR bits. The shared integer interpreter's LDC SR
        # does not mask reserved bits; do not claim those synthetic inputs.
        if status & ~0x3F3:
            continue
        t = Machine()
        t.sr = status
        t.pr = 0x12345678
        t.gbr = 0xAABBCCDD
        w(t,0x8000,status,2)
        before,sp = ram(t),t.r[15]
        execute_slice(t,0x10400,0x10416)
        assert t.vbr == 0x10000 and t.gbr == 0xFFFF8000
        assert t.sr == (status&~0xF0)|0xF0
        assert ram(t) == before and t.r[15] == sp-4
        assert t.read(sp-4,4) == 0x12345678 and t.pr == 0x12345678
        assert not t.intc.accesses
        counts['boot_prefix_cases'] += 1
    for seed in range(64):
        for caller in [False,True]:
            t = Machine(seed=seed)
            w(t,0x6000,seed,4)
            w(t,0x868C,0xA55A,2)
            t.sr = seed*13
            before = SHRotate(TCU)
            before.ram = dict(t.ram)
            sp,sr = t.r[15],t.sr
            if caller:
                w(before,0x868C,0,2)
                execute_slice(t,0x15574,0x1558C)
                assert t.r[15] == sp-12
                counts['priority_caller_cases'] += 1
            else:
                t.run(0x143DC)
                assert t.r[15] == sp
                counts['priority_leaf_cases'] += 1
            assert t.sr == sr and ram(t) == ram(before)
            assert t.intc.accesses == [['write',0xFFFFED00+2*i,2,v] for i,v in enumerate(PRIORITIES)]
            assert t.intc.values == {0xFFFFED00+2*i:v for i,v in enumerate(PRIORITIES)}
    for address,size in [(0xFFFFED12,1),(0xFFFFED12,4),(0xFFFFED18,2)]:
        for writing in [False,True]:
            owner = InterruptRegisters(0)
            try:
                if writing:
                    owner.write(address,0,size)
                else:
                    owner.read(address,size)
            except ValueError:
                counts['rejected'] += 1
            else:
                raise AssertionError('Unsupported access accepted')
    vectors = {188:0x16D6C,192:0x16CF4}
    for number,target in vectors.items():
        assert int.from_bytes(TCU[0x10000+4*number:0x10004+4*number],'big') == target
    result = dict(status='PASS',scope=__doc__,rom_sha256=rom_sha,counts=counts,
        configured_intc={hex(0xFFFFED00+2*i):v for i,v in enumerate(PRIORITIES)},
        vector_base=0x10000,vector_targets={str(k):hex(v) for k,v in vectors.items()},
        compatible_manual_priorities=dict(cmt0=9,cmt1=8),
        limits='Executed local boot/configuration prefixes, not reset-to-main reachability, unmasking, hardware exception acceptance, RTE, start offset or application-task cadence.')
    (ROOT/'tcu-interrupt-setup-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
