"""Original TCU list lifecycle -> request slot2 -> CAN216 -> ECU spark.

Uses startup-copied descriptors, real allocation/set/release/select routines.
Candidate values/modes are fixtures; physical policy entry and time are open.
"""
import itertools
import json
from pathlib import Path
import random

from verify_tcu_spark_requests import initialized, put, reference
from verify_can201_byte6 import TCU, w, r
from verify_spark_interaction import paired
from sh_subset import signed

BANKS = [dict(base=0xA20A, flags=0xA245, count=0xA202, capacity=12,
              init=0x4C69A, allocate=0x4C6C2, set=0x4C6DA, release=0x4C734,
              selected=0xA244, value=0xA204, mode=0xA208),
         dict(base=0xA25A, flags=0xA271, count=0xA258, capacity=3,
              init=0x4CA64, allocate=0x4CA90, set=0x4CAA8, release=0x4CACE,
              selected=0xA270, value=0xA206, mode=0xA209)]


def fixture():
    t = initialized()
    t.run(0x15D04)  # Entire real startup data-copy function.
    assert bytes(r(t, 0xAD4C+i) for i in range(0x3E0)) == TCU[0x5F220:0x5F600]
    assert r(t, 0xB028, 4) == 0x010C7FFF
    assert r(t, 0xB02C, 4) == 0x01037FFF
    for bank in BANKS:
        t.run(bank['init'])
    w(t, 0x80B4, 250, 2)
    t.run(0x216D8)
    assert r(t, 0x92E4, 2) == 800
    return t


def allocate(t, bank):
    return t.run(bank['allocate'], 1) & 255


def update(t, bank, index, value, mode):
    assert 2 <= index < 2 + bank['capacity']
    t.r[5], t.r[6] = value & 65535, mode
    t.run(bank['set'], index)


def selected(active, values):
    if not active:
        return 255, 32767, 0
    index = next((i for i in active if values[i][0] != 32767), active[-1])
    return index, *values[index]


def merged(a, b):
    va, ma = a
    vb, mb = b
    if ma == mb:
        if signed(va, 16) < signed(vb, 16) and vb != 32767:
            return vb, mb
    elif mb == 1:
        return vb, 1
    return va, ma


def verify(t, models):
    t.run(0x4C7AC)
    candidates = []
    for bank, (active, free, values) in zip(BANKS, models):
        assert r(t, bank['count'], 2) == len(active)
        # Independent high-level queue model also checks the original linked
        # nodes, including the free-list head and both forward/back links.
        for head, members in [(0, active), (1, free)]:
            chain = [head] + members
            for pos, index in enumerate(chain):
                assert r(t, bank['base'] + 4*index) == chain[pos-1]
                assert r(t, bank['base'] + 4*index + 1) == chain[(pos+1) % len(chain)]
        index, value, mode = selected(active, values)
        assert r(t, bank['selected']) == index
        assert r(t, bank['value'], 2) == value
        assert r(t, bank['mode']) == mode
        candidates.append((value, mode))
    value, mode = merged(*candidates)
    assert r(t, 0x80E4, 2) == value
    expected = (32767, 255) if value == 32767 else (value, mode)
    assert (r(t, 0x9160, 2), r(t, 0x9168)) == expected
    t.run(0x1FB8C)
    _, _, _, _, output = reference(
        [r(t, 0x915C + 2*i, 2) for i in range(5)],
        [r(t, 0x9166 + i) for i in range(5)], 800)
    assert r(t, 0x915A, 2) == output
    return output


def empty_models():
    return [([], list(range(2, 2+b['capacity'])), {}) for b in BANKS]


def add(t, bank, model, value, mode):
    active, free, values = model
    index = allocate(t, bank)
    assert index == free.pop(0)
    active.append(index)
    values[index] = (value & 65535, mode)
    update(t, bank, index, value, mode)
    return index


