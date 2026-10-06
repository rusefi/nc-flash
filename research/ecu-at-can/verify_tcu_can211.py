"""TCU CAN211 copy slice, dispatch and receipt monitoring with synthetic RAM.

The slice starts after hardware filter matching and ends before controller
acknowledgement. No full interrupt, peripheral, scheduler or vehicle is run.
Payload-read absence applies only to explicitly executed paths and states.
"""
import hashlib
import itertools
import json
from pathlib import Path

from disassemble import refs
from sh_subset import MASK, SH, signed

ROOT = Path(__file__).resolve().parents[2]
ROM = (ROOT / "examples/LFG1TF000.bin").read_bytes()
SHA = hashlib.sha256(ROM).hexdigest()
assert SHA == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
BUFFER = 0xFFFF8F34
PACKET = 0xFFFFB000


class AuditSH(SH):
    audit_payload = False

    def read(self, addr, size):
        if self.audit_payload and (addr & MASK) < BUFFER + 5 and (addr & MASK) + size > BUFFER:
            raise AssertionError(f"Unexpected payload read at PC {self.pc:08x}")
        return super().read(addr, size)


def w(t, addr, value, size=1):
    t.write(0xFFFF0000 + addr, value, size)


def r(t, addr, size=1):
    return t.read(0xFFFF0000 + addr, size)


def receive_slice(t, payload, dlc):
    """Enter with the matched hardware-filter index9 on the synthetic stack."""
    t.r[15] = 0xFFFED000
    t.write(t.r[15], 9, 1)
    t.r[12] = PACKET
    t.r[11] = PACKET + 0x20
    t.write(t.r[11], PACKET, 4)
    t.write(PACKET, dlc, 1)
    for i, byte in enumerate(payload):
        t.write(PACKET + 4 + i, byte, 1)
    t.pc = 0x1B630
    for _ in range(2000):
        if t.pc == 0x1B798:
            return
        nxt, delay = t.instruction(t.pc)
        if delay:
            _, nested = t.instruction(t.pc + 2)
            assert not nested
        t.pc = nxt
    raise AssertionError("Copy slice did not reach its boundary")


assert ROM[0x5C8D8 + 9] == 7
assert ROM[0x5C8E4 + 7] == 5
assert int.from_bytes(ROM[0x5C90C:0x5C910], "big") == BUFFER
assert ROM[0x5C920 + 7*4:0x5C920 + 8*4] == bytes(4)
assert ROM[0x1ACEC:0x1ACF0] == bytes.fromhex("000b0009")  # RTS; NOP

# Two bounded literal-reference searches, not a computed-pointer dataflow proof.
literal_scan = []
for target in range(BUFFER, BUFFER + 5):
    pools, long_users = refs(ROM, target)
    word_users = []
    for pc in range(0x10000, len(ROM) - 1, 2):
        opcode = int.from_bytes(ROM[pc:pc+2], "big")
        pool = pc + 4 + (opcode & 255)*2
        if opcode >> 12 == 9 and pool + 2 <= len(ROM):
            if signed(int.from_bytes(ROM[pool:pool+2], "big"), 16) & MASK == target:
                word_users.append(pc)
    assert not long_users and not word_users
    literal_scan.append({"target": hex(target), "aligned_long_pools": [hex(a) for a in pools],
                         "mov_l_users": long_users, "application_mov_w_users": word_users})

boundary_cases = 0
accepted_cases = 0
for mode, dlc, irq in itertools.product(range(16), range(9), [0, 5, 15]):
    t = AuditSH(ROM)
    t.sr = irq << 4
    w(t, 0x8F6C, mode)
    for i in range(-1, 9):
        t.write(BUFFER + i, 0xCC, 1)
    payload = bytes.fromhex("0123456789abcdef")
    receive_slice(t, payload, dlc)
    accepted = dlc >= 5 and bool(mode & 12)
    assert bytes(t.read(BUFFER+i, 1) for i in range(5)) == (payload[:5] if accepted else bytes([0xCC])*5)
    assert all(t.read(BUFFER+i, 1) == 0xCC for i in [-1, 5, 6, 7, 8])
    assert r(t, 0x8F4E) == (0x80 if accepted else 0)
    assert r(t, 0x8F71) == accepted
    assert t.sr & 0xF0 == irq << 4
    boundary_cases += 1
    accepted_cases += accepted

# Basis-bit and contrasting payloads: copy -> callback -> watchdog, expiry,
# recovery. Read audit runs only during the real dispatch/watchdog functions.
payloads = [bytes(8), bytes([255])*8, bytes.fromhex("a55a0123456789ab")]
payloads += [(1 << bit).to_bytes(8, "big") for bit in range(64)]
reference_states = None
for payload in payloads:
    t = AuditSH(ROM)
    w(t, 0x8F6C, 8)
    w(t, 0x868C, 1)
    for index in range(18):
        w(t, 0x8B38 + index*8, 100000, 4)
    states = []
    for now, fresh in [(100, True), (109, False), (110, False), (111, True)]:
        w(t, 0x84D0, now, 4)
        if fresh:
            receive_slice(t, payload, 8)
            t.audit_payload = True
            t.run(0x1BD10)
            assert 0x1C242 in t.visited and 0x1ACEC in t.visited
            assert r(t, 0x8F87) & 12 == 12 and r(t, 0x8F8D) & 12 == 12
            assert r(t, 0x8F4E) == 0 and r(t, 0x8F71) == 0
        t.audit_payload = True
        t.run(0x19AF0)
        t.audit_payload = False
        assert bytes(t.read(BUFFER+i, 1) for i in range(5)) == payload[:5]
        states.append({"tick": now, "received": fresh, "deadline": r(t, 0x8B48, 4),
                       "fault_bitmap": r(t, 0x8EE2, 2), "field_bits_8f87": r(t, 0x8F87)})
    assert [s["fault_bitmap"] for s in states] == [0, 0, 4, 0]
    assert [s["deadline"] for s in states] == [110, 110, 120, 121], states
    if reference_states is None:
        reference_states = states
    assert states == reference_states

print(json.dumps({"scope": __doc__.strip(), "rom_sha256": SHA,
                  "copy_slice": "0x1b630 through before 0x1b798; filter index9 already matched",
                  "mode_dlc_interrupt_mask_cases": boundary_cases,
                  "accepted_copy_cases": accepted_cases,
                  "payload_lifecycles": len(payloads), "audited_payload_reads": 0,
                  "lifecycle": reference_states, "literal_scan": literal_scan,
                  "limits": "No claim of global non-use: computed addresses, other tasks and untested states remain outside this audit."}, indent=2))
