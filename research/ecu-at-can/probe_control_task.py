"""Probe original complete ECU dispatcher18DC8 without stubbing callees.

Zero RAM is an explicit exploratory fixture, not actual startup. Failures are
recorded with exact instruction/call history; no default peripheral fallback.
"""
import hashlib
import json
from pathlib import Path
from sh_control_task import ControlTaskArithmetic
from verify_control_contributions import ECU, w, r

ROOT = Path(__file__).resolve().parent


class Probe(ControlTaskArithmetic):
    def __init__(self):
        super().__init__()
        self.sr = 0xF0
        self.tail = []
        self.calls = []
        self.entries = []
        self.delays = []

    def instruction(self, pc):
        self.tail.append(pc)
        self.tail = self.tail[-32:]
        if pc in [0x399B0, 0x74DF8, 0x77F62, 0x77F12, 0x77F46,
                  0x6CD96, 0x6CE24, 0x6CF06, 0x6CFD8, 0x6D876, 0x6D904, 0x6D9E6]:
            self.entries.append(pc)
        if pc == 0x2580:
            self.delays.append(dict(pc=pc, argument=self.r[4], pr=self.pr))
        opcode = self.read(pc, 2)
        if 0x18DC8 <= pc < 0x1CAE8 and opcode & 0xF0FF == 0x400B:
            self.calls.append(dict(pc=pc, target=self.r[(opcode >> 8) & 15]))
        return super().instruction(pc)


def main():
    rows = []
    for mode in [0, 1]:
        for phase in range(8):
            e = Probe()
            w(e, 0x535C, mode, 4)
            w(e, 0x5360, phase)
            stack = e.r[15]
            try:
                e.run(0x18DC8, limit=1000000)
                status = 'returned'
                assert e.r[15] == stack
            except (ValueError, AssertionError, NotImplementedError, RuntimeError) as exc:
                status = type(exc).__name__ + ': ' + str(exc)
            rows.append(dict(mode=mode, phase=phase, status=status, pc=e.pc,
                             instruction_tail=e.tail, direct_calls=e.calls,
                             target_entries=e.entries, final_phase=r(e, 0x5360),
                             stack=e.r[15], registers=e.r, delay_entries=e.delays,
                             peripheral_accesses=e.accesses))
            print(mode, phase, status, hex(e.pc), 'calls', len(e.calls), flush=True)
    (ROOT / 'control-task-probe.json').write_text(json.dumps(dict(
        scope=__doc__, rom_sha256=hashlib.sha256(ECU).hexdigest(), rows=rows), indent=2) + '\n')


if __name__ == '__main__':
    main()
