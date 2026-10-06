"""TCU CAN201 copy and complete application dispatch with payload read audit.

Copy slice begins after filter matching and ends before controller ack.
Absence of speed-byte reads applies only to these executed callback paths.
No claim of global non-use, physical units, scheduler or hardware behavior.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_integer_arithmetic import SHIntegerArithmetic
from sh_subset import MASK

ROM = (Path(__file__).resolve().parents[2] / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ROM).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
BUFFER, PACKET = 0xFFFF8F39, 0xFFFFB000


class AuditedSH(SHIntegerArithmetic):
    def __init__(self, rom):
        super().__init__(rom)
        self.audit = False
        self.payload_reads = set()

    def read(self, address, size):
        address &= MASK
        if self.audit:
            for byte in range(address, address+size):
                if BUFFER <= byte < BUFFER+7:
                    self.payload_reads.add((self.pc, byte-BUFFER))
        return super().read(address, size)


def w(t, address, number, size=1):
    t.write(0xFFFF0000+address, number, size)


def r(t, address, size=1):
    return t.read(0xFFFF0000+address, size)


def copy_slice(t, payload, dlc):
    t.r[15] = 0xFFFED000
    t.write(t.r[15], 10, 1)
    t.r[12], t.r[11] = PACKET, PACKET+0x20
    t.write(t.r[11], PACKET, 4)
    t.write(PACKET, dlc, 1)
    for i, byte in enumerate(payload):
        t.write(PACKET+4+i, byte, 1)
    t.pc = 0x1B630
    for _ in range(2000):
        if t.pc == 0x1B798:
            return
        nxt, delay = t.instruction(t.pc)
        if delay:
            _, nested = t.instruction(t.pc+2)
            assert not nested
        t.pc = nxt
    raise AssertionError("Copy slice exceeded boundary")


assert int.from_bytes(ROM[0x5C8D4:0x5C8D6], "little") >> 5 == 0x201
assert ROM[0x5C8D8+10] == 8 and ROM[0x5C8E4+8] == 7
assert int.from_bytes(ROM[0x5C910:0x5C914], "big") == BUFFER
assert int.from_bytes(ROM[0x5CA30:0x5CA34], "big") == 0x1C264

copy_cases = accepted_cases = 0
for mode, dlc, irq in itertools.product(range(16), range(9), [0, 5, 15]):
    t = AuditedSH(ROM)
    w(t, 0x8F6C, mode)
    t.sr = irq << 4
    for i in range(-1, 9):
        t.write(BUFFER+i, 0xCC, 1)
    payload = bytes.fromhex("0123456789abcdef")
    copy_slice(t, payload, dlc)
    accepted = dlc >= 7 and bool(mode & 12)
    assert bytes(t.read(BUFFER+i, 1) for i in range(7)) == (payload[:7] if accepted else bytes([0xCC])*7)
    assert all(t.read(BUFFER+i, 1) == 0xCC for i in [-1, 7, 8])
    assert r(t, 0x8F4F) == accepted and r(t, 0x8F71) == accepted
    assert t.sr & 0xF0 == irq << 4
    copy_cases += 1
    accepted_cases += accepted

dispatch_cases = 0
reads = set()
# Vary all unconsumed payload bits, plus first-word and byte6 sentinels.
middle_values = [0, 0xFFFFFFFF, 0x12345678] + [1 << bit for bit in range(32)]
for word0, byte6, middle in itertools.product([0, 1, 3, 4, 12345, 65534, 65535], [0, 1, 24, 254, 255], middle_values):
    t = AuditedSH(ROM)
    w(t, 0x8F6C, 8)
    w(t, 0x8814, 1234, 2)
    w(t, 0x8808, 4321, 2)
    payload = word0.to_bytes(2, "big")+middle.to_bytes(4, "big")+bytes([byte6, 0xA5])
    copy_slice(t, payload, 8)
    t.audit = True
    t.run(0x1BD10)
    t.audit = False
    assert all(pc in t.visited for pc in [0x1C264, 0x1ACD8, 0x171CC, 0x17070, 0x18158])
    assert (r(t, 0x8814, 2), r(t, 0x8816)) == ((1234, 1) if word0 == 65535 else (word0//4, 2))
    assert (r(t, 0x8808, 2), r(t, 0x880A)) == ((4321, 1) if byte6 == 255 else (byte6*5, 2))
    assert (r(t, 0x89DC, 2), r(t, 0x89DE)) == (word0, 1 if word0 == 65535 else 2)
    assert r(t, 0x8F87) & 0x30 == 0x30 and r(t, 0x8F8D) & 0x30 == 0x30
    assert r(t, 0x8F4F) == r(t, 0x8F71) == 0
    assert {offset for _, offset in t.payload_reads} == {0, 1, 6}
    reads.update(t.payload_reads)
    dispatch_cases += 1

print(json.dumps({"scope": __doc__.strip(), "copy_mode_dlc_irq_cases": copy_cases,
                  "accepted_copy_cases": accepted_cases, "audited_dispatch_cases": dispatch_cases,
                  "payload_read_sites": [{"pc": hex(pc), "byte_offset": offset} for pc, offset in sorted(reads)],
                  "word0": "floor(raw/4);FFFF holds old numeric value, validity1; valid=2",
                  "byte6": "raw*5;FF holds old numeric value, validity1; valid=2",
                  "speed_bytes4_5_reads_in_audited_dispatch": 0,
                  "limits": "Full callback for listed fixtures only; other tasks/computed consumers and vehicle meaning remain open."}, indent=2))
