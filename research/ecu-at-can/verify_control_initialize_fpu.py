"""Independent instruction vectors for bounded startup exception support."""
import hashlib
import itertools
import json
from pathlib import Path
from probe_control_initialize_fpu import SelfTest
from verify_control_contributions import ECU
from verify_control_raw_inputs import application, expected_write

ROOT = Path(__file__).resolve().parent


def fixture(opcode):
    e = SelfTest()
    e.rom = opcode.to_bytes(2, 'big')
    e.r = [0xA5000000 + i for i in range(16)]
    e.fr = [0x3F800000] * 16
    e.sr = 0x3F3
    return e


def verify(e, want_fr, want_sr, want_fpscr, want_gpr=None, want_fpul=None):
    before = e.r.copy() if want_gpr is None else want_gpr
    ram = e.ram.copy()
    saved = (e.gbr, e.pr, e.macl, e.mach, e.fpul if want_fpul is None else want_fpul)
    assert e.instruction(0) == (2, False)
    assert e.fr == want_fr and e.r == before and e.ram == ram
    assert e.sr == want_sr and e.fpscr == want_fpscr
    assert (e.gbr, e.pr, e.macl, e.mach, e.fpul) == saved


def main():
    transfers = division = comparison = finite = rejected = 0
    fields = [5, 6, 10, 11, 15, 16]
    for register, pattern in itertools.product(range(16), range(64)):
        writable = sum(1 << bit for i, bit in enumerate(fields) if pattern & (1 << i))
        e = fixture(0x406A + register * 256)
        e.r[register] = writable | 0xFFFE739F  # also attempt every fixed/reserved bit
        verify(e, e.fr.copy(), e.sr, writable + 0x40001)
        e = fixture(0x006A + register * 256)
        e.fpscr = writable + 0x40001
        want = e.r.copy(); want[register] = e.fpscr
        verify(e, e.fr.copy(), e.sr, e.fpscr, want)
        transfers += 2
    for cause_v, cause_z, flag_v, flag_z in itertools.product(range(2), repeat=4):
        old = 0x40001 + cause_v * 65536 + cause_z * 32768 + flag_v * 64 + flag_z * 32
        for numerator, denominator in itertools.product([0, 0x80000000], repeat=2):
            e = fixture(0xFBA3); e.fpscr = old
            e.fr[11], e.fr[10] = numerator, denominator
            want = e.fr.copy(); want[11] = 0x7FBFFFFF
            verify(e, want, e.sr, 0x50041 + flag_z * 32)
            division += 1
        for op, quiet, other, reverse in itertools.product(
            [0xFBA4, 0xFBA5], [0x7F800001, 0x7FBFFFFF, 0xFF800001, 0xFFBFFFFF],
            [0, 0x80000000, 0x3F800000, 0xBF800000], range(2)
        ):
            e = fixture(op); e.fpscr = old
            e.fr[10], e.fr[11] = (quiet, other) if reverse else (other, quiet)
            status = (0x50041 + flag_z * 32) if op == 0xFBA5 else (0x40001 + flag_v * 64 + flag_z * 32)
            verify(e, e.fr.copy(), 0x3F2, status)
            comparison += 1
        for op, output in [(0xFBA0, 0x40000000), (0xFBA1, 0), (0xFBA2, 0x3F800000), (0xFBA3, 0x3F800000)]:
            e = fixture(op); e.fpscr = old
            want = e.fr.copy(); want[11] = output
            verify(e, want, e.sr, 0x40001 + flag_v * 64 + flag_z * 32)
            finite += 1
        for op, output in [(0xFBAE, 0x40000000), (0xFB4D, 0xBF800000), (0xFB5D, 0x3F800000), (0xFB2D, 0x3F800000)]:
            e = fixture(op); e.fpscr = old; e.fpul = 1
            if op == 0xFB5D: e.fr[11] = 0xBF800000
            want = e.fr.copy(); want[11] = output
            verify(e, want, e.sr, 0x40001 + flag_v * 64 + flag_z * 32)
            finite += 1
        e = fixture(0xFB3D); e.fpscr = old
        verify(e, e.fr.copy(), e.sr, 0x40001 + flag_v * 64 + flag_z * 32, want_fpul=1)
        finite += 1
        for op, sr in [(0xFBA4, 0x3F3), (0xFBA5, 0x3F2)]:
            e = fixture(op); e.fpscr = old
            verify(e, e.fr.copy(), sr, 0x40001 + flag_v * 64 + flag_z * 32)
            finite += 1
    for op, a, b in [(0xFBA3, 0, 0), (0xFBA5, 0x7FBFFFFF, 0x3F800000)]:
        e = fixture(op); e.fpscr = 0x40801; e.fr[10], e.fr[11] = a, b
        old_fr, old_sr = e.fr.copy(), e.sr
        try:
            e.instruction(0)
        except NotImplementedError:
            assert e.fr == old_fr and e.sr == old_sr and e.fpscr == 0x50841
            rejected += 1
        else:
            raise AssertionError('Enabled trap silently bypassed')
    for other in [0x7FC00000, 0x7FFFFFFF, 0x7F800000, 1]:
        e = fixture(0xFBA5); e.fr[10], e.fr[11] = 0x7FBFFFFF, other
        try:
            e.instruction(0)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('Unsupported operand accepted')
    results = []
    for seed in range(8):
        e = SelfTest(); e.r[8:15] = [0xA0000000 + seed * 16 + i for i in range(7)]
        saved = e.r[8:16].copy(); gbr = e.gbr
        want = application(e)
        # Original routine compares FR4 with its expected ROM literal29054.
        expected_write(want, 0x6418, 0x41CCCCCA, 4)
        expected_write(want, 0x641C, 0x41CCCCCA, 4)
        e.run(0x28DFC)
        assert e.r[0] == 0x55555555 and e.r[8:16] == saved and e.gbr == gbr
        assert application(e) == want and e.fpscr == 0x40001
        results.append(dict(result=e.r[0], fpscr=e.fpscr))
    report = dict(rom_sha256=hashlib.sha256(ECU).hexdigest(), scope=__doc__,
                  transfer_cases=transfers, zero_division_cases=division,
                  quiet_comparison_cases=comparison, finite_cause_cases=finite,
                  expected_rejections=rejected, original_selftest_returns=results)
    (ROOT / 'control-initialize-fpu-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(report)


if __name__ == '__main__':
    main()
