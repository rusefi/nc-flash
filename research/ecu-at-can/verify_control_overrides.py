"""Execute stock ECU numeric override producers and retained serial commands.

Independent finite RTZ numeric/state oracles; actual original ROM helpers,
protected writes, selected task order. Upstream sources and peer are fixtures.
"""
import hashlib
import itertools
import json
from fractions import Fraction

from verify_control_timers import setup_loop, cycle, ECU, TCU, w, r, f, rf, q, number
from verify_control_admission import fixture, protected
from verify_throttle_candidate import checksum
from verify_traction_flags import protected_byte


def relative(e, closed_valid=True):
    count = r(e, 0x5668, 2)
    threshold = int.from_bytes(ECU[0xBAE52:0xBAE54], 'big')
    if count < threshold:
        want = number(0xBB194)
    elif count == threshold:
        closed = rf(e, 0x2114) if closed_valid else number(0xBADD8)
        want = q(rf(e, 0x5534)-closed)
    else:
        want = min(number(0xBB198), q(rf(e, 0x5620)+number(0xBB19C)))
    stack = e.r[15]
    e.run(0x23A24)
    assert e.r[15] == stack and rf(e, 0x5620) == want
    checksum(e, 0x5620)
    return float(want)


def absolute(e, closed_valid=True):
    closed = rf(e, 0x2114) if closed_valid else number(0xBADD8)
    enable, previous, stage = r(e, 0x5635), r(e, 0x565A), r(e, 0x5634)
    count = r(e, 0x5658, 2)
    if stage >= 3 and previous == 0 and enable == 1:
        candidate = q(rf(e, 0x8248)+closed)
        count = 0
    elif count <= int.from_bytes(ECU[0xBB1A0:0xBB1A2], 'big'):
        candidate = q(rf(e, 0x8248)+closed)
        count = min(65535, count+1)
    else:
        candidate = q(rf(e, 0x5650)+number(0xBB1A8))
    want = min(q(number(0xBB1A4)+closed), candidate)
    stack = e.r[15]
    e.run(0x245FC)
    assert e.r[15] == stack
    actual = (rf(e, 0x5650), r(e, 0x5658, 2), r(e, 0x565A))
    assert actual == (want, count, enable), (actual, (want, count, enable))
    checksum(e, 0x5650)
    return dict(value=float(want), timer=count, previous=enable)


def highest(e):
    want = max(number(0xBB170), number(0xBB174)) if r(e, 0x566C) == 1 else 0
    stack = e.r[15]
    e.run(0x246E8)
    assert e.r[15] == stack and rf(e, 0x565C) == want
    checksum(e, 0x565C)
    return float(want)


def initialize(e, closed_valid=True):
    closed = rf(e, 0x2114) if closed_valid else number(0xBADD8)
    old_previous = r(e, 0x565A)
    for address in [0x23A1C, 0x245D8, 0x246E0]: e.run(address)
    assert rf(e, 0x5620) == rf(e, 0x565C) == 0
    assert rf(e, 0x5650) == q(closed+number(0xBB1A4))
    assert r(e, 0x5658, 2) == 65535 and r(e, 0x565A) == old_previous
    for address in [0x5620, 0x5650, 0x565C]: checksum(e, address)


def integrated(e, call, **kwargs):
    row = cycle(e, call, numeric_producers=(highest, relative, absolute), **kwargs)
    row.update(relative=float(rf(e, 0x5620)), absolute=float(rf(e, 0x5650)),
               absolute_timer=r(e, 0x5658, 2), source=float(rf(e, 0x8248)),
               source_stage=r(e, 0x5634), source_enable=r(e, 0x5635))
    return row


