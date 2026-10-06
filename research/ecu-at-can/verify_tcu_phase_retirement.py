"""Original phase acknowledgements, ring retirement and initialized-group CAN paths.

The larger fixture executes62 individual original initialization functions;
it is not a complete boot/peripheral model. Ring oracle inputs and measured
sources are explicit. No instruction or callback is stubbed.
"""
import hashlib
import itertools
import json
import random

from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_dispatch import fixture
from verify_tcu_request_admission import periodic, paired_snapshot

GROUPS = [5, 6, 0x20, 0xB, 2, 0x25, 0x14, 0x1A, 0x26, 0x29]
REQUIRED = set(range(1, 8))
CALLBACKS = [0x30B82, 0x30A9E, 0x31168]


class RetirementTCU(SHRotate):
    def __init__(self):
        super().__init__(TCU)
        self.acks = []
        self.retired = []

    def instruction(self, pc):
        if pc == 0x31C18:
            self.acks.append((self.r[4] & 255, self.r[5] & 65535))
        if pc in CALLBACKS:
            self.retired.append((pc, self.r[4] & 65535))
        return super().instruction(pc)


def full_fixture():
    t = RetirementTCU()
    t.ram = dict(fixture().ram)
    entries = [int.from_bytes(TCU[a:a+4], 'big') for a in range(0x1E2B4, 0x1E3AC, 4)]
    assert len(entries) == 62 and entries[:4] == [0x30A80, 0x30B20, 0x310F0, 0x31524]
    assert entries[-1] == 0x34290
    for fn in entries:
        t.r[5] = 0
        t.run(fn, 0, limit=1000000)
    return t


def ack(t, index, group):
    p = 0xFFFFA900
    t.write(p, group, 2)
    t.write(p+2, index, 1)
    t.r[5] = p
    t.run(0x31524, 3, limit=100000)


def seed(t, head, codes, state=3):
    t.run(0x31524, 0)
    w(t, 0x8088, 2)
    w(t, 0x96C4, head)
    w(t, 0x96C5, len(codes))
    w(t, 0x96C6, 7)
    for i, code in enumerate(codes):
        address = 0x95D4+15*((head+i) % 16)
        for j in range(15):
            w(t, address+j, 0)
        w(t, address+10, code)
        w(t, address+13, state)


