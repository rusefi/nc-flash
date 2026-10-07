"""Execute complete pulse wrapper and diagnostic response construction/handoff.

Compare all application RAM/peripheral state with independent models. Both
record indices and stock service rows tested; input dispatch and transmission
are not replaced with stubs or inferred from buffer construction.
"""
import copy
import hashlib
import itertools
import json
import random
from pathlib import Path

import verify_tcu_pulse_request as request
from verify_tcu_pulse_request import TCU, pins, r, source, w, writers

ROOT = Path(__file__).resolve().parent
BUFFERS = [int.from_bytes(TCU[a:a + 4], 'big') & 65535 for a in [0x5CC20, 0x5CC24]]
HEADERS = [TCU[0x5CA3C + 16 * i] for i in range(22)]
assert BUFFERS == [0x8FA8, 0x90B8] and HEADERS[3] == 0x44
assert int.from_bytes(TCU[0x5CA3C + 3 * 16 + 8:0x5CA3C + 3 * 16 + 12], 'big') == 0x53B5C


def fixture(seed=0):
    t = request.fixture(seed)
    rng = random.Random(seed)
    for address in [0x90AB, 0x90AD]:
        w(t, address, rng.randrange(22))
    for address in [0x90A8, 0x90B7, 0x8F90]:
        w(t, address, rng.randrange(256))
    for address in [0x90C0, 0x90C2, 0x90C4, 0x90C6, 0x90B0, 0x90B2]:
        w(t, address, rng.randrange(65536), 2)
    for buffer in BUFFERS:
        for i in range(8):
            w(t, buffer + i, rng.randrange(256))
    w(t, 0x8F66, [0, 1, 254, 255][seed % 4])
    return t


def critical_pair(t):
    if r(t, 0x8F66) == 0:
        w(t, 0x8F65, (t.sr >> 4) & 15)


def timer_model(t):
    if r(t, 0x90B6) != 1 or r(t, 0x90A8) & 128:
        w(t, 0x90C6, 500, 2)


def build_model(t, index, length):
    buffer = BUFFERS[index]
    for address in [0x90C0, 0x90C2, 0x90C4, 0x90C6]:
        w(t, address, 0, 2)
    error = r(t, 0x90B4 + index)
    critical_pair(t)
    w(t, 0x90AC + 2 * index, r(t, 0x90AC + 2 * index) | 128)
    if error:
        original = r(t, buffer)
        for offset, value in enumerate([0x7F, original, error]):
            w(t, buffer + offset, value)
        w(t, 0x90B0 + 2 * index, 3, 2)
    else:
        w(t, buffer, HEADERS[r(t, 0x90AB + 2 * index)])
        w(t, 0x90B0 + 2 * index, (length + 1) & 65535, 2)


def cleanup_model(t, index, argument):
    address = 0x90AC + 2 * index
    if r(t, 0x90B4 + index) == 0 and argument & 255 == 0:
        w(t, address, r(t, address) | 4)
    timer_model(t)
    w(t, 0x90A8, r(t, 0x90A8) & 239)
    if index == 0:
        w(t, 0x90C2, 0, 2)
        w(t, 0x90C4, 0, 2)
        w(t, 0x90AC, r(t, 0x90AC) & 199)
        w(t, 0x90B7, r(t, 0x90B7) & 191)
        w(t, 0x8F90, r(t, 0x8F90) & 63)
    else:
        critical_pair(t)
        w(t, address, r(t, address) & 223)


def handoff_model(t, index, length):
    critical_pair(t)
    w(t, 0x90A7, index ^ 1)
    w(t, 0x90B7, r(t, 0x90B7) & 127)
    if r(t, 0x90AC + 2 * index) & 2:
        build_model(t, index, length)
    else:
        cleanup_model(t, index, 0)


def wrapper_model(t, pointer, length):
    w(t, 0xA688, pointer, 4)
    w(t, 0xA68C, pointer, 4)
    w(t, 0xA690, length & 65535, 2)
    error = request.permission_model(t, 4)
    if not error:
        if length & 65535:
            error = 0x12
        elif not request.predicate_model(t):
            error = 0x22
        else:
            w(t, 0x9418, 1)
    result = request.response_model(t, error) if error else 0
    w(t, 0xA694, result, 2)
    handoff_model(t, r(t, 0x90A7), result)


def check(t, entry, model, argument=0, second=0):
    t.r[5] = second
    ref = copy.deepcopy(t)
    model(ref)
    pins.execute(t, entry, argument)
    source.equal(t, ref)