def main():
    relative_cases = absolute_cases = highest_cases = init_cases = 0
    for count, feedback, old, closed, corrupt in itertools.product(
            [0, 1, 49, 50, 51, 65535], [-10, 0, 10.5, 12.5, 40],
            [-5, 0, 11.5, 12], [0, 10.5, 20], [False, True]):
        e = fixture(); w(e, 0x5668, count, 2)
        f(e, 0x5534, feedback); protected(e, 0x5620, old); protected(e, 0x2114, closed)
        if corrupt: w(e, 0x2118, 0, 2); w(e, 0x211A, 0, 2)
        relative(e, not corrupt); relative_cases += 1
    for stage, enable, previous, count, source in itertools.product(
            [0, 2, 3, 4, 128, 255], [0, 1, 2, 255], [0, 1, 2],
            [0, 62, 63, 64, 32768, 65535], [-20, 0, 5, 6, 7]):
        e = fixture()
        for a, v in [(0x5634, stage), (0x5635, enable), (0x565A, previous)]: w(e, a, v)
        w(e, 0x5658, count, 2); f(e, 0x8248, source)
        protected(e, 0x5650, [-5, 10, 16.5, 20][absolute_cases % 4])
        corrupt = absolute_cases % 7 == 0
        protected(e, 0x2114, [0, 10.5, 20][absolute_cases % 3])
        if corrupt: w(e, 0x2118, 0, 2); w(e, 0x211A, 0, 2)
        absolute(e, not corrupt); absolute_cases += 1
    for enabled in [0, 1, 2, 127, 128, 255]:
        e = fixture(); w(e, 0x566C, enabled); highest(e); highest_cases += 1
    for closed, corrupt, previous in itertools.product([0, 10.5, 20], [False, True], [0, 1, 2]):
        e = fixture(); protected(e, 0x2114, closed); w(e, 0x565A, previous)
        if corrupt: w(e, 0x2118, 0, 2); w(e, 0x211A, 0, 2)
        initialize(e, not corrupt); init_cases += 1
    # No direct5620/5650/565C injection; initialization and every update execute.
    e = setup_loop(numeric_fixtures=False); initialize(e); f(e, 0x8248, 2)
    boundaries = {1, 5, 6, 624, 625, 673, 674, 675, 706, 707, 708, 824, 825, 1875, 1876, 1878}
    rows = []
    for call in range(1, 1879):
        row = integrated(e, call, update_can=call in boundaries)
        branch = 'normal' if call < 6 else 'feedback' if call < 625 else 'relative' if call <= 1875 else 'bypass'
        assert row['branch'] == branch, row
        if 625 <= call < 674: assert rf(e, 0x56A0) == Fraction(23, 2), row
        if call == 674: assert rf(e, 0x56A0) == rf(e, 0x5534), row
        if 707 <= call <= 1875: assert rf(e, 0x5620) == number(0xBB198), row
        if call in boundaries: rows.append(row)
    # Force dispatcher to the fourth priority using upstream mode/source
    # fixtures, keeping timers, admission, producer and serial path original.
    e = setup_loop(numeric_fixtures=False); initialize(e)
    for a in [0x210C, 0x2076, 0x2088, 0x208A]: protected_byte(e, a, 0)
    w(e, 0x722A, 1); f(e, 0x6CB4, 8); e.run(0x1DED8)
    w(e, 0x5634, 3); w(e, 0x5635, 1); f(e, 0x8248, 2)
    absolute_rows = []
    for call in range(1, 701):
        if call == 66: f(e, 0x8248, -5)  # ignored after count>63
        if call == 570: w(e, 0x5635, 0)
        if call == 571: w(e, 0x5635, 1)  # reset on exactly0->1 atstage>=3
        if call == 600: w(e, 0x5635, 2)  # raw nonBoolean priority quirk
        if call == 601: w(e, 0x5635, 1)  # 2->1 does NOT reset
        row = integrated(e, call, update_can=call in [1, 64, 65, 66, 570, 571, 600, 601, 636, 637, 700])
        assert row['selection'] == ('normal' if call in [570, 600] else '5672'), row
        if call == 1: assert row['absolute_timer'] == 0 and rf(e, 0x5650) == Fraction(25, 2)
        if call == 65: assert row['absolute_timer'] == 64 and rf(e, 0x5650) == Fraction(25, 2)
        if call == 569: assert rf(e, 0x5650) == Fraction(33, 2), row
        if call == 571: assert row['absolute_timer'] == 0 and rf(e, 0x5650) == Fraction(11, 2), row
        if call == 601: assert row['absolute_timer'] == 30, row
        if call in [1, 2, 64, 65, 66, 569, 570, 571, 572, 600, 601, 635, 636, 637, 700]: absolute_rows.append(row)
    print(json.dumps(dict(ecu_sha256=hashlib.sha256(ECU).hexdigest(), tcu_sha256=hashlib.sha256(TCU).hexdigest(),
          relative_cases=relative_cases, absolute_cases=absolute_cases, highest_cases=highest_cases,
          initialization_cases=init_cases, retained_serial_cycles=2578, paired_can_boundary_updates=len(boundaries)+11,
          relative_lifecycle=rows, absolute_lifecycle=absolute_rows,
          limits='Finite normal/zero float operands; selected task bodies, explicit local source8248/stage5634/enable5635/mode/6CB4 fixtures and synthetic SCI1 peer. Full scheduler, remote/physical behavior remain open.'), indent=2))


if __name__ == '__main__': main()
