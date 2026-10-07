"""Observe original cut eligibility in the unchanged320-pair recovery fixture.

Same seven-frame receipts, timer interleave and external capture timestamps as
probe_tcu_recovery_reference --second-approach. No internal timer, cut, phase,
acknowledgement or fault writes. Existing cut model checks complete application
RAM at24FA0 return;2513E predicate checks return and unchanged application RAM.
This is supplied scheduling/MMIO input, not physical CAN/actuation evidence.
"""
import probe_tcu_recovery_reference as reference_probe
from sh_rotate import SHRotate
from verify_can201_byte6 import TCU, r, w
from verify_can201_cut_loop import reference
from verify_software_lookup import expected_curve
from verify_tcu_base_publication import ram

FIELDS = [(0x9454,1),(0x9455,1),(0x828B,1),(0x82A5,1),(0x82A6,1),(0x82A7,1),
          (0x9316,1),(0x9317,1),(0x94F4,1),(0x92C9,1),(0x92C6,1),
          (0x9334,2),(0x800E,1),(0x80E8,2)]


def state(t):
    return {hex(a):r(t,a,n) for a,n in FIELDS}


class Observed(reference_probe.Observed):
    def instruction(self, pc):
        while self.cut_pending and self.cut_pending[-1]['return_pc']==pc:
            b=self.cut_pending.pop()
            assert ram(self)==b.pop('expected_ram'), ('cut return RAM',b,hex(pc))
            b['whole_application_ram_checked']=True
            b['after']=state(self)
            b['returned']=self.r[0]
            if b['entry']=='0x2513e':
                assert self.r[0]==b['expected']
            else:
                value,history,timers=b['expected']
                assert [r(self,a) for a in [0x9454,0x9455,0x82A5,0x82A6,0x82A7]]==[value,history,*timers]
            self.cut_checks.append(b)
        if pc in [0x24FA0,0x2513E]:
            b=dict(entry=hex(pc),return_pc=self.pr,before=state(self))
            if pc==0x2513E:
                b['expected']=int(not(r(self,0x92C9)&64 or r(self,0x9317)&1 or r(self,0x92C6)&2))
                b['expected_ram']=ram(self)
            else:
                b['expected']=reference(self)
                b['threshold']=expected_curve(r(self,0x9334,2))
                ref=SHRotate(TCU);ref.ram=dict(self.ram)
                value,history,timers=b['expected']
                for a,v in zip([0x9454,0x9455,0x82A5,0x82A6,0x82A7],[value,history,*timers]):
                    w(ref,a,v)
                b['expected_ram']=ram(ref)
            self.cut_pending.append(b)
        return super().instruction(pc)


def fixture():
    t=reference_probe.fixture()
    t.__class__=Observed
    t.cut_pending,t.cut_checks=[],[]
    t.measured_interval=lambda call:(5890 if call<48 else 6490 if call<80 else 4430 if call<128 else 9120)
    t.capture_enabled=lambda call,entry:call<280
    return t


def before_task(t,call):
    assert not t.cut_pending
    t.cut_checks=[]
    reference_probe.before_task(t,call)


def after_task(t,call):
    out=reference_probe.after_task(t,call)
    assert not t.cut_pending
    out['cut_checks']=t.cut_checks
    return out


def main():
    reference_probe.recovery.qualified.admitted.rx.phase.received.capture.task.main(
        cycles=320,timer=True,filename='tcu-recovery-cut-probe.json',
        machine_factory=fixture,before_task=before_task,after_task=after_task,scope=__doc__)


if __name__=='__main__':
    main()
