"""Native missing-frame receipts -> qualified communication recovery.

Reuse the original receive/application/diagnostic pipeline. Eight original
11014 calls and100 original11864 ticks per pair are explicit scheduling.
CAN201/215 encoder fixtures andzero4EC continue. Fromcall64, add zero payloads
for CAN4F1/420/240/200 through original ISR prefixes. These are synthetic
payloads, not recovered OEM traffic or evidence that every application input
is physically healthy. No direct receipt, freshness, fault or recovery writes.
"""
import probe_tcu_qualified_receive as qualified
from verify_can201_byte6 import r, w, TCU
from sh_rotate import SHRotate
from verify_tcu_base_publication import ram

RESTORE_AT = 64
EXTRA_INDICES = (0, 4, 5, 9)


class Observed(qualified.Observed):
    def instruction(self, pc):
        if self.motion_pending and self.motion_pending['return_pc'] == pc:
            boundary = self.motion_pending
            self.motion_pending = None
            assert ram(self) == boundary.pop('expected_ram'), '50F26 actual return RAM'
            boundary['whole_application_ram_checked'] = True
            boundary['after'] = [r(self, a, n) for a, n in
                                  [(0x80A4, 2), (0x80BA, 2), (0xA4FC, 1)]]
            self.motion_checks.append(boundary)
        if pc == 0x22DDC:
            self.motion_entries.append(dict(entry=hex(pc),
                source_80ea=r(self, 0x80EA, 2), source_91a2=r(self, 0x91A2, 2)))
        if pc == 0x50F26:
            assert self.motion_pending is None
            ref = SHRotate(TCU)
            ref.ram = dict(self.ram)
            for src, dst in [(0x932C, 0x80A4), (0x932E, 0x80BA)]:
                w(ref, dst, r(self, src, 2)*10//256, 2)
            w(ref, 0xA4FC, r(self, 0xA4FA))
            self.motion_pending = dict(entry=hex(pc), return_pc=self.pr,
                before=[r(self, a, n) for a, n in [(0x932C, 2), (0x932E, 2), (0xA4FA, 1)]],
                expected_ram=ram(ref))
        return super().instruction(pc)


def fixture():
    t = qualified.fixture()
    t.__class__ = Observed
    t.motion_pending = None
    t.motion_checks, t.motion_entries = [], []
    t.wheel_calls = 8
    return t


def before_task(t, call):
    assert t.motion_pending is None
    t.motion_checks, t.motion_entries = [], []
    qualified.before_task(t, call)
    if call >= RESTORE_AT:
        for index in EXTRA_INDICES:
            t.rx_receipts.append(qualified.admitted.rx.receipt(t, index, bytes(8)))


def after_task(t, call):
    row = qualified.after_task(t, call)
    row['recovery'] = {hex(a): r(t, a, n) for a, n in
                       [(0x80A4, 2), (0x932C, 2), (0xA99B, 1), (0xA735, 1),
                        (0xA721, 1), (0xA722, 1), (0xA726, 1), (0xA728, 1),
                        (0xA729, 1), (0x868C, 1)]}
    assert t.motion_pending is None
    row['motion_checks'], row['motion_entries'] = t.motion_checks, t.motion_entries
    return row


def main(stop_captures_at=None):
    def configured():
        t = fixture()
        if stop_captures_at is not None:
            t.capture_enabled = lambda call, entry: call < stop_captures_at
        return t
    name = ('tcu-receive-recovery-probe.json' if stop_captures_at is None else
            'tcu-receive-recovery-stopped-captures.json')
    qualified.admitted.rx.phase.received.capture.task.main(
        cycles=160, timer=True, filename=name,
        machine_factory=configured, before_task=before_task, after_task=after_task,
        scope=__doc__+f'\nStop both external capture callbacks at: {stop_captures_at}.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stop-captures-at', type=int)
    main(parser.parse_args().stop_captures_at)
