"""Execute real integer packers/unpackers from the supplied ECU and TCU ROMs.

Run from any directory. Prints evidence JSON. Does not modify ROMs or access
CAN hardware. Physical units/control dynamics are NOT validated by this test.
"""
import hashlib
import json
import random
import struct
from pathlib import Path

from sh_subset import SH

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def u32(b, a):
    return struct.unpack_from(">I", b, a)[0]


def payload(cpu, addr, size=8):
    return bytes(cpu.read(addr + i, 1) for i in range(size))


def transfer(source, src, target, dst, size=8):
    for i in range(size):
        target.write(dst + i, source.read(src + i, 1), 1)


ecu_descriptors = []
for a in list(range(0x378CC, 0x3795C, 16)) + list(range(0x379CC, 0x37A4C, 16)):
    ecu_descriptors.append({"address": hex(a), "can_id": hex(u32(ECU, a)),
                            "direction": "RX" if ECU[a + 4] else "TX",
                            "mailbox": ECU[a + 5], "dlc": ECU[a + 6],
                            "buffer": hex(u32(ECU, a + 8))})
tcu_tx = []
for i in range(5):
    packed = TCU[0x5C864 + 2*i:0x5C866 + 2*i]
    tcu_tx.append({"index": i, "id_register_value": packed.hex(),
                   "can_id": hex(int.from_bytes(packed, "little") >> 5),
                   "dlc": TCU[0x5C86E + i], "buffer": hex(u32(TCU, 0x5C874 + 4*i))})
tcu_rx = []
for slot in range(12):
    index = TCU[0x5C8D8 + slot]
    tcu_rx.append({"filter_index": slot, "logical_index": index,
                   "can_id": hex(int.from_bytes(TCU[0x5C8C0+2*slot:0x5C8C2+2*slot], "little") >> 5),
                   "copied_bytes": TCU[0x5C8E4 + index],
                   "buffer": hex(u32(TCU, 0x5C8F0+4*index)),
                   "callback": hex(u32(TCU, 0x5C920+4*index))})
assert [x['can_id'] for x in tcu_tx] == ['0x7e9', '0x4c1', '0x231', '0x218', '0x216']

# Confirm the generic bitfield setter's MSB-relative bit numbering by running
# its machine code, including the subroutine's shift loops and delay slot.
bitfield_cases = 0
for initial in (0, 0x55, 0xAA, 255):
    for offset in range(8):
        for width in range(1, 9-offset):
            for value in (0, 1, 0x55, 0xFF):
                t = SH(TCU)
                t.write(0xFFFF8EF8, initial, 1)
                t.r[0], t.r[1], t.r[2] = value, (offset << 8) | width, 0xFFFF8EF8
                t.run(0x5AD7C)
                shift = 8-offset-width
                mask = ((1 << width)-1) << shift
                expected = (initial & ~mask) | ((value << shift) & mask)
                assert t.read(0xFFFF8EF8, 1) == expected
                bitfield_cases += 1

rng = random.Random(0x218)
words = [0, 1, 0x7FFF, 0x8000, 0xFFFE, 0xFFFF] + [rng.randrange(65536) for _ in range(58)]
counts = {"0x216": 0, "0x218": 0, "0x231": 0, "0x201": 0}
for value in words:
    t, e = SH(TCU), SH(ECU)
    fields = [(0x1C448, value), (0x1C476, value & 255),
              (0x1C50A, value & 1), (0x1C51C, value ^ 0xFFFF),
              (0x1C54C, value >> 8), (0x1C5B8, value & 1)]
    for func, arg in fields:
        t.run(func, arg)
    transfer(t, 0xFFFF8EF5, e, 0xFFFF6A68)
    e.run(0x35420)
    assert e.read(0xFFFF6A92, 2) == value
    assert e.read(0xFFFF6A96, 1) == value & 255
    assert e.read(0xFFFF6A97, 1) == (value & 1) << 7
    assert e.read(0xFFFF6A94, 2) == value ^ 0xFFFF
    assert e.read(0xFFFF6A98, 1) == value >> 8
    assert e.read(0xFFFF6A99, 1) == (value & 1) << 7
    counts['0x218'] += 1

    for func, arg in [(0x1C5CA, value), (0x1C624, value ^ 0xFFFF),
                      (0x1C654, value & 255), (0x1C666, value), (0x1C702, value & 1)]:
        t.run(func, arg)
    transfer(t, 0xFFFF8EFD, e, 0xFFFF6A40)
    e.run(0x35034)
    assert e.read(0xFFFF6A48, 2) == value
    assert e.read(0xFFFF6A4C, 2) == value ^ 0xFFFF
    assert e.read(0xFFFF6A58, 1) == value & 255
    assert e.read(0xFFFF6A50, 2) == value
    assert e.read(0xFFFF6A5A, 1) == (value & 1) << 7
    counts['0x216'] += 1

    for func, arg in [(0x1C2BA, value & 15), (0x1C2CC, (value >> 4) & 15),
                      (0x1C3AC, value & 1), (0x1C3BE, value)]:
        t.run(func, arg)
    transfer(t, 0xFFFF8EED, e, 0xFFFF6ABC)
    e.run(0x35BB8)
    assert e.read(0xFFFF6ADC, 1) == ((value & 15) | (((value >> 4) & 15) << 4))
    assert e.read(0xFFFF6ADD, 1) == (value & 1) << 7
    assert e.read(0xFFFF6ADA, 2) == value
    counts['0x231'] += 1

    # Reverse direction: execute ECU message assembler and TCU receiver getter.
    # Interrupt mask is initially high to take the real helper's simple path.
    e.sr = 0xF0
    e.write(0xFFFF734A, 0x80, 1)
    e.write(0xFFFF6B3C, value, 2)
    e.run(0x365D0)
    transfer(e, 0xFFFF6B2C, t, 0xFFFF8F39, 7)
    assert t.run(0x1C890) == value
    counts['0x201'] += 1

