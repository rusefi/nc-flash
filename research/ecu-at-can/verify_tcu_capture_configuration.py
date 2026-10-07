"""Original capture A/B enable and caller slice, using strict existing latches.

Independent whole-RAM and exact ordered-MMIO models. Compatible SH7055S
clock interpretation is separate; no counter progression, pin or IRQ model.
"""
import hashlib
import json
import random
from pathlib import Path
from verify_tcu_timer_configuration import ConfigurationRegisters, WIDTHS
from verify_can201_byte6 import TCU
from verify_control_acquisition_schedule import execute_slice


def fixture(seed):
    t = ConfigurationRegisters(TCU)
    t.configuring = True
    rng = random.Random(seed)
    t.configuration = {a: rng.randrange(1 << (8*n)) for a, n in WIDTHS.items()}
    t.configuration[0xF42A] = seed
    t.configuration[0xF42E] = seed % 32
    t.configuration[0xF401] = (seed*73) % 256
    t.configuration_trace = []
    t.sr = (seed % 16)*16 | (seed & 1) | ((seed & 6) << 7)
    for a in range(0xFFFF8000, 0xFFFF8100):
        t.write(a, rng.randrange(256), 1)
    return t


def model(registers, trace, channel):
    def rmw(a, size, keep, set_bits):
        value = registers[a]
        trace.append(('read', a, size, value))
        value = (value & keep) | set_bits
        registers[a] = value
        trace.append(('write', a, size, value))
    bit = 1 if channel == 'A' else 4
    rmw(0xF42A, 1, 255, bit)
    rmw(0xF42A, 1, 255 ^ (bit*2), 0)
    rmw(0xF42E, 2, 65535, 1 if channel == 'A' else 2)
    rmw(0xF401, 1, 255, 1)


def main():
    components = callers = prescalers = 0
    for seed in range(256):
        for channel, entry in [('A', 0x16C5C), ('B', 0x16B24)]:
            t = fixture(seed)
            want, trace = t.configuration.copy(), []
            model(want, trace, channel)
            memory, saved, sr = t.ram.copy(), t.r[8:].copy(), t.sr
            t.run(entry)
            assert t.configuration == want and t.configuration_trace == trace
            assert t.ram == memory and t.r[8:] == saved and t.sr == sr
            components += 1
        t = fixture(seed)
        want, trace = t.configuration.copy(), []
        model(want, trace, 'A')
        model(want, trace, 'B')
        memory, saved, sr = t.ram.copy(), t.r[8:].copy(), t.sr
        saved[6] = 2  # Original caller's delay-slot assignment to R14.
        execute_slice(t, 0x12324, 0x12330)
        assert t.configuration == want and t.configuration_trace == trace
        assert t.ram == memory and t.r[8:] == saved and t.sr == sr
        callers += 1
        t = fixture(seed)
        memory, registers, sr = t.ram.copy(), t.r[8:].copy(), t.sr
        want = t.configuration.copy()
        for a in [0xF404, 0xF406, 0xF408, 0xF40A]:
            want[a] = 1
        t.run(0x1448E)
        assert t.configuration == want
        assert t.configuration_trace == [('write', a, 1, 1) for a in [0xF404, 0xF406, 0xF408, 0xF40A]]
        assert t.ram == memory and t.r[8:] == registers and t.sr == sr
        prescalers += 1
    rejected = 0
    for address, size in [(0xFFFFF42A, 2), (0xFFFFF42E, 1), (0xFFFFF401, 2)]:
        for write in [False, True]:
            t = fixture(0)
            before = t.configuration.copy()
            try:
                t.write(address, 0, size) if write else t.read(address, size)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError('unsupported register width accepted')
            assert t.configuration == before and not t.configuration_trace
    result = dict(status='PASS', scope=__doc__, original_enable_cases=components,
        original_caller_cases=callers, original_prescaler_cases=prescalers,
        rejected_accesses=rejected, caller_accesses=16,
        rom_sha256=hashlib.sha256(TCU).hexdigest(),
        clock_interpretation='Compatible PSCR1=1 and channel0 direct phi-prime imply Pphi/2; ICR0A/B capture same32-bit TCNT0.',
        source_pages_zero=[240, 241, 262, 266, 267, 277, 278, 318, 370],
        limits='Caller12324..12330 only; no readiness gates/fullreset/clockprogress/physicaledges/hardwareIRQ.')
    Path(__file__).with_name('tcu-capture-configuration-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result)


if __name__ == '__main__':
    main()
