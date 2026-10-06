"""Independent MOVA/BRAF vectors and delay-slot execution for the TCU extension."""
import itertools
import json
from sh_relative_branch import SHRelativeBranch


def main():
    mova = 0
    for pc, disp, flag in itertools.product([0, 2], range(256), [0x3F0, 0x3F1]):
        t = SHRelativeBranch(bytes(pc)+(0xC700+disp).to_bytes(2, 'big'))
        t.sr = flag
        t.r = list(range(16))
        expected = t.r.copy()
        expected[0] = 4+disp*4
        assert t.instruction(pc) == (pc+2, False)
        assert t.r == expected and t.sr == flag
        mova += 1
    braf = 0
    for pc, n, value, flag in itertools.product([0, 0xFFFFD000], range(16),
                                               [0, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF], [0, 1]):
        op = 0x0023 | n << 8
        t = SHRelativeBranch(op.to_bytes(2, 'big'))
        if pc:
            t.write(pc, op, 2)
        t.r[n], t.sr = value, 0x3F0 | flag
        before = t.r.copy()
        assert t.instruction(pc) == ((pc+4+value) % (2**32), True)
        assert t.r == before and t.sr == 0x3F0 | flag and t.pr == 0xFFFFFFF0
        braf += 1
    # BRAF R2 captures displacement4, then the slot changes R2 to100.
    t = SHRelativeBranch(bytes.fromhex('0223e26400090009000b0009'))
    t.r[2] = 4
    t.run(0)
    assert t.r[2] == 100 and 8 in t.visited and 4 not in t.visited
    delay_cases = 1
    for target in [8, 10]:
        for disp in [0, 1, 255]:
            code = bytearray(bytes.fromhex('02230000000900090009000b0009'))
            code[2:4] = (0xC700+disp).to_bytes(2, 'big')
            code[target:target+4] = bytes.fromhex('000b0009')
            t = SHRelativeBranch(bytes(code));t.r[2] = target-4
            t.run(0)
            assert t.r[0] == (8 if target == 8 else 12)+disp*4
            delay_cases += 1
    # Branches in slots and unsupported PC-relative memory slots reject.
    rejections = 0
    for slot in [0x0023, 0x9000, 0xD000]:
        t = SHRelativeBranch(bytes.fromhex('0223')+slot.to_bytes(2, 'big')+bytes(16))
        t.r[2] = 4
        try:
            t.run(0)
        except ValueError:
            rejections += 1
        else:
            raise AssertionError('Expected rejection')
    print(json.dumps({'mova_cases': mova, 'braf_cases': braf, 'delay_cases': delay_cases,
                      'expected_rejections': rejections,
                      'reference': 'Renesas REJ09B0316-0200 sections7.2.8 and7.2.34',
                      'source': 'https://www.renesas.com/en/document/mah/sh-2e-software-manual'}, indent=2))


if __name__ == '__main__':
    main()
