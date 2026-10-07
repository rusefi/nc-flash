"""Explicit HCAN samples for original receive ISR prefix and dispatcher.

The finite register read sequence is a fixture, not a controller simulation.
Execute1B438 through register restoration, stop at1B7D4 before RTE. No actual
interrupt admission, CAN wire delivery, overrun, concurrency or clock claim.
"""
import probe_tcu_captured_phase as phase
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w, r
from verify_tcu_base_publication import ram

SLOTS = {0: 2, 1: 3, 4: 6, 5: 7, 6: 8, 8: 10, 9: 11}
BUFFERS = {i: int.from_bytes(TCU[0x5C8F0+4*i:0x5C8F4+4*i], 'big') for i in SLOTS}
LENGTHS = {i: TCU[0x5C8E4+i] for i in SLOTS}
assert BUFFERS == {0: 0xFFFF8F05, 1: 0xFFFF8F0D, 4: 0xFFFF8F23,
                   5: 0xFFFF8F24, 6: 0xFFFF8F2C, 8: 0xFFFF8F39, 9: 0xFFFF8F40}
assert LENGTHS == {0: 8, 1: 7, 4: 1, 5: 8, 6: 8, 8: 7, 9: 7}
CALLBACKS = {i: int.from_bytes(TCU[0x5CA10+4*i:0x5CA14+4*i], 'big') for i in SLOTS}
for i, slot in SLOTS.items():
    assert TCU[0x5C8D8+slot] == i
    assert int.from_bytes(TCU[0x5C920+4*i:0x5C924+4*i], 'big') == 0


def observe_receive(self, pc):
    if self.rx_pending and self.rx_pending[-1]['return_pc'] == pc:
        row = self.rx_pending.pop()
        row['after'] = receive_state(self)
        self.rx_boundaries.append(row)
        if row['entry'] == '0x19af0':
            assert row['after']['deadlines'] == row['expected_deadlines']
            assert row['after']['faults'] == row['expected_faults']
            assert row['after']['fresh'] == row['expected_fresh']
    if pc in [0x1BD10, 0x19AF0]:
        row = dict(entry=hex(pc), return_pc=self.pr, before=receive_state(self))
        if pc == 0x19AF0:
            row.update(watchdog_model(self))
        self.rx_pending.append(row)
    if pc in CALLBACKS.values():
        self.rx_callbacks.append(hex(pc))


class ReceiveRegisters(phase.Observed):
    def read(self, address, size):
        if self.rx_registers is not None and 0xFFFFE400 <= address < 0xFFFFE600:
            key = (address, size)
            if key not in self.rx_registers:
                raise ValueError(f'Unprovided HCAN read {address:08X}/{size}')
            value = self.rx_registers[key]
            if isinstance(value, list):
                if not value:
                    raise ValueError(f'Exhausted HCAN samples {address:08X}/{size}')
                value = value.pop(0)
            self.rx_accesses.append(['read', address, size, value])
            return value
        return super().read(address, size)

    def write(self, address, value, size):
        if self.rx_registers is not None and 0xFFFFE400 <= address < 0xFFFFE600:
            if size != 2 or address not in [0xFFFFE40E, 0xFFFFE41A]:
                raise ValueError(f'Unprovided HCAN write {address:08X}/{size}')
            self.rx_accesses.append(['write', address, size, value & 65535])
            return
        return super().write(address, value, size)

    def instruction(self, pc):
        observe_receive(self, pc)
        return super().instruction(pc)


def fixture():
    t = phase.approach_fixture()
    t.__class__ = ReceiveRegisters
    t.rx_registers = None
    t.rx_accesses = []
    t.rx_callbacks = []
    t.rx_pending = []
    t.rx_boundaries = []
    return t


WATCHED = [(0, 46), (1, 44), (2, 43), (3, 31), (7, 24), (8, 23),
           (9, 22), (10, 18), (12, 6), (13, 0)]


