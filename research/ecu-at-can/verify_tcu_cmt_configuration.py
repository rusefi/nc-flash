"""Execute original CMT startup writes; infer relative periods conditionally.

Strict software register latches, not clock counting or interrupt delivery.
The manual describes compatible SH7055S registers, not identified board silicon.
"""
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice

ROOT = Path(__file__).resolve().parent
REGISTERS = tuple(range(0xFFFFF710, 0xFFFFF71E, 2))
WRITES = {
    0x14686: [(0xFFFFF710, 0)],
    0x1469A: [(0xFFFFF714, 0), (0xFFFFF71A, 0)],
    0x1468E: [(0xFFFFF712, 0x41), (0xFFFFF718, 0x41)],
}
ORDER = [0x14686, 0x1469A, 0x1468E]


class Registers:
    def __init__(self, seed):
        rng = random.Random(seed)
        self.values = {a: rng.randrange(65536) for a in REGISTERS}
        self.accesses = []

    def read(self, address, size):
        if address not in self.values or size != 2:
            raise ValueError('Unsupported CMT read')
        value = self.values[address]
        self.accesses.append(['read', address, size, value])
        return value

    def write(self, address, value, size):
        if address not in self.values or size != 2:
            raise ValueError('Unsupported CMT write')
        value &= 65535
        self.values[address] = value
        self.accesses.append(['write', address, size, value])


class Machine(SHRotate):
    def __init__(self, seed):
        super().__init__(TCU)
        self.io = Registers(seed)
        self.entries = []

    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.io.read(address, size)
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            return self.io.write(address, value, size)
        return super().write(address, value, size)

    def instruction(self, pc):
        if pc in ORDER:
            self.entries.append(pc)
        return super().instruction(pc)


def candidates():
    """Candidate aligned MOV.W literal users; not a complete dataflow search."""
    result = {}
    for value in [0xF710, 0xF712, 0xF718]:
        pools = {a for a in range(0, len(TCU)-1, 2)
                 if int.from_bytes(TCU[a:a+2], 'big') == value}
        users = []
        for pc in range(0, len(TCU)-1, 2):
            op = int.from_bytes(TCU[pc:pc+2], 'big')
            target = pc+4+2*(op & 255)
            if op >> 12 == 9 and target in pools:
                users.append([hex(pc), hex(target)])
        result[hex(value)] = dict(pools=list(map(hex, sorted(pools))), users=users)
    return result


def main():
    assert hashlib.sha256(TCU).hexdigest() == '8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6'
    counts = dict(component=0, caller_slice=0, compare_start_chain=0,
                  actual_start_caller_slice=0, rejected=0)
    examples = []
    for seed in range(32):
        for entry in ORDER + [None]:
            t = Machine(seed)
            for a in range(0x8000, 0x8020):
                w(t, a, (a*37+seed*19)&255)
            before = ram(t)
            expected = dict(t.io.values)
            order = ORDER if entry is None else [entry]
            trace = []
            for item in order:
                for a, value in WRITES[item]:
                    expected[a] = value
                    trace.append(['write', a, 2, value])
            sp, sr = t.r[15], t.sr
            if entry is None:
                execute_slice(t, 0x15608, 0x15614)
                counts['caller_slice'] += 1
            else:
                t.run(entry)
                counts['component'] += 1
            assert t.r[15] == sp and t.sr == sr
            assert ram(t) == before and t.entries == order
            assert t.io.values == expected and t.io.accesses == trace
            if entry is None:
                # Original compare/start leaves, in an explicitly supplied order.
                # This does not establish the full boot caller's start ordering.
                t.run(0x16D5C)
                t.run(0x16CE4)
                trace += [['write', 0xFFFFF716, 2, 624],
                          ['read', 0xFFFFF710, 2, 0], ['write', 0xFFFFF710, 2, 1],
                          ['write', 0xFFFFF71C, 2, 1279],
                          ['read', 0xFFFFF710, 2, 1], ['write', 0xFFFFF710, 2, 3]]
                expected.update({0xFFFFF716:624, 0xFFFFF71C:1279, 0xFFFFF710:3})
                assert t.io.values == expected and t.io.accesses == trace
                assert ram(t) == before
                counts['compare_start_chain'] += 1
                if seed == 0:
                    examples.append(dict(registers={hex(a):v for a,v in expected.items()}, accesses=trace))
        t = Machine(seed)
        execute_slice(t, 0x15608, 0x15614)
        t.io.accesses = []
        for a, size in [(0x8009,1),(0x800A,1),(0x84D0,4),(0x84D4,1),
                        (0x84D5,1),(0x84D6,1),(0x8494,4),(0x8498,4),(0x849C,4),
                        (0x91AC,2),(0x90C8,2)]:
            w(t,a,((seed+1)*0x1234567)&((1<<(8*size))-1),size)
        ref = SHRotate(TCU)
        ref.ram = dict(t.ram)
        for a, size in [(0x84D0,4),(0x84D4,1),(0x84D5,1),(0x84D6,1),
                        (0x8494,4),(0x8498,4),(0x849C,4)]:
            w(ref,a,0,size)
        w(ref,0x8009,1)
        w(ref,0x800A,1)
        sp, sr = t.r[15], t.sr
        execute_slice(t,0x11698,0x116A4)
        assert ram(t) == ram(ref) and t.r[15] == sp and t.sr == sr
        assert t.io.accesses == [['write',0xFFFFF716,2,624],
            ['read',0xFFFFF710,2,0],['write',0xFFFFF710,2,1],
            ['write',0xFFFFF71C,2,1279],['read',0xFFFFF710,2,1],
            ['write',0xFFFFF710,2,3]]
        assert t.io.values[0xFFFFF712] == t.io.values[0xFFFFF718] == 0x41
        counts['actual_start_caller_slice'] += 1
    for address, size in [(0xFFFFF712,1), (0xFFFFF718,4), (0xFFFFF71E,2)]:
        for writing in [False, True]:
            owner = Registers(0)
            try:
                if writing:
                    owner.write(address, 0, size)
                else:
                    owner.read(address, size)
            except ValueError:
                counts['rejected'] += 1
            else:
                raise AssertionError('Illegal access accepted')
    periods = [(624+1)*32, (1279+1)*32]
    ratio = Fraction(periods[1], periods[0])
    assert periods == [20000, 40960] and ratio == Fraction(256,125)
    pdf = ROOT/'sources/renesas-sh7055s-hardware-rej09b0045-0200h.pdf'
    result = dict(status='PASS', scope=__doc__, counts=counts, examples=examples,
        rom_sha256=hashlib.sha256(TCU).hexdigest(), candidate_literal_users=candidates(),
        source_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), source_pdf_pages_zero=[488,489,490,491,492],
        interpretation=dict(control=65, divider=32, interrupt_enabled=True,
            peripheral_clock_cycles_per_match=periods, cmt0_to_cmt1_event_rate=str(ratio),
            previous_supplied_ratio='100/8', same_as_previous_supplied_ratio=False),
        limits='Original15608..15614 configuration and11698..116A4 start caller slices; not full boot between them. Compatible manual conditional relative frequency, not measured periods, board silicon, start offset, interrupt acceptance or application-task cadence.')
    (ROOT/'tcu-cmt-configuration-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=counts,interpretation=result['interpretation']),indent=2))


if __name__ == '__main__':
    main()
