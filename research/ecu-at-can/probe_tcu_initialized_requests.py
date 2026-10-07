"""Complete126EC task after the existing62 original group initializers.

No injected creation or ack event. External samples and RAM not initialized by
these routines remain explicit fixtures; this is not full boot or physical time.
Retain actual transition messages, admission outcomes and managed-ring records.
"""
import hashlib
import json
from pathlib import Path

import probe_tcu_periodic_request as prior
import verify_tcu_phase_retirement as retirement
from verify_can201_byte6 import TCU, w, r
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent


def snapshot(t):
    addresses = [0x8007, 0x8080, 0x8081, 0x8084, 0x8088, 0x84F4, 0x84F5,
                 0x916F, 0x9410, 0x9545, 0x96C4, 0x96C5, 0x96C6,
                 0x9C87, 0x9C88, 0x9C8A, 0xA1AC, 0xA2B8, 0xA2B9, 0xA2BA]
    result = {hex(a): r(t, a) for a in addresses}
    result['request_word_915a'] = r(t, 0x915A, 2)
    result['first_list_count_a202'] = r(t, 0xA202, 2)
    result['ramp_timers_8115'] = [r(t, 0x8115+i) for i in range(12)]
    result['primary_timer_phase_8494'] = r(t, 0x8494, 4)
    result['heap_first_header_9f3c'] = r(t, 0x9F3C, 4)
    count, head = r(t, 0xA2BA), r(t, 0xA2B9)
    assert count <= 12 and head < 12, (count, head)
    result['managed'] = []
    for n in range(count):
        entry = 0xA2BC+12*((head+n) % 12)
        pointer = r(t, entry, 4)
        result['managed'].append(dict(index=(head+n) % 12, pointer=hex(pointer),
                                      entry=[r(t, entry+i) for i in range(12)],
                                      record=[t.read(pointer+i, 1) for i in range(20)]))
    count, head = r(t, 0x96C5), r(t, 0x96C4)
    assert count <= 16 and head < 16, (count, head)
    result['phases'] = [dict(index=(head+n) % 16,
                             bytes=[r(t, 0x95D4+15*((head+n) % 16)+i)
                                    for i in range(15)]) for n in range(count)]
    return result


def observe_initialized(self, pc):
    if self.ack_pending is not None and self.ack_pending[0] == pc:
        _, expected, result, callbacks, old_count, args = self.ack_pending
        self.ack_pending = None
        actual = ram(self)
        assert actual == expected, {hex(a): (actual.get(a, 0), expected.get(a, 0))
                                   for a in actual.keys() | expected.keys()
                                   if actual.get(a, 0) != expected.get(a, 0)}
        assert self.r[0] == result
        assert self.retired[old_count:] == [[hex(fn), code] for fn, code in callbacks]
        self.ack_checks.append(dict(arguments=args, return_pc=hex(pc),
                                    retired=callbacks, result=result))
    if self.creation_returns and self.creation_returns[-1]['return_pc'] == pc:
        entry = self.creation_returns.pop()
        entry['after'] = snapshot(self)
    if pc == 0x31524 and self.r[4] == 1:
        pointer = self.r[5]
        entry = dict(return_pc=self.pr,
                     payload=[self.read(pointer+i, 2) for i in [0, 2, 4]],
                     before=snapshot(self))
        self.creations.append(entry)
        self.creation_returns.append(entry)
    if pc == 0x31C18:
        args = [self.r[4] & 255, self.r[5] & 65535]
        self.acks.append(args)
        assert self.ack_pending is None
        ref = SHRotate(TCU)
        ref.ram = dict(self.ram)
        result, callbacks = retirement.ack_model(ref, *args)
        self.ack_pending = (self.pr, ram(ref), result, callbacks,
                            len(self.retired), args)
    if pc in retirement.CALLBACKS:
        self.retired.append([hex(pc), self.r[4] & 65535])


class ObservedInitialized(prior.ObservedRequest):
    def instruction(self, pc):
        observe_initialized(self, pc)
        return super().instruction(pc)

def fixture():
    t, _ = prior.fixture()
    t.__class__ = ObservedInitialized
    t.creations = []
    t.creation_returns = []
    t.acks = []
    t.ack_pending = None
    t.ack_checks = []
    t.retired = []
    retirement.full_fixture(t)
    for a, v in [(0x8007, 3), (0x84F5, 2), (0x84F4, 0)]:
        w(t, a, v)
    return t


def run_primary_timer(t):
    if hasattr(t, 'primary_delivery'):
        t.primary_delivery()
    else:
        t.run(0x11014)


def main(cycles=32, timer=False, filename='tcu-initialized-requests-probe.json',
         machine_factory=fixture, before_task=None, after_task=None, scope=None):
    t = machine_factory()
    initial = snapshot(t)
    rows = []
    for call in range(cycles):
        t.creations = []
        t.acks = []
        t.ack_checks = []
        t.retired = []
        t.request_checks = []
        t.request_events = []
        t.request_calls = []
        before = snapshot(t)
        try:
            if timer:
                run_primary_timer(t)
            if before_task is not None:
                before_task(t, call)
            result = prior.app.run(t)
            assert not t.creation_returns and t.request_pending is None and t.ack_pending is None
            extra = after_task(t, call) if after_task is not None else None
            status, error = 'returned', None
        except (ValueError, RuntimeError, AssertionError, KeyError) as exc:
            status, error = 'rejected', type(exc).__name__+': '+str(exc)
            result = None
            extra = None
        rows.append(dict(call=call, status=status, error=error, pc=hex(t.pc),
                         before=before, after=snapshot(t), creations=t.creations,
                         acks=t.acks, ack_checks=t.ack_checks,
                         retired=t.retired, checks=t.request_checks,
                         events=t.request_events, callbacks=t.request_calls,
                         application=result))
        if extra is not None:
            rows[-1]['extra'] = extra
        if status != 'returned':
            break
    data = dict(scope=scope or __doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(),
                explicit_timer_before_each_task=timer, initial=initial, rows=rows)
    (ROOT/filename).write_text(json.dumps(data, indent=2)+'\n')
    print(dict(completed=sum(row['status']=='returned' for row in rows),
               creations=sum(len(row['creations']) for row in rows),
               acks=sum(len(row['acks']) for row in rows),
               failures=[row['error'] for row in rows if row['error']]))


if __name__ == '__main__':
    main()
