"""CAN201 change -> stock TCU selection pipeline, with explicit task fixtures.

No instruction replacement. RAM fixtures do not establish physical gear state,
full scheduler order, or global absence of other flag writers.
"""
import itertools
import json
import random
from verify_can201_byte6 import SH, TCU, ecu_payload, receive, w, r


STAGES = [0x452DC, 0x44664, 0x466B8, 0x4662C, 0x46DB6, 0x46D34,
          0x46DE4, 0x46CC8, 0x46D30, 0x46A34, 0x46B00]


class AuditedSH(SH):
    """Observe original instructions; never intercept calls or change results."""
    def __init__(self):
        super().__init__(TCU)
        self.entries = []
        self.flag_writes = []
        self.floor_writes = []
        self.executing_pc = None

    def instruction(self, pc):
        self.executing_pc = pc
        if pc in STAGES:
            self.entries.append(pc)
        return super().instruction(pc)

    def write(self, addr, value, size):
        address = addr & 0xFFFFFFFF
        if address <= 0xFFFF92D5 < address+size and self.executing_pc is not None:
            self.flag_writes.append({'pc': hex(self.executing_pc), 'address': hex(address),
                                     'size': size, 'value': value & ((1 << (size*8))-1)})
        if self.executing_pc in [0x46D24, 0x46D28]:
            self.floor_writes.append({'pc': hex(self.executing_pc), 'value': value & 255})
        super().write(addr, value, size)


def selection(t, requested, previous, valid=1):
    for a, v in [(0xB600, requested), (0xB601, 9), (0x9B3C, previous), (0x8080, valid)]:
        w(t, a, v)
    t.r[5] = 0xFFFFB601
    t.run(0x452DC, 0xFFFFB600)
    assert t.entries == STAGES
    return [r(t, 0xB600), r(t, 0xB601)]


def main():
    assert TCU[0x5DEA0:0x5DEAC] == bytes.fromhex('00044664000466b80004662c')
    assert int.from_bytes(TCU[0x7744C:0x7744E], 'big') == 3
    assert TCU[0x77334:0x77337] == bytes(3)
    initialization_cases = 0
    rng = random.Random(21734)
    for before, pattern in itertools.product(range(256), range(2)):
        t = AuditedSH()
        inputs = [0]*4 if pattern == 0 else [rng.randrange(256) for _ in range(4)]
        w(t, 0x92D5, before)
        for a, v in zip([0xA57C, 0xA57D, 0xA57E, 0xA598], inputs):
            w(t, a, v)
        t.run(0x21734)
        expected = before & 0x88
        expected |= sum((1 << i) for i, value in enumerate(inputs[:3]) if value)
        expected |= (inputs[3] & 1) << 6
        assert r(t, 0x92D5) == expected, (before, inputs, expected, r(t, 0x92D5))
        assert any(row['pc'] == '0x21b18' for row in t.flag_writes)
        initialization_cases += 1

    preservation_cases = 0
    for before, group in itertools.product(range(256), [None, 0x35, 0x36, 0x3A, 0x3C, 0x3D]):
        t = SH(TCU)
        w(t, 0x92D5, before)
        if group is not None:
            w(t, 0xA6EC+group, 4)
        for fn in [0x570F6, 0x57258, 0x21C1C]:
            t.run(fn)
        assert r(t, 0x92D5) & 0x20 == before & 0x20
        preservation_cases += 1

    pipeline_cases = 0
    for delta, flag, previous, requested, valid in itertools.product(
            [-2560, -1, 0, 1, 2560], [0, 32], range(6), range(6), [1, 255]):
        t = AuditedSH()
        w(t, 0x92B8, delta, 2)
        w(t, 0x92D5, flag)
        override = delta < 0 and flag and valid != 255 and requested < previous
        result = selection(t, requested, previous, valid)
        assert result == ([previous, 255] if override else [requested, 9]), (
            delta, flag, previous, requested, valid, result)
        assert len(t.floor_writes) == (2 if override else 0)
        pipeline_cases += 1

    paired = []
    for source, preserve_injected_flag in itertools.product([45, 50, 55], range(2)):
        t = AuditedSH()
        for _ in range(5):
            receive(t, ecu_payload(50, 0, 0))
            t.run(0x21500)
        receive(t, ecu_payload(source, 0, 0))
        w(t, 0x92D5, 32)
        # Original task shows21C1C ->21734 before21500. Contrast deliberately
        # omitted21734 with the actual default-input update; never patch ROM.
        t.run(0x21C1C)
        if not preserve_injected_flag:
            t.run(0x21734)
        t.run(0x21500)
        assert r(t, 0x92B8, 2) == ((source-50)*256) & 65535
        t.entries.clear()
        result = selection(t, 0, 3)
        override = source < 50 and preserve_injected_flag
        assert result == ([3, 255] if override else [0, 9])
        paired.append({'ecu_source': source, 'omitted_default_input_update': bool(preserve_injected_flag),
                       'flag20': bool(r(t, 0x92D5) & 32), 'signed_change': (source-50)*256,
                       'selection_pair': result, 'floor_writes': t.floor_writes})

    print(json.dumps({'scope': __doc__.strip(), 'default_input_cases': initialization_cases,
                      'diagnostic_preservation_cases': preservation_cases,
                      'pipeline_cases': pipeline_cases, 'executed_stage_order': [hex(a) for a in STAGES],
                      'paired_ecu_paths': paired,
                      'conclusion': '21734/21A16 clearsflag20;21C1C preservesit. Stock3-stage pipeline calls46CC8, whose floor requires flag20. Injected-path activation is not proof of normal activation.',
                      'limits': 'Other branch controls zero-initialized; source/selection physical identities, intervening writers and whole scheduler remain unproved.'}, indent=2))


if __name__ == '__main__':
    main()
