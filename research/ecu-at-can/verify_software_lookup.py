"""Verify added ISA and every u16 input of stock TCU cut-threshold lookup."""
import hashlib
import itertools
import json
from pathlib import Path

from sh_software_arithmetic import SHSoftwareArithmetic

ROM = (Path(__file__).resolve().parents[2] / "examples/LFG1TF000.bin").read_bytes()
assert hashlib.sha256(ROM).hexdigest() == "8fb064e91dd2590a30189d70874f5607350812e6c8f98f6e4a132085c4a808d6"


def expected_curve(x):
    if x < 2560:
        return 8960
    if x < 10240:
        return 8960 - (1280*(x-2560)//7680)
    if x < 15360:
        return 7680 - (512*(x-10240)//5120)
    return 7168


def main():
    isa = 0
    values = [0, 1, 0x12345678, 0x89ABCDEF, 0xFFFFFFFF] + [1 << bit for bit in range(32)]
    for operation, value, incoming, n in itertools.product([0x4005, 0x4025], values, range(2), [0, 2, 15]):
        t = SHSoftwareArithmetic((operation | (n << 8)).to_bytes(2, "big"))
        t.r[n], t.sr = value, 0x3F0 | incoming
        bits = f"{value:032b}"
        expected = int((str(incoming) if operation == 0x4025 else bits[-1])+bits[:-1], 2)
        assert t.instruction(0) == (2, False)
        assert t.r[n] == expected and t.sr == 0x3F0 | int(bits[-1])
        isa += 1
    for value, n, m, flag in itertools.product(values, [0, 2, 15], [0, 2, 15], range(2)):
        t = SHSoftwareArithmetic((0x6009 | (n << 8) | (m << 4)).to_bytes(2, "big"))
        t.r[m], t.sr = value, 0x3F0 | flag
        before = t.r.copy()
        data = value.to_bytes(4, "big")
        before[n] = int.from_bytes(data[2:]+data[:2], "big")
        assert t.instruction(0) == (2, False)
        assert t.r == before and t.sr == 0x3F0 | flag
        isa += 1
    for flag in [0, 1, 0x3F0, 0x3F1, 0xFFFFFFFF]:
        t = SHSoftwareArithmetic(bytes.fromhex("0008"))
        t.sr = flag
        before = t.r.copy()
        assert t.instruction(0) == (2, False)
        assert t.sr == flag & ~1 and t.r == before
        isa += 1

    assert ROM[0x703C0:0x703C9].hex() == "040a283c64231e1c1c"
    t = SHSoftwareArithmetic(ROM)
    digest = hashlib.sha256()
    examples = []
    for x in range(65536):
        t.r[5] = 0x703C0
        actual = t.run(0x10764, x)
        assert actual == expected_curve(x), (x, actual, expected_curve(x))
        digest.update(actual.to_bytes(2, "big"))
        if x in [0, 2559, 2560, 2561, 2565, 2566, 5000, 10239, 10240, 10241, 15359, 15360, 25599, 25600, 65535]:
            examples.append({"axis": x, "threshold": actual})
    print(json.dumps({"scope": __doc__, "isa_cases": isa, "stock_curve_u16_cases": 65536,
                      "outputs_be16_sha256": digest.hexdigest(), "examples": examples,
                      "limits": "Original software arithmetic executed, no helper stubs. This curve's bounded operands do not validate arbitrary software-double operations or physical units."}, indent=2))


if __name__ == "__main__":
    main()
