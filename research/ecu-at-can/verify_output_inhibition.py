"""Shared CAN211/216 inhibition -> ECU scheduler -> observed timer writes.

Register values are fixed samples. No timer counting, pin state, interrupt
delivery or vehicle wiring is simulated. All firmware helpers execute.
"""
import hashlib
import itertools
import json
from fractions import Fraction

from verify_model_sources import ECU, TCU, SHModelFloat, number, f, rf, w, r
from verify_traction_pattern import source_case, event
from verify_spark_interaction import TRACTION, GATES
from sh_software_arithmetic import SHSoftwareArithmetic
from sh_subset import MASK, signed


class TimerSamples(SHModelFloat, SHSoftwareArithmetic):
    """Compose existing arithmetic and add SHAL plus an explicit register slice."""
    READABLE = {0xFFFFF440, 0xFFFFF666, 0xFFFFF66C,
                *range(0xFFFFF640, 0xFFFFF648, 2), *range(0xFFFFF444, 0xFFFFF44C, 2)}
    WRITABLE = READABLE - {0xFFFFF440, 0xFFFFF666}

    def __init__(self, rom=ECU):
        super().__init__(rom)
        self.registers = {a: 0 for a in self.READABLE}
        self.register_writes = []

    def read(self, addr, size):
        addr &= MASK
        if addr in self.READABLE and size == 2:
            return self.registers[addr]
        return super().read(addr, size)

    def write(self, addr, value, size):
        addr &= MASK
        if addr in self.WRITABLE and size == 2:
            self.registers[addr] = value & 65535
            self.register_writes.append([hex(addr), value & 65535, size])
            return
        super().write(addr, value, size)

    def instruction(self, pc):
        opcode = self.read(pc, 2)
        if opcode & 0xF0FF == 0x4020:  # SHAL: same data/T operation as SHLL
            n = (opcode >> 8) & 15
            value = self.r[n]
            self.t(bool(value & 0x80000000))
            self.r[n] = (value << 1) & MASK
            self.visited.add(pc)
            return pc+2, False
        return super().instruction(pc)


def fixed_div(a, b):
    if not a:
        return 0
    if not b:
        return 0x7FFFFFFF if a > 0 else -0x80000000
    return max(-0x80000000, min(0x7FFFFFFF, int(Fraction(a*65536, b))))


def initialize():
    e = TimerSamples()
    e.run(0x1FA8C)
    for c in range(4):
        p = 0x53DC+40*c
        assert r(e, p+12) == r(e, p+16) == c
        assert r(e, p+8, 4) == int.from_bytes(ECU[0x2F3B4+4*c:0x2F3B8+4*c], 'big')
    e.registers[0xFFFFF440] = 100
    e.registers[0xFFFFF666] = 0
    e.registers[0xFFFFF66C] = 65535
    for c in range(4):
        e.registers[0xFFFFF640+2*c] = 200+c
        e.registers[0xFFFFF444+2*c] = 300+c
        w(e, 0x6784+4*c, 1234+c, 4)
    return e


def configure(e, mode=0, inhibit=0, state=0, child=0, hardware=0, deadline=1000):
    for c in range(4):
        p = 0x53DC+40*c
        for a, v, size in [(p, mode, 1), (p+1, inhibit, 1), (p+2, state, 1),
                           (p+8, deadline, 4), (p+17, child, 1), (p+24, 50, 4),
                           (p+28, 100, 4), (p+32, 500, 4),
                           (0x41FB+24*c, hardware, 1), (0x410C, 65536, 4)]:
            w(e, a, v, size)


def apply(e, mask, now=0):
    e.r[5] = mask
    e.run(0x20290, now)


def release_limit(e, c, mode):
    p = 0x53DC+40*c
    if mode == 0:
        return r(e, p+32, 4)
    # 20584 calls1F94E/1F962 and original signed Q16 division2138.
    extra = int(number(0xCC1E4)/Fraction(1, 4))
    numerator = signed(r(e, 0x41E4, 4)+r(e, p+24, 4)+extra)
    calculated = signed(fixed_div(numerator, signed(r(e, 0x410C, 4)))*180+r(e, p+28, 4))
    return max(r(e, p+32, 4)+1, calculated)