def main():
    t = fixture()
    models = empty_models()
    assert verify(t, models) == 32767
    capacity_checks = []
    for which, bank in enumerate(BANKS):
        t = fixture()
        models = empty_models()
        model = models[which]
        for _ in range(bank['capacity']):
            add(t, bank, model, 32767, 0)
            verify(t, models)
        # Failed allocation still increments the wrapper's bookkeeping word.
        assert allocate(t, bank) == 255
        assert r(t, bank['count'], 2) == bank['capacity'] + 1
        capacity_checks.append({'capacity': bank['capacity'], 'failed_handle': 255,
                                'counter_after_failure': r(t, bank['count'], 2)})
        # Reset this independent fixture; never pass FF to an unchecked setter.

    choices = [None] + list(itertools.product([0, 1, 320, 640, 32767, 32768, 65535], [0, 1, 2, 255]))
    merge_cases = 0
    examples = []
    for first, second in itertools.product(choices, repeat=2):
        t = fixture()
        models = empty_models()
        for bank, model, value in zip(BANKS, models, [first, second]):
            if value is not None:
                add(t, bank, model, *value)
        source = verify(t, models)
        if (first, second) in [(None, (320, 0)), (None, (320, 1)),
                               ((32767, 1), (320, 1)), ((320, 1), (640, 1)),
                               ((640, 0), (320, 1)), ((640, 1), (320, 2))]:
            examples.append({'first': first, 'second': second,
                             'slot2': r(t, 0x9160, 2), 'mode': r(t, 0x9168), 'source915A': source})
        merge_cases += 1

    # Stateful lists exercise insertion order, sentinel skipping, removal,
    # recycling and count/link invariants using independent Python queues.
    rng = random.Random(216)
    t = fixture()
    models = empty_models()
    list_cases = 0
    for _ in range(600):
        which = rng.randrange(2)
        bank, model = BANKS[which], models[which]
        active, free, values = model
        action = rng.choice(['allocate', 'update', 'release'])
        if not active or (action == 'allocate' and free):
            add(t, bank, model, rng.choice([0, 320, 640, 32767, 32768, 65535]), rng.choice([0, 1, 2, 255]))
        elif action == 'release':
            index = rng.choice(active)
            t.run(bank['release'], index)
            active.remove(index)
            free.append(index)
            assert r(t, bank['flags'] + index) == 0
        else:
            index = rng.choice(active)
            values[index] = (rng.choice([0, 320, 640, 32767, 32768, 65535]), rng.choice([0, 1, 2, 255]))
            update(t, bank, index, *values[index])
        verify(t, models)
        list_cases += 1

    paired_cases = []
    for first, second, record1, cut in itertools.product(
        [None, (320, 1), (32767, 1)], [None, (0, 1), (320, 1), (640, 1), (640, 0)],
        [None, 320], [0, 1]
    ):
        t = fixture()
        models = empty_models()
        for bank, model, candidate in zip(BANKS, models, [first, second]):
            if candidate is not None:
                add(t, bank, model, *candidate)
        if record1 is not None:
            put(t, 1, record1, 1)
        source = verify(t, models)
        result = paired(source, 16, 1, 1, cut, t=t)
        paired_cases.append({'first': first, 'second': second, 'record1': record1, **result})

    # One original policy callback, supplied with a valid allocated handle.
    # Stock773E8=0 makes this callback publish zero/mode0, not an active demand.
    t = fixture()
    models = empty_models()
    index = add(t, BANKS[1], models[1], 640, 1)
    record = 0xA2B0  # Explicit synthetic callback record, separate from lists.
    w(t, record+4, index)
    w(t, record+8, 255)
    t.r[5] = 0xFFFF0000 + record
    t.run(0x4D98A)
    assert TCU[0x773E8:0x773EA] == b'\0\0'
    assert r(t, record+2, 2) == 0 and r(t, record+8) == 127
    models[1][2][index] = (0, 0)
    assert verify(t, models) == 32767
    callback = {'entry': '4D98A', 'calibration773E8': 0, 'value': 0, 'mode': 0,
                'aggregate_source915A': r(t, 0x915A, 2), 'entry_conditions_unproved': True}

    result = {'startup_copy': {'source': '5F220..5F5FF', 'destination': 'FFFFAD4C..FFFFB12B', 'bytes_verified': 992,
                              'descriptor_A': '010C7FFF', 'descriptor_B': '01037FFF'},
              'capacity_checks': capacity_checks, 'merge_cases': merge_cases,
              'stateful_list_cases': list_cases, 'merge_examples': examples,
              'paired_cases': paired_cases, 'stock_policy_callback': callback,
              'scope': 'Original initialized list mechanics and slot2 merge through CAN216/ECU spark. Candidate fixtures do not prove physical policy entry, gear or real timing.'}
    Path(__file__).with_name('tcu-slot2-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: (len(v) if k == 'paired_cases' else v) for k, v in result.items()}, indent=2))


if __name__ == '__main__':
    main()
