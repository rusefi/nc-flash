"""Independent whole-application-RAM model of original56B06 diagnostic gates."""
import itertools
import json
import random
from pathlib import Path
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w, r
from verify_tcu_base_publication import ram

BANKS = [(0xA93C, 0xA938), (0xA944, 0xA939), (0xA94C, 0xA93A)]
assert [int.from_bytes(TCU[a:a+2], 'big') for a in range(0x5EB68, 0x5EB76, 2)] == [10200, 9000, 10500, 10000, 400, 400, 2000]


def model(t):
    reset = r(t, 0x9415)
    if reset == 1 and r(t, 0xA954) == 0:
        for state, published in BANKS:
            w(t, state, 2)
            w(t, published, 0)
    w(t, 0xA954, reset)
    x = r(t, 0xA518, 2)
    dependent = r(t, 0x809E, 2) > 400 and bool(r(t, 0xA98E) & 1)
    flags = [(x > 10200 and dependent, x > 9000 and dependent),
             (x > 10200, x > 9000),
             (x > 10500 and dependent, x > 10000 and dependent)]
    if r(t, 0x8006) != 3:
        flags = [(False, False)]*3
    now = r(t, 0x84D0, 4)
    for (address, published), (high, low) in zip(BANKS, flags):
        state = r(t, address)
        if state == 0:
            if not low:
                w(t, address, 2)
                w(t, published, 0)
        elif not high:
            w(t, address, 2)
        elif state == 1:
            if now >= r(t, address+4, 4):
                w(t, published, 1)
                w(t, address, 0)
        else:
            w(t, address+4, (now+2000) & 0xFFFFFFFF, 4)
            w(t, address, 1)


def expected(t):
    ref = SHRotate(TCU)
    ref.ram = dict(t.ram)
    model(ref)
    return ram(ref)


def main():
    rng = random.Random(0x56B06)
    count = 0
    for mode, x, dependency, summary, reset in itertools.product(
            [0, 1, 3, 5], [0, 9000, 9001, 10000, 10001, 10200, 10201, 10500, 10501, 65535],
            [399, 400, 401, 65535], [0, 1, 2, 3], [0, 1]):
        t = SHRotate(TCU)
        for a, v, n in [(0x8006, mode, 1), (0xA518, x, 2), (0x809E, dependency, 2),
                         (0xA98E, summary, 1), (0x9415, reset, 1), (0xA954, count % 3, 1),
                         (0x84D0, rng.choice([0, 1999, 2000, 2001, 0xFFFFFFFF]), 4)]:
            w(t, a, v, n)
        for a, p in BANKS:
            w(t, a, rng.choice([0, 1, 2, 255]))
            w(t, a+4, rng.choice([0, 2000, 2001, 0xFFFFFFFF]), 4)
            w(t, p, rng.choice([0, 1, 255]))
        wanted = expected(t)
        t.run(0x56B06)
        assert ram(t) == wanted, (mode, x, dependency, summary, reset,
                                  {hex(a): (ram(t).get(a, 0), wanted.get(a, 0))
                                   for a in ram(t).keys() | wanted.keys()
                                   if ram(t).get(a, 0) != wanted.get(a, 0)})
        count += 1
    result = dict(status='PASS', scope=__doc__, whole_ram_cases=count,
                  seed=hex(0x56B06), limits='Actualclock period, A518 physicalunits andfullboot unproved.')
    (Path(__file__).resolve().parent/'tcu-diagnostic-admission-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS', count, 'wholeRAM56B06 cases')


if __name__ == '__main__':
    main()
