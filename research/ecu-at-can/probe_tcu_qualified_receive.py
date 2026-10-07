"""Original diagnostic initializer/task joined to native receive/application task.

Explicit task modes, peripheral samples and100 originaltick calls per taskpair.
Only201/215/4EC frames supplied; othermissingframes must not be called healthy.
No injected diagnostic admission/active/fault flags; not fullboot/realcadence.
"""
import probe_tcu_admitted_requests as admitted
from probe_tcu_initialized_requests import run_primary_timer
from verify_can201_byte6 import w, r
from verify_tcu_diagnostic_admission import expected, ram


def diagnostic_state(t):
    return {hex(a): r(t, a, n) for a, n in
            [(0x8006, 1), (0xA518, 2), (0x84D0, 4), (0x9415, 1), (0xA954, 1),
             (0x8464, 2), (0xA936, 1), (0xA938, 1),
             (0xA939, 1), (0xA93A, 1), (0xA944, 1), (0xA948, 4),
             (0xA76C, 1), (0xA722, 1), (0xA978, 1), (0xA98E, 1),
             (0xA98D, 1), (0xA98F, 1), (0x92D5, 1), (0x92C9, 1),
             (0x80E8, 2), (0x9454, 1), (0x916F, 1), (0x8EE2, 2)]}


def observe_diagnostic(self,pc):
    """Shared actual-return observer; the machine owns pending/boundary state."""
    if self.diag_pending and self.diag_pending[-1]['return_pc'] == pc:
        row = self.diag_pending.pop()
        if 'expected_ram' in row:
            wanted = row.pop('expected_ram')
            assert ram(self) == wanted, ('56B06 actual return RAM', pc)
            row['whole_application_ram_checked'] = True
        row['after'] = diagnostic_state(self)
        self.diag_boundaries.append(row)
    if pc in [0x56B06, 0x56F80, 0x56658, 0x57F50, 0x570F6, 0x57258, 0x1A598]:
        self.diag_pending.append(dict(entry=hex(pc), return_pc=self.pr,
                                      before=diagnostic_state(self)))
        if pc == 0x56B06:
            self.diag_pending[-1]['expected_ram'] = expected(self)
        if pc == 0x1A598:
            self.diag_pending[-1]['arguments'] = self.r[4:7].copy()


class Observed(admitted.rx.ReceiveRegisters):
    def finish_diagnostic_interval(self):
        """Default once/application fixture; timed drivers override delivery."""
        self.run(0x12682, limit=2000000)
        # Tail-dispatched56F80 returns to the normal-run sentinel.
        boundary = self.diag_pending.pop()
        assert boundary['entry'] == '0x56f80' and boundary['return_pc'] == 0xFFFFFFF0
        boundary['after'] = diagnostic_state(self)
        self.diag_boundaries.append(boundary)
        assert not self.diag_pending

    def instruction(self,pc):
        observe_diagnostic(self,pc)
        return super().instruction(pc)


def fixture():
    t = admitted.expiry_fixture()
    t.__class__ = Observed
    t.diag_pending, t.diag_boundaries = [], []
    t.advance_receive_tick = t.omit_can201 = False
    t.run(0x1267C, limit=2000000)
    w(t, 0x8006, 3)  # Explicit scheduler task-mode input, not diagnostic flags.
    assert r(t, 0xA936) == 1 and r(t, 0xA939) == 0
    return t


def before_task(t, call):
    assert not t.diag_pending
    t.diag_boundaries = []
    # The shared runner already executes one original timer-wheel call.
    for _ in range(getattr(t, 'wheel_calls', 1)-1):
        run_primary_timer(t)
    for _ in range(100):
        if hasattr(t, 'clock_delivery'):
            t.clock_delivery()
        else:
            t.run(0x11864)
    admitted.before_task(t, call)


def after_task(t, call):
    row = admitted.after_task(t, call)
    row['before_diagnostic'] = diagnostic_state(t)
    t.finish_diagnostic_interval()
    row['after_diagnostic'] = diagnostic_state(t)
    row['diagnostic_boundaries'] = t.diag_boundaries
    return row


def main(cycles=64, wheel_calls=1, filename='tcu-qualified-receive-probe.json'):
    assert wheel_calls >= 1
    def configured():
        t = fixture()
        t.wheel_calls = wheel_calls
        return t
    admitted.rx.phase.received.capture.task.main(cycles=cycles, timer=True,
        filename=filename, machine_factory=configured,
        before_task=before_task, after_task=after_task,
        scope=__doc__+f'\nExplicit original11014 calls per pair: {wheel_calls}.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles', type=int, default=64)
    parser.add_argument('--wheel-calls', type=int, default=1)
    parser.add_argument('--filename', default='tcu-qualified-receive-probe.json')
    args = parser.parse_args()
    main(args.cycles, args.wheel_calls, args.filename)