def direct():
    counts = dict(timer=0, build=0, cleanup=0, handoff=0, wrapper=0)
    for state, flags in itertools.product([0, 1, 2, 4, 255], range(256)):
        t = fixture(flags)
        w(t, 0x90B6, state)
        w(t, 0x90A8, flags)
        check(t, 0x1D83A, timer_model)
        counts['timer'] += 1
    for index, row, error, length in itertools.product(range(2), range(22), [0, 0x12], [0, 2, 65535]):
        t = fixture(row + length)
        w(t, 0x90AB + 2 * index, row)
        w(t, 0x90B4 + index, error)
        check(t, 0x1D85E, lambda ref: build_model(ref, index, length), index, length)
        counts['build'] += 1
    for index, bits, state, error, argument in itertools.product(range(2), range(64), [1, 2], [0, 0x12], [0, 1]):
        t = fixture(bits)
        flags = 0x41 | sum(((bits >> i) & 1) << bit for i, bit in enumerate([1, 2, 3, 4, 5, 7]))
        w(t, 0x90AC + 2 * index, flags)
        w(t, 0x90B6, state)
        w(t, 0x90B4 + index, error)
        check(t, 0x1D9F2, lambda ref: cleanup_model(ref, index, argument), index, argument)
        counts['cleanup'] += 1
    for index, flags, error in itertools.product(range(2), range(256), [0, 0x12]):
        t = fixture(flags)
        length = [0, 2, 32768, 65535][flags % 4]
        w(t, 0x90AC + 2 * index, flags)
        w(t, 0x90B4 + index, error)
        check(t, 0x1D94C, lambda ref: handoff_model(ref, index, length), index, length)
        counts['handoff'] += 1
    for index, state, length, blocked, mode, pending in itertools.product(
        range(2), [0, 1, 2, 4], [0, 1], [0, 1], range(4), [0, 0x31]
    ):
        t = fixture(index + state + length)
        for address, value in [(0x90A7, index), (0x90B6, state), (0x90AB + 2 * index, 3),
                               (0x90AC + 2 * index, 2 | (mode << 3)), (0x90B4 + index, pending),
                               (0xA962, blocked), (0xA98E, 0)]:
            w(t, address, value)
        w(t, 0x80A4, 100, 2)
        w(t, 0xB128, 100, 2)
        pointer = 0xFFFF0000 + BUFFERS[index] + 1
        check(t, 0x53B5C, lambda ref: wrapper_model(ref, pointer, length), pointer, length)
        assert {0x54AFC, 0x1D94C} <= t.visited
        counts['wrapper'] += 1
    return counts


def retained():
    t = writers.task_fixture()
    w(t, 0x90A7, 0)
    rows = []
    for call in range(24):
        event = None
        if call in [0, 1, 5, 6, 10, 11]:
            index = r(t, 0x90A7)
            buffer = BUFFERS[index]
            length = int(call in [5, 6])
            for address, value in [(0x90B6, 1), (0x90AB + 2 * index, 3),
                                   (0x90AC + 2 * index, 0x12 if call == 5 else 2),
                                   (0x90B4 + index, 0), (0xA962, 0), (0xA98E, 0),
                                   (0x8F66, 0), (buffer, 4)]:
                w(t, address, value)
            pointer = 0xFFFF0000 + buffer + 1
            check(t, 0x53B5C, lambda ref: wrapper_model(ref, pointer, length), pointer, length)
            event = dict(index=index, next_index=r(t, 0x90A7), result=r(t, 0xA694, 2),
                         bytes=[r(t, buffer + i) for i in range(3)],
                         length=r(t, 0x90B0 + 2 * index, 2), flags=r(t, 0x90AC + 2 * index),
                         pending_error=r(t, 0x90B4 + index), request=r(t, 0x9418))
        row = writers.task_call(t)
        row.update(call=call, event=event)
        rows.append(row)
    events = [row['event'] for row in rows if row['event']]
    assert [row['index'] for row in events] == [0, 1, 0, 1, 0, 1]
    assert all(events[i]['bytes'][0] == 0x44 and events[i]['length'] == 1 for i in [0, 1, 4, 5])
    assert events[2]['bytes'][0] == 4 and events[2]['flags'] & 128 == 0
    assert events[3]['bytes'] == [0x7F, 4, 0x12] and events[3]['length'] == 3
    return rows


def main():
    counts = direct()
    rows = retained()
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), counts=counts,
                  buffers=BUFFERS, headers=HEADERS, retained=rows,
                  limits='Incoming record flags/service rows/error resets and request interleaving are fixtures. Message construction only: no actual transport/acknowledgement, clock or hardware proof.')
    (ROOT / 'tcu-pulse-response-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(counts, 'retained tasks', len(rows), 'complete wrappers', 6, flush=True)


if __name__ == '__main__':
    main()
