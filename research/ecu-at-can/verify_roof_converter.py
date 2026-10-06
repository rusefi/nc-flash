"""Bounded execution of the public Openhoonage NC 1.01 selector builder.

AVR byte PCs 0x19c4..0x1a26 only: body after stack setup, stopping BEFORE
the SPI sender call. This is not an AVR system or roof-controller emulator.
Unsupported instructions/branches/memory fail closed. See roof-aftermarket.txt.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parent
HEX_SHA = "b45768a97782aacadb5f6216f5b6e07c3a9e6214e01b316043eaf38ab550d48f"
BIN_SHA = "23fbf7ce002e574364030a156660c1e6dcff6f61643565538ceda8e3e5a9f56b"


def read_hex():
    raw = (ROOT / "roof/nc_cc_1_01.hex").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == HEX_SHA
    memory = {}
    eof = False
    for line in raw.decode("ascii").splitlines():
        assert line.startswith(":") and not eof
        record = bytes.fromhex(line[1:])
        assert len(record) == record[0] + 5 and sum(record) % 256 == 0
        address = int.from_bytes(record[1:3], "big")
        if record[3] == 0:
            for offset, value in enumerate(record[4:-1]):
                assert address + offset not in memory
                memory[address + offset] = value
        else:
            assert record == bytes.fromhex("00000001ff")
            eof = True
    assert eof and min(memory) == 0 and len(memory) == max(memory) + 1
    binary = bytes(memory[i] for i in range(len(memory)))
    assert len(binary) == 29172 and hashlib.sha256(binary).hexdigest() == BIN_SHA
    return binary


def signed(value, bits):
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def selector_body(binary, selector, gear, scratch=0xA5):
    registers = [0] * 32
    registers[28:30] = [0, 6]  # Synthetic Y frame at SRAM 0x600.
    memory = {0x600 + i: scratch for i in range(1, 17)}
    memory.update({0x272: selector, 0x273: gear})
    carry = zero = None
    pc = 0x19C4
    for _ in range(100):
        if pc == 0x1A26:
            assert binary[pc:pc + 4] == bytes.fromhex("0e94b308")
            return bytes(registers[8:24]), registers[24] | registers[25] << 8
        assert 0x19C4 <= pc < 0x1A26 and pc % 2 == 0
        opcode = int.from_bytes(binary[pc:pc + 2], "little")
        pc += 2
        register = (opcode >> 4) & 31
        immediate = ((opcode >> 4) & 0xF0) | (opcode & 15)
        if opcode & 0xF000 == 0xE000:  # LDI
            registers[16 + ((opcode >> 4) & 15)] = immediate
        elif opcode & 0xF000 == 0x3000:  # CPI: only C/Z consumed here.
            value = registers[16 + ((opcode >> 4) & 15)]
            carry, zero = value < immediate, value == immediate
        elif opcode & 0xFE0F == 0x9000:  # LDS, full 16-bit direct address.
            address = int.from_bytes(binary[pc:pc + 2], "little")
            pc += 2
            assert address in (0x272, 0x273)
            registers[register] = memory[address]
        elif opcode & 0xD208 in (0x8008, 0x8208):  # LDD/STD Y+q
            displacement = (opcode & 7) | ((opcode >> 7) & 0x18) | ((opcode >> 8) & 0x20)
            address = (registers[28] | registers[29] << 8) + displacement
            assert 0x601 <= address <= 0x610
            if opcode & 0x0200:
                memory[address] = registers[register]
            else:
                registers[register] = memory[address]
        elif opcode & 0xFC00 == 0xF400:  # BRBC: only BRCC/BRNE.
            bit = opcode & 7
            assert bit in (0, 1)
            flag = carry if bit == 0 else zero
            assert flag is not None
            if not flag:
                pc += 2 * signed((opcode >> 3) & 0x7F, 7)
        elif opcode & 0xF000 == 0xC000:  # RJMP
            pc += 2 * signed(opcode & 0xFFF, 12)
        else:
            raise ValueError(f"Unsupported opcode {opcode:04x} at {pc - 2:04x}")
    raise AssertionError("Instruction budget exceeded")


def verify(binary):
    digest = hashlib.sha256()
    samples = []
    for selector in range(256):
        for gear in range(256):
            actual, interface = selector_body(binary, selector, gear)
            first = selector if selector < 5 else 4 if selector in (5, 6) else 0
            second = {5: 0x80, 6: 0x40}.get(selector, 0)
            expected = bytes([0x31, 2, 0, 0, 0, 0xA5, 0xA5, 8,
                              first, second, 0, 0, 0, 0, 0, gear])
            assert actual == expected and interface == 0x32E
            digest.update(actual)
            if gear == 2 and selector in range(8):
                samples.append({"selector": selector, "gear": gear,
                                "payload": actual[8:].hex()})
    # The builder leaves record bytes5/6 untouched; do not silently zero them.
    for scratch in (0, 0xFF):
        for selector in range(256):
            actual, _ = selector_body(binary, selector, 6, scratch)
            assert actual[5:7] == bytes([scratch, scratch])
    rejected = 0
    for address, replacement in [(0x19C4, b"\xff\xff"),
                                 (0x19C4, b"\x01\xf4"),
                                 (0x19DE, b"\x74\x02"),
                                 (0x19C4, b"\xff\xc7")]:
        altered = bytearray(binary)
        altered[address:address + 2] = replacement
        try:
            selector_body(altered, 1, 2)
        except (AssertionError, ValueError):
            rejected += 1
        else:
            raise AssertionError("Unsupported fixture unexpectedly passed")
    labels = {1: 0xB0F, 2: 0xB07, 3: 0xAFF, 4: 0xAF8, 5: 0xAF0, 6: 0xAEC}
    names = {}
    for state, address in labels.items():
        names[state] = binary[address:binary.index(0, address)].decode("ascii").strip()
    assert list(names.values()) == ["Park", "Reverse", "Neutral", "Drive", "Manual", "AT"]
    return {
        "artifact": "Openhoonage NC Cluster Commander 1.01 (aftermarket, not Mazda PRHT)",
        "hex_sha256": HEX_SHA, "binary_sha256": BIN_SHA, "binary_size": len(binary),
        "execution": "AVR byte PC19c4 through 1a26; stops before sender1166",
        "selector_gear_cases": 65536, "scratch_preservation_cases": 512,
        "expected_fail_closed_rejections": rejected,
        "record_digest_sha256": digest.hexdigest(), "samples": samples,
        "static_menu_labels": names,
        "limits": ["No SPI/CAN/PRHT execution", "No prologue or scheduler execution",
                   "Record bytes5/6 are uninitialized in this builder",
                   "Menu label cross-references reviewed statically in roof/converter-excerpts.txt",
                   "P/N agreement is independent corroboration, not OEM receiver proof"],
    }


def excerpts(binary, objdump):
    spans = [(0xD3A, 0xD48), (0x110E, 0x1302), (0x17EC, 0x18D0),
             (0x199C, 0x1A50), (0x24E6, 0x250E), (0x258A, 0x263E)]
    result = ["Openhoonage NC CC 1.01; AVR5; byte addresses; static excerpts.\n"]
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "nc_cc_1_01.bin"
        path.write_bytes(binary)
        for start, end in spans:
            output = subprocess.check_output(
                [objdump, "-D", "-b", "binary", "-m", "avr5",
                 f"--start-address={start}", f"--stop-address={end}", str(path)], text=True)
            result.append(output.replace(str(path), "nc_cc_1_01.bin"))
    (ROOT / "roof/converter-excerpts.txt").write_text("\n".join(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objdump", help="Optionally regenerate tracked disassembly excerpts")
    args = parser.parse_args()
    binary = read_hex()
    result = verify(binary)
    if args.objdump:
        excerpts(binary, args.objdump)
    print(json.dumps(result, indent=2))
