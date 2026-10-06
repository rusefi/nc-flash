"""Original proposal scan and pending-work/history/qualification classification.

Independent models observe complete original bodies, including software map
arithmetic. Physical meaning of 96C8/CA/CC and real task timing stay open.
"""
import hashlib
import itertools
import json
import random

from sh_subset import signed
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, w, r
from verify_tcu_request_maps import lookup
from verify_tcu_request_dispatch import curve
from verify_tcu_source_selection import SampledSelection, manager_traces, sample
from verify_tcu_ascending_map import lifecycle
from verify_tcu_request_admission import paired_snapshot


CODE_TABLE = [list(TCU[a:a+6]) for a in range(0x5E1AC, 0x5E1E8, 6)]
PENDING_GROUPS = [i for i in range(10) if TCU[0x5D3BC+4*i+2] == 0]


def proposal_model(t):
    old = value = r(t, 0x8084)
    operation = r(t, 0x9B3D)
    measured = r(t, 0x80EA, 2)
    for step in range(5):
        up, down = old+step, 9-step
        if up < 5:
            change = measured >= r(t, 0x9B1E+2*up, 2) and value != 5
            if change:
                value = (value+1) & 255
                operation = r(t, 0x9B14+up)
        else:
            change = measured < r(t, 0x9B1E+2*down, 2) and value != 0
            if change:
                value = (value-1) & 255
                operation = r(t, 0x9B14+down)
    return value, operation


def qualification_model(t):
    limit = max(r(t, 0x939E, 2), int.from_bytes(TCU[0x7734A:0x7734C], 'big'))
    x, y, z = [r(t, a, 2) for a in [0x96C8, 0x96CA, 0x96CC]]
    values = [lookup(0x75144, x, z), curve(0x75166, y), lookup(0x75155, z, y)]
    flags = r(t, 0x9C54) & 248
    for i, (value, source) in enumerate(zip(values, [x, y, z])):
        flags |= int(value >= limit or source == 25600) << i
    return limit, flags


def pending_model(t):
    if r(t, 0x8088) != 2:
        return 0
    head, count = r(t, 0x96C4), r(t, 0x96C5)
    if r(t, 0x95D4+15*head+13) in [0, 1, 2]:
        return 1
    return int(any(r(t, 0x95D4+15*((head+i) % 16)+g) == 0
                   for i in range(count) for g in PENDING_GROUPS))


def history_model(t, old, accepted):
    old, accepted = old & 255, accepted & 255
    measured = signed(r(t, 0x80EE, 2), 16)
    value = old
    if old < accepted and measured <= signed(r(t, 0x9218+4*(old+1), 4)+128):
        value += 1
    elif old > accepted and measured > signed(r(t, 0x9218+4*old, 4)-128):
        value -= 1
    if not pending_model(t) or signed(r(t, 0x80EA, 2), 16) < 256 or r(t, 0x8080) == 255:
        value = accepted
    return value


def row_model(history, proposed, flags):
    history, proposed = history & 255, proposed & 255
    if history == 0:
        return 0
    if history == 1:
        return 2 if flags & 1 else 1
    if history == 2:
        if proposed == 1:
            return 4 if flags & 1 else 3
        if proposed == 2:
            return 6 if flags & 4 else 5
        return 3
    return {3: 7, 4: 8}.get(history, 9)


def code_model(history, accepted, proposed, flags):
    proposed &= 255
    assert proposed < 6
    return 255 if (accepted & 255) == proposed else CODE_TABLE[row_model(history, proposed, flags)][proposed]


def classification_model(t, operation, proposed):
    limit, flags = qualification_model(t)
    accepted = r(t, 0x8081)
    history = history_model(t, r(t, 0x9C50), accepted)
    code = code_model(history, accepted, proposed, flags)
    code = {20: 11, 21: 10, 22: 10, 25: 9, 26: 3}.get(operation & 255, code)
    return code, history, limit, flags


