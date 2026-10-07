"""Native readiness and diagnostics with CMT1 and capture interrupts.

Extend the existing readiness event loop, preserving original initialization
and all later RAM/history. Finite inputs, conditional clocks, external epochs,
zero service latency and foreground cadence remain explicit fixtures.
"""
import hashlib
import json
from pathlib import Path

import verify_tcu_diagnostic_startup as startup
import verify_tcu_cmt1_interrupt as primary
import verify_tcu_capture_interrupts as capture
from probe_tcu_capture_timeline import edges
from probe_tcu_captured_requests import sources
from verify_can201_byte6 import TCU, r, w
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent
END_PHI = startup.END_PHI


class Machine(startup.Machine):
    def read(self, address, size):
        if (address & 0xFFFFFFFF) >= 0xFFFFE000:
            if self.cmt1_active:
                return self.cmt1_io.read(address, size)
            if self.capture_active:
                return self.capture_io.read(address, size)
        return super().read(address, size)

    def write(self, address, value, size):
        if (address & 0xFFFFFFFF) >= 0xFFFFE000:
            if self.cmt1_active:
                return self.cmt1_io.write(address, value, size)
            if self.capture_active:
                return self.capture_io.write(address, value, size)
        return super().write(address, value, size)

    def instruction(self, pc):
        if self.cmt1_active and pc in [0x12386, 0x12886, 0x11014]:
            self.cmt1_entries.append(hex(pc))
        if self.capture_active and pc in [0x179A8, 0x17A58]:
            self.capture_callbacks.append([pc, self.r[4]])
        return super().instruction(pc)

    def initialize_extra(self):
        result = super().initialize_extra()
        ref = SHRotate(TCU)
        ref.ram = self.ram.copy()
        w(ref, 0x8009, 1)
        for a in [0x8494, 0x8498, 0x849C]:
            w(ref, a, 0, 4)
        self.cmt1_io.samples = {(0xFFFFF710, 2): [1]}
        self.cmt1_active = True
        try:
            self.run(0x12374)
        finally:
            self.cmt1_active = False
        assert ram(self) == ram(ref)
        assert self.cmt1_io.accesses == [['write', 0xFFFFF71C, 2, 1279],
            ['read', 0xFFFFF710, 2, 1], ['write', 0xFFFFF710, 2, 3]]
        assert all(not v for v in self.cmt1_io.samples.values())
        result['cmt1_initializer'] = dict(whole_application_ram_checked=True,
                                         mmio=self.cmt1_io.accesses.copy())
        return result

    def deliver_extra_event(self, kind, n, stamp):
        if kind == 'cmt1':
            self.cmt1_active = True
            try:
                event = primary.execute_prefix(self, 128, 128, stamp, (stamp+50)&0xFFFFFFFF)
            finally:
                self.cmt1_active = False
            assert event['active'] and event['mode'] == (1 if n == 1 else 3)
            event.update(whole_application_ram_checked=True, mmio=self.cmt1_io.accesses.copy())
            return event
        if kind in ['capture_A', 'capture_B']:
            channel = kind[-1]
            mask = capture.CHANNELS[channel]['mask']
            input_mode = (self.configuration[0xF42A] >> (0 if channel == 'A' else 2)) & 3
            enabled = bool(self.configuration[0xF401] & 1
                           and self.configuration[0xF42E] & mask and input_mode == 1)
            if not enabled:
                return dict(delivered=False, reason='Original capture enable has not occurred')
            self.capture_active = True
            try:
                # CaptureTCNT0 has an explicit zero epoch, independent of profileTCNT10A.
                captured = self.capture_times[(kind, n)]//2
                event = capture.execute_prefix(self, channel, mask, mask, captured,
                                                stamp, (stamp+50)&0xFFFFFFFF)
            finally:
                self.capture_active = False
            event.update(delivered=True, differential_whole_application_ram_checked=True)
            return event
        return super().deliver_extra_event(kind, n, stamp)

    def observe_extra(self):
        return dict(**super().observe_extra(), sources=sources(self),
                    primary_mode=r(self, 0x8009))


def fixture(end_phi=END_PHI):
    t = startup.fixture(end_phi=end_phi)
    t.__class__ = Machine
    t.cmt1_active = t.capture_active = False
    t.cmt1_io = primary.Samples()
    t.capture_io = capture.CaptureSamples()
    t.cmt1_entries, t.capture_callbacks = [], []
    t.additional_events += [(n*40960, 0.6, 'cmt1', n)
                            for n in range(1, end_phi//40960+1)]
    t.capture_times = {}
    for channel, rank in [('A', 0.7), ('B', 0.8)]:
        for n, phi in enumerate(edges(channel), 1):
            if phi > end_phi:
                break
            kind = 'capture_'+channel
            t.capture_times[(kind, n)] = phi
            t.additional_events.append((phi, rank, kind, n))
    return t


def main():
    results = [startup.native.run(period, epoch, machine_factory=fixture, end_phi=END_PHI)
               for period, epoch in [(50000, 7), (50000, 0), (65536, 0xFFFFFF00)]]
    for result in results:
        if result['status'] != 'PASS':
            continue
        rows = result['rows']
        result['summary'].update(cmt1_interrupts=sum(r['kind']=='cmt1' for r in rows),
            capture_interrupts=sum(r['event'].get('delivered', False) for r in rows),
            skipped_capture_edges=sum(r['event'].get('delivered') is False for r in rows))
        assert result['summary']['cmt1_interrupts'] == END_PHI//40960
        for channel in ['A', 'B']:
            captures = [r for r in rows if r['kind'] == 'capture_'+channel]
            expected = [phi for phi in edges(channel)
                        if result['summary']['capture_enabled_phi'] < phi <= END_PHI]
            delivered = [r['phi'] for r in captures if r['event']['delivered']]
            assert delivered == expected and delivered
            result['summary']['capture_'+channel+'_interrupts'] = len(delivered)
    result = dict(scope=__doc__, rom_sha256=hashlib.sha256(TCU).hexdigest(), scenarios=results,
        limits='CMT1 initializer afterdiagnostic beforeevents; partialnative order. Captureedges useprevioussynthetictrajectory fromepoch0, ignoreduntiloriginalenable. TieCMT0/diagnostic/CMT1/A/B/application/foreground. NoCANyet/fullreset/hardwareIRQ.')
    (ROOT/'tcu-native-capture-startup-verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print([dict(status=s['status'], summary=s.get('summary'), error=s.get('error'), pc=s.get('pc'))
           for s in results], flush=True)
    assert all(s['status']=='PASS' for s in results)


if __name__ == '__main__':
    main()
