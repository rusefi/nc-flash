"""Independent bit-string oracle for the isolated ROTL/ROTR interpreter."""
import itertools
import json
import random

from sh_rotate import SHRotate


def main():
    rng = random.Random(0x4404)
    values = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0xAAAAAAAA, 0x55555555]
    values += [1 << bit for bit in range(32)]
    values += [rng.randrange(1 << 32) for _ in range(64)]
    cases = 0
    for right, register, initial_t, value in itertools.product([False, True], range(16), [0, 1], values):
        opcode = (0x4005 if right else 0x4004) | register << 8
        t = SHRotate(opcode.to_bytes(2, 'big'))
        t.r = list(range(16))
        t.r[register] = value
        before = t.r[:]
        t.sr = 0x3F2 | initial_t
        bits = f'{value:032b}'
        expected_bits = bits[-1]+bits[:-1] if right else bits[1:]+bits[0]
        outgoing = int(bits[-1] if right else bits[0])
        assert t.instruction(0) == (2, False)
        before[register] = int(expected_bits, 2)
        assert t.r == before
        assert t.sr == 0x3F2 | outgoing
        cases += 1
    # RTS and BRAF delay slots execute the rotation once, preserving destination.
    t = SHRotate(bytes.fromhex('00 0b 40 04'))
    t.r[0] = 0x80000000
    assert t.run(0) == 1 and t.sr & 1
    t = SHRotate(bytes.fromhex('00 23 40 04 00 09 00 09 00 0b 00 09'))
    t.r[0] = 4
    assert t.run(0) == 8 and 8 in t.visited and 4 not in t.visited
    rejected = 0
    for opcode in [0xFFFF, 0x4006]:
        try:
            SHRotate(opcode.to_bytes(2, 'big')).instruction(0)
        except NotImplementedError:
            rejected += 1
    assert rejected == 2
    print(json.dumps({'bit_string_oracle_cases': cases, 'delay_programs': 2,
                      'unsupported_rejections': rejected, 'source': SHRotate.__module__}, indent=2))


if __name__ == '__main__':
    main()
