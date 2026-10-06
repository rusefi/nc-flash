"""Execute original TCU timer wheels and periodic request service.

No simulated interrupt frequency. Coupled call orders are explicit fixtures,
not a claim about elapsed time or the vehicle's application scheduler.
"""
import itertools
import json

from sh_relative_branch import SHRelativeBranch
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_dispatch import fixture, create
from verify_spark_interaction import paired


class ObserveService(SHRelativeBranch):
    """Observation only; every instruction and callee still executes."""
    def __init__(self):
        super().__init__(TCU)
        self.groups = []

    def instruction(self, pc):
        if pc == 0x31E78:
            self.groups.append((self.r[6] >> 16) & 65535)
        return super().instruction(pc)


# RAM intervals, width, cap, and positions within the 512-call supercycle.
# Independent expected schedule; do not derive it from firmware jump tables.
RANGES = [
    (0x810C, 0x8157, 1, 255, 2, (0,)),
    (0x8158, 0x8188, 1, 255, 4, (1,)),
    (0x8188, 0x8281, 1, 255, 8, (3,)),
    (0x8284, 0x82BC, 1, 255, 16, (7,)),
    (0x82BC, 0x82D0, 1, 255, 32, (15,)),
    (0x82D0, 0x82DC, 1, 255, 64, (31,)),
    (0x82DC, 0x82DD, 1, 255, 256, (127,)),
    (0x82E0, 0x8330, 2, 65535, 4, (1,)),
    (0x8330, 0x8372, 2, 65535, 8, (3,)),
    (0x8374, 0x8376, 2, 65535, 64, (31,)),
    (0x8378, 0x837C, 2, 65535, 256, (127,)),
    (0x837C, 0x837E, 2, 65535, 512, (511,)),
    (0x8380, 0x8410, 2, 32767, 4, (1,)),
]


