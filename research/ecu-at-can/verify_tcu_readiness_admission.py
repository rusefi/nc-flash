"""Join native foreground ADC callers, capture readiness and application IRQ.

Original initializers and timer prefixes; independent whole-RAM readiness,
wheel and command/pin oracles plus the existing application ISR differential.
Foreground polling, counter epoch, peripheral inputs and zero-latency event
ordering are explicit fixtures. No counter-reset, full boot or hardware claim.
"""
import copy
import hashlib
import json
from pathlib import Path

import verify_tcu_application_interrupt as app
import verify_tcu_capture_readiness as capture
import verify_tcu_readiness_a as adc_a
import verify_tcu_readiness_b as adc_b
from verify_tcu_capture_interrupts import CaptureSamples
from verify_tcu_cmt0_interrupt import Samples
from verify_tcu_timer_configuration import ConfigurationRegisters
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from verify_control_acquisition_schedule import execute_slice
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent
CAPTURE_PORTS = {0xFFFFF401,0xFFFFF42A,0xFFFFF42E}


def state(t):
    return {hex(a):r(t,a) for a in [0x84A0,0x84D8,0x84EC,0x8450,0x8007,0x84F5,0x84F4]}


class Machine(app.Machine):
    def read(self,address,size):
        address &= 0xFFFFFFFF
        if self.cmt_active and address >= 0xFFFFE000:
            return self.cmt_io.read(address,size)
        if self.foreground_active and address >= 0xFFFFE000:
            return self.foreground_io.read(address,size)
        if self.capture_pending is not None and address in CAPTURE_PORTS:
            return ConfigurationRegisters.read(self,address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        address &= 0xFFFFFFFF
        if self.cmt_active and address >= 0xFFFFE000:
            return self.cmt_io.write(address,value,size)
        if self.capture_pending is not None and address in CAPTURE_PORTS:
            return ConfigurationRegisters.write(self,address,value,size)
        result = super().write(address,value,size)
        if address == 0xFFFFF401:
            assert size == 1
            self.configuration[0xF401] = value&255
        return result

    def instruction(self,pc):
        if self.cmt_active and pc in [0x123C2,0x128B6,0x11864,0x1E506,0x11A64]:
            self.cmt_entries.append(hex(pc))
        if self.capture_pending is not None and pc == self.capture_pending['return_pc']:
            pending = self.capture_pending
            self.capture_pending = None
            assert ram(self) == pending['ram'], ('capture return RAM',hex(pc))
            assert self.configuration == pending['configuration']
            assert self.configuration_trace[pending['trace_start']:] == pending['trace']
            assert self.r[8:] == pending['registers'] and self.sr&~1 == pending['mask']
            self.configuring = pending['configuring']
            self.capture_returns.append(dict(before=pending['before'],after=state(self),
                enabled=pending['enabled'],return_pc=hex(pc),mmio=pending['trace'],
                whole_application_ram_checked=True))
        if pc == 0x122F4:
            assert self.capture_pending is None
            ref = SHRotate(TCU)
            ref.ram = self.ram.copy()
            expected = self.configuration.copy()
            trace,enabled = capture.model(ref,expected)
            self.capture_pending = dict(return_pc=self.pr,ram=ram(ref),configuration=expected,
                trace_start=len(self.configuration_trace),trace=trace,enabled=enabled,
                registers=self.r[8:].copy(),mask=self.sr&~1,before=state(self),
                configuring=self.configuring)
            self.configuring = True
        return super().instruction(pc)


def fixture():
    # Prior peripheral/port setup is explicit. Startup states are initialized by
    # original callers below, not inherited operational mode3.
    t = app.fixture(mode=0,stage=0,phase=0)
    t.__class__ = Machine
    t.cmt_active = t.foreground_active = False
    t.cmt_io = Samples()
    t.cmt_entries = []
    t.foreground_io = CaptureSamples()
    t.capture_pending = None
    t.capture_returns = []
    t.adc_samples[0xFFFFF810] = t.adc_samples[0xFFFFF812] = 600<<6
    return t


def foreground(t,count_a,count_b,now):
    before = state(t)
    ref = SHRotate(TCU)
    ref.ram = t.ram.copy()
    timed = [adc_a.model(ref,count_a,now),adc_b.model(ref,count_b,now)]
    expected = []
    for address,count,clocked in zip([0xFFFFF810,0xFFFFF812],[count_a,count_b],timed):
        expected += [['read',0xFFFFF818,1,0],['read',0xFFFFF818,1,128],
                     ['read',address,2,count<<6]]
        if clocked:
            expected.append(['read',0xFFFFF6C0,4,now])
    t.foreground_io.accesses = []
    t.foreground_io.samples = {(0xFFFFF818,1):[0,128,0,128],
        (0xFFFFF810,2):[count_a<<6],(0xFFFFF812,2):[count_b<<6],
        (0xFFFFF6C0,4):[now]*sum(timed)}
    saved,sp,mask = t.r[8:14],t.r[15],t.sr&~0x301
    t.foreground_active = True
    try:
        execute_slice(t,0x11534,0x11540)
    finally:
        t.foreground_active = False
    assert ram(t) == ram(ref)
    assert (t.r[8:14],t.r[15],t.sr&~0x301) == (saved,sp,mask)
    assert t.r[14] == 0x11DEE
    assert t.foreground_io.accesses == expected
    assert all(not v for v in t.foreground_io.samples.values())
    return dict(before=before,after=state(t),timestamp=now,mmio=expected,
                whole_application_ram_checked=True)


def initialize(t):
    before = state(t)
    ref = SHRotate(TCU)
    ref.ram = t.ram.copy()
    for a,v,n in [(0x84A0,1,1),(0x84A2,0,2),(0x84A8,0,4),(0x84AC,0,4),
                  (0x84B0,0,4),(0x84D8,1,1),(0x84DA,0,2),(0x84E0,0,4),(0x84E4,0,4)]:
        w(ref,a,v,n)
    execute_slice(t,0x11518,0x11524)
    assert ram(t) == ram(ref)
    capture.initialize(t)
    t.cmt_io.samples = {(0xFFFFF710,2):[0]}
    t.cmt_active = True
    try:
        t.run(0x123B0)
    finally:
        t.cmt_active = False
    old = t.configuration[0xF401]
    t.application_io.samples = {(0xFFFFF401,1):[old,old&247]}
    t.application_io.accesses = []
    t.run(0x121F8,limit=2000000)
    t.check_pending(0xFFFFFFF0)
    assert t.pending is None and t.capture_pending is None
    assert all(not v for v in t.application_io.samples.values())
    assert t.application_io.accesses == [
        ['read',0xFFFFF401,1,old],['write',0xFFFFF401,1,old&247],
        ['write',0xFFFFF442,2,0],['write',0xFFFFF454,2,2560],
        ['read',0xFFFFF401,1,old&247],['write',0xFFFFF401,1,old|8]]
    assert r(t,0x8007) == 1 and r(t,0x84F5) == 0 and r(t,0x84F4) == 0
    assert [r(t,a) for a in [0x84A0,0x84D8,0x84EC]] == [1,1,1]
    return dict(before=before,after=state(t),application_timer_mmio=t.application_io.accesses,
                limits='ADC/capture initializers have independentRAM checks; full121F8 completion is coverage with selected state/MMIO assertions, not a complete initializer oracle.')


def run(poll_period,epoch,machine_factory=fixture,end_phi=3000000):
    t = machine_factory()
    rows = []
    result = dict(poll_period=poll_period,timestamp_epoch=epoch,rows=rows)
    try:
        result['initialization'] = initialize(t)
        if hasattr(t,'initialize_extra'):
            result['extra_initialization'] = t.initialize_extra()
        events = [(n*20000,0,'cmt0',n) for n in range(1,end_phi//20000+1)]
        events += [(n*81920,1,'application',n) for n in range(1,end_phi//81920+1)]
        events += [(n*poll_period,2,'foreground',n) for n in range(end_phi//poll_period+1)]
        events += getattr(t,'additional_events',[])
        for phi,rank,kind,n in sorted(events):
            stamp = (epoch+phi//2)&0xFFFFFFFF
            if kind == 'foreground':
                event = foreground(t,600,600,stamp)
            elif kind == 'cmt0':
                event = capture.tick(t,n,stamp,(stamp+50)&0xFFFFFFFF)
            elif kind == 'application':
                prior = state(t)
                captures = len(t.capture_returns)
                t.verified_boundaries = []
                compare = (n*2560)&65535
                event = app.execute_prefix(t,1,1,compare,compare,compare,stamp,(stamp+50)&0xFFFFFFFF)
                event['before'] = prior
                event['after'] = state(t)
                event['capture_returns'] = copy.deepcopy(t.capture_returns[captures:])
            else:
                event = t.deliver_extra_event(kind,n,stamp)
            rows.append(dict(phi=phi,rank=rank,kind=kind,ordinal=n,event=event,state=state(t)))
            if hasattr(t,'observe_extra'):
                rows[-1].update(t.observe_extra())
            if hasattr(t,'observe_event'):
                rows[-1].update(t.observe_event(kind,n))
        result['status'] = 'PASS'
        result['summary'] = summarize(rows,end_phi)
    except (AssertionError,ValueError,RuntimeError,KeyError,ZeroDivisionError) as error:
        result['status'] = 'REJECTED'
        result['error'] = type(error).__name__+': '+str(error)
        result['pc'] = hex(t.pc)
        result['state'] = state(t)
    return result


def summarize(rows,end_phi=3000000):
    applications = [row for row in rows if row['kind']=='application']
    foregrounds = [row for row in rows if row['kind']=='foreground']
    timers = [row for row in rows if row['kind']=='cmt0']
    assert len(applications)==end_phi//81920 and len(timers)==end_phi//20000
    admitted = []
    capture_checks = 0
    command_checks = 0
    for row in applications:
        event = row['event']
        before,after = event['before'],event['after']
        active = before['0x8007']==3
        admit = before['0x8007']==1 and all(before[a]==3 for a in ['0x84a0','0x84d8','0x84ec'])
        entries = ['0x1220a']+(['0x126da'] if admit else [])+['0x126ec']
        if active:
            entries.append('0x1e5f6')
        assert event['entries']==entries
        assert after['0x8007']==(3 if admit else before['0x8007'])
        if admit:
            assert after['0x84f5']==2 and after['0x84f4']==8
            admitted.append(row)
        if not active and not admit:
            assert len(event['capture_returns'])==1
        else:
            assert not event['capture_returns']
        capture_checks += len(event['capture_returns'])
        command_checks += event['independent_command_pin_boundaries']
    assert len(admitted)==1 and command_checks==2*len(applications)
    enabled = [row for row in applications if any(c['enabled'] for c in row['event']['capture_returns'])]
    assert len(enabled)==1
    capture_ready = next(row for row in applications if row['state']['0x84ec']==3)
    assert capture_ready['event']['before']['0x84ec']==2
    assert capture_ready['state']['0x8007']==1
    assert admitted[0]['ordinal']==capture_ready['ordinal']+1
    assert applications[-1]['state']['0x8007']==3
    assert all(f['event']['whole_application_ram_checked'] for f in foregrounds)
    adc_ready = next(row for row in foregrounds if all(row['state'][a]==3 for a in ['0x84a0','0x84d8']))
    return dict(cmt0_interrupts=len(timers),application_interrupts=len(applications),
        foreground_ram_checks=len(foregrounds),capture_return_ram_checks=capture_checks,
        command_pin_return_checks=command_checks,adc_ready_phi=adc_ready['phi'],
        capture_enabled_phi=enabled[0]['phi'],capture_ready_phi=capture_ready['phi'],
        application_admitted_phi=admitted[0]['phi'],application_admitted_ordinal=admitted[0]['ordinal'],
        additional_application_interrupt_required=True)


def main():
    results = [run(period,epoch) for period,epoch in [(50000,7),(50000,0),(65536,0xFFFFFF00)]]
    output = dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),scenarios=results,
        limits='Pphi periods from prior conditionalconfiguration; sampledTCNT10A=epoch+phi/2 with unprovedepoch/reset/physicalcounter. Foregroundpoll period/tie orderCMT0,application,foreground and fiftycountprofileduration arefixtures. No otherinterrupts/pulses/fullboot/vehicle.')
    (ROOT/'tcu-readiness-admission-verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print([dict(poll=r['poll_period'],epoch=r['timestamp_epoch'],status=r['status'],
                events=len(r['rows']),error=r.get('error'),pc=r.get('pc')) for r in results])
    assert all(r['status']=='PASS' for r in results)


if __name__ == '__main__':
    main()
