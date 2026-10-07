"""Run original11FA0 CAN-task initialization with existing strict peripherals.

Coverage probe only; preserve the first unsupported access instead of guessing
hardware behavior or writing receive mode8. No full boot or physical proof.
"""
import hashlib
import copy
import json
from pathlib import Path

import verify_tcu_native_capture_startup as startup
from verify_can201_byte6 import TCU, r
from verify_tcu_timer_configuration import ConfigurationRegisters
from verify_tcu_base_publication import ram

ROOT = Path(__file__).resolve().parent


class Machine(startup.Machine):
    def read(self, address, size):
        if address == 0xFFFFF732:
            old = self.configuring
            self.configuring = True
            try:
                return ConfigurationRegisters.read(self, address, size)
            finally:
                self.configuring = old
        return super().read(address, size)

    def write(self, address, value, size):
        if address == 0xFFFFF732:
            old = self.configuring
            self.configuring = True
            try:
                return ConfigurationRegisters.write(self, address, value, size)
            finally:
                self.configuring = old
        return super().write(address, value, size)

    def instruction(self, pc):
        self.last_instruction = pc
        if pc in [0x11FA0, 0x124F8, 0x19EC4, 0x19AD0, 0x1A056, 0x1B060,
                  0x1D4DA, 0x1C912, 0x1BB30, 0x1BBEA, 0x1BBB0, 0x16650]:
            self.can_entries.append(hex(pc))
        return super().instruction(pc)


def fixture():
    t = startup.fixture()
    startup.startup.native.initialize(t)
    t.initialize_extra()
    t.__class__ = Machine
    t.can_entries = []
    t.last_instruction = None
    return t


def main(machine_factory=fixture, filename='tcu-native-can-startup-probe.json', scope=None):
    t = machine_factory()
    for low in range(256):
        leaf = copy.deepcopy(t)
        value = ((low*131)&255)*256+low
        leaf.configuration[0xF732] = value
        leaf.configuration_trace = []
        memory, saved, mask = ram(leaf), leaf.r[8:].copy(), leaf.sr
        leaf.run(0x1AC70)
        assert ram(leaf) == memory and leaf.r[8:] == saved and leaf.sr == mask
        assert leaf.configuration[0xF732] == value | 0xA0
        assert leaf.configuration_trace == [('read', 0xF732, 2, value),
                                            ('write', 0xF732, 2, value | 0xA0)]
    before = dict(task_mode=r(t, 0x8003), receive_mode=r(t, 0x8F6C))
    try:
        t.run(0x11FA0, limit=2000000)
        if hasattr(t, 'check_startup'):
            t.check_startup()
        status, error = 'RETURNED', None
    except (AssertionError, ValueError, RuntimeError, KeyError, ZeroDivisionError) as exc:
        status, error = 'REJECTED', type(exc).__name__+': '+str(exc)
    result = dict(scope=scope or __doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
        status=status, error=error, last_instruction=hex(t.last_instruction),
        entries=t.can_entries, before=before, pbcrh_leaf_cases=256,
        after=dict(task_mode=r(t, 0x8003), receive_mode=r(t, 0x8F6C)),
        hcan_trace=t.hcan_trace, configuration_trace=t.configuration_trace,
        limits='Originalpartialstartup afterexisting readiness/diagnostic/CMT1initializers, beforeevents. Unsupportedaccess means fixture boundary, notfirmware defect.')
    if hasattr(t, 'startup_evidence'):
        result['startup_evidence'] = t.startup_evidence()
    (ROOT/filename).write_text(json.dumps(result, indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['configuration_trace', 'hcan_trace', 'scope', 'startup_evidence']})


if __name__ == '__main__':
    main()
