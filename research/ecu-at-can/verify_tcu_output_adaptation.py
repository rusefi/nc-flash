"""Execute output-gain adaptation, offset lookup and eight-slot dispatch.

Original TCU instructions and independent integer/state models. Retained
handoff uses explicit samples/order; no physical clock, plant or persistence.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_output_handoff as handoff
from verify_tcu_output_handoff import TCU, w, r, s, signed, sd, clamp_word, execute
from verify_tcu_output_service import word

ROOT = Path(__file__).resolve().parent
assert [int.from_bytes(TCU[a:a+4], 'big') for a in range(0x5C5EC, 0x5C60C, 4)] == [0x18C38]*4 + [0x18E76]*4


def fixture():
    t = handoff.fixture()
    handoff.initialize(t)
    return t


class TimerRegisters(handoff.OutputSink):
    WIDTHS = {0xFFFFF400: 1, 0xFFFFF401: 1, 0xFFFFF600: 2, 0xFFFFF604: 2,
              **{a: 2 for a in range(0xFFFFF500, 0xFFFFF520, 2)}}

    def read(self, address, size):
        if address in self.WIDTHS:
            if self.WIDTHS[address] != size:
                raise ValueError('Timer width mismatch')
            self.timer_trace.append(('read', address, size, self.timer_registers[address]))
            return self.timer_registers[address]
        return super().read(address, size)

    def write(self, address, value, size):
        if address in self.WIDTHS:
            if self.WIDTHS[address] != size:
                raise ValueError('Timer width mismatch')
            value &= (1 << (8*size))-1
            self.timer_trace.append(('write', address, size, value))
            self.timer_registers[address] = value
            return
        super().write(address, value, size)


def timer_fixture(value):
    t = fixture(); t.__class__ = TimerRegisters
    t.timer_registers = {a: (value*257) & ((1 << (8*n))-1) for a, n in t.WIDTHS.items()}
    t.timer_trace = []
    w(t, 0x87F4, value)
    return t


def timer_initialize(t):
    ref = copy.deepcopy(t)
    old = ref.timer_registers[0xFFFFF401]
    events = [('read', 0xFFFFF401, 1, old), ('write', 0xFFFFF401, 1, old & 0xFB),
              ('write', 0xFFFFF400, 1, 0)]
    events += [('write', 0xFFFF0000+a, 2, 0) for a in [0xF506, 0xF504, 0xF502, 0xF500]]
    events += [('write', 0xFFFF0000+a, 2, 33333) for a in
               [0xF50A, 0xF508, 0xF50E, 0xF50C, 0xF512, 0xF510,
                0xF516, 0xF514, 0xF51A, 0xF518, 0xF51E, 0xF51C]]
    events += [('write', 0xFFFFF400, 1, 0), ('write', 0xFFFFF600, 2, 0),
               ('write', 0xFFFFF604, 2, 4166), ('write', 0xFFFFF400, 1, 15),
               ('read', 0xFFFFF401, 1, old & 0xFB), ('write', 0xFFFFF401, 1, old | 4)]
    for kind, address, size, value in events:
        if kind == 'write': ref.timer_registers[address] = value
    ref.timer_trace.extend(events); w(ref, 0x87F4, 0)
    execute(t, 0x168AC); handoff.equal(t, ref)
    assert t.timer_trace == ref.timer_trace
    assert t.timer_registers == ref.timer_registers


def adaptation_model(t, i):
    j = 2*i
    base, error = r(t, 0xA5D4+j, 2), s(t, 0x8A34+j)
    normalized = signed(sd(error*1000, base), 16) if base else 0
    admitted = (base >= 200 and s(t, 0x8AB6) < error < s(t, 0x8AB4)
                and s(t, 0x8ABA) < normalized < s(t, 0x8AB8))
    if not admitted:
        return dict(admitted=False)
    target = clamp_word(sd(sd(s(t, 0x8AAC+j)*80, 100)*1000, base), 3700, 9700)
    old = s(t, 0x8A6C+j)
    delta = clamp_word((signed(target, 16)-old) >> 4, -100, 100)
    difference = abs(signed(target-old, 16))
    w(t, 0x8AC2+j, difference, 2)
    if r(t, 0x8A60+i) == 0 and signed(difference, 16) < word(0x5C5E8):
        w(t, 0x8A60+i, 1)
    coarse = False
    if r(t, 0x89AC):
        if r(t, 0x8ABD+i) == 0:
            if word(0x5FCFC) <= r(t, 0x89AA, 2) <= word(0x5FCFE):
                target = 4788 + sd(s(t, 0x89A8)*223, 10)
            delta = target-old
            w(t, 0x8ABD+i, 1)
            coarse = True
        w(t, 0x8A9C+4*i, s(t, 0x8A9C+4*i, 4)-signed(delta, 16)*base, 4)
        w(t, 0x8A6C+j, old+delta, 2)
    gain = r(t, 0x8A6C+j, 2)
    for destination, source in [(0x8A8C, 0x8A94), (0x8A7C, 0x8A84)]:
        w(t, destination+j, sd(r(t, source+j, 2)*gain, r(t, 0x8A74+j, 2)), 2)
    return dict(admitted=True, normalized=normalized, target=target, delta=delta,
                coarse=coarse, difference=signed(difference, 16))


def adaptation(t, i):
    ref = copy.deepcopy(t); result = adaptation_model(ref, i)
    execute(t, 0x18C38, i); handoff.equal(t, ref)
    return result


def offset_model(t, i):
    x = max(8000, min(16000, r(t, 0xA518, 2))) - 8000
    index, remainder = divmod(x, 2000)
    p = r(t, 0x8AD4, 4) + 12*i
    a, b = t.read(p+2*index, 2), t.read(p+2*index+2, 2)
    value = signed(a, 16)
    if remainder and b != 65535:
        value += sd((b-a)*remainder, 2000)
    result = max(0, min(32767, value & 65535))
    w(t, 0x8A44+2*i, result, 2)
    return result


def offset(t, i):
    ref = copy.deepcopy(t); result = offset_model(ref, i)
    execute(t, 0x18E76, i); handoff.equal(t, ref)
    return result


def dispatch_model(t):
    # MOV.W sign extends both operands before unsigned CMP/HI.
    run_slot = (s(t, 0x8ACA) & 0xFFFFFFFF) > (s(t, 0x8ACC) & 0xFFFFFFFF)
    slot = None; result = {}
    if run_slot:
        w(t, 0x8ACA, 0, 2)
        slot = r(t, 0x8ACE)
        assert 0 <= slot <= 7
        result = adaptation_model(t, slot) if slot < 4 else dict(offset=offset_model(t, slot-4))
        w(t, 0x8ACE, (slot+1) % 8)
    if r(t, 0x8AD0, 2) > 3000:
        for address, value in [(0x8ACC, 15), (0x8AB4, 5), (0x8AB6, -5)]:
            w(t, address, value, 2)
    w(t, 0x8AD0, r(t, 0x8AD0, 2)+1, 2)
    w(t, 0x8ACA, r(t, 0x8ACA, 2)+1, 2)
    return dict(slot=slot, result=result)


def dispatch(t):
    ref = copy.deepcopy(t); result = dispatch_model(ref)
    execute(t, 0x18830); handoff.equal(t, ref)
    return result


def seed(t, rng, i):
    j = 2*i
    for a in [0xA5D4, 0x8AAC, 0x8A6C, 0x8A94, 0x8A84]:
        w(t, a+j, rng.randrange(65536), 2)
    w(t, 0x8A74+j, rng.randrange(1, 65536), 2)
    for a in [0x8A34+j, 0x8AB4, 0x8AB6, 0x8AB8, 0x8ABA, 0x89AA, 0x89A8]:
        w(t, a, rng.randrange(65536), 2)
    for a in [0x89AC, 0x8ABD+i, 0x8A60+i]:
        w(t, a, rng.choice([0, 1, 2, 255]))
    w(t, 0x8A9C+4*i, rng.randrange(1 << 32), 4)


def direct():
    counts = dict(adaptation_boundaries=0, adaptation_random=0, offsets=0, dispatch=0)
    branches = set(); t = fixture()
    for i, base, error, enabled, once in itertools.product(range(4),
            [0, 199, 200, 201, 1000], [-100, -50, -49, -10, -9, 0, 9, 10, 49, 50, 100],
            [0, 1, 2], [0, 1]):
        w(t, 0xA5D4+2*i, base, 2); w(t, 0x8A34+2*i, error, 2)
        w(t, 0x8AAC+2*i, 6000, 2); w(t, 0x8A6C+2*i, 5500, 2)
        w(t, 0x89AC, enabled); w(t, 0x8ABD+i, once)
        result = adaptation(t, i)
        branches.add(('admitted' if result['admitted'] else 'rejected', result.get('coarse', False)))
        counts['adaptation_boundaries'] += 1
    rng = random.Random(0x18C38)
    for n in range(2048):
        i = n % 4; seed(t, rng, i)
        if n % 2:
            # Force admitted cases with wide strict limits while retaining
            # arbitrary gain/output/integral and first-update conditions.
            w(t, 0xA5D4+2*i, rng.choice([200, 201, 500, 1000, 65535]), 2)
            w(t, 0x8A34+2*i, 0, 2)
            for a, v in [(0x8AB4, 32767), (0x8AB6, -32768), (0x8AB8, 32767), (0x8ABA, -32768)]:
                w(t, a, v, 2)
            w(t, 0x89AA, rng.choice([9, 10, 11, 999, 1000, 1001, 65535]), 2)
        adaptation(t, i); counts['adaptation_random'] += 1
    for i, value in itertools.product(range(4),
            [0, 7999, 8000, 8001, 9999, 10000, 10001, 11999, 12000, 12001,
             13999, 14000, 14001, 15999, 16000, 16001, 32767, 32768, 65535] + list(range(8000, 16001, 127))):
        w(t, 0xA518, value, 2); offset(t, i); counts['offsets'] += 1
    for count, limit, age, slot in itertools.product([0, 1, 3, 4, 15, 16, 32767, 32768, 65535],
            [0, 3, 15, 32767, 32768, 65535], [0, 3000, 3001, 65535], range(8)):
        for a, v in [(0x8ACA, count), (0x8ACC, limit), (0x8AD0, age)]: w(t, a, v, 2)
        w(t, 0x8ACE, slot)
        dispatch(t); counts['dispatch'] += 1
    assert branches == {('rejected', False), ('admitted', False), ('admitted', True)}
    return counts


def retained():
    t = fixture(); rows = []; dispatched = []
    w(t, 0xA518, 12000, 2); w(t, 0x89AC, 1); w(t, 0x89AA, 10, 2)
    for i in range(4):
        w(t, 0xA5D4+2*i, 500, 2); w(t, 0xA5E4+2*i, 500, 2)
        w(t, 0x8A34+2*i, 0, 2); w(t, 0x8AAC+2*i, 3437, 2)
    # Original dispatcher cadence and warm-up evolution, with known stable
    # feedback fixtures; later handoff replay tests the closed numeric chain.
    for call in range(1, 3041):
        result = dispatch(t)
        if result['slot'] is not None:
            dispatched.append([call, result['slot']])
        if call <= 8 or call in [31, 32, 33, 2999, 3000, 3001, 3002, 3003, 3004, 3019, 3020, 3036, 3040]:
            rows.append(dict(call=call, **result, count=r(t, 0x8ACA, 2), limit=r(t, 0x8ACC, 2),
                age=r(t, 0x8AD0, 2), gain=[r(t, 0x8A6C+2*i, 2) for i in range(4)]))
    assert dispatched[:8] == [[4+4*i, i] for i in range(8)]
    assert r(t, 0x8ACC, 2) == 15 and s(t, 0x8AB4) == 5 and s(t, 0x8AB6) == -5
    t = fixture(); chain = []
    admitted_count = 0
    w(t, 0xA518, 12000, 2); w(t, 0x89AC, 1); w(t, 0x89AA, 10, 2)
    for i in range(4):
        w(t, 0xA5D4+2*i, 500, 2); w(t, 0xA5E4+2*i, 500, 2)
    for call in range(1, 161):
        # One acquisition per rotating service gives four samples per channel
        # after startup. Dispatcher call frequency remains a harness choice.
        handoff.acquire(t, [368 << 6]*4)
        i = (call-1) % 4
        output = handoff.handoff(t, i)
        update = dispatch(t)
        admitted_count += bool(update['result'].get('admitted'))
        if call <= 12 or call % 16 == 0:
            chain.append(dict(call=call, channel=i, handoff=output, adaptation=update,
                gains=[r(t, 0x8A6C+2*j, 2) for j in range(4)],
                offsets=[r(t, 0x8A44+2*j, 2) for j in range(4)]))
    assert admitted_count > 8, admitted_count
    return rows, dispatched, chain, admitted_count


def literal_word_leads():
    """Candidate MOV.W PC-relative references, including possible ROM data."""
    result = {hex(a): [] for a in [0xF500, 0xF502, 0xF504, 0xF506, 0xF50A,
                                  0xF50C, 0xF50E, 0xF400, 0xF402]}
    for pc in range(0, len(TCU)-2, 2):
        opcode = word(pc)
        if opcode >> 12 == 9:
            pool = pc+4+2*(opcode & 255)
            key = hex(word(pool))
            if key in result:
                result[key].append(hex(pc))
    return result


def main():
    counts = direct(); print('Direct', counts, flush=True)
    rows, dispatched, chain, admitted_count = retained()
    for value in range(256):
        t = timer_fixture(value); timer_initialize(t)
    counts['timer_initialization'] = 256
    counts['rejected_timer_accesses'] = 0
    for address, size in [(0xFFFFF400, 2), (0xFFFFF500, 1), (0xFFFFF401, 4), (0xFFFFF520, 2)]:
        for writing in [False, True]:
            try:
                if writing: t.write(address, 0, size)
                else: t.read(address, size)
            except ValueError:
                counts['rejected_timer_accesses'] += 1
            else:
                raise AssertionError('Unexpected timer access accepted')
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
        counts=counts, dispatcher_calls=3040, dispatches=dispatched, dispatcher_rows=rows,
        handoff_calls=160, admitted_handoff_adaptations=admitted_count, retained_handoff=chain,
        timer_initialization_trace=t.timer_trace,
        candidate_word_literal_users=literal_word_leads(),
        limits='Valid dispatcher slots0..7; nonzero gain baseline divisors; original '
               'helpers, finite integer models. No ROM/shared ISA edits. Timer168AC writes '
               'execute against latches; prior clock/mode setup, actual task cadence, '
               'signal identity and physical integration remain open.')
    (ROOT/'tcu-output-adaptation-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('Retained', 3040, 160, flush=True)


if __name__ == '__main__':
    main()