def receive_state(t):
    return dict(mode=r(t, 0x8F6C), pending=r(t, 0x8F71),
                bitmap=[r(t, 0x8F4E+i) for i in range(2)],
                fresh=[r(t, 0x8F82+i) for i in range(6)],
                consumer_fresh=[r(t, 0x8F88+i) for i in range(6)],
                tick=r(t, 0x84D0, 4), recovery=r(t, 0x868C),
                deadlines=[r(t, 0x8B38+8*i, 4) for i in range(18)],
                faults=r(t, 0x8EE2, 2))


def watchdog_model(t):
    return watchdog_state_model(receive_state(t))


def watchdog_state_model(s):
    deadlines, faults, fresh = list(s['deadlines']), s['faults'], list(s['fresh'])
    if s['mode'] & 8:
        for index, field in WATCHED:
            offset, mask = TCU[0x5C9A0+field], TCU[0x5C9CF+field]
            received = bool(fresh[offset] & mask)
            expired = s['tick'] >= deadlines[index]
            fresh[offset] &= ~mask
            if received or expired:
                interval = int.from_bytes(TCU[0x5C618+28*index:0x5C61A+28*index], 'big')
                deadlines[index] = (s['tick']+interval) & 0xFFFFFFFF
            if received:
                if s['recovery']:
                    faults &= ~(1 << index)
            elif expired:
                faults |= 1 << index
    return dict(expected_deadlines=deadlines, expected_faults=faults, expected_fresh=fresh)


def receipt(t, index, payload, dlc=8):
    """One explicit mailbox sample; compare all application RAM at ISR exit."""
    assert index in SLOTS and len(payload) == 8 and 0 <= dlc <= 8
    slot = SLOTS[index]
    bit = 1 << ((slot+8) % 16)
    native_id = int.from_bytes(TCU[0x5C8C0+2*slot:0x5C8C2+2*slot], 'big')
    registers = {(0xFFFFE40E, 2): [bit, 0], (0xFFFFE41A, 2): 0,
                 (0xFFFFE420+8*slot, 1): dlc,
                 (0xFFFFE424+8*slot, 1): native_id >> 8,
                 (0xFFFFE425+8*slot, 1): native_id & 255}
    registers.update({(0xFFFFE4B0+8*slot+i, 1): v for i, v in enumerate(payload)})
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    w(ref, 0x8F48, 0xFFFF8F50, 4)
    for offset, value in [(0, dlc), (2, native_id >> 8), (3, native_id & 255),
                          *[(4+i, v) for i, v in enumerate(payload)]]:
        w(ref, 0x8F50+offset, value)
    admitted = dlc >= LENGTHS[index] and bool(r(t, 0x8F6C) & 12)
    if admitted:
        w(ref, 0x8F71, 1)
        for i, value in enumerate(payload[:LENGTHS[index]]):
            ref.write(BUFFERS[index]+i, value, 1)
        address = 0x8F4E+TCU[0x5C950+index]
        w(ref, address, r(ref, address) | TCU[0x5C95C+index])
    saved, pr, macl, mask = t.r.copy(), t.pr, t.macl, t.sr & ~0x301
    t.rx_registers, t.rx_accesses = registers, []
    pc = 0x1B438
    for _ in range(10000):
        if pc == 0x1B7D4:
            break
        nxt, delay = t.instruction(pc)
        if delay:
            _, nested = t.instruction(pc+2)
            assert not nested
        pc = nxt
    else:
        raise AssertionError('Receive ISR instruction bound')
    assert TCU[pc:pc+2] == bytes.fromhex('002b')
    assert t.r == saved and t.pr == pr and t.macl == macl and t.sr & ~0x301 == mask
    assert ram(t) == ram(ref), {hex(a): (ram(t).get(a, 0), ram(ref).get(a, 0))
                                for a in ram(t).keys() | ram(ref).keys()
                                if ram(t).get(a, 0) != ram(ref).get(a, 0)}
    assert registers[(0xFFFFE40E, 2)] == []
    assert [x for x in t.rx_accesses if x[0] == 'write'] == [
        ['write', 0xFFFFE40E, 2, bit], ['write', 0xFFFFE41A, 2, bit]]
    row = dict(index=index, mailbox=slot, dlc=dlc, payload=list(payload),
               admitted=admitted, accesses=t.rx_accesses, stopped_before_rte=hex(pc),
               whole_application_ram_checked=True)
    t.rx_registers = None
    return row
