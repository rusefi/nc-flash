"""Original timestamp counter start/read with strict documented access widths.

Software register samples only. Preserve the original counter-reset word-write
conflict with the compatible SH7055S manual instead of inventing its behavior.
"""
import hashlib
import json
import random
from pathlib import Path

import verify_tcu_capture_configuration as config
from verify_can201_byte6 import TCU
from verify_control_acquisition_schedule import execute_slice

ROOT = Path(__file__).resolve().parent


class TimestampRegisters(config.ConfigurationRegisters):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if 0xFFFFF6C0 <= address < 0xFFFFF6C4:
            if address != 0xFFFFF6C0 or size != 4:
                raise ValueError('TCNT10A requires longword access in retained manual')
            self.timestamp_trace.append(('read', address, size, self.timestamp))
            return self.timestamp
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if 0xFFFFF6C0 <= address < 0xFFFFF6C4:
            if address != 0xFFFFF6C0 or size != 4:
                raise ValueError('TCNT10A requires longword access in retained manual')
            raise ValueError('Counter writes are outside this read/start fixture')
        return super().write(address, value, size)


def fixture(seed):
    t = config.fixture(seed)
    t.__class__ = TimestampRegisters
    t.timestamp = 0
    t.timestamp_trace = []
    return t


def word_reference_candidates(target):
    found = []
    for pc in range(0x10000, len(TCU)-2, 2):
        op = int.from_bytes(TCU[pc:pc+2], 'big')
        if op >> 12 != 9:
            continue
        literal = pc+4+2*(op & 255)
        if int.from_bytes(TCU[literal:literal+2], 'big') == target:
            found.append(dict(pc=hex(pc), literal=hex(literal)))
    return found


def main():
    starts = reads = rejects = 0
    for seed in range(256):
        t = fixture(seed)
        memory, saved, sr = t.ram.copy(), t.r[8:].copy(), t.sr
        before = t.configuration.copy()
        old = before[0xF401]
        before[0xF401] = old | 128
        t.run(0x15544)
        assert t.configuration == before
        assert t.configuration_trace == [('read', 0xF401, 1, old),
                                          ('write', 0xF401, 1, old | 128)]
        assert t.ram == memory and t.r[8:] == saved and t.sr == sr
        assert not t.timestamp_trace
        starts += 1
    rng = random.Random(0x15730)
    samples = [0, 1, 65535, 65536, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF]
    samples += [rng.randrange(1 << 32) for _ in range(1016)]
    for index, sample in enumerate(samples):
        t = fixture(index & 255)
        t.timestamp = sample
        memory, saved, sr = t.ram.copy(), t.r[8:].copy(), t.sr
        before = t.configuration.copy()
        t.run(0x15730)
        assert t.r[0] == sample
        assert t.timestamp_trace == [('read', 0xFFFFF6C0, 4, sample)]
        assert t.configuration == before and not t.configuration_trace
        assert t.ram == memory and t.r[8:] == saved and t.sr == sr
        reads += 1
    for address, size in [(0xFFFFF6C0, 1), (0xFFFFF6C0, 2), (0xFFFFF6C2, 2)]:
        for writing in [False, True]:
            t = fixture(0)
            try:
                t.write(address, 0, size) if writing else t.read(address, size)
            except ValueError:
                rejects += 1
            else:
                raise AssertionError('Unsupported counter width accepted')
            assert not t.timestamp_trace and not t.configuration_trace
    # Original initializer's precise conflicting access. Do not permit it just
    # because doing so would allow a full boot fixture to proceed.
    t = fixture(0)
    t.r[4] = 0
    try:
        execute_slice(t, 0x1465C, 0x14664)
    except ValueError as error:
        conflict = dict(instruction='0x1465e', address='0xfffff6c2', size=2,
                        value=0, exception=str(error))
    else:
        raise AssertionError('Expected undocumented reset access was accepted')
    assert not t.timestamp_trace
    result = dict(status='PASS', scope=__doc__, starts=starts, reads=reads,
        rejected_widths=rejects, retained_reset_width_conflict=conflict,
        rom_sha256=hashlib.sha256(TCU).hexdigest(),
        word_literal_candidates={hex(a): word_reference_candidates(a)
            for a in [0xF6C0, 0xF6C2, 0xF6E2, 0xF6E4]},
        source_pages_zero=[248, 262, 266, 377, 386, 388, 395],
        limits='No counter progression/reset-write semantics/fullboot. PSCR4=1 supports conditional Pphi/2 only if documented channel10 mapping applies and TI10 clear input is disabled.')
    (ROOT/'tcu-timestamp-configuration-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(dict(status='PASS', starts=starts, reads=reads, rejected_widths=rejects,
               reset_width_conflict='preserved'))


if __name__ == '__main__':
    main()
