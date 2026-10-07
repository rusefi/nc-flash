"""CAN task readiness gate and original1669A interrupt prefix.

Reuse the verified compare/profile pipeline. Whole-RAM body comparison is
differential against original11FB2; admission, profile and MMIO are independent.
Finite external HCAN/clock inputs; stop beforeRTE, no hardware IRQ proof.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path

import probe_tcu_hcan_startup as setup
import verify_tcu_diagnostic_timer as timer
from verify_tcu_capture_interrupts import CaptureSamples
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent
SPEC = dict(index=8, flag=1024, compare=0xFFFFF4E2, counter=0xFFFFF4E0,
            increment=625, entry=0x1669A, stop=0x166FA, body=0x11FB2, mode=0x8003)
IRQ_PORTS = {0xFFFFF4E2, 0xFFFFF4E0, 0xFFFFF480, 0xFFFFF6C0}


class Samples(CaptureSamples):
    def write(self, address, value, size):
        if size != 2 or address not in [0xFFFFF480, 0xFFFFF4E2]:
            raise ValueError('Unsupported CAN interrupt write')
        self.accesses.append(['write', address, size, value&65535])


class Machine(setup.Machine):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if self.can_irq_active and address in IRQ_PORTS:
            return self.can_irq_io.read(address, size)
        if address == 0xFFFFE401 and self.can_operational:
            if size != 1:
                raise ValueError('Operational GSR byte sample required')
            self.hcan_trace.append(('read', address, size, self.gsr))
            return self.gsr
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if self.can_irq_active and address in IRQ_PORTS:
            return self.can_irq_io.write(address, value, size)
        if address == 0xFFFFE406 and self.can_operational:
            if size != 2:
                raise ValueError('TXPR word command required')
            self.hcan_trace.append(('write', address, size, value&65535))
            return
        return super().write(address, value, size)

    def instruction(self, pc):
        if pc in [0x11FB2, 0x12516, 0x19F32, 0x19F6A]:
            self.can_irq_entries.append(hex(pc))
        return super().instruction(pc)


def expected_mode(mode, adc_a, adc_b):
    if mode == 1 and adc_a in [2, 3] and adc_b in [2, 3]:
        return 3
    return 5 if mode == 3 and adc_a == 4 else mode


def execute_prefix(t, status, second, compare, count, reloaded, start, end):
    before = r(t, 0x8003)
    wanted = expected_mode(before, r(t, 0x84A0), r(t, 0x84D8)) if status&1024 else before
    t.can_irq_entries = []
    ref = copy.deepcopy(t)
    ref.can_irq_active = False
    t.can_irq_active = True
    try:
        row = timer.execute_prefix(t, status, second, compare, count, reloaded, start, end,
                                   spec=SPEC, reference=ref, io=t.can_irq_io)
    except (AssertionError, ValueError, RuntimeError, KeyError, ZeroDivisionError):
        t.can_failure_context = dict(dut_last_instruction=hex(t.last_instruction),
                                     reference_last_instruction=hex(ref.last_instruction))
        raise
    finally:
        t.can_irq_active = False
    assert r(t, 0x8003) == wanted
    assert (t.mcr, t.hcan_trace, t.can_configuration) == (ref.mcr, ref.hcan_trace, ref.can_configuration)
    assert t.can_irq_entries == ref.can_irq_entries
    row.update(mode_before=before, entries=t.can_irq_entries.copy())
    return row


def fixture():
    t = setup.fixture()
    t.run(0x11FA0, limit=2000000)
    t.check_startup()
    t.can_timer_active = False
    t.__class__ = Machine
    t.can_irq_active = False
    t.can_operational = True
    t.can_irq_io = Samples()
    t.can_irq_entries = []
    return t


def main():
    cases = [(mode, a, b) for mode in range(256) for a,b in itertools.product([0,2,3], repeat=2)]
    cases += [(1, value, 3) for value in range(256)]
    cases += [(1, 3, value) for value in range(256)]
    cases += [(3, value, 0) for value in range(256)]
    for mode,a,b in cases:
        t = SHRotate(TCU)
        for address,value in [(0x8003,mode), (0x84A0,a), (0x84D8,b)]:
            w(t, address, value)
        ref = SHRotate(TCU)
        ref.ram = t.ram.copy()
        w(ref, 0x8003, expected_mode(mode,a,b))
        execute_slice(t, 0x11FB2, 0x12516)
        assert ram(t) == ram(ref)
    base = fixture()
    rows = []
    for mode,ready,armed in itertools.product([0,1,3,5,255],[False,True],[False,True]):
        t = copy.deepcopy(base)
        for address,value in [(0x8003,mode),(0x84A0,3 if ready else 0),(0x84D8,3 if ready else 0)]:
            w(t, address, value)
        n = len(rows)
        compare,count = [(0,65535),(65530,4),(2000,2010),(3000,3000)][n%4]
        start,end = [(1000,2000),(0xFFFFFF00,500),(100,900100),(1234,1234)][n%4]
        try:
            event = execute_prefix(t, int(armed)*1024, 0xBEEF, compare, count, 65530, start, end)
            rows.append(dict(status='PASS', initial_mode=mode, ready=ready, **event))
        except (AssertionError, ValueError, RuntimeError, KeyError, ZeroDivisionError) as error:
            rows.append(dict(status='REJECTED', initial_mode=mode, ready=ready, armed=armed,
                             error=type(error).__name__+': '+str(error),
                             context=getattr(t,'can_failure_context',{})))
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
                  independent_gate_cases=len(cases), prefixes=rows,
                  limits='Explicit isolated mode/readiness inputs; completedoriginal11FA0 fixture. No physical CAN IRQ/RTE/clock.')
    (ROOT/'tcu-can-task-interrupt-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(dict(gates=len(cases), passed=sum(r['status']=='PASS' for r in rows),
               failures=[r for r in rows if r['status']!='PASS']))
    assert all(r['status']=='PASS' for r in rows)


if __name__ == '__main__':
    main()