def main():
    t = SHRelativeBranch(TCU)
    helper_cases = 0
    for fn, size, cap, values in [
        (0x1127E, 1, 255, range(256)),
        (0x11292, 2, 65535, [0, 1, 32766, 32767, 32768, 65534, 65535]),
        (0x112A6, 2, 32767, [0, 1, 32766, 32767, 32768, 65534, 65535]),
    ]:
        for value in values:
            w(t, 0xA900, value, size)
            t.run(fn, 0xFFFFA900)
            expected = value if value == cap else (value+1) & ((1 << (8*size))-1)
            assert r(t, 0xA900, size) == expected
            helper_cases += 1

    model = {}
    for start, end, size, cap, _, _ in RANGES:
        for i, addr in enumerate(range(start, end, size)):
            value = [0, cap-1, cap, (1 << (8*size))-1][i % 4]
            model[addr] = value
            w(t, addr, value, size)
    for addr in [0x8494, 0x8498, 0x849C]:
        w(t, addr, 0xDEADBEEF, 4)
    t.run(0x12880)
    assert all(r(t, a, 4) == 0 for a in [0x8494, 0x8498, 0x849C])
    w(t, 0x90C8, 65534, 2)
    wheel_checks = 0
    for tick in range(1024):
        t.run(0x11014)
        for start, end, size, cap, period, positions in RANGES:
            due = tick % period in positions
            for addr in range(start, end, size):
                if due and model[addr] != cap:
                    model[addr] = (model[addr]+1) & ((1 << (8*size))-1)
                assert r(t, addr, size) == model[addr], (tick, hex(addr))
                wheel_checks += 1
        assert r(t, 0x8494, 4) == (tick+1) % 16
        assert r(t, 0x8498, 4) == ((tick+1)//16) % 16
        assert r(t, 0x849C, 4) == ((tick+1)//256) % 2
        assert r(t, 0x90C8, 2) == (65534+(tick+2)//2) % 65536

    mode_cases = 0
    for entry, mode in itertools.product([0x12886, 0x12386], range(256)):
        w(t, 0x8009, mode)
        t.run(0x11004)
        w(t, 0x8115, 0)
        t.run(entry)
        active = mode == 3 or (entry == 0x12386 and mode == 1)
        assert r(t, 0x8494, 4) == int(active)
        assert r(t, 0x8115) == int(active)
        assert r(t, 0x8009) == (3 if entry == 0x12386 and mode == 1 else mode)
        mode_cases += 1

    periodic_cases = []
    for state, old_phase in itertools.product(range(3), range(8)):
        base = fixture()
        t = ObserveService()
        t.ram = dict(base.ram)
        w(t, 0x8088, state); w(t, 0x96C6, old_phase)
        t.r[5] = 0
        t.run(0x31524, 4, limit=300000)
        new_phase = (old_phase+1) % 8 if state == 2 else old_phase
        expected = []
        if state == 2:
            if new_phase % 2 == 0:
                expected = [5, 6, 0x26, 0x29]
            elif new_phase in (1, 5):
                expected = [0x20, 0xB, 2, 0x25, 0x14, 0x1A]
        assert t.groups == expected, (state, old_phase, t.groups)
        assert r(t, 0x8088) == state and r(t, 0x96C6) == new_phase
        assert r(t, 0xA1AC) == 0
        periodic_cases.append({'state': state, 'old_phase': old_phase,
                               'new_phase': new_phase, 'groups': t.groups})

    # Each loop is ONE real timer-wheel call, with event4 every N such calls.
    # N is a test input. Initial wheel phase varies; no timer value is injected.
    lifecycles, paired_paths = [], []
    for code, interval, initial_phase in itertools.product([6, 7], [1, 3, 7], [0, 15]):
        t = fixture(); record = create(t, code, 0x17 if code == 7 else 0)
        t.run(0x11004); w(t, 0x8494, initial_phase, 4)
        w(t, 0x8009, 1); w(t, 0x8088, 2)
        w(t, 0x80EE, 1000 if code == 7 else 872, 2)
        state, value, hold, ramp, service_phase = 2, 0, 0, 0, 0
        duration, peak = (18, 576) if code == 7 else (49, 1024)
        assert r(t, 0x8115) == r(t, 0x81F2) == 0
        transitions = []
        for tick in range(1, 2001):
            old = (initial_phase+tick-1) % 16
            if old % 2 == 0:
                ramp = min(255, ramp+1)
            if old in (3, 11):
                hold = min(255, hold+1)
            t.run(0x12386)
            previous = state
            if tick % interval == 0:
                service_phase = (service_phase+1) % 8
                if service_phase % 2 == 0:
                    if state == 2:
                        state, value = 3, peak
                    elif state == 3:
                        hold = 0
                        if code == 7:
                            state = 4
                        else:
                            state, ramp = 5, 0
                    elif state == 4 and hold >= 3:
                        state, ramp = 5, 0
                    elif state == 5:
                        if ramp >= duration:
                            state, value = 0, 0
                        else:
                            value = peak*(duration-ramp)//duration
                t.r[5] = 0
                t.run(0x31524, 4, limit=300000)
                t.run(0x4C7AC); t.run(0x1FB8C)
            assert r(t, 0x8115) == ramp and r(t, 0x81F2) == hold
            assert r(t, record) == state, (code, interval, initial_phase, tick, state, r(t, record))
            assert r(t, record+4, 2) == value
            if previous != state:
                transitions.append({'tick': tick, 'state': state or 'released',
                                    'hold': hold, 'ramp': ramp, 'value': value})
            if state == 0:
                assert r(t, 0xA2BA) == r(t, 0xA202, 2) == r(t, 0xA1AC) == 0
                assert r(t, 0x9F3C, 4) == 0x007FFFFF
                paired_paths.append(paired(r(t, 0x915A, 2), 10016, True, True, 0, t=t))
                break
        else:
            raise AssertionError('request did not finish')
        lifecycles.append({'code': code, 'service_every_timer_calls': interval,
                           'initial_phase': initial_phase, 'transitions': transitions})

    print(json.dumps({'status': 'passed', 'helper_cases': helper_cases,
                      'timer_wheel_calls': 1024, 'timer_value_checks': wheel_checks,
                      'mode_cases': mode_cases, 'periodic_cases': periodic_cases,
                      'explicit_call_order_lifecycles': lifecycles,
                      'released_CAN216_ECU_paths': paired_paths,
                      'limits': 'No hardware ISR, physical frequency, or full application scheduling claim.'}, indent=2))


if __name__ == '__main__':
    main()
