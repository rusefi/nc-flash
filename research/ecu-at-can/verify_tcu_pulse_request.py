"""Execute the TCU pulse request, admission gates and response paths.

Independent full application RAM/peripheral and return-value oracles. Original
helpers execute, including interrupt-mask save/restore. Input values and task
interleaving are explicit fixtures; no physical units or received CAN proof.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_inhibit_writers as writers
from verify_tcu_inhibit_writers import TCU, pins, r, source, w

ROOT = Path(__file__).resolve().parent
PERMISSIONS = list(zip(TCU[0x5EB28:0x5EB54:2], TCU[0x5EB29:0x5EB54:2]))
assert len(PERMISSIONS) == 22 and PERMISSIONS[3] == (4, 1)
REQUEST = 0xFFFFB200


def fixture(seed=0):
    t = writers.fixture(seed)
    rng = random.Random(seed)
    t.sr = (t.sr & ~0xF0) | ((seed % 16) << 4)
    for address in [0xA4E8, 0xA962, 0xA964, 0xA98E, 0x90B4, 0x90B5, 0x8F65]:
        w(t, address, rng.randrange(256))
    for address in [0x80A4, 0x809E, 0xB128, 0xB12A]:
        w(t, address, rng.randrange(65536), 2)
    w(t, 0x90A7, seed % 2)
    w(t, 0x90B6, 1)
    w(t, 0x8F66, 0)
    w(t, 0x90AC, rng.randrange(65536), 2)
    w(t, 0x90AE, rng.randrange(65536), 2)
    w(t, 0xB208, 0, 2)
    return t


def permission_model(t, service):
    row = next((row for row in PERMISSIONS if row[0] == service & 255), None)
    state = r(t, 0x90B6)
    if row is None or state not in [1, 2, 4]:
        return 0x11
    mask = row[1]
    return 0 if mask & state else 0x22 if mask & (~state & 255) else 0x11


def predicate_model(t):
    first = r(t, 0x80A4, 2) >= r(t, 0xB128, 2) and r(t, 0xA962) & 1
    second = r(t, 0x809E, 2) >= r(t, 0xB12A, 2) and r(t, 0xA98E) & 1
    extra = r(t, 0xA4E8) not in [0, 2] and r(t, 0xA964) & 1
    return int(not (first or (second and extra)))


def response_model(t, error, alternate=0):
    index = r(t, 0x90A7)
    state = (r(t, 0x90AC + 2 * index) >> 3) & 3
    target = 0 if alternate & 255 == 1 else index
    if state == 2 and error & 255 != 0x22:
        if r(t, 0x8F66) == 0:
            w(t, 0x8F65, (t.sr >> 4) & 15)
        address = 0x90AC + 2 * target
        w(t, address, r(t, address) & 253)
        return 0
    address = 0x90B4 + target
    if r(t, address) == 0:
        w(t, address, error & 255)
    return 2


def request_model(t):
    error = permission_model(t, 4)
    if not error:
        if r(t, 0xB208, 2):
            error = 0x12
        elif not predicate_model(t):
            error = 0x22
        else:
            w(t, 0x9418, 1)
    return response_model(t, error) if error else 0


def check(t, entry, model, argument=0):
    ref = copy.deepcopy(t)
    expected = model(ref)
    actual = pins.execute(t, entry, argument)
    assert actual == expected, (hex(entry), actual, expected)
    source.equal(t, ref)
    return actual


def direct():
    counts = dict(permission=0, predicate=0, response=0, request=0)
    for service, state in itertools.product(range(256), [0, 1, 2, 3, 4, 255]):
        t = fixture(service)
        w(t, 0x90B6, state)
        check(t, 0x5604C, lambda ref: permission_model(ref, service), service)
        counts['permission'] += 1
    # Both unsigned word comparisons straddle thresholds, including sign-bit
    # and extreme values. Every validity-bit combination and mode category.
    pairs = [(0, 0), (0, 1), (99, 100), (100, 100), (101, 100),
             (32767, 32768), (32768, 32767), (65535, 65535)]
    for pair1, pair2, flags, mode in itertools.product(pairs, pairs, range(8), [0, 1, 2, 255]):
        t = fixture(flags + mode)
        for address, value in [(0x80A4, pair1[0]), (0xB128, pair1[1]),
                               (0x809E, pair2[0]), (0xB12A, pair2[1])]:
            w(t, address, value, 2)
        for bit, address in enumerate([0xA962, 0xA98E, 0xA964]):
            w(t, address, 0xFE | ((flags >> bit) & 1))
        w(t, 0xA4E8, mode)
        check(t, 0x53520, predicate_model)
        counts['predicate'] += 1
    for byte, error, alternate in itertools.product(range(256), [0x11, 0x12, 0x22], [0, 1]):
        t = fixture(byte)
        index = r(t, 0x90A7)
        w(t, 0x90AC + 2 * index, byte)
        w(t, 0x90B4, 0 if byte & 1 else 7)
        w(t, 0x90B5, 7 if byte & 1 else 0)
        w(t, 0x8F66, [0, 1, 254, 255][byte % 4])
        t.r[5] = alternate
        check(t, 0x541CC, lambda ref: response_model(ref, error, alternate), error)
        counts['response'] += 1
    for state, length, blocked, response, pending in itertools.product(
        [0, 1, 2, 4, 255], [0, 1, 65535], [0, 1], range(4), [0, 7]
    ):
        t = fixture(state + length)
        index = r(t, 0x90A7)
        w(t, 0x90B6, state)
        w(t, 0xB208, length, 2)
        w(t, 0xA962, blocked)
        w(t, 0x80A4, 100, 2)
        w(t, 0xB128, 100, 2)
        w(t, 0xA98E, 0)
        w(t, 0x90AC + 2 * index, 0xA7 | (response << 3))
        w(t, 0x90B4 + index, pending)
        check(t, 0x54AFC, request_model, REQUEST)
        assert {0x5604C, 0x1D246, 0x5607A} <= t.visited
        counts['request'] += 1
    return counts


def retained():
    t = writers.task_fixture()
    rows = []
    pins.execute(t, 0x12880)
    # Original request precedes each task; inputs controlling admission are
    # fixture values, reset at each request to isolate ordering and overlap.
    for call in range(48):
        for _ in range(8):
            writers.wheel(t)
        request = None
        if call in [9, 10, 24, 25, 26]:
            for address, value in [(0x90A7, 0), (0x90B6, 1), (0xA962, 0), (0xA98E, 0),
                                   (0x90AC, 0x12), (0x90B4, 0), (0x8F66, 0)]:
                w(t, address, value)
            w(t, 0xB208, int(call in [25, 26]), 2)
            # At25 the response mode suppresses the error;26 records it.
            if call == 26:
                w(t, 0x90AC, 2)
            old_request = r(t, 0x9418)
            returned = check(t, 0x54AFC, request_model, REQUEST)
            request = dict(returned=returned, old=old_request, after=r(t, 0x9418),
                           response_flags=r(t, 0x90AC), pending_error=r(t, 0x90B4))
        row = writers.task_call(t)
        row.update(call=call, request=request, latch=r(t, 0x9418), timer=r(t, 0x82B9))
        rows.append(row)
    assert rows[9]['request']['after'] == rows[10]['request']['after'] == 1
    assert rows[12]['latch'] == 0 and rows[12]['mode'] == 1
    assert rows[24]['latch'] == 0 and rows[24]['timer'] == 0
    assert rows[25]['request']['returned'] == 0 and rows[25]['request']['after'] == 0
    assert rows[25]['request']['response_flags'] == 0x10
    assert rows[26]['request']['returned'] == 2 and rows[26]['request']['pending_error'] == 0x12
    return rows


def main():
    counts = direct()
    rows = retained()
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), counts=counts,
                  permissions=PERMISSIONS, retained=rows, timer_wheel_calls=384,
                  limits='Admission/status inputs and8:1 timer/task ratio explicit. No receivedCAN dispatch, transmission, realcadence, physicalunits or persistence proof.')
    (ROOT / 'tcu-pulse-request-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(counts, 'retained tasks', len(rows), 'original timer wheel calls', 384, flush=True)


if __name__ == '__main__':
    main()