class ObservedClassification(SampledSelection):
    """Read-only assertions at original entry/return; no policy substitutions."""
    def __init__(self):
        super().__init__()
        self.proposal_checks = 0
        self.classification_checks = 0
        self.classification_rows = []
        self.proposal_rows = []
        self.creation_calls = []
        self.pending_proposal = self.pending_classification = None

    def instruction(self, pc):
        if pc == 0x319BC:
            self.creation_calls.append([self.r[i] & 255 for i in [4,5,6]])
        if pc == 0x4508A:
            p, q = self.r[4], self.r[5]
            row = dict(old=r(self, 0x8084), measured=r(self, 0x80EA, 2),
                       thresholds=[r(self, 0x9B1E+2*i, 2) for i in range(10)],
                       operations=[r(self, 0x9B14+i) for i in range(10)])
            self.pending_proposal = p, q, proposal_model(self), row
        elif pc == 0x450F8:
            p, q, expected, row = self.pending_proposal
            assert (self.read(p, 1), self.read(q, 1)) == expected
            row.update(proposed=expected[0], operation=expected[1])
            if not self.proposal_rows or self.proposal_rows[-1] != row:
                self.proposal_rows.append(row)
            self.proposal_checks += 1
            self.pending_proposal = None
        elif pc == 0x4744C:
            operation, proposed = self.r[4] & 255, self.r[5] & 255
            expected = classification_model(self, operation, proposed)
            row = dict(operation=operation, proposed=proposed, accepted=r(self, 0x8081),
                       old_history=r(self, 0x9C50), pending=pending_model(self),
                       axes=[r(self, a, 2) for a in [0x96C8, 0x96CA, 0x96CC]])
            self.pending_classification = expected, row
        elif pc == 0x474AC:
            expected, row = self.pending_classification
            actual = self.r[0] & 255, r(self, 0x9C50), r(self, 0x9C52, 2), r(self, 0x9C54)
            assert actual == expected, (actual, expected, row)
            row.update(code=actual[0], history=actual[1], limit=actual[2], flags=actual[3])
            if not self.classification_rows or self.classification_rows[-1] != row:
                self.classification_rows.append(row)
            self.classification_checks += 1
            self.pending_classification = None
        return super().instruction(pc)


def direct_cases():
    counts = dict(proposal=0, pending=0, qualification=0, history=0, row=0, code=0, classification=0)
    rng = random.Random(0x4744C)
    t = SHRotate(TCU)
    for old, trial in itertools.product(range(256), range(12)):
        thresholds = [rng.randrange(65536) for _ in range(10)]
        measured = [0, 65535, thresholds[trial % 10], (thresholds[trial % 10]-1) & 65535][trial % 4]
        w(t, 0x8084, old); w(t, 0x80EA, measured, 2); w(t, 0x9B3D, 199)
        for i, value in enumerate(thresholds):
            w(t, 0x9B1E+2*i, value, 2); w(t, 0x9B14+i, 128+i)
        expected = proposal_model(t)
        w(t, 0xA900, 0xA1B2C3D4, 4)
        t.r[5] = 0xFFFFA902
        t.run(0x4508A, 0xFFFFA901)
        assert (r(t, 0xA901), r(t, 0xA902)) == expected
        assert (r(t, 0xA900), r(t, 0xA903), r(t, 0x8084)) == (0xA1, 0xD4, old)
        counts['proposal'] += 1
    assert PENDING_GROUPS == list(range(1, 8))
    for head, phase, bitmap in itertools.product([0, 15], [0, 1, 2, 3, 255], range(1024)):
        w(t, 0x8088, 2); w(t, 0x96C4, head); w(t, 0x96C5, 1)
        w(t, 0x95D4+15*head+13, phase)
        for g in range(10):
            w(t, 0x95D4+15*head+g, 128 if bitmap & (1 << g) else 0)
        assert t.run(0x31720) == pending_model(t)
        counts['pending'] += 1
    for mode, head, count, phase in itertools.product([0,1,2,255], [0,7,15], [0,1,2,16], [0,3]):
        w(t, 0x8088, mode); w(t, 0x96C4, head); w(t, 0x96C5, count)
        for i in range(16):
            w(t, 0x95D4+15*i+13, phase)
            for g in range(10): w(t, 0x95D4+15*i+g, 1)
        if count: w(t, 0x95D4+15*((head+count-1)%16)+7, 0)
        assert t.run(0x31720) == pending_model(t)
        counts['pending'] += 1
    for x, y, z in itertools.product([0,6400,12800,25599,25600,25601,65535], repeat=3):
        for limit in [0, 9600, 22528, 65535]:
            w(t, 0x939E, limit, 2); w(t, 0x9C54, rng.randrange(256))
            for a, v in zip([0x96C8,0x96CA,0x96CC], [x,y,z]): w(t,a,v,2)
            expected = qualification_model(t)
            t.run(0x474C4)
            assert (r(t,0x9C52,2),r(t,0x9C54)) == expected
            counts['qualification'] += 1
    for old, accepted, measured, ref in itertools.product(range(6), range(6), [0,127,128,129,32767,32768,65535], [0,256,5000,0x7FFFFFFF,0x80000000]):
        for i in range(6): w(t, 0x9218+4*i, ref, 4)
        w(t,0x8088,2); w(t,0x96C4,0); w(t,0x95E1,0); w(t,0x8080,6)
        w(t,0x80EE,measured,2); w(t,0x80EA,256,2)
        expected = history_model(t,old,accepted)
        t.r[5] = accepted
        assert t.run(0x475DC,old) & 255 == expected
        counts['history'] += 1
    for mode, phase, count, source, measured in itertools.product([1,2], [0,3], [0,1], [6,255], [255,256,32767,32768,65535]):
        w(t,0x8088,mode); w(t,0x95E1,phase); w(t,0x96C5,count); w(t,0x8080,source)
        w(t,0x80EA,measured,2)
        t.r[5] = 5
        expected = history_model(t,0,5)
        assert t.run(0x475DC,0) & 255 == expected
        counts['history'] += 1
    for history, proposed, flags in itertools.product(range(256), range(6), range(8)):
        w(t,0x9C54,flags | 0xA0); t.r[5] = proposed
        assert t.run(0x476A4,history) == row_model(history,proposed,flags)
        counts['row'] += 1
    for history, accepted, proposed, flags in itertools.product([0,1,2,3,4,5,255], range(6), range(6), range(8)):
        w(t,0x9C54,flags); t.r[5], t.r[6] = accepted,proposed
        assert t.run(0x47670,history) == code_model(history,accepted,proposed,flags)
        counts['code'] += 1
    for operation, proposed, accepted in itertools.product(range(256), [1,2], [1,2]):
        for a,v in [(0x9C50,1),(0x8081,accepted),(0x8080,6),(0x8088,2),(0x95E1,0)]: w(t,a,v)
        for a,v in [(0x80EA,4672),(0x80EE,1000),(0x939E,0),(0x96C8,12800 if operation%2 else 0),(0x96CA,0),(0x96CC,0)]: w(t,a,v,2)
        w(t,0x9220,5000,4)
        expected = classification_model(t,operation,proposed)
        t.r[5] = proposed
        code = t.run(0x4744C,operation)
        assert (code,r(t,0x9C50),r(t,0x9C52,2),r(t,0x9C54)) == expected
        counts['classification'] += 1
    return counts


