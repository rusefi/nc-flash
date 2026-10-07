"""Strict byte fixtures and original80D4 compare/counter configuration."""
import hashlib
import itertools
import json
from pathlib import Path
from probe_control_initialize_timer import TimerStartup
from verify_control_contributions import ECU, w, f
from verify_control_activity_conditions import expected as condition_expected
from verify_control_raw_inputs import application, expected_write


def main():
    byte_cases = rejected = 0
    for address in [0xFFFFF6D8, 0xFFFFF6C4]:
        e = TimerStartup()
        for value in list(range(256)) + [-1, 256, 65535, 0x12345678]:
            before = e.registers.copy()
            e.write(address, value, 1)
            before[address] = value % 256
            assert e.read(address, 1) == value % 256 and e.registers == before
            assert e.accesses[-2:] == [('write', address, value % 256, 1), ('read', address, value % 256, 1)]
            byte_cases += 1
        for location, size in [(address, 2), (address, 4), (address+1, 1)]:
            for writing in [False, True]:
                before = e.registers.copy()
                try:
                    e.write(location, 1, size) if writing else e.read(location, size)
                except ValueError:
                    assert e.registers == before
                    rejected += 1
                else:
                    raise AssertionError('Unsupported access accepted')
    for index in range(256):
        e = TimerStartup(); w(e, 0x4119, index); w(e, 0x414B, index ^ 255)
        want = application(e)
        value = 0 if ECU[0xDC3A9] == 0x5A else ECU[0x1115D + 2*index] & 127
        expected_write(want, 0x414B, value, 1)
        saved, gbr = e.r[8:16].copy(), e.gbr
        e.run(0x80D4)
        assert application(e) == want and e.r[8:16] == saved and e.gbr == gbr
        assert e.accesses == [('write', 0xFFFFF6D8, value, 1), ('write', 0xFFFFF6C4, 0, 1)]
        assert e.registers[0xFFFFF6D8] == value and e.registers[0xFFFFF6C4] == 0
    initializer_cases = 0
    reload_value = min(65535, sum(int.from_bytes(ECU[a:a+2], 'big') for a in [0xE0862, 0xE0864, 0xE0866]))
    for first, second, old_first, old_second in itertools.product([-1000, -782, -777, 0], [-1000, -782, -777, 0], [0, 255], [0, 255]):
        e = TimerStartup()
        f(e,0x6D40,first); f(e,0x6D20,second)
        w(e,0x8FE0,old_first);w(e,0x8FDF,old_second)
        w(e,0x8FD4,0xA55A,2);w(e,0x8FD6,255);w(e,0x8FD7,255)
        want = condition_expected(e,0x6F2C8)
        expected_write(want,0x8FD4,reload_value,2)
        for address in [0x8FD6,0x8FD7]:expected_write(want,address,ECU[0xE0860],1)
        saved,gbr=e.r[8:16].copy(),e.gbr
        e.run(0x6F29C)
        assert application(e)==want and e.r[8:16]==saved and e.gbr==gbr
        assert not e.accesses and 0x6F2C8 in e.visited
        initializer_cases += 1
    report = dict(rom_sha256=hashlib.sha256(ECU).hexdigest(), scope=__doc__,
                  byte_configuration_cases=byte_cases, expected_rejections=rejected,
                  original_routine_whole_ram_cases=256, calibration_dc3a9=ECU[0xDC3A9],
                  activity_initializer_whole_ram_cases=initializer_cases,
                  limitation='No external AGCK, compare event, interrupt, elapsed time or board wiring model.')
    Path(__file__).with_name('control-initialize-timer-verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(report)


if __name__ == '__main__':
    main()
