"""Independent whole-RAM and exact-MMIO models for native HCAN/timer setup.

Setup index0 only, as called by original19EC4. GSR8/0 external samples do not
prove hardware reset delivery. Whole11FA0 coverage has separate limits.
"""
import copy
import hashlib
import json
from pathlib import Path

import probe_tcu_hcan_startup as probe
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram

ROOT = Path(__file__).resolve().parent


def configuration_model(mcr):
    trace = []
    memory = {}

    def read(address, size, value):
        trace.append(('read', 0xFFFF0000+address, size, value))

    def write(address, size, value, retain=True):
        trace.append(('write', 0xFFFF0000+address, size, value))
        if retain:
            for i, byte in enumerate(value.to_bytes(size, 'big')):
                memory[0xFFFF0000+address+i] = byte

    read(0xE400, 1, mcr)
    write(0xE400, 1, mcr|1, False)
    read(0xE401, 1, 8)
    write(0xE412, 2, 256, False)
    write(0xE402, 2, int.from_bytes(TCU[0x5C968:0x5C96A], 'big'))
    for first in [0xE420, 0xE4B0]:
        for address in range(first, first+128):
            write(address, 1, 0)
    write(0xE404, 2, 256)
    write(0xE408, 2, 0xFEFF, False)
    write(0xE412, 2, 1, False)
    write(0xE40A, 2, 0xFEFF, False)
    write(0xE416, 2, 0xBCEE)
    write(0xE414, 2, 65535)
    read(0xE414, 2, 65535)
    mask, directions = 0xFEFF, 256
    write(0xE414, 2, mask)
    write(0xE424, 2, int.from_bytes(TCU[0x5C96C:0x5C96E], 'big'))
    write(0xE41E, 2, int.from_bytes(TCU[0x5C96A:0x5C96C], 'big'))
    for slot in range(1, 12):
        bit = 1 << ((slot+8) % 16)
        read(0xE414, 2, mask)
        mask &= ~bit
        write(0xE414, 2, mask)
        address = 0x5C8C0+2*slot
        write(0xE424+8*slot, 2, int.from_bytes(TCU[address:address+2], 'big'))
        write(0xE420+8*slot, 1, TCU[0x5C8E4+slot])
        read(0xE404, 2, directions)
        directions |= bit
        write(0xE404, 2, directions)
    read(0xE400, 1, mcr|1)
    write(0xE400, 1, (mcr|1)&0xA3, False)
    read(0xE414, 2, mask)
    mask &= 0xFF7F
    write(0xE414, 2, mask)
    write(0xE400, 1, 128, False)
    read(0xE401, 1, 0)
    read(0xE414, 2, mask)
    assert mask == 0x70 and directions == 0xFF0F
    return trace, memory


def main():
    base = probe.fixture()
    examples = []
    for seed in range(256):
        t = copy.deepcopy(base)
        t.mcr = seed
        t.hcan_trace = []
        t.configuration_trace = []
        port = ((seed*37)&255)*256+seed
        t.configuration[0xF732] = port
        for a in [0x8F5C, 0x8F68, 0x8F69]:
            w(t, a, seed)
        ref = SHRotate(TCU)
        ref.ram = t.ram.copy()
        w(ref, 0x8F5C, 255)
        w(ref, 0x8F68, 0x70, 2)
        saved, mask = t.r[8:].copy(), t.sr & ~0x301
        t.run(0x1AEAA, 0, limit=2000000)
        expected, memory = configuration_model(seed)
        assert ram(t) == ram(ref), 'HCAN initializer RAM'
        assert t.r[8:] == saved and t.sr & ~0x301 == mask
        assert t.hcan_trace == expected
        assert t.can_configuration == memory and t.mcr == 128 and not t.reset_samples
        assert t.configuration_trace == [('read', 0xF732, 2, port),
                                          ('write', 0xF732, 2, port|160)]
        if seed in [0, 255]:
            examples.append(dict(seed=seed, mmio=expected, mailbox_mask=r(t, 0x8F68, 2)))
    for seed in range(256):
        t = copy.deepcopy(base)
        args = [seed, seed*257, (seed*131)&65535, seed]
        t.can_timer_io.samples, expected = probe.timer_inputs(*args)
        before, saved, mask = ram(t), t.r[8:].copy(), t.sr
        t.run(0x16650)
        assert ram(t) == before and t.r[8:] == saved and t.sr == mask
        assert t.can_timer_io.accesses == expected
        assert all(not values for values in t.can_timer_io.samples.values())
    rejects = 0
    for address, size, write in [
        (0xFFFFE402, 1, True), (0xFFFFE402, 4, True),
        (0xFFFFE421, 2, True), (0xFFFFE4A0, 1, True),
        (0xFFFFE530, 1, True), (0xFFFFE418, 1, True),
        (0xFFFFE402, 2, False), (0xFFFFE408, 2, False),
        (0xFFFFE420, 1, False), (0xFFFFE401, 2, False)]:
        t = copy.deepcopy(base)
        try:
            t.write(address, 0, size) if write else t.read(address, size)
        except ValueError:
            rejects += 1
        else:
            raise AssertionError(('Unprovided access accepted', hex(address), size))
    result = dict(status='PASS', scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
        hcan_whole_ram_mmio_cases=256, timer_whole_ram_mmio_cases=256,
        unsupported_access_rejections=rejects, hcan_accesses=len(configuration_model(0)[0]), examples=examples,
        limits='Software configuration writes/finite reset status, not bus timing/physical reset/pin proof. Whole11FA0 initializer not independently modeled.')
    (ROOT/'tcu-hcan-startup-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print({k:v for k,v in result.items() if k not in ['examples','scope']})


if __name__ == '__main__':
    main()
