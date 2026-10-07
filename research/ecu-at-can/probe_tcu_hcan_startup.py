"""Original CAN startup with bounded documented HCAN configuration registers.

GSR reset/normal samples are external inputs, not simulated reset completion.
Mailbox/configuration writes are retained; command/status writes are recorded
without inventing hardware outcomes. Unsupported accesses still stop execution.
"""
import probe_tcu_native_can_startup as prior
from verify_tcu_diagnostic_timer import initialization_inputs
from verify_tcu_capture_interrupts import CaptureSamples

CONFIGURATION = {0xFFFF0000+a for a in [0xE402, 0xE404, 0xE414, 0xE416, 0xE41C, 0xE41E]}
COMMANDS = {0xFFFF0000+a for a in [0xE408, 0xE40A, 0xE412]}
TIMER_WIDTHS = {0xFFFFF401:1, 0xFFFFF480:2, 0xFFFFF482:2,
                0xFFFFF4EB:1, 0xFFFFF4E0:2, 0xFFFFF4E2:2}


class TimerSamples(CaptureSamples):
    def write(self, address, value, size):
        if TIMER_WIDTHS.get(address) != size:
            raise ValueError('Unsupported CAN timer write')
        self.accesses.append(['write', address, size, value & ((1 << (8*size))-1)])


def timer_inputs(old, status, enable, control):
    return initialization_inputs(old, status, enable, control, start_bit=64,
        status_bit=1024, control_address=0xFFFFF4EB, counter_address=0xFFFFF4E0, compare=625)


def mailbox(address, size):
    return size in [1, 2] and address % size == 0 and any(
        first <= address and address+size <= last
        for first, last in [(0xFFFFE420, 0xFFFFE4A0), (0xFFFFE4B0, 0xFFFFE530)])


class Machine(prior.Machine):
    def read(self, address, size):
        address &= 0xFFFFFFFF
        if self.can_timer_active and address >= 0xFFFFE000:
            return self.can_timer_io.read(address, size)
        if address == 0xFFFFE401:
            if size != 1 or not self.reset_samples:
                raise ValueError('Missing explicit HCAN GSR sample')
            value = self.reset_samples.pop(0)
            self.hcan_trace.append(('read', address, size, value))
            return value
        if address in CONFIGURATION or mailbox(address, size):
            if address in CONFIGURATION and size != 2:
                raise ValueError('HCAN setup word required')
            if any(address+i not in self.can_configuration for i in range(size)):
                raise ValueError('HCAN configuration read before known write')
            value = int.from_bytes(bytes(self.can_configuration[address+i] for i in range(size)), 'big')
            self.hcan_trace.append(('read', address, size, value))
            return value
        if 0xFFFFE402 <= address < 0xFFFFE600:
            raise ValueError(f'Unsupported HCAN setup read {address:08X}/{size}')
        return super().read(address, size)

    def write(self, address, value, size):
        address &= 0xFFFFFFFF
        if self.can_timer_active and address >= 0xFFFFE000:
            self.can_timer_io.write(address, value, size)
            self.configuration[address-0xFFFF0000] = value & ((1 << (8*size))-1)
            return
        if address in CONFIGURATION or address in COMMANDS or mailbox(address, size):
            if address in CONFIGURATION | COMMANDS and size != 2:
                raise ValueError('HCAN setup word required')
            value &= (1 << (8*size))-1
            self.hcan_trace.append(('write', address, size, value))
            if address not in COMMANDS:
                for i, byte in enumerate(value.to_bytes(size, 'big')):
                    self.can_configuration[address+i] = byte
            return
        if 0xFFFFE402 <= address < 0xFFFFE600:
            raise ValueError(f'Unsupported HCAN setup write {address:08X}/{size}')
        return super().write(address, value, size)

    def instruction(self, pc):
        if pc == 0x16650:
            self.can_timer_active = True
        return super().instruction(pc)

    def check_startup(self):
        assert not self.reset_samples
        assert self.can_timer_io.accesses == self.expected_timer
        assert all(not v for v in self.can_timer_io.samples.values())
        assert prior.r(self, 0x8003) == 1 and prior.r(self, 0x8F6C) == 10

    def startup_evidence(self):
        return dict(configuration={hex(a):v for a,v in sorted(self.can_configuration.items())},
                    remaining_gsr_samples=self.reset_samples,
                    can_timer_mmio=self.can_timer_io.accesses,
                    limits='Read-after-write configuration only; command/status writes have no simulated side effects. GSR samples8/0 externally supplied.')


def fixture():
    t = prior.fixture()
    t.__class__ = Machine
    t.can_configuration = {}
    t.reset_samples = [8, 0]
    t.can_timer_active = False
    t.can_timer_io = TimerSamples()
    t.can_timer_io.samples, t.expected_timer = timer_inputs(
        *[t.configuration[a] for a in [0xF401, 0xF480, 0xF482, 0xF4EB]])
    return t


if __name__ == '__main__':
    prior.main(machine_factory=fixture, filename='tcu-hcan-startup-probe.json', scope=__doc__)
