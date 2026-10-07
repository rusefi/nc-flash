"""Original capture callbacks -> complete task -> clonedCAN216/ECU decode.

Timestamp increments, peripheral samples and timer/capture/task order are
explicit experiment inputs. No forced ages, measurements, requests or acks.
Packet mode1 and ECU receive gates are explicit; no physical bus proof.
Optional capture_enabled(call, entry) suppresses an external capture event;
capture_intervals remains the configured increments, while source_boundaries
records which callbacks actually executed.
"""
import probe_tcu_initialized_requests as task
import verify_tcu_measurement as measurement
from verify_can201_byte6 import TCU, ECU, w, r
from sh_rotate import SHRotate
from sh_exact_float import SHExactFloat, exact_value
from sh_subset import signed

assert int.from_bytes(TCU[0x76DE2:0x76DE4], 'big') == 360


def sources(t):
    return {hex(a): r(t, a, size) for a, size in
            [(0x80EA, 2), (0x80EC, 2), (0x80EE, 2), (0x80F0, 2),
             (0x810C, 1), (0x810D, 1), (0x9244, 1), (0x9195, 1),
             (0x800D, 1), (0x91B4, 1), (0x9238, 4), (0x9198, 4),
             (0x92C6, 1), (0x9410, 1), (0x915A, 2),
             (0x809A, 2), (0x809C, 2), (0x880C, 2), (0x8808, 2), (0x89B0, 2)]}


class Captured(task.ObservedInitialized):
    def instruction(self, pc):
        if self.source_pending and self.source_pending[-1]['return_pc'] == pc:
            entry = self.source_pending.pop()
            entry['after'] = sources(self)
            if 'expected_measurement' in entry:
                assert r(self, 0x80EE, 2) == entry['expected_measurement']
                assert r(self, 0x9238, 4) == entry['expected_period'] & 0xFFFFFFFF
                entry['measurement_checked'] = True
        if pc in [0x179A8, 0x17A58, 0x2124C, 0x2086C, 0x2117C]:
            entry = dict(entry=hex(pc), return_pc=self.pr,
                         argument=self.r[4], before=sources(self))
            if pc == 0x2124C:
                stale = r(self, 0x810C) >= 18 or r(self, 0x9244) >= 18
                value, period = ((0, 0x7FFFFFFF) if stale else
                                 measurement.model(measurement.history(self), r(self, 0x800D)))
                entry.update(expected_measurement=value, expected_period=period)
            self.source_rows.append(entry)
            self.source_pending.append(entry)
        return super().instruction(pc)


def fixture():
    t = task.fixture()
    t.__class__ = Captured
    t.source_pending = []
    t.source_rows = []
    t.run(0x20658)
    t.run(0x211C4)
    return t


def before_task(t, call):
    t.source_rows = []
    assert not t.source_pending
    reference_interval = 12160
    measured_interval = (t.measured_interval(call) if hasattr(t, 'measured_interval')
                         else 5890 if call < 48 else 6490)
    t.capture_intervals = [reference_interval, measured_interval]
    for entry, prior, delta in [(0x179A8, 0x88FC, reference_interval),
                                (0x17A58, 0x890C, measured_interval)]:
        if hasattr(t, 'capture_enabled') and not t.capture_enabled(call, entry):
            continue
        captured = (r(t, prior, 4)+delta) & 0xFFFFFFFF
        if hasattr(t, 'capture_delivery'):
            t.capture_delivery(entry, captured)
            assert not t.source_pending
            continue
        t.run(entry, captured)
        # Normal top-level return is a sentinel, not an executed instruction.
        assert t.source_pending[-1]['return_pc'] == 0xFFFFFFF0
        row = t.source_pending.pop()
        row['after'] = sources(t)


def wire(t):
    c = SHRotate(TCU)
    c.ram = dict(t.ram)
    c.run(0x18F10, 1)
    c.run(0x18F8C, 1)
    payload = [r(c, 0x8EFD+i) for i in range(8)]
    source = r(t, 0x915A, 2)
    expected = 0xFFFE if source == 0x7FFF else max(0, (signed(source, 16) >> 5)+512)
    assert int.from_bytes(bytes(payload[:2]), 'big') == expected
    e = SHExactFloat(ECU)
    for a, v in [(0x734A, 0x80), (0x734C, 1), (0x6A5D, 1)]:
        w(e, a, v)
    for i, value in enumerate(payload):
        w(e, 0x6A40+i, value)
    e.run(0x35034)
    e.run(0x34CEC)
    normalized = exact_value(r(e, 0x6A34, 4))
    assert normalized == expected-512
    return dict(source=source, payload=payload, normalized=float(normalized))


def after_task(t, call):
    assert not t.source_pending
    return dict(capture_intervals=t.capture_intervals, source_boundaries=t.source_rows,
                final_sources=sources(t), wire=wire(t))


def main():
    task.main(cycles=96, timer=True, filename='tcu-captured-requests-probe.json',
              machine_factory=fixture, before_task=before_task, after_task=after_task,
              scope=__doc__)


if __name__ == '__main__':
    main()