def main():
    assert [int.from_bytes(TCU[0x5D3BC+4*i:0x5D3BE+4*i], 'big') for i in range(10)] == GROUPS
    bitmap_cases = 0
    for index, state, bitmap in itertools.product([0, 15], [0, 3], range(1024)):
        t = RetirementTCU()
        seed(t, index, [7], state)
        for j in range(10):
            w(t, 0x95D4+15*index+j, bool(bitmap & (1 << j)))
        ack(t, index, 0xFFFF)  # Unknown group does not add an acknowledgement.
        ready = all(bitmap & (1 << j) for j in REQUIRED)
        complete = bitmap == 1023
        assert r(t, 0x95E2+15*index) == int(ready)
        assert r(t, 0x96C5) == int(not complete)
        assert r(t, 0x96C4) == (index+int(complete)) % 16
        assert r(t, 0x8088) == (1 if complete else 2)
        assert r(t, 0x96C6) == (0 if complete else 7)
        assert t.retired == ([(fn, 7) for fn in CALLBACKS] if complete else [])
        bitmap_cases += 1

    rng = random.Random(0x31C18)
    stateful_acks = 0
    ring_cases = []
    for head, count in itertools.product([0, 7, 15], [1, 2, 3, 8, 16]):
        t = RetirementTCU()
        codes = [i % 12 for i in range(count)]
        seed(t, head, codes)
        active = [(head+i) % 16 for i in range(count)]
        by_index = {index: {'code': code, 'acks': set()} for index, code in zip(active, codes)}
        messages = [(index, group) for index in active for group in GROUPS]
        rng.shuffle(messages)
        messages += messages[:5]  # Duplicates arriving after idle must be ignored.
        expected_head = head
        retired_codes = []
        for index, group in messages:
            if active:
                by_index[index]['acks'].add(GROUPS.index(group))
                while active and len(by_index[active[0]]['acks']) == 10:
                    retired_codes.append(by_index[active.pop(0)]['code'])
                    expected_head = (expected_head+1) % 16
                while active and len(by_index[active[-1]]['acks']) == 10:
                    retired_codes.append(by_index[active.pop()]['code'])
            ack(t, index, group)
            assert r(t, 0x96C4) == expected_head
            assert r(t, 0x96C5) == len(active)
            assert r(t, 0x8088) == (2 if active else 1)
            assert t.retired == [(fn, code) for code in retired_codes for fn in CALLBACKS]
            stateful_acks += 1
        assert not active and len(retired_codes) == count
        ring_cases.append({'head': head, 'count': count, 'callback_code_order': retired_codes,
                           'final_head': expected_head})

    base = full_fixture()
    lifecycles = []
    paired_checks = 0
    for old, requested, head in itertools.product([3, 4, 5, 0, 1], [None], [0, 15]):
        requested = old-1 if old >= 3 else old+1
        t = RetirementTCU()
        t.ram = dict(base.ram)
        w(t, 0x96C4, head)
        w(t, 0x606F, old)
        t.run(0x48BC0)
        for address, value in [(0x8080, 6), (0x8084, requested), (0x92D0, 4), (0xA93A, 1)]:
            w(t, address, value)
        for address, value in [(0x80EA, 4672), (0x80F6, 4224), (0x809C, 20000), (0x80EE, 1000)]:
            w(t, address, value, 2)
        t.run(0x48C08, limit=1000000)
        code = r(t, 0x9C87)
        assert code == (old+4 if old >= 3 else old)
        group = r(t, 0xA2C0, 2)
        assert group == (8 if old >= 3 else 7)
        phase = 0x95D4+15*head
        w(t, 0x9218+4*requested, 5000, 4)
        record = r(t, 0xA2BC, 4) & 65535
        assert r(t, record) == 2
        rows, last = [], None
        if code == 9:
            assert r(t, 0x80D8, 2) == 1000  # Real creation callback now initialized.
        for call in range(451):
            if call:
                if call == 80:
                    w(t, 0x80EE, 5000, 2)
                if code == 9 and call == 400:
                    assert r(t, phase+13) == 3 and r(t, record) == 4 and r(t, 0x96C5) == 1
                    w(t, 0x80D8, 64, 2)
                if code == 9 and call == 401:
                    assert r(t, record) == 4
                    w(t, 0x80D8, 63, 2)
                t.run(0x11014)
                t.run(0x31524, 2, limit=1000000)
                periodic(t)
            else:
                t.run(0x4C7AC)
                t.run(0x1FB8C)
            state = (r(t, phase+13), r(t, record), r(t, 0x96C5), r(t, phase+14))
            if state != last or call in [400, 401]:
                rows.append({'call': call, 'phase_state': state[0], 'request_state': state[1],
                             'phase_count': state[2], 'required_groups_done': state[3],
                             'acknowledgements': [r(t, phase+i) for i in range(10)],
                             'source80d8': r(t, 0x80D8, 2), **paired_snapshot(t)})
                paired_checks += 1
                last = state
            if not r(t, 0x96C5):
                break
        assert call < 450 and r(t, 0x8088) == 1
        assert r(t, 0x96C4) == (head+1) % 16 and r(t, 0x96C6) == 0
        assert {group for index, group in t.acks if index == head} == set(GROUPS)
        assert t.retired == [(fn, code) for fn in CALLBACKS]
        assert r(t, 0xA2BA) == r(t, 0xA202, 2) == 0
        assert r(t, 0x915A, 2) == 0x7FFF
        assert t.run(0x3159A, code) & 255 == 255
        assert t.run(0x31720) == 0
        # Stale payload/event3 while idle and further periodic service do not recreate work.
        prior = list(t.retired)
        ack(t, head, 5)
        for _ in range(3):
            t.run(0x31524, 2)
            periodic(t)
        assert t.retired == prior and r(t, 0x96C5) == 0
        assert r(t, 0x915A, 2) == 0x7FFF
        lifecycles.append({'old': old, 'requested': requested, 'head': head, 'code': code,
                           'manager_group': group, 'retired_at': call, 'ack_order': t.acks,
                           'checkpoints': rows})
    print(json.dumps({'scope': __doc__.strip(), 'tcu_sha256': hashlib.sha256(TCU).hexdigest(),
                      'bitmap_cases': bitmap_cases, 'stateful_acknowledgements': stateful_acks,
                      'ring_cases': ring_cases, 'initializer_calls': 62,
                      'paired_can216_ecu_checks': paired_checks, 'lifecycles': lifecycles,
                      'limits': 'Boundary ring records/ack inputs are synthetic; integrated lifecycles use actual initialized groups. Code9 release uses explicit80D8 input64/63 after prolonged hold. Complete boot/task/hardware, source units, ascending predicate semantics and multi-request calibration remain open.'}, indent=2))


if __name__ == '__main__':
    main()
