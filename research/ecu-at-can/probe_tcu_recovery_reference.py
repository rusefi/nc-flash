"""Observe original reference/cache/phase boundaries in the recovery fixture.

No new firmware inputs: reuse seven-frame restoration and stop both external
capture callbacks at120. No phase, cache, age, source or fault injection.
Selected-output reference/discrepancy models and phase-predicate checks do not
claim a whole-RAM oracle for all209B4/20CBC/20FAC effects or physical cadence.
"""
import probe_tcu_receive_recovery as recovery
from verify_can201_byte6 import r
from verify_tcu_reference_source import branch_model
from verify_tcu_reference_policy import discrepancy
from verify_tcu_transition_classification import pending_model

FIELDS = [(0x8080,1),(0x8081,1),(0x8088,1),(0x96C4,1),(0x96C5,1),
          (0x8196,1),(0x810C,1),(0x810D,1),(0x9195,1),(0x9194,1),
          (0x91A6,1),(0x92C6,1),(0x91A8,2),(0x91C7,1),(0x91C4,2),
          (0x91C9,1),(0x91C6,1),(0x80EA,2),(0x80EC,2),(0x80EE,2),
          (0x91A2,2),(0x9198,4),(0x80A4,2),(0xAC87,1)]


def state(t):
    out = {hex(a): r(t,a,n) for a,n in FIELDS}
    head = r(t,0x96C4)
    out['head_phase'] = r(t,0x95D4+15*head+13)
    return out


class Observed(recovery.Observed):
    def instruction(self, pc):
        while self.reference_pending and self.reference_pending[-1]['return_pc'] == pc:
            b = self.reference_pending.pop()
            b['after'] = state(self)
            b['returned'] = self.r[0]
            if b['entry'] == '0x31720':
                assert self.r[0] == b['expected'], ('31720', b)
                b['predicate_checked'] = True
            elif b['entry'] == '0x20fac':
                e = b['expected']
                assert [r(self,a,n) for a,n in [(0x91A6,1),(0x91C6,1),(0x91C4,2),(0x91C9,1)]] == [e[k] for k in ['flags','count','cache','index']]
                assert [r(self,0x91B8+2*i,2) for i in range(6)] == e['history']
                b['discrepancy_checked'] = True
            elif b['entry'] == '0x209b4':
                e = b['expected']
                assert self.r[0] == e['result'] and r(self,0x80EC,2) == e['reference']
                assert r(self,0x9198,4) == e['period'] & 0xFFFFFFFF
                assert r(self,0x91A6) == e['flags']
                assert r(self,0x9194) & 2 == 2*bool(e['flags'] & 4)
                b['reference_checked'] = True
            self.reference_checks.append(b)
        if pc in [0x209B4, 0x20CBC, 0x20FAC, 0x31720]:
            b = dict(entry=hex(pc), return_pc=self.pr, before=state(self))
            if pc == 0x20FAC:
                b['expected'] = discrepancy(self, bool(pending_model(self)))
            elif pc == 0x31720:
                b['expected'] = pending_model(self)
            self.reference_pending.append(b)
        if pc == 0x20AAC:
            b = self.reference_pending[-1]
            assert b['entry'] == '0x209b4'
            b['branch_inputs'] = state(self)
            b['selected_registers'] = {str(i): self.r[i] for i in [5,6,9,10]}
            b['expected'] = branch_model(self, self.r)
        return super().instruction(pc)


def fixture():
    t = recovery.fixture()
    t.__class__ = Observed
    t.reference_pending, t.reference_checks = [], []
    t.capture_enabled = lambda call, entry: call < 120
    return t


def before_task(t, call):
    assert not t.reference_pending
    t.reference_checks = []
    recovery.before_task(t, call)


def after_task(t, call):
    out = recovery.after_task(t, call)
    assert not t.reference_pending
    out['reference_checks'] = t.reference_checks
    return out


def main(approach=False, second_approach=False):
    approach = approach or second_approach
    def configured():
        t = fixture()
        if approach:
            t.measured_interval = lambda call: 5890 if call < 48 else 6490 if call < 80 else 4430
            t.capture_enabled = lambda call, entry: call < 220
        if second_approach:
            t.measured_interval = lambda call: (5890 if call < 48 else 6490 if call < 80
                                                else 4430 if call < 128 else 9120)
            t.capture_enabled = lambda call, entry: call < 280
        return t
    scope = __doc__
    if approach:
        scope += ('\nVariant: measured timestamp interval4430 from80; stopbothcaptures220; '
                  '256pairs. Externalinputs only; no phase/ack/source injection.')
    if second_approach:
        scope += ('\nSecond approach overrides prior stop/length: interval9120 from128, '
                  'stopbothcaptures280, 320pairs; other inputs unchanged.')
    recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=320 if second_approach else 256 if approach else 160,timer=True,
        filename='tcu-recovery-reference-second-approach.json' if second_approach else 'tcu-recovery-reference-target-approach.json' if approach else 'tcu-recovery-reference-probe.json',
        machine_factory=configured,before_task=before_task,after_task=after_task,scope=scope)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approach', action='store_true')
    parser.add_argument('--second-approach', action='store_true')
    args = parser.parse_args()
    main(args.approach, args.second_approach)