def main():
    counts = {}
    isa = 0
    for reg, value, sr in itertools.product(range(16), [0, 1, 0x7FFFFFFF, 0x80000000, 0x80000001, MASK], [0, 1, 0x3F0, 0x3F1]):
        e = TimerSamples((0x4020 | reg << 8).to_bytes(2, 'big'))
        e.r[reg] = value; e.sr = sr
        before = e.r[:]
        assert e.instruction(0) == (2, False)
        before[reg] = (2*value) & MASK
        assert e.r == before and e.sr == (sr & ~1) | (value >> 31)
        isa += 1
    counts['shal_vectors'] = isa

    division = 0
    for a, b in itertools.product([-2147483648, -100000, -32768, -3, -1, 0, 1, 3, 32767, 100000, 2147483647],
                                  [-65536, -3, -1, 0, 1, 3, 65536]):
        e = TimerSamples(); e.r[5] = b & MASK
        assert signed(e.run(0x2138, a)) == fixed_div(a, b), (a, b)
        division += 1
    counts['signed_q16_division'] = division

    rejections = 0
    e = TimerSamples()
    for operation in [lambda: e.read(0xFFFFF640, 1), lambda: e.write(0xFFFFF666, 0, 2),
                      lambda: e.read(0xFFFFF648, 2), lambda: e.write(0xFFFFF440, 0, 2)]:
        try: operation()
        except ValueError: rejections += 1
        else: raise AssertionError('Unmodelled register access admitted')
    counts['expected_register_rejections'] = rejections

    cancels = 0
    for c, hardware, alternate, dstr, counter in itertools.product(range(4), [0, 1, 2], [0, 1, 2],
                                                                   [0, 1, 5, 15, 65535], [0, 1, 32768, 65535]):
        e = initialize(); e.sr = 0xF0
        e.registers[0xFFFFF440] = counter
        e.registers[0xFFFFF666] = dstr
        w(e, 0x41FB+24*c, hardware)
        w(e, 0x41FC+24*c, alternate)
        e.run(0x96F4, c)
        expected = []
        if hardware == 0:
            if alternate == 1:
                expected = [['0xfffff66c', 65535 & ~(1 << c), 2]]
            else:
                expected = [[hex(0xFFFFF444+2*c), (counter-1)&65535, 2]]
                if dstr & (1 << c) == 0:
                    expected += [[hex(0xFFFFF640+2*c), 0, 2]]*2
        assert e.register_writes == expected
        assert r(e, 0x41FB+24*c) == 0 and e.sr == 0xF0
        assert r(e, 0x41FC+24*c) == (0 if hardware == 0 and alternate == 1 else alternate)
        cancels += 1
    counts['low_level_cancellation'] = cancels

    admission = 0
    for mode, inhibit, state, child, hardware, desired, deadline in itertools.product(
            [0, 1], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 15],
            [-0x2D00000-1, -1, 0, 499, 500, 501, 1000000]):
        e = initialize(); configure(e, mode, inhibit, state, child, hardware, deadline)
        limits = [release_limit(e, c, mode) for c in range(4)]
        delta = signed(deadline)
        distance = signed(delta+0x2D00000) if delta <= 0 else delta
        want = bool(desired)
        changed = (inhibit == 1 and not want) or (inhibit == 0 and want)
        expected_inhibit, expected_state = inhibit, state
        cancel = False
        if changed and distance >= 0:
            if want:
                if state == 0:
                    expected_inhibit = 1
                elif state == 1 and (child not in [1, 2] or child == 1 and hardware != 0):
                    expected_inhibit, expected_state, cancel = 1, 0, True
            elif state == 1 or state == 0 and distance >= limits[0]:
                expected_inhibit = 0
            elif state == 0:
                expected_state = 2
        apply(e, desired)
        assert [(r(e, 0x53DC+40*c+1), r(e, 0x53DC+40*c+2)) for c in range(4)] == [(expected_inhibit, expected_state)]*4, (mode,inhibit,state,child,hardware,desired,deadline,limits)
        assert [r(e, 0x6784+4*c, 4) for c in range(4)] == ([0]*4 if cancel else [1234+c for c in range(4)])
        assert bool(e.register_writes) == (cancel and hardware == 0)
        admission += 1
    counts['complete_admission_and_release'] = admission

    mixed = 0
    for mask in range(16):
        e = initialize(); configure(e, state=1)
        apply(e, mask)
        assert [r(e, 0x53DD+40*c) for c in range(4)] == [(mask >> c)&1 for c in range(4)]
        assert [r(e, 0x6784+4*c, 4) for c in range(4)] == [0 if mask & (1 << c) else 1234+c for c in range(4)]
        assert e.register_writes == [entry for c in range(4) if mask & (1 << c) for entry in
            [[hex(0xFFFFF444+2*c), 99, 2], [hex(0xFFFFF640+2*c), 0, 2], [hex(0xFFFFF640+2*c), 0, 2]]]
        mixed += 1
    counts['all_cylinder_masks'] = mixed

    boundaries = []
    for mode in [0, 1]:
        base = initialize(); configure(base, mode=mode, inhibit=1)
        threshold = release_limit(base, 0, mode)
        for deadline in [threshold-1, threshold, threshold+1]:
            e = initialize(); configure(e, mode=mode, inhibit=1, deadline=deadline)
            apply(e, 0)
            expected = (0, 0) if deadline >= threshold else (1, 2)
            assert [(r(e,0x53DD+40*c),r(e,0x53DE+40*c)) for c in range(4)] == [expected]*4
            boundaries.append({'mode':mode,'distance':deadline,'release_threshold':threshold,
                               'inhibited':expected[0],'state':expected[1]})
    counts['release_boundary_cases'] = len(boundaries)

    for mask in range(16):
        e = initialize(); configure(e, state=1)
        w(e, 0x5489, 0); w(e, 0x736A, mask, 2)
        e.run(0x1FB5A, 0)
        assert r(e, 0x5486, 2) == mask
        assert [(r(e,0x53DD+40*c),r(e,0x53DE+40*c)) for c in range(4)] == [
            (1, 2) if mask & (1 << c) else (0, 1) for c in range(4)]
        assert len(e.register_writes) == 3*mask.bit_count()
    counts['whole_scheduler_caller'] = 16

    # A cached mask change is not automatically retried every call. Observe
    # deferral, unchanged-cache hold, then application at the cycle boundary.
    e = initialize(); configure(e, state=1, child=1)
    w(e, 0x5489, 0); w(e, 0x736A, 15, 2)
    lifecycle = []
    for step in range(3):
        if step == 1:
            for c in range(4): w(e, 0x41FB+24*c, 2)
        if step == 2:
            for c in range(4): w(e, 0x53DC+40*c+8, 0, 4)
        e.run(0x1FB5A, 0)
        states = [(r(e,0x53DD+40*c),r(e,0x53DE+40*c)) for c in range(4)]
        assert states == ([(0,1)]*4 if step < 2 else [(1,0)]*4)
        assert r(e, 0x5486, 2) == 15 and e.register_writes == []
        lifecycle.append({'step':step,'cached_mask':15,'records':states})
    counts['deferred_cache_lifecycle'] = len(lifecycle)

    paired = []
    for request, cut in itertools.product([0, 20, 40], [0, 1]):
        # Continue the original model-produced RAM using a register-aware
        # interpreter. No model helper or firmware routine is substituted.
        model = source_case()
        e = initialize(); e.ram.update(model.ram)
        configure(e, state=1)
        for a, v in {**GATES, 0x734A: 0x80, 0x734C: 1, 0x6A5D: 1, 0x6590: 1,
                     0xA488: 1, 0x6DFE: 1, 0x6567: 1, 0x65F0: 1}.items(): w(e, a, v)
        f(e, 0x7140, 200); w(e, 0x6A10, 10000+request, 2)
        for fn in TRACTION[:9]+[0x3FAFC,0x3FD4C,0x3FD9C,0x40660]: e.run(fn)
        t = SHSoftwareArithmetic(TCU)
        w(t, 0x9454, cut); w(t, 0x92C6, 0x20)
        t.run(0x18F10, 1); t.run(0x18F8C, 1)
        payload = bytes(r(t, 0x8EFD+i) for i in range(8))
        for i, byte in enumerate(payload): w(e, 0x6A40+i, byte)
        for fn in [0x35034,0x34CEC,0x3AE52,0x3B4D4,0x3AD04,0x3AC14]: e.run(fn)
        for c in range(1, 5):
            w(e, 0x6DF2, ECU[0x4F4F0+4*c+3]); e.run(0x4D716)
        for event_id in [2, 0, 4, 6]: event(e, event_id)
        e.run(0x1F864)
        mask = e.r[0] & 65535
        assert mask == (15 if cut else {0:5,20:1,40:0}[request])
        w(e, 0x5489, 0)
        e.run(0x1FB5A, 0)
        assert r(e, 0x5486, 2) == mask
        assert [r(e, 0x53DD+40*c) for c in range(4)] == [(mask >> c)&1 for c in range(4)]
        assert len(e.register_writes) == 3*mask.bit_count()
        paired.append({'can211_word0':10000+request, 'tcu_cut':cut, 'can216':payload.hex(' '),
                       'pattern':r(e,0x74F1), 'shared_mask':mask, 'register_writes':e.register_writes})
    counts['paired_can_to_registers'] = len(paired)
    print(json.dumps({'ecu_sha256':hashlib.sha256(ECU).hexdigest(), 'tcu_sha256':hashlib.sha256(TCU).hexdigest(),
                      'counts':counts, 'paired_cases':paired,
                      'release_boundaries':boundaries, 'deferred_lifecycle':lifecycle,
                      'limits':'Fixed register samples, explicit model/record scheduling. No timer clock, pin polarity, ECU wiring or physical injector behavior simulated.'}, indent=2))


if __name__ == '__main__':
    main()
