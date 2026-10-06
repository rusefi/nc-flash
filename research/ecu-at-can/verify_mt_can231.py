"""Original ECU MT CAN231 publication and actual TCU selector comparison.

Full RAM-level producers/packers execute unchanged. TX admission stops at
the real driver entry; no peripheral return or successful transmission is
invented. Scheduling, input sampling and PRHT reception remain unproved.
"""
import hashlib
import itertools
import json
from pathlib import Path

from sh_subset import SH

ROOT = Path(__file__).resolve().parents[2]
ECU = (ROOT / "examples/LFFEEE-stock.bin").read_bytes()
TCU = (ROOT / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ECU).hexdigest() == "7604cb21aefe7b7484da236aaead82cebaf94df2a6e1915f5ea8a087dae5cb08"
assert hashlib.sha256(TCU).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def w(e, address, value, size=1):
    e.write(0xFFFF0000 + address, value, size)


def r(e, address, size=1):
    return e.read(0xFFFF0000 + address, size)


def payload(e, address):
    return bytes(r(e, address + i) for i in range(8))


def seed(mode, configuration):
    e = SH(ECU)
    e.sr = 0xF0
    w(e, 0x734A, mode)
    w(e, 0x734C, configuration)
    w(e, 0x6AC4, 0x1234, 2)
    w(e, 0x6AC6, 0xA5)
    w(e, 0x6AC7, 0x5A)
    for i in range(8):
        w(e, 0x6B64 + i, 0x80 + i)
    return e


class DriverEntry(Exception):
    pass


class Admission(SH):
    def instruction(self, pc):
        if pc == 0x6A48:
            assert self.r[4] == 0x3793C
            raise DriverEntry
        return super().instruction(pc)


