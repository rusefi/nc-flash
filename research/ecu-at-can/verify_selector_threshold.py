"""Execute TCU diagnostic scaling and the resulting selector fault CAN path.

Starts at application words932C/932E, not at capture hardware. Upstream
arithmetic remains a static trace; unsupported instructions fail explicitly.
"""
import hashlib
import json
from pathlib import Path

from sh_subset import SH

ROOT = Path(__file__).resolve().parents[2]
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"


def w(t, a, v, n=1):
    t.write(0xFFFF0000+a, v, n)


def r(t, a, n=1):
    return t.read(0xFFFF0000+a, n)


class CaptureRegisters(SH):
    """Explicit read/write fixtures for three initialization registers only."""
    def __init__(self, mode):
        super().__init__(TCU)
        self.registers = {0xFFFFF42A: [1, mode], 0xFFFFF42E: [2, 0xAAAA],
                          0xFFFFF401: [1, 0x54]}

    def read(self, addr, size):
        if addr in self.registers:
            assert size == self.registers[addr][0]
            return self.registers[addr][1]
        return super().read(addr, size)

    def write(self, addr, value, size):
        if addr in self.registers:
            assert size == self.registers[addr][0]
            self.registers[addr][1] = value & ((1 << (8*size))-1)
            return
        super().write(addr, value, size)


for mode in range(256):
    t = CaptureRegisters(mode)
    t.run(0x16C5C)
    assert t.registers == {0xFFFFF42A: [1, (mode | 1) & 0xFD],
                           0xFFFFF42E: [2, 0xAAAB], 0xFFFFF401: [1, 0x55]}


# Exhaustive u16 domain, opposite inputs verify independent channels and
# byte-sized status copy. No ROM or interpreter substitutions are used.
t = SH(TCU)
for raw in range(65536):
    w(t, 0x932E, raw, 2)
    w(t, 0x932C, 65535-raw, 2)
    w(t, 0xA4FA, raw & 255)
    t.run(0x50F26)
    assert r(t, 0x80BA, 2) == raw*10//256
    assert r(t, 0x80A4, 2) == (65535-raw)*10//256
    assert r(t, 0xA4FC) == raw & 255
    assert (r(t, 0x80BA, 2) >= 300) == (raw >= 7680)

# With no selector input, the first timer is explicitly already expired.
# At/above raw7680 the second countdown arms; its expiry is then supplied
# as a fixture. Actual timer execution was verified in selector-recovery.
examples = []
for raw in [0, 7678, 7679, 7680, 7681, 32767, 32768, 65280, 65535]:
    for expired in [False, True]:
        t, e = SH(TCU), SH(ECU)
        t.run(0x5327C)
        t.run(0x5853C)
        w(t, 0xA938, 1)
        w(t, 0xA962, 1)
        w(t, 0x843E, 0, 2)
        w(t, 0x8440, 0 if expired else 65535, 2)
        w(t, 0x932E, raw, 2)
        for fn in [0x50F26, 0x58548]:
            t.run(fn)
        t.run(0x56908, 0x16)
        for fn in [0x570F6, 0x21C1C, 0x22416]:
            t.run(fn)
        t.run(0x19414, 1)
        active = expired and raw >= 7680
        expected_timer = (0 if expired else 28000) if raw >= 7680 else 65535
        assert r(t, 0x8440, 2) == expected_timer
        assert r(t, 0xA702) == (4 if active else 2)
        assert r(t, 0x8EED) == (0xFF if active else 0x10)
        w(e, 0x734A, 0x80)
        w(e, 0x734C, 1)
        for i in range(8):
            w(e, 0x6ABC+i, r(t, 0x8EED+i))
        for fn in [0x35BB8, 0x3585C, 0x411F0]:
            e.run(fn)
        assert r(e, 0x723A, 2) == 0xFF
        examples.append({"raw_932e": raw, "scaled_80ba": r(t, 0x80BA, 2),
                         "timer_fixture_expired": expired, "timer_8440": r(t, 0x8440, 2),
                         "group16_active": r(t, 0xA702), "can231_byte0": r(t, 0x8EED),
                         "ecu_combined_flag": r(e, 0x723A)})

# Preserve exact execution limits rather than mocking arithmetic helpers.
unsupported = []
for start, message in [(0x22DDC, "Opcode 212F at 00022DFE"),
                       (0x5AF44, "Opcode 0019 at 0005AF4C")]:
    t = SH(TCU)
    t.r[0], t.r[1] = 10, 100
    try:
        t.run(start)
    except NotImplementedError as exc:
        assert str(exc) == message
        unsupported.append({"start": hex(start), "stop": str(exc)})
    else:
        raise AssertionError("Expected strict-harness boundary changed; reassess scope")

print(json.dumps({"scope": __doc__.strip(), "capture_initialization_cases": 256,
                  "exhaustive_scaling_cases": 65536,
                  "paired_threshold_examples": examples, "unsupported_upstream": unsupported,
                  "limits": "No full capture-to-CAN execution, physical units, pin naming, timer clocks, or PRHT/DSC controller interpretation."}, indent=2))
