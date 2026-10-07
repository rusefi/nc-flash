"""Execute original 6CFD8 report selection and real 8FAC8/cache callees.

Whole-application-RAM oracle covers cache-only paths: global gate not exactly
one, or runtime mask without stock groups' 0x8000 admission bit. No stored-DTC,
physical signal identity, external-controller or real cadence claim.
"""
import hashlib
import itertools
import json
from pathlib import Path
from sh_control_task import ControlTaskArithmetic
from verify_control_contributions import ECU, r, w
from verify_control_raw_inputs import application, expected_write

ROOT = Path(__file__).resolve().parent


def reports(e):
    if r(e, 0x8EFF) == 1:
        return [(0x1F, 2), (0x20, 2)]
    return [(g, 1) for g, a in [(0x1F, 0x8EFB), (0x20, 0x8EFC)] if r(e, a) == 1]


def expected(e):
    want = application(e)
    selected = reports(e)
    if selected and r(e, 0x99D5) == 1:
        assert not (r(e, 0x99D8, 2) & 0x8000), 'downstream admission outside cache oracle'
    if r(e, 0x9462) != 1 and r(e, 0x9A28) != 1:
        for group, mode in selected:
            expected_write(want, 0x971E + group, mode, 1)
    return want, selected


class Observed(ControlTaskArithmetic):
    def __init__(self):
        super().__init__()
        self.reports = []
        self.mapping_reads = []

    def instruction(self, pc):
        if pc == 0x8FAC8:
            self.reports.append((self.r[4], self.r[5]))
        return super().instruction(pc)

    def read(self, address, size):
        value = super().read(address, size)
        if address in [0xE12C6, 0xE12C8] and size == 2:
            self.mapping_reads.append((address, value))
        return value


def case(values, reset, suppress, active, mask):
    e = Observed()
    for a, value in zip([0x8EFF, 0x8EFB, 0x8EFC], values):
        w(e, a, value)
    for a, value in [(0x9462, reset), (0x9A28, suppress), (0x99D5, active),
                     (0x973D, 0xA5), (0x973E, 0x5A), (0x973C, 0x3C), (0x973F, 0xC3)]:
        w(e, a, value)
    w(e, 0x9463, reset ^ 255)
    w(e, 0x99D8, mask, 2)
    want, selected = expected(e)
    saved = e.r[8:16].copy(); gbr = e.gbr; interrupt = e.sr & 0xF0
    e.run(0x6CFD8)
    assert application(e) == want, (values, reset, suppress, active, mask)
    assert e.r[8:16] == saved and e.gbr == gbr and e.sr & 0xF0 == interrupt
    assert e.reports == selected
    assert e.mapping_reads == [(0xE1288 + 2*g, g) for g, _ in selected]
    assert not {0x8FCB8, 0x8FE4E, 0xDAE8} & e.visited
    assert (0x9034E in e.visited) == (active == 1 and bool(selected))


def main():
    count = 0
    for values, reset, suppress, active, mask in itertools.product(
            itertools.product([0, 1, 2, 255], repeat=3), [0, 1, 2, 255],
            [0, 1, 2, 255], [0, 1, 2], [0, 1, 0x7FFF]):
        case(values, reset, suppress, active, mask); count += 1
    sweeps = 0
    for i, value in itertools.product(range(3), range(256)):
        values = [0, 1, 1]; values[i] = value
        case(values, 0, 0, 0, 0xFFFF); sweeps += 1
    masks = 0
    for group in [0x1F, 0x20]:
        assert ECU[0xE1288+2*group:0xE128A+2*group] == group.to_bytes(2, 'big')
        assert ECU[0xAC008+2*group:0xAC00A+2*group] == b'\x80\0'
        e = Observed()
        for mask in range(65536):
            e.r[5] = mask
            assert e.run(0x9034E, group) == int(not (mask & 0x8000))
            masks += 1
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(ECU).hexdigest(),
                  whole_ram_cases=count, full_byte_sweeps=sweeps, mask_cases=masks,
                  groups=[31,32], mappings=[31,32], dispatch_masks=[32768,32768], status='PASS')
    (ROOT/'control-qualification-report-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result)


if __name__ == '__main__':
    main()