mode_examples = []
for mode in (0, 1, 16):
    t = SH(TCU)
    t.write(0xFFFF941C, 120, 2)
    t.write(0xFFFF80F2, 20*128, 2)
    t.write(0xFFFF8080, 6, 1)
    t.run(0x191F0, mode)
    data = payload(t, 0xFFFF8EF5)
    assert data.hex() == {0: '0fa04600ffff0000', 1: '0eb04600ffff0000', 16: 'ffffff80ffff0000'}[mode]
    mode_examples.append({"mode_argument": mode, "payload": data.hex(' '),
                          "first_field_decoded": int.from_bytes(data[:2], 'big')*0.05-200
                          if data[:2] != b'\xff\xff' else None})

# Complete 216 word producer, including the distinct FFFE/FFFF sentinels.
# The first source is a literal address FFFF915A, not GBR+BA.
word216_examples = []
for mode, first, second, expected in [
    (1, 3200, 6400, (612, 712)),
    (1, 0x7FFF, 0x7FFF, (0xFFFE, 0xFFFE)),
    (0, 3200, 6400, (0xFFFE, 0xFFFE)),
    (16, 3200, 6400, (0xFFFF, 0xFFFF)),
    (1, -32768, -16385, (0, 0)),
    (1, -32, -1, (511, 511)),
    (1, 32766, 0, (1535, 512)),
]:
    t = SH(TCU)
    t.write(0xFFFF915A, first, 2)
    t.write(0xFFFF80BC, second, 2)
    t.write(0xFFFF80BA, 9999, 2)  # decoy catches the previous source error
    t.run(0x18F10, mode)
    assert (t.read(0xFFFF8EFD, 2), t.read(0xFFFF8EFF, 2)) == expected
    word216_examples.append({"mode": mode, "first_source": first,
                             "second_source": second,
                             "first_four_payload_bytes": payload(t, 0xFFFF8EFD, 4).hex(' ')})

# Execute the application sender as well as the ECU's state decoder. These
# are synthetic internal states, not measured selector positions or gears.
state_examples = []
for state in range(6):
    t, e = SH(TCU), SH(ECU)
    t.write(0xFFFF8080, 6, 1)
    t.write(0xFFFF8081, state, 1)
    t.run(0x19414, 1)
    e.sr = 0xF0
    e.write(0xFFFF734A, 0x80, 1)
    e.write(0xFFFF734C, 1, 1)
    transfer(t, 0xFFFF8EED, e, 0xFFFF6ABC)
    e.run(0x35BB8)
    e.run(0x3585C)
    flags = [e.read(0xFFFF6ACB+i, 1) for i in range(6)]
    assert flags == [int(i == state) for i in range(6)]
    assert t.read(0xFFFF8EED, 1) >> 4 == state + 1
    state_examples.append({"tcu_internal_state": state,
                           "payload": payload(t, 0xFFFF8EED).hex(' '),
                           "ecu_flags_6acb_through_6ad0": flags})

decoder_cases = 0
for high in range(16):
    for low in range(16):
        e = SH(ECU)
        e.sr = 0xF0
        e.write(0xFFFF734C, 1, 1)
        e.write(0xFFFF6ADC, (high << 4) | low, 1)
        e.run(0x3585C)
        assert [e.read(0xFFFF6ACB+i, 1) for i in range(6)] == [int(high == i+1) for i in range(6)]
        assert [e.read(0xFFFF6AD1+i, 1) for i in range(7)] == [int(low == i) for i in range(7)]
        decoder_cases += 1

gate_cases = 0
for flags, config in [(0x40, 1), (0x80, 0), (0x80, 2)]:
    e = SH(ECU)
    e.sr = 0xF0
    e.write(0xFFFF734A, flags, 1)
    e.write(0xFFFF734C, config, 1)
    e.write(0xFFFF6ADC, 0x11, 1)
    for i in range(6):
        e.write(0xFFFF6ACB+i, 0x55, 1)
    e.run(0x3585C)
    assert [e.read(0xFFFF6ACB+i, 1) for i in range(6)] == [0x55]*6
    gate_cases += 1

print(json.dumps({"rom_sha256": {"ECU": hashlib.sha256(ECU).hexdigest(),
                                  "TCU": hashlib.sha256(TCU).hexdigest()},
                  "ecu_descriptors": ecu_descriptors, "tcu_tx": tcu_tx,
                  "tcu_rx": tcu_rx, "bitfield_machine_code_cases": bitfield_cases,
                  "paired_machine_code_cases": counts, "tcu_218_mode_examples": mode_examples,
                  "paired_231_application_state_examples": state_examples,
                  "ecu_231_nibble_decoder_cases": decoder_cases,
                  "ecu_231_inactive_gate_cases": gate_cases,
                  "tcu_216_word_producer_examples": word216_examples,
                  "scope": "Isolated integer machine code, synthetic RAM and direct payload transfer; no bus, timing, FPU, or vehicle simulation."}, indent=2))
