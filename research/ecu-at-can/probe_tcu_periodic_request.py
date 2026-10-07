"""Observe request gates at actual complete126EC task boundaries.

Reuse prior cancellation-bit and enable-byte models. These are selected-field
oracles, not a complete RAM oracle for1FD24. Optional managed request is
created by original initializers/event1 with explicit application inputs.
Task cadence, peripheral samples and initial RAM remain fixtures.
"""
import hashlib
import json
from pathlib import Path

import verify_tcu_application_order as app
import verify_tcu_request_admission as admission
from verify_tcu_request_dispatch import WATCH
from verify_can201_byte6 import TCU, w, r

ROOT = Path(__file__).resolve().parent


class ObservedRequest(app.ObservedTask):
    def instruction(self, pc):
        if self.request_pending is not None and self.request_pending[0] == pc:
            _, address, mask, expected, entry = self.request_pending
            self.request_pending = None
            actual = r(self, address) & mask
            assert actual == expected, (hex(entry), expected, actual)
            self.request_checks.append(dict(entry=hex(entry), return_pc=hex(pc),
                                            address=hex(address), mask=mask,
                                            expected=expected, actual=actual))
        if pc == 0x1FD24:
            assert self.request_pending is None
            self.request_pending = (self.pr, 0x916F, 1,
                                    int(admission.cancelled(self)), pc)
        if pc == 0x23BF0:
            assert self.request_pending is None
            values = [r(self, a, n) for a, n in
                      [(0x9410, 1), (0x916D, 1), (0x80F6, 2),
                       (0x809A, 2), (0x809C, 2), (0x80EE, 2),
                       (0x80C8, 2), (0x8081, 1), (0x80C4, 2)]]
            expected = admission.gate_model(*values)
            self.request_pending = (self.pr, 0x9410, 255, expected, pc)
        if pc == 0x31524:
            self.request_events.append(dict(event=self.r[4], payload=self.r[5],
                                            caller=hex(self.pr)))
        if pc == 0x31A14:
            self.creation_callbacks.append(self.r[3])
        if pc in WATCH:
            self.request_calls.append(hex(pc))
        return super().instruction(pc)


def fixture(phase=0, managed=False):
    t = app.fixture(phase=phase)
    t.__class__ = ObservedRequest
    t.request_pending = None
    t.request_checks = []
    t.request_events = []
    t.request_calls = []
    t.creation_callbacks = []
    record = None
    if managed:
        t, record, _ = admission.upstream(t=t)
        # Restore application entry selection after explicit request initialization.
        for a, v in [(0x8007, 3), (0x84F5, 2), (0x84F4, phase)]:
            w(t, a, v)
    return t, record


def main():
    rows = []
    for managed in [False, True]:
        t, record = fixture(managed=managed)
        for call in range(24):
            t.request_checks = []
            t.request_events = []
            t.request_calls = []
            old_phase = r(t, 0x84F4) & 7
            before = {hex(a): r(t, a) for a in
                      [0x916F, 0x9410, 0xA2B8, 0xA2BA, 0xA1AC, 0x96C5]}
            try:
                result = app.run(t)
                assert t.request_pending is None
                assert [v['entry'] for v in t.request_checks] == (
                    ['0x1fd24', '0x23bf0'] if old_phase in [0, 4] else [])
                status, error = 'returned', None
            except (ValueError, RuntimeError, AssertionError, KeyError) as exc:
                result = None
                status, error = 'rejected', type(exc).__name__ + ': ' + str(exc)
            rows.append(dict(managed=managed, call=call, phase=old_phase,
                             status=status, error=error, pc=hex(t.pc),
                             before=before,
                             after={hex(a): r(t, a) for a in
                                    [0x916F, 0x9410, 0xA2B8, 0xA2BA,
                                     0xA1AC, 0x96C5]},
                             record=record,
                             record_bytes=([r(t, record+i) for i in range(20)]
                                           if record is not None else None),
                             checks=t.request_checks.copy(),
                             events=t.request_events.copy(),
                             callbacks=t.request_calls.copy(), application=result))
            if status != 'returned':
                break
    data = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), rows=rows)
    (ROOT/'tcu-periodic-request-probe.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps([dict(managed=managed,
                           completed=sum(v['managed']==managed and v['status']=='returned'
                                         for v in rows),
                           failures=[v['error'] for v in rows
                                     if v['managed']==managed and v['error']])
                      for managed in [False, True]]))


if __name__ == '__main__':
    main()
