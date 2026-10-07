"""Bounded local SH-2E exception support for original application startup.

Only signed-zero/zero FDIV and quiet-NaN comparisons extend finite arithmetic.
Enabled exceptions stop the probe; no trap handler or full FPU is simulated.
FPSCR fixed bits follow manual figure4.2, including DN=1 and RM=01.
See control-initialize-fpu.txt for sources, scope and reproducible checks.
"""
import json
import hashlib
from pathlib import Path
from probe_control_application_initialize import Initialize
from verify_control_contributions import ECU

ROOT = Path(__file__).resolve().parent


class SelfTest(Initialize):
    def __init__(self):
        super().__init__()
        self.fpscr = 0x40001
        self.selftest_returns = []
        self.selftest_return_pc = None

    def instruction(self, pc):
        if pc == 0x28DFC:
            self.selftest_return_pc = self.pr
        if pc == self.selftest_return_pc:
            self.selftest_returns.append(dict(pc=pc, result=self.r[0], fpscr=self.fpscr))
            self.selftest_return_pc = None
        op = self.read(pc, 2)
        n, m, lo = (op >> 8) & 15, (op >> 4) & 15, op & 15
        if op & 0xF0FF == 0x406A:  # LDS Rn,FPSCR
            self.fpscr = (self.r[n] & 0x18C60) | 0x40001
        elif op & 0xF0FF == 0x006A:  # STS FPSCR,Rn
            self.r[n] = self.fpscr
        elif op & 0xF00F == 0xF003 and all(
            self.fr[i] & 0x7FFFFFFF == 0 for i in (n, m)
        ):
            self.fpscr = (self.fpscr & ~0x18000) | 0x10040
            if self.fpscr & 0x800:
                raise NotImplementedError('Enabled FPU invalid-operation trap')
            self.fr[n] = 0x7FBFFFFF
        elif op >> 12 == 15 and lo in (4, 5) and any(
            0x7F800000 < (self.fr[i] & 0x7FFFFFFF) < 0x7FC00000 for i in (n, m)
        ):
            for i in (n, m):
                bits = self.fr[i] & 0x7FFFFFFF
                if bits >= 0x7FC00000 or bits == 0x7F800000 or 0 < bits < 0x800000:
                    raise ValueError('NaN compare counterpart outside bounded support')
            self.fpscr &= ~0x18000
            if lo == 5:
                self.fpscr |= 0x10040
                if self.fpscr & 0x800:
                    raise NotImplementedError('Enabled FPU invalid-comparison trap')
            self.t(False)
        else:
            result = super().instruction(pc)
            if op >> 12 == 15 and (
                lo in (0, 1, 2, 3, 4, 5, 14)
                or op & 0xF0FF in (0xF02D, 0xF03D, 0xF04D, 0xF05D)
            ):
                self.fpscr &= ~0x18000
            return result
        self.visited.add(pc)
        return pc + 2, False


def run_probe(machine_type=SelfTest, filename='control-initialize-fpu-probe.json', scope=__doc__,
              entry=0x1619A, instruction_limit=2000000):
    e = machine_type()
    e.registers[0xFFFFF74E] = 1
    sp, gbr = e.r[15], e.gbr
    try:
        e.run(entry, limit=instruction_limit)
        status = 'returned'
        assert e.r[15] == sp and e.gbr == gbr
    except (ValueError, RuntimeError, NotImplementedError, AssertionError) as exc:
        status = type(exc).__name__ + ': ' + str(exc)
    result = dict(scope=scope, entry=entry, instruction_limit=instruction_limit,
                  rom_sha256=hashlib.sha256(ECU).hexdigest(), status=status, pc=e.pc, tail=e.tail,
                  registers=e.r, float_registers=e.fr, fpscr=e.fpscr,
                  entries=e.initializer_entries, calls=e.initializer_calls,
                  selftest_returns=e.selftest_returns, bank=e.bank_checked,
                  accesses=e.accesses)
    (ROOT / filename).write_text(json.dumps(result, indent=2) + '\n')
    print(status, hex(e.pc), 'initializer direct calls', len(e.initializer_calls),
          'self-test returns', e.selftest_returns)


if __name__ == '__main__':
    run_probe()