def main():
    source_cases = 0
    for raw, override, cfg, selector in itertools.product(
        range(256), [0, 1, 2], [0, 1, 2, 255], [0, 1, 3, 15]
    ):
        e = seed(0x40, cfg)
        w(e, 0x44A4, raw)
        w(e, 0x7002, override)
        w(e, 0x6AD2, int(selector == 1))
        w(e, 0x6AD4, int(selector == 3))
        e.run(0x411F0)
        e.run(0x412A2)
        combined = int(override == 1 or (selector in (1, 3) if cfg == 1 else not raw & 1))
        auxiliary = int(override == 1 or not raw & 0x40)
        for address, value in [(0x723A, combined), (0x7244, combined), (0x723E, auxiliary)]:
            assert r(e, address, 2) == value * 256 + (value ^ 255)
        assert e.sr & ~1 == 0xF0
        source_cases += 1

    producer_cases = 0
    for mode, neutral, auxiliary, first, second in itertools.product(
        [0, 0x40, 0x80, 0xC0], [0, 1, 2, 255], [0, 1, 2, 255],
        [0, 1, 2, 255], [0, 1, 2, 255]
    ):
        e = seed(mode, 0)
        for address, value in [(0x723A, neutral), (0x723E, auxiliary),
                               (0x8EBC, first), (0x8EBE, second)]:
            w(e, address, value)
        e.run(0x35BAA)  # Full producer calls all three MT builders.
        e.run(0x36DB0)  # Full packer, real interrupt-mask helpers.
        flags = 4 * (neutral == 1) + 2 * (auxiliary == 1) + int(first == 1 or second == 1)
        expected = bytes([255, flags, 255, 255, 0, 0, 0, 0]) if mode & 0x40 else bytes.fromhex("a55a123400000000")
        assert payload(e, 0x6B64) == expected and e.sr & ~1 == 0xF0
        producer_cases += 1

    pack_gate_cases = 0
    for mode, cfg in itertools.product(range(256), range(256)):
        e = seed(mode, cfg)
        e.run(0x36DB0)
        expected = bytes.fromhex("a55a123400000000") if mode & 0x40 or cfg == 0 else bytes(range(0x80, 0x88))
        assert payload(e, 0x6B64) == expected and e.sr & ~1 == 0xF0
        pack_gate_cases += 1

    admission_cases = 0
    for mode, cfg, counter in itertools.product(
        range(256), [0, 1, 2, 255], [0, 23, 24, 25, 65534, 65535]
    ):
        e = Admission(ECU)
        w(e, 0x734A, mode)
        w(e, 0x734C, cfg)
        w(e, 0x6B6C, counter, 2)
        attempted = False
        try:
            e.run(0x36D52)
        except DriverEntry:
            attempted = True
        incremented = (counter + 1) & 65535
        due = incremented >= 25
        assert attempted == bool(due and (mode & 0x40 or cfg == 0))
        assert r(e, 0x6B6C, 2) == (0 if due and not attempted else incremented)
        admission_cases += 1

    initialization_cases = 0
    for mode, cfg in itertools.product([0, 0x40, 0x80, 0xC0], [0, 1, 2, 255]):
        e = Admission(ECU)
        w(e, 0x734A, mode)
        w(e, 0x734C, cfg)
        w(e, 0x723A, 1)
        attempted = False
        try:
            e.run(0x36D40)  # Initializes FFFE, produces, packs, falls into service.
        except DriverEntry:
            attempted = True
        assert attempted == bool(mode & 0x40 or cfg == 0)
        assert r(e, 0x6B6C, 2) == (65535 if attempted else 0)
        if mode & 0x40:
            assert payload(e, 0x6B64) == bytes.fromhex("ff04ffff00000000")
        initialization_cases += 1

    lifecycle = []
    for mode, cfg in [(0x40, 0), (0x80, 1)]:
        e = Admission(ECU)
        w(e, 0x734A, mode)
        w(e, 0x734C, cfg)
        e.run(0x36DA8)
        for call in range(1, 26):
            attempted = False
            try:
                e.run(0x36D52)
            except DriverEntry:
                attempted = True
            assert attempted == (call == 25 and mode == 0x40)
            assert r(e, 0x6B6C, 2) == (0 if call == 25 and not attempted else call)
        lifecycle.append({"mode": mode, "configuration": cfg, "service_calls": 25,
                          "driver_reached": attempted, "counter": r(e, 0x6B6C, 2)})

    paired_cases = 0
    samples = []
    for mask, mode, cfg, raw, override in itertools.product(
        range(16), [0x40, 0x80], [0, 1, 2], [0, 1, 0x40, 0x41], [0, 1]
    ):
        t = SH(TCU)
        for i in range(4):
            w(t, 0x88B4 + i, (mask >> i) & 1)
        t.run(0x22416)
        t.run(0x19414, 1)
        wire = payload(t, 0x8EED)
        e = seed(mode, cfg)
        for i, value in enumerate(wire):
            w(e, 0x6ABC + i, value)
        w(e, 0x44A4, raw)
        w(e, 0x7002, override)
        for fn in [0x35BB8, 0x3585C, 0x411F0, 0x412A2, 0x35BAA, 0x36DB0]:
            e.run(fn)
        accepted = not mode & 0x40 and cfg == 1
        # For inconsistent MT+cfg1 fixtures, normalizer skips its update;
        # the seeded (zero) selector flags are what411F0 actually reads.
        combined = int(override == 1 or (
            (accepted and wire[0] & 15 in (1, 3)) if cfg == 1 else not raw & 1))
        assert r(e, 0x723A) == combined
        if mode & 0x40:
            auxiliary = int(override == 1 or not raw & 0x40)
            expected = bytes([255, 4 * combined + 2 * auxiliary, 255, 255, 0, 0, 0, 0])
        elif cfg == 0:
            expected = bytes.fromhex("a55a123400000000")
        else:
            expected = bytes(range(0x80, 0x88))
        assert payload(e, 0x6B64) == expected and e.sr & ~1 == 0xF0
        if mask in (1, 2, 4, 8) and raw == 0x41 and override == 0 and cfg in (0, 1):
            samples.append({"tcu_input_mask": mask, "mode": mode, "configuration": cfg,
                            "tcu231": wire.hex(), "ecu_combined": combined,
                            "ecu231_buffer": expected.hex(),
                            "ecu_publish_gate": bool(mode & 0x40 or cfg == 0)})
        paired_cases += 1

    print(json.dumps({
        "ecu_sha256": hashlib.sha256(ECU).hexdigest(),
        "tcu_sha256": hashlib.sha256(TCU).hexdigest(),
        "source_cases": source_cases, "mt_producer_cases": producer_cases,
        "pack_gate_cases": pack_gate_cases, "tx_admission_cases": admission_cases,
        "initialization_cases": initialization_cases, "countdown_lifecycles": lifecycle,
        "paired_tcu_ecu_cases": paired_cases, "samples": samples,
        "limits": ["Explicit scheduling and RAM fixtures", "No physical switch sampling",
                   "TX admission stops before driver6A48", "No PRHT receiver/capture",
                   "Physical transmission-type signal remains unproved"],
    }, indent=2))


if __name__ == "__main__":
    main()
