"""Original complete mode0 tasks with retained RAM and qualification oracles.

SCI0 ready/reply samples are synthetic; peripherals have no physical clock.
No boot, acquisition cadence, actual sensor or remote-controller claim.
"""
from collections import deque
import copy
import hashlib
import json
from pathlib import Path
from sh_control_task_serial import TaskSerial
from sh_control_task import ControlTaskArithmetic
import verify_control_raw_inputs as raw
import verify_control_raw_enable as first
import verify_control_raw_provenance as second
from verify_control_task_activity import expected as activity_expected, ENTRIES
from verify_control_contributions import ECU, r, w

ROOT=Path(__file__).resolve().parent
MODELS={0x74DF8:first.enable,0x6CD96:first.qualify,0x6CE24:first.countdown,
        0x6CF06:first.latch,0x6D876:second.qualify,0x6D904:second.countdown,
        0x6D9E6:raw.fallback_latch}
ORDER=[0x74DF8,*ENTRIES,0x6CD96,0x6CE24,0x6CF06,0x6D876,0x6D904,0x6D9E6]


class Observed(TaskSerial):
    def __init__(self):
        super().__init__();self.pending=None;self.boundaries=[]

    def instruction(self,pc):
        if self.pending is not None and pc==self.pending['return_pc']:
            saved=self.pending
            assert raw.application(self)==saved.pop('expected'),hex(saved['entry'])
            assert self.r[8:16]==saved.pop('preserved'),hex(saved['entry'])
            assert self.sr&~1==saved.pop('sr')
            saved['after']=[r(self,a) for a in [0x914B,0x8EF8,0x8EFF,0x8F30,0x8F37,0x91E4,0x91E5,0x91E6]]
            self.boundaries.append(saved);self.pending=None
        if pc in MODELS or pc in ENTRIES:
            assert self.pending is None
            if pc in ENTRIES:want=activity_expected(self,pc)
            else:
                # Existing verifier first constructs an independent RAM oracle,
                # executes the original routine, and asserts that oracle. Use a
                # plain CPU copy so no observer recursively evaluates itself.
                reference=ControlTaskArithmetic()
                reference.__dict__.update(copy.deepcopy(self.__dict__))
                MODELS[pc](reference)
                want=raw.application(reference)
            self.pending=dict(entry=pc,return_pc=self.pr,expected=want,
                              preserved=self.r[8:16].copy(),sr=self.sr&~1,
                              phase=r(self,0x5360),before=[r(self,a) for a in
                              [0x914B,0x8EF8,0x8EFF,0x8F30,0x8F37,0x91E4,0x91E5,0x91E6]])
        return super().instruction(pc)


def task(e):
    phase=r(e,0x5360);before=len(e.boundaries);sp=e.r[15];serial=len(e.sci0_tx)
    e.run(0x18DC8,limit=1000000)
    assert e.r[15]==sp and e.pending is None
    final=(phase+1)&255
    assert r(e,0x5360)==final
    calls=e.boundaries[before:]
    assert [x['entry'] for x in calls]==(ORDER if final%4==2 else [])
    assert len(e.sci0_tx)-serial==int(final%4==2)
    return dict(initial_phase=phase,final_phase=final,boundaries=calls,
                serial_bytes=len(e.sci0_tx)-serial,first_fallback=r(e,0x8EF8),
                second_fallback=r(e,0x8F30))


def fixture():
    e=Observed();e.sci0_status=0xC0;e.sci0_rx.extend([0]*128)
    e.timer_samples=deque(range(20000))  # explicit +1/read samples, not real time
    return e


def main():
    isolated=[]
    for phase in [0,1,2,3,4,5,6,7,253,254,255]:
        e=fixture();w(e,0x5360,phase);isolated.append(task(e))
    e=fixture();retained=[]
    failure=None
    for i in range(32):
        try:retained.append(task(e))
        except (RuntimeError,ValueError,NotImplementedError) as exc:
            failure=dict(call=i,pc=e.pc,status=type(exc).__name__+': '+str(exc),
                         phase=r(e,0x5360),mode=r(e,0x535C,4),
                         tail=e.tail,delay_entries=e.delays[-8:],terminal_entries=e.terminal_entries,
                         completed_tasks=retained,remaining_timer_samples=len(e.timer_samples))
            (ROOT/'control-task-retained-clock-limit.json').write_text(json.dumps(failure,indent=2)+'\n')
            assert i==16 and isinstance(exc,RuntimeError) and e.terminal_entries
            assert e.terminal_entries[-1]['pc']==0xF8D6 and e.pending is None
            break
    assert failure is not None  # explicit zero-state fixture reaches terminal loop
    # Explicit high initial phase tests the byte wrap and subsequent gates.
    e=fixture();w(e,0x5360,252);wrap=[task(e) for _ in range(8)]
    rows=isolated+retained+wrap
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),complete_tasks=len(rows),
                verified_boundaries=sum(len(x['boundaries']) for x in rows),
                isolated=isolated,retained=retained,wrap=wrap,terminal_limit=failure,scope=__doc__)
    (ROOT/'control-task-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('complete tasks',len(rows),'verified boundaries',result['verified_boundaries'])


if __name__=='__main__':main()
