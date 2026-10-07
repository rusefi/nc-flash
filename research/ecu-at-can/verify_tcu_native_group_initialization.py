"""Compare native1DFF8 initialization with the older explicit group fixture.

Original code executes throughout. The62-call comparison is differential,
not an independent semantic oracle or evidence of full reset/peripherals.
"""
import copy
import hashlib
import json
from pathlib import Path

import verify_tcu_readiness_admission as native
import verify_tcu_phase_retirement as retirement
from verify_can201_byte6 import TCU
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent
ENTRIES = [int.from_bytes(TCU[a:a+4], 'big')
           for a in range(0x1E2B4, 0x1E3AC, 4)]


def difference(left, right):
    return {hex(a): [left.get(a, 0), right.get(a, 0)]
            for a in sorted(left.keys() | right.keys())
            if left.get(a, 0) != right.get(a, 0)}


class Machine(native.Machine):
    def instruction(self, pc):
        if pc == 0x1E08E:
            assert self.group_reference is None
            ref = SHRotate(TCU)
            ref.ram = self.ram.copy()
            for fn in ENTRIES:
                ref.r[5] = 0
                ref.run(fn, 0, limit=1000000)
            self.group_reference = ram(ref)
            self.before_groups = ram(self)
        if pc == 0x1E254:
            assert self.group_reference is not None
            assert ram(self) == self.group_reference, difference(ram(self), self.group_reference)
            self.group_checks += 1
            self.group_changes = difference(self.before_groups, ram(self))
            self.group_reference = None
        if 0x1DFF8 <= pc < 0x1E25A or 0x1E3AC <= pc < 0x1E3CC:
            op = int.from_bytes(TCU[pc:pc+2], 'big')
            if op & 0xF0FF in [0x400B, 0x402B]:
                self.native_calls.append(dict(pc=hex(pc), target=hex(self.r[(op >> 8) & 15]),
                                              r4=self.r[4], r5=self.r[5]))
        return super().instruction(pc)


def fixture():
    t = native.fixture()
    native.initialize(t)
    t.__class__ = Machine
    t.group_reference = None
    t.group_checks = 0
    t.group_changes = {}
    t.native_calls = []
    return t


def main():
    base = fixture()
    rows = []
    for argument in [0, 0x12345678, 0xFFFFFFFF]:
        t = copy.deepcopy(base)
        legacy = copy.deepcopy(base)
        before = ram(t)
        saved = t.r[8:].copy()
        t.r[5] = argument ^ 0xA5A5A5A5
        try:
            t.run(0x1DFF8, argument, limit=2000000)
            assert t.r[8:] == saved and t.group_reference is None and t.group_checks == 1
            calls = [int(c['target'], 16) for c in t.native_calls
                     if 0x1E08E <= int(c['pc'], 16) < 0x1E254]
            assert calls == ENTRIES
            retirement.full_fixture(legacy)
            rows.append(dict(status='PASS', argument=argument,
                group_whole_application_ram_checked=True, group_calls=len(calls),
                native_calls=t.native_calls, group_changes=t.group_changes,
                native_changes=difference(before, ram(t)),
                legacy_changes=difference(before, ram(legacy)),
                native_vs_legacy=difference(ram(t), ram(legacy))))
        except (AssertionError, ValueError, RuntimeError, KeyError, ZeroDivisionError) as error:
            rows.append(dict(status='REJECTED', argument=argument, pc=hex(t.pc),
                             error=type(error).__name__+': '+str(error)))
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), rows=rows,
                  limits='Identical preinitialized peripheral/RAM fixture; direct1DFF8 invocation, no native interrupt admission in this test. Fullfixture also initializes prerequisites and supplies80B4=250/216D8. No fullreset or physical test.')
    (ROOT / 'tcu-native-group-initialization-verification.json').write_text(
        json.dumps(result, indent=2) + '\n')
    print([dict(status=r['status'], argument=r['argument'], error=r.get('error'),
                differences=len(r.get('native_vs_legacy', {}))) for r in rows], flush=True)
    assert all(row['status'] == 'PASS' for row in rows)


if __name__ == '__main__':
    main()
