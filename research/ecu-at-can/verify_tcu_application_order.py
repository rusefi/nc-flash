"""Execute126EC/1E5F6 with explicit HCAN/ADC/digital/port fixtures.

Verify direct task call order, phase/counter behavior and independently
modeled complete529AC/185F8 effects at their actual call boundaries. Nested
application bodies execute but not every body has a full semantic oracle.
No boot, real interrupts, clock, peripheral side effects or physical proof.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import probe_tcu_application_task as probe
from probe_tcu_application_task import pins,w,r,TCU

ROOT=Path(__file__).resolve().parent
COMMON=[0x19FF0,0x17250,0x17418,0x174A0,0x175A8,0x17C20,0x17C94,0x17D60,
        0x51460,0x516E6,0x517B2,0x216D8,0x588D8,0x2124C,0x22B84,0x3935C,
        0x30B9E,0x30C82,0x3324C,0x40544,0x43130,0x3E1F8,0x3E394,0x3E480,
        0x3CE00,0x41988,0x31524,0x2C738,0x2E7CC,0x4C0F4]
PHASES=[[0x1E780,0x1E7DE]*4,[0x1ED88,0x1ED88,0x1ED88,0x1EC5A,0x1ED88,0x1ED88,0x1ED88,0x1ED50],
        [0x1E880,0x1EAC4,0x1EB08,0x1EB90]*2]
TAIL=[0x52D8C,0x186A4,0x186EA]
for base,expected in zip([0x5CC28,0x5CC48,0x5CC68],PHASES):
    assert [int.from_bytes(TCU[a:a+4],'big') for a in range(base,base+32,4)]==expected


class ObservedTask(probe.ApplicationRegisters):
    def check_pending(self,pc):
        if self.pending is not None and self.pending[0]==pc:
            _,ref,entry=self.pending;self.pending=None
            pins.setup.equal(self,ref)
            assert (self.mcr,self.gsr,self.hcan_trace,self.digital_trace)==(ref.mcr,ref.gsr,ref.hcan_trace,ref.digital_trace)
            self.verified_boundaries.append(entry)
    def instruction(self,pc):
        self.check_pending(pc)
        if pc in [0x529AC,0x185F8]:
            assert self.pending is None
            ref=copy.deepcopy(self)
            (pins.command_model if pc==0x529AC else pins.dispatch_model)(ref)
            self.pending=(self.pr,ref,pc)
        if pc==0x1E5F6:self.periodic_arguments.append(self.r[4]&255)
        if pc==0x31524 and self.pr==0x1E6A8:self.events.append([self.r[4],self.r[5]])
        if 0x1E5F6<=pc<=0x1E6E8:
            op=int.from_bytes(TCU[pc:pc+2],'big')
            if op&0xF0FF in [0x400B,0x402B]:self.direct_calls.append([pc,self.r[(op>>8)&15]])
        return super().instruction(pc)


def fixture(**kw):
    t=probe.fixture(**kw);t.__class__=ObservedTask;t.pending=None
    t.direct_calls=[];t.periodic_arguments=[];t.events=[];t.verified_boundaries=[]
    return t


def run(t):
    mode,stage,phase,count=[r(t,a) for a in [0x8007,0x84F5,0x84F4,0x90CC]]
    t.direct_calls=[];t.periodic_arguments=[];t.events=[];t.verified_boundaries=[]
    t.hcan_trace=[];t.digital_trace=[];t.adc_reads=[];t.configuration_trace=[]
    if hasattr(t,'application_delivery'):
        t.application_delivery()
    else:
        pins.execute(t,0x126EC)
    t.check_pending(0xFFFFFFF0);assert t.pending is None
    active=mode==3 and stage==2
    expected=COMMON+[row[phase&7] for row in PHASES]+TAIL if active else []
    assert [target for pc,target in t.direct_calls]==expected
    assert t.periodic_arguments==([phase&7] if active else [])
    assert t.events==([[4,0]] if active else [])
    assert t.verified_boundaries==[0x529AC,0x185F8]
    assert r(t,0x90CC)==((count+int(active))&255)
    assert r(t,0x84F4)==(8 if mode==3 and stage==1 else (phase+1)&255 if mode==3 else phase)
    assert r(t,0x84F5)==(2 if mode==3 and stage==1 else stage)
    return dict(mode=mode,stage=stage,phase=phase,next_phase=r(t,0x84F4),counter=r(t,0x90CC),
                command=r(t,0x8A18),sources=[r(t,a) for a in [0xA5A1,0xA5A2]],
                direct_calls=t.direct_calls.copy(),events=t.events.copy(),
                adc_reads=t.adc_reads.copy(),digital_trace=t.digital_trace.copy(),hcan_trace=t.hcan_trace.copy(),
                port_trace=t.configuration_trace.copy(),verified_boundaries=t.verified_boundaries.copy())


def integrated():
    task=pins.setup.cycle.task;cycle=pins.setup.cycle
    t=fixture(stage=2);task.initialize_history(t)
    for a,v in [(0x8002,1),(0x8008,3),(0x84F8,3),(0xA975,1),(0xA976,1),(0xA958,1)]:w(t,a,v)
    rows=[]
    for call in range(24):
        adc=600 if call<12 else 400
        t.adc_samples[0xFFFFF810]=t.adc_samples[0xFFFFF812]=adc<<6
        t.timer[0xFFFFF500]=2;t.timer[0xFFFFF522]=1
        t.timestamps=[100000*call,100000*call+234]
        t.timer_trace=[];t.adc_reads=[];t.output_writes=[];cycle.cycle(t)
        # Explicit order: cycle, application, four compares. Physical interrupt
        # delivery/nesting and relative task cadence are NOT inferred.
        w(t,0xA5A1,int(4<=call<8 or 16<=call<20))
        application=run(t);outputs=[]
        for phase in range(4):
            t.timer[0xFFFFF62C]=1
            t.timer[0xFFFFF600]=(t.timer[0xFFFFF604]+7)&65535
            t.timestamps=[100000*call+1000+phase*1000,100000*call+1123+phase*1000]
            t.timer_trace=[];t.adc_reads=[];t.output_writes=[]
            task.interrupt(t);outputs.extend(t.output_writes)
        assert len(outputs)==4
        rows.append(dict(call=call,adc=adc,application=application,A518=r(t,0xA518,2),
                         inhibit=r(t,0xA5A0),output_phase=r(t,0x84F8),outputs=outputs))
    assert {row['inhibit'] for row in rows}=={0,1}
    return rows


def main():
    rows=[]
    for mode,stage,phase in itertools.product([0,1,2,3,255],[0,1,2,3],[0,7,255]):
        t=fixture(mode=mode,stage=stage,phase=phase);w(t,0x90CC,255)
        rows.append(run(t))
    for phase,gsr,source,adc in itertools.product(range(8),[0,8],[0,1],[400,600]):
        t=fixture(phase=phase,gsr=gsr,source=source)
        t.adc_samples[0xFFFFF810]=t.adc_samples[0xFFFFF812]=adc<<6
        rows.append(run(t))
    retained=[];t=fixture(stage=1)
    for call in range(32):
        # Explicit sample/status/source schedule, not real-world timing.
        t.gsr=8 if 12<=call<16 else 0
        w(t,0xA5A1,int(4<=call<8 or 20<=call<24))
        adc=600 if call>=16 else 400
        t.adc_samples[0xFFFFF810]=t.adc_samples[0xFFFFF812]=adc<<6
        retained.append(run(t))
    rejects=0;t=fixture()
    for a,n,write in [(0xFFFFE400,4,False),(0xFFFFE401,1,True),(0xFFFFF726,1,False),(0xFFFFF73E,1,True),(0xFFFFF77A,2,False)]:
        try:
            if write:t.write(a,0,n)
            else:t.read(a,n)
        except ValueError:rejects+=1
        else:raise AssertionError('unsupported access admitted')
    integrated_rows=integrated()
    result=dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),cases=len(rows),retained_calls=len(retained),
        rejected=rejects,boundary_checks=2*(len(rows)+len(retained)+len(integrated_rows)),rows=rows,retained=retained,integrated=integrated_rows,
        limits='Exactdirectcalls/phase/event4 plus completecommand-and-pin oracles. Other nestedbody semantics not independently checked here; uninitialized RAM remains fixture. No fullboot/interruptdelivery/clock/pins/plant/remotecontroller proof.')
    (ROOT/'tcu-application-order-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('cases',len(rows),'retained',len(retained),'boundaries',result['boundary_checks'],'integrated',len(integrated_rows),'rejected',rejects,flush=True)


if __name__=='__main__':main()