def first_selection(axis):
    """Bounded original two-record creation, followed by original CAN builders.

    The lifecycle is deliberately stopped before periodic service. This probe
    claims creation/publication only; the separate retained traces retire both.
    """
    t = ObservedClassification()
    class CreationObserved(Exception):
        pass
    result = {}
    def upstream(t, call):
        assert call == 1
        t.run(0x17230); t.run(0x17D54)
        w(t,0x921C,6500,4)
        w(t,0x96C8,axis,2)  # Explicit upstream axis, never a flag/code injection.
        sample(t,0)
        t.run(0x44CFE,limit=1000000)
        t.run(0x48C08,limit=1000000)
        result.update(axis96c8=axis, proposal=t.proposal_rows,
                      classification=t.classification_rows,
                      phase_codes=[r(t,0x95DE+15*((r(t,0x96C4)+i)%16)) for i in range(r(t,0x96C5))],
                      accepted=r(t,0x8081), published_code=r(t,0x9C87),
                      published_operation=r(t,0x9C88), head=r(t,0x96C4),
                      creation_calls=t.creation_calls, acknowledgements=t.acks,
                      retired_callbacks=t.retired,
                      stored_records=[[r(t,0x95D4+15*i+j) for j in range(15)] for i in [0,1]],
                      **paired_snapshot(t))
        raise CreationObserved
    try:
        lifecycle(25000,t=t,upstream=upstream)
    except CreationObserved:
        pass
    assert result and result['published_code'] == (6 if axis else 0), result
    assert result['phase_codes'] == ([6] if axis else [1,0]), result
    assert result['creation_calls'] == [[1,0,0],[6 if axis else 0,8,0]]
    assert result['retired_callbacks'] == ([(a,1) for a in [0x30B82,0x30A9E,0x31168]] if axis else [])
    assert result['head'] == int(bool(axis))
    return result


def main():
    counts = direct_cases()
    print('direct checks:', counts, flush=True)
    probes = [first_selection(axis) for axis in [0,12800]]
    instances = []
    def factory():
        t = ObservedClassification()
        instances.append(t)
        return t
    traces = manager_traces(t_factory=factory)
    with open('research/ecu-at-can/tcu-source-selection-verification.json') as f:
        previous = json.load(f)
    # Compare the existing retained caller result, not just the new counters.
    assert traces == previous['manager_traces']
    observed = []
    for t in instances:
        assert t.pending_proposal is None and t.pending_classification is None
        observed.append(dict(proposal_checks=t.proposal_checks,
                             classification_checks=t.classification_checks,
                             proposals=t.proposal_rows, classifications=t.classification_rows))
    result = dict(tcu_sha256=hashlib.sha256(TCU).hexdigest(), direct_cases=counts,
                  code_table=CODE_TABLE, pending_groups=PENDING_GROUPS,
                  creation_probes=probes, retained_observations=observed,
                  prior_manager_traces_identical=True)
    path = 'research/ecu-at-can/tcu-transition-classification-verification.json'
    with open(path,'w') as f: json.dump(result,f,indent=2); f.write('\n')
    print(path, flush=True)


if __name__ == '__main__':
    main()
