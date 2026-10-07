"""Observe original numeric/phase boundaries within received-frame/capture task.

Reuse independent map, release, phase and output models at actual returns.
Optional capture interval change is an external timestamp fixture only.
No phase, request, acknowledgement, reference or permission state injection.
"""
import probe_tcu_received_captured_requests as received
import verify_tcu_ascending_phase as phase
from verify_tcu_ascending_map import candidate
from verify_tcu_ascending_release import release
from verify_tcu_spark_requests import reference
from verify_tcu_slot2 import BANKS
from verify_can201_byte6 import TCU, r


class Observed(received.Received):
    def instruction(self, pc):
        if self.numeric_pending and self.numeric_pending[-1]['return_pc'] == pc:
            row = self.numeric_pending.pop()
            entry, expected = row['entry'], row['expected']
            if entry == 0x32614:
                index = row['index']
                actual = (self.r[0], r(self, 0x96CF+index),
                          r(self, 0x96DF+index), r(self, 0x971A))
            elif entry == 0x1FB8C:
                actual = ([r(self, 0x915C+2*i, 2) for i in range(5)],
                          [r(self, 0x9166+i) for i in range(5)],
                          r(self, 0x80BE, 2), r(self, 0x9158), r(self, 0x915A, 2))
            else:
                p = row['record']
                actual = ((r(self, p+4, 2), r(self, p+8)) if entry == 0x4E036
                          else (r(self, p+4, 2), r(self, p+6, 2), r(self, p+8)))
                handle = r(self, p+2)
                assert r(self, BANKS[0]['base']+4*handle+2, 2) == expected[0]
                assert r(self, BANKS[0]['flags']+handle) == int(expected[0] > 0)
            assert actual == expected, (hex(entry), actual, expected, row)
            row['actual'] = actual
            self.numeric_checks.append(row)
        if pc in [0x32614, 0x4E036, 0x4E0EE, 0x1FB8C]:
            row = dict(entry=pc, return_pc=self.pr)
            if pc == 0x32614:
                index, code, operation = [self.r[i] & 65535 for i in [4, 5, 6]]
                args = phase.inputs(self, index, code, operation)
                row.update(index=index, inputs=args, expected=phase.model(*args))
            elif pc == 0x1FB8C:
                values = [r(self, 0x915C+2*i, 2) for i in range(5)]
                flags = [r(self, 0x9166+i) for i in range(5)]
                base = r(self, 0x92E4, 2)
                vv, ff, selected, flag, result = reference(values, flags, base)
                expected = (vv, ff, (-selected) & 65535,
                            (r(self, 0x9158) & 254) | int(flag != 0), result)
                row.update(inputs=[values, flags, base], expected=expected)
            else:
                p = self.r[5] & 65535
                code = r(self, p+1)
                row['record'] = p
                if pc == 0x4E036:
                    args = (code, r(self, 0x80F8, 2), r(self, p+18, 2),
                            r(self, p+16, 2), r(self, p+8), r(self, 0x8276))
                    value = candidate(*args)
                    permission, inhibit = r(self, 0x9410), r(self, 0x92D5)
                    if inhibit & 1 or not permission & 1:
                        value = 0
                    row.update(permission=permission, inhibit=inhibit,
                               inputs=args, expected=(value, (args[4] & 127) | (128 if value else 0)))
                else:
                    args = (code, r(self, p+12), r(self, 0x80EA, 2), r(self, 0x80F0, 2),
                            r(self, 0x80EE, 2), r(self, 0x9218+4*TCU[0x5D446+code], 4),
                            r(self, p+10, 2), r(self, p+4, 2), r(self, p+6, 2), r(self, p+8))
                    row.update(inputs=args, expected=release(*args)[:3])
            self.numeric_pending.append(row)
        return super().instruction(pc)


def fixture():
    t = received.fixture()
    t.__class__ = Observed
    t.numeric_pending = []
    t.numeric_checks = []
    return t


def approach_fixture():
    t = fixture()
    t.measured_interval = lambda call: 5890 if call < 48 else 6490 if call < 256 else 4430
    return t


def before_task(t, call):
    assert not t.numeric_pending
    t.numeric_checks = []
    received.before_task(t, call)


def after_task(t, call):
    assert not t.numeric_pending
    row = received.after_task(t, call)
    row['numeric_checks'] = t.numeric_checks
    return row


def main(approach=False):
    received.capture.task.main(cycles=512 if approach else 256, timer=True,
        filename='tcu-captured-phase-approach.json' if approach else 'tcu-captured-phase-probe.json',
        machine_factory=approach_fixture if approach else fixture,
        before_task=before_task, after_task=after_task, scope=__doc__)


if __name__ == '__main__':
    import sys
    main('--approach' in sys.argv)
