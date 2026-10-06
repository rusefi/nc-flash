"""Execute ECU serial input/filter code with explicit peripheral read fixtures.

No serial chip, interrupt timing, watchdog or electrical simulation. All called
ROM functions execute; status readiness and received bytes are test inputs.
"""
import itertools
import json
from pathlib import Path

from sh_subset import SH
from verify_mt_can231 import ECU, w, r, payload


class InputSamples(SH):
    WIDTHS = {**{0xFFFFF000 + i: 1 for i in range(7)},
              **{0xFFFF0000 + a: 2 for a in (0xF72C, 0xF764, 0xF746, 0xF74E)}}

    def __init__(self):
        super().__init__(ECU)
        self.registers = dict.fromkeys(self.WIDTHS, 0)
        self.banks = [0, 0, 0]
        self.delay_polls = 0
        self.pending_polls = 0
        self.polls = 0
        self.accesses = []

    def read(self, address, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            if self.WIDTHS.get(address) != size:
                raise ValueError(f"Unsupported peripheral read {address:08X}/{size}")
            value = self.registers[address]
            if address == 0xFFFFF004:
                # Explicit sampled SSR, not a storage-register emulation.
                value = 0x80
                if self.pc == 0x78CA:
                    self.polls += 1
                    if self.pending_polls:
                        self.pending_polls -= 1
                    else:
                        value |= 0x40
            elif address == 0xFFFFF005:
                selected = self.registers[0xFFFFF72C] & 0xC000
                bank = {0: 0, 0x4000: 1, 0x8000: 2}[selected]
                value = self.banks[bank]
            self.accesses.append(("read", address, value, size))
            return value
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if address >= 0xFFFFE000:
            if (self.WIDTHS.get(address) != size or
                    address in (0xFFFFF005, 0xFFFFF746, 0xFFFFF74E)):
                raise ValueError(f"Unsupported peripheral write {address:08X}/{size}")
            value &= (1 << (8 * size)) - 1
            self.accesses.append(("write", address, value, size))
            self.registers[address] = value
            if address == 0xFFFFF003:
                self.pending_polls = self.delay_polls
            return
        super().write(address, value, size)


def majority(old, previous, current, bits):
    # Independent per-bit voting oracle, rather than the ROM's bitwise formula.
    return sum((sum((value >> i) & 1 for value in (old, previous, current)) >= 2)
               << i for i in range(bits))


def main():
    serial_cases = 0
    for bank, value, delay in itertools.product([0, 1, 2, 255], range(256), [0, 3]):
        e = InputSamples()
        e.sr = 0xF0
        e.banks = [value] * 3
        e.delay_polls = delay
        e.registers[0xFFFFF72C] = 0xA55A
        e.registers[0xFFFFF764] = 0x5555
        assert e.run(0x76B4, bank) & 255 == value
        selected = 0 if bank == 0 else 0x4000 if bank == 1 else 0x8000
        assert e.registers[0xFFFFF72C] == (0x255A | selected)
        assert e.registers[0xFFFFF764] == 0x5555
        assert e.registers[0xFFFFF000] == 0x80
        assert e.registers[0xFFFFF001] == 4
        assert e.registers[0xFFFFF002] == 0x30
        assert e.registers[0xFFFFF006] == 0xF2
        assert e.registers[0xFFFFF003] == 255
        assert e.polls == delay + 1 and e.sr & ~1 == 0xF0
        assert {0x786E, 0x794C, 0xE744, 0x22E4, 0x22F4, 0x3880, 0x3894} <= e.visited
        assert [(a, v) for kind, a, v, _ in e.accesses
                if kind == "write" and a == 0xFFFFF764] == [
                    (0xFFFFF764, 0x5554), (0xFFFFF764, 0x5555)]
        serial_cases += 1

    initialization_cases = 0
    for value, threshold in itertools.product(range(256), [0, 0x7FFF, 0x8000, 0xFFFF]):
        e = InputSamples()
        e.banks = [17, value, value ^ 255]
        e.registers[0xFFFFF746] = value * 257
        e.registers[0xFFFFF74E] = (value ^ 255) * 257
        w(e, 0x401C, threshold, 2)
        w(e, 0x44B0, 0xA5)
        e.run(0xCA94)
        for a, b, expected, width in [
            (0x44A0, 0x44AA, value * 257, 2),
            (0x44A2, 0x44AC, (value ^ 255) * 257, 2),
            (0x44A4, 0x44AE, value, 1), (0x44A5, 0x44AF, value ^ 255, 1),
            (0x44A6, 0x44A8, int(threshold >= 0x8000), 2),
        ]:
            assert r(e, a, width) == r(e, b, width) == expected
        assert r(e, 0x44B0) == 0xA5 and e.polls == 2
        initialization_cases += 1

    filter_cases = 0
    # All eight truth-table combinations at each bit, with distinct neighboring
    # patterns; both GPIO words and both serial bytes run in the full caller.
    for bit, old, previous, current, changed in itertools.product(
            range(16), [0, 1], [0, 1], [0, 1], [False, True]):
        e = InputSamples()
        mask = 1 << bit
        a = (0xA55A & ~mask) | (old << bit)
        b = (0x5AA5 & ~mask) | (previous << bit)
        c = (0xAA55 & ~mask) | (current << bit)
        e.banks = [0, c & 255, (c ^ 0xFFFF) & 255]
        e.registers[0xFFFFF746] = c
        e.registers[0xFFFFF74E] = c ^ 0xFFFF
        channels = [(0x44A0, 0x44AA, 2, False), (0x44A2, 0x44AC, 2, True),
                    (0x44A4, 0x44AE, 1, False), (0x44A5, 0x44AF, 1, True)]
        for filtered, raw, width, invert in channels:
            w(e, filtered, a ^ (0xFFFF if invert else 0), width)
            w(e, raw, b ^ (0xFFFF if invert else 0), width)
        w(e, 0x44A6, old, 2)
        w(e, 0x44A8, previous, 2)
        w(e, 0x401C, current << 15, 2)
        w(e, 0x44B0, 9)
        w(e, 0x4004, 10 if changed else 9)
        e.run(0xCADE)
        expected = majority(a, b, c, 16)
        for filtered, raw, width, invert in channels:
            width_mask = (1 << (width * 8)) - 1
            assert r(e, filtered, width) == (expected ^ (0xFFFF if invert else 0)) & width_mask
            assert r(e, raw, width) == (c ^ (0xFFFF if invert else 0)) & width_mask
        assert r(e, 0x44A6, 2) == (int(old + previous + current >= 2) if changed else old)
        assert r(e, 0x44A8, 2) == (current if changed else previous)
        assert r(e, 0x44B0) == (10 if changed else 9)
        filter_cases += 1

    e = InputSamples()
    e.banks = [0, 0xFF, 0xFF]
    e.run(0xCA94)
    w(e, 0x734A, 0x40)
    w(e, 0x734C, 0)
    trace = []
    old = previous = 255
    for sample in [255, 254, 255, 254, 254, 190, 190, 255, 255]:
        e.banks[1] = sample
        e.run(0xCADE)
        old = majority(old, previous, sample, 8)
        previous = sample
        for entry in (0x411F0, 0x412A2, 0x35BAA, 0x36DB0):
            e.run(entry)
        flags = (4 if not old & 1 else 0) | (2 if not old & 64 else 0)
        assert payload(e, 0x6B64) == bytes([255, flags, 255, 255, 0, 0, 0, 0])
        trace.append({"serial_byte": sample, "filtered_byte": old,
                      "can231": payload(e, 0x6B64).hex()})

    rejected = 0
    for operation in [lambda e: e.read(0xFFFFF007, 1),
                      lambda e: e.read(0xFFFFF005, 2),
                      lambda e: e.write(0xFFFFF005, 1, 1),
                      lambda e: e.write(0xFFFFF746, 1, 2)]:
        try:
            operation(InputSamples())
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Unsupported peripheral access accepted")
    e = InputSamples()
    e.delay_polls = 100000
    try:
        e.run(0x76B4, 1, limit=2000)
    except RuntimeError as error:
        assert "Instruction limit" in str(error) and 0x78CA <= e.pc <= 0x78D2
        assert not any(kind == "read" and a == 0xFFFFF005 for kind, a, _, _ in e.accesses)
    else:
        raise AssertionError("Serial wait unexpectedly returned")

    result = {"serial_cases": serial_cases, "initialization_cases": initialization_cases,
              "full_filter_cases": filter_cases, "input_to_can231_trace": trace,
              "rejected_accesses": rejected, "not_ready_stays_in_poll_loop": True,
              "scope": "Original ROM code with sampled peripheral inputs; no hardware timing or OEM PRHT receiver proof."}
    Path(__file__).with_name("local-inputs-verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
