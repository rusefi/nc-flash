"""Independent full64bit multiply, MACH transfers, rotations and ROM2488 oracle."""
import itertools
import json
import random
from pathlib import Path
from sh_control_task import ControlTaskArithmetic

ROOT = Path(__file__).resolve().parent


def signed_bytes(value):
    return int.from_bytes(value.to_bytes(4, 'big'), 'big', signed=True)


def main():
    values = [0, 1, 2, 65535, 65536, 0x7FFFFFFF, 0x80000000, 0x80000001, 0xFFFFFFFE, 0xFFFFFFFF]
    counts = dict(subv=0, original_subtract=0, multiply=0, transfers=0, rotations=0, original_helper=0, fsts=0, peripheral_rejections=0)
    for a, b, n, m in itertools.product(values, values, [0, 4, 15], [0, 5, 15]):
        e = ControlTaskArithmetic(); e.rom = (0x300D | n << 8 | m << 4).to_bytes(2, 'big')
        e.r[n] = a; e.r[m] = b
        registers = e.r.copy(); sr = e.sr
        product = signed_bytes(registers[n]) * signed_bytes(registers[m])
        encoded = product.to_bytes(8, 'big', signed=True)
        assert e.instruction(0) == (2, False)
        assert e.mach.to_bytes(4, 'big') + e.macl.to_bytes(4, 'big') == encoded
        assert e.r == registers and e.sr == sr
        counts['multiply'] += 1
    for a, b, n, m, incoming in itertools.product(values, values, [0, 4, 15], [0, 5, 15], [0, 1]):
        e = ControlTaskArithmetic(); e.rom = (0x300B | n << 8 | m << 4).to_bytes(2, 'big')
        e.r[n] = a; e.r[m] = b; e.sr = 0x3F0 | incoming
        expected = e.r.copy()
        difference = signed_bytes(expected[n]) - signed_bytes(expected[m])
        expected[n] = difference % 2**32
        overflow = not -(2**31) <= difference < 2**31
        e.instruction(0)
        assert e.r == expected and e.sr == 0x3F0 | int(overflow)
        counts['subv'] += 1
    for a, b in itertools.product(values, values):
        e = ControlTaskArithmetic(); e.r[5] = b; before = e.r[8:16].copy()
        expected = max(-(2**31), min(2**31 - 1, signed_bytes(a) - signed_bytes(b))) & 0xFFFFFFFF
        assert e.run(0x2560, a) == expected
        assert e.r[8:16] == before
        counts['original_subtract'] += 1
    for value, n, store in itertools.product(values, [0, 1, 4, 15], [False, True]):
        e = ControlTaskArithmetic(); e.mach = value; e.r[n] = value ^ 0xFFFFFFFF
        e.macl = 0xDEADBEEF; sr = e.sr
        e.rom = ((0x000A if store else 0x400A) | n << 8).to_bytes(2, 'big')
        e.instruction(0)
        assert e.mach == (value if store else value ^ 0xFFFFFFFF)
        assert e.r[n] == (value if store else value ^ 0xFFFFFFFF)
        assert e.macl == 0xDEADBEEF and e.sr == sr
        counts['transfers'] += 1
    for value, n in itertools.product(values, [0, 1, 4, 15]):
        e = ControlTaskArithmetic(); e.r[n] = value; e.mach = 0x12345678
        e.rom = (0x401A | n << 8).to_bytes(2, 'big')
        e.instruction(0)
        assert e.macl == value and e.mach == 0x12345678 and e.sr == 0xF0
        counts['transfers'] += 1
    for value, incoming, opcode in itertools.product(values + [1 << bit for bit in range(32)], [0, 1], [0x4404, 0x4405, 0x4425]):
        e = ControlTaskArithmetic(); e.rom = opcode.to_bytes(2, 'big'); e.r[4] = value; e.sr |= incoming
        bits = f'{value:032b}'
        expected = bits[1:] + bits[0] if opcode == 0x4404 else (str(incoming) if opcode == 0x4425 else bits[-1]) + bits[:-1]
        outgoing = bits[0] if opcode == 0x4404 else bits[-1]
        e.instruction(0)
        assert e.r[4] == int(expected, 2) and e.sr == 0xF0 | int(outgoing)
        counts['rotations'] += 1
    for bits, n in itertools.product(values + [0x7FC00001, 0x7F800000, 0x80000000], range(16)):
        e = ControlTaskArithmetic(); e.fpul = bits; e.fr = list(range(16))
        expected = e.fr.copy(); expected[n] = bits
        e.rom = (0xF00D | n << 8).to_bytes(2, 'big')
        e.instruction(0)
        assert e.fr == expected and e.fpul == bits and e.sr == 0xF0
        counts['fsts'] += 1
    e = ControlTaskArithmetic(); e.registers[0xFFFFF74E] = 0xA55A
    assert e.read(0xFFFFF74E, 2) == 0xA55A
    e.write(0xFFFFF74E, 0x12345, 2)
    assert e.read(0xFFFFF74E, 2) == 0x2345
    for operation, address, size in [('read', 0xFFFFF74E, 1), ('write', 0xFFFFF74E, 1), ('read', 0xFFFFF750, 2)]:
        try:
            if operation == 'read': e.read(address, size)
            else: e.write(address, 0, size)
        except ValueError:
            counts['peripheral_rejections'] += 1
        else:
            raise AssertionError('Unexpected admitted peripheral access')
    for address in [0xFFFFF72C, 0xFFFFF76C, 0xFFFFF738, 0xFFFFF510, 0xFFFFF512, 0xFFFFF514, 0xFFFFF516]:
        e.write(address, 0x1A55A, 2)
        assert e.read(address, 2) == 0xA55A
        try: e.write(address, 0, 1)
        except ValueError: counts['peripheral_rejections'] += 1
        else: raise AssertionError('Incorrect peripheral width admitted')
    e.write(0xFFFFF430, 0x123456789, 4)
    assert e.read(0xFFFFF430, 4) == 0x23456789
    assert e.read(0xFFFFF430, 4) == 0x23456789  # frozen fixture
    for size in [1, 2]:
        for operation in ['read', 'write']:
            try:
                if operation == 'read': e.read(0xFFFFF430, size)
                else: e.write(0xFFFFF430, 0, size)
            except ValueError: counts['peripheral_rejections'] += 1
            else: raise AssertionError('Incorrect TCNT0 width admitted')
    e.write(0xFFFFF002, 0x1A5, 1)
    assert e.read(0xFFFFF002, 1) == 0xA5
    for operation in ['read', 'write']:
        try:
            if operation == 'read': e.read(0xFFFFF002, 2)
            else: e.write(0xFFFFF002, 0, 2)
        except ValueError: counts['peripheral_rejections'] += 1
        else: raise AssertionError('Incorrect SCR0 fixture width admitted')
    rng = random.Random(0x2488)
    pairs = list(itertools.product(values, repeat=2)) + [(rng.randrange(2**32), rng.randrange(2**32)) for _ in range(256)]
    for a, b in pairs:
        e = ControlTaskArithmetic(); e.r[5] = b
        e.mach = 0x12345678; e.macl = 0x87654321
        before = e.r[8:16].copy()
        quotient = (signed_bytes(a) * signed_bytes(b)) // 65536
        expected = max(-(2**31), min(2**31-1, quotient)) & 0xFFFFFFFF
        actual = e.run(0x2488, a)
        assert actual == expected, (a, b, actual, expected)
        assert (e.mach, e.macl) == (0x12345678, 0x87654321)
        assert e.r[8:16] == before and e.sr & ~1 == 0xF0
        counts['original_helper'] += 1
    (ROOT / 'control-task-arithmetic-verification.json').write_text(json.dumps(counts, indent=2) + '\n')
    print(counts)


if __name__ == '__main__':
    main()
