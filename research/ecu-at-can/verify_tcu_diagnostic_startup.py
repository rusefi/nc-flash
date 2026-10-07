"""Native diagnostic initialization/admission joins the retained readiness path.

No forced diagnostic/application mode3 or ready flags. Explicit foreground
polling, timestamp epochs, conditional timer periods and peripheral samples;
original ISR prefixes stop before RTE. No full boot or hardware claim.
"""
import copy
import hashlib
import json
from pathlib import Path

import verify_tcu_readiness_admission as native
import verify_tcu_diagnostic_timer as diagnostic
from probe_tcu_qualified_receive import diagnostic_state,observe_diagnostic
from verify_can201_byte6 import TCU,r,w
from verify_tcu_base_publication import ram
from sh_rotate import SHRotate

ROOT = Path(__file__).resolve().parent
END_PHI = 4000000


class Machine(native.Machine):
    def read(self,address,size):
        if self.diagnostic_active and (address&0xFFFFFFFF)>=0xFFFFE000:
            return self.io.read(address,size)
        return super().read(address,size)

    def write(self,address,value,size):
        if self.diagnostic_active and (address&0xFFFFFFFF)>=0xFFFFE000:
            self.io.write(address,value,size)
            self.configuration[(address&0xFFFFFFFF)-0xFFFF0000] = value&((1<<(8*size))-1)
            return
        return super().write(address,value,size)

    def instruction(self,pc):
        observe_diagnostic(self,pc)
        if self.diagnostic_active and pc in [0x1218E,0x1267C,0x12682,0x57002,0x56F80]:
            self.diagnostic_entries.append(hex(pc))
        return super().instruction(pc)

    def initialize_extra(self):
        ref = SHRotate(TCU)
        ref.ram = self.ram.copy()
        w(ref,0x8006,1)
        values = [self.configuration[a] for a in [0xF401,0xF480,0xF482,0xF4AB]]
        self.io.samples,expected = diagnostic.initialization_inputs(*values)
        self.io.accesses = []
        before = diagnostic_state(self)
        saved,mask = self.r[8:].copy(),self.sr
        self.diagnostic_active = True
        try:
            self.run(0x1217C)
        finally:
            self.diagnostic_active = False
        assert ram(self)==ram(ref) and self.r[8:]==saved and self.sr==mask
        assert self.io.accesses==expected and all(not v for v in self.io.samples.values())
        assert not self.diag_pending
        return dict(before=before,after=diagnostic_state(self),mmio=expected,
                    whole_application_ram_checked=True)

    def deliver_extra_event(self,kind,n,stamp):
        assert kind=='diagnostic' and not self.diag_pending
        before = diagnostic_state(self)
        readiness = [r(self,a) for a in [0x84A0,0x84D8,0x8007]]
        boundary = len(self.diag_boundaries)
        self.diagnostic_entries = []
        self.diagnostic_active = True
        try:
            compare = (n*15625)&65535
            event = diagnostic.execute_prefix(self,1,1,compare,compare,compare,
                                              stamp,(stamp+50)&0xFFFFFFFF)
        finally:
            self.diagnostic_active = False
        assert not self.diag_pending
        admitted = before['0x8006']==1 and all(v==3 for v in readiness)
        expected_mode = 3 if admitted else 5 if before['0x8006']==3 and readiness[0]==4 else before['0x8006']
        assert r(self,0x8006)==expected_mode
        expected_entries = ['0x1218e']+(['0x1267c'] if admitted else [])+['0x12682']
        if expected_mode in [3,5]:
            expected_entries += ['0x57002','0x56f80']
        assert self.diagnostic_entries==expected_entries
        event.update(before=before,after=diagnostic_state(self),readiness=readiness,
            admitted=admitted,entries=self.diagnostic_entries.copy(),
            boundaries=copy.deepcopy(self.diag_boundaries[boundary:]))
        return event

    def observe_extra(self):
        return dict(diagnostic_state=diagnostic_state(self),
            diagnostic_ram_checks=sum(bool(b.get('whole_application_ram_checked')) for b in self.diag_boundaries))


def fixture(end_phi=END_PHI):
    t = native.fixture()
    t.__class__ = Machine
    t.diagnostic_active = False
    t.io = diagnostic.Samples()
    t.diagnostic_entries = []
    t.diag_pending,t.diag_boundaries = [],[]
    # Existing ranks0/1/2 remain unchanged for default regression identity.
    # Diagnostic ties follow CMT0; no application/diagnostic ties in this horizon.
    t.additional_events = [(n*500000,0.5,'diagnostic',n) for n in range(1,end_phi//500000+1)]
    return t


def main():
    results = [native.run(period,epoch,machine_factory=fixture,end_phi=END_PHI)
               for period,epoch in [(50000,7),(50000,0),(65536,0xFFFFFF00)]]
    for result in results:
        if result['status']!='PASS':
            continue
        diagnostics = [row for row in result['rows'] if row['kind']=='diagnostic']
        admitted = [row for row in diagnostics if row['event']['admitted']]
        assert len(diagnostics)==8 and len(admitted)==1
        assert admitted[0]['phi'] > result['summary']['application_admitted_phi']
        assert all(row['event']['before']['0x8006']==1 for row in diagnostics[:6])
        assert all(row['event']['after']['0x8006']==3 for row in diagnostics[5:])
        result['summary'].update(diagnostic_interrupts=8,diagnostic_admitted_phi=admitted[0]['phi'],
            diagnostic_actual_return_ram_checks=result['rows'][-1]['diagnostic_ram_checks'])
    output = dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),scenarios=results,
        limits='Diagnostic500000phi; CMT0/diagnostic/application/foreground tieorder; externaltimestamp epochs/phi-divisor2/pollperiods andzero service latency remainfixtures. Additional initializer1217C runsafterbaseinitializers beforeeventepoch, notcomplete1168A/reset.')
    (ROOT/'tcu-diagnostic-startup-verification.json').write_text(json.dumps(output,indent=2)+'\n')
    print([dict(poll=s['poll_period'],epoch=s['timestamp_epoch'],status=s['status'],
                summary=s.get('summary'),error=s.get('error'),pc=s.get('pc')) for s in results])
    assert all(s['status']=='PASS' for s in results)


if __name__=='__main__':
    main()
