"""Execute original2BCE6 event2 with explicit initialized input and SCI/timer fixtures.

Exploratory admission trace; no callee stubs or physical queue/clock claim.
"""
import hashlib
import json
from pathlib import Path
from verify_control_task_stop_retained import Observed
from verify_control_task_stop import TerminalEntry
from verify_control_contributions import ECU,r,w

ROOT=Path(__file__).resolve().parent
ENTRIES=[0x18282,0x18DC8,0x1CAE8,0x1CAF0,0x1CB04,0x1CB0C,0x1616C,0x16172,0x16178,0x1617E]


class Outer(Observed):
    def __init__(self):
        super().__init__();self.outer_entries=[]

    def write(self,a,v,size):
        if a&0xFFFFFFFF==0xFFFFF75E:
            # SH7058 table22.21: PLDR R/W. Explicit 14-bit word latch;
            # no pin-direction or external-input model. Local probe only.
            if size!=2:raise ValueError('Outer PLDR fixture requires word')
            value=v&0x3FFF
            self.registers[a]=value;self.accesses.append(('write',a,value,size))
            return
        return super().write(a,v,size)

    def instruction(self,pc):
        if pc in ENTRIES:self.outer_entries.append(dict(pc=pc,pr=self.pr,phase=r(self,0x651C)))
        return super().instruction(pc)


def main():
    check=Outer();check.write(0xFFFFF75E,0xFFFF,2)
    assert check.read(0xFFFFF75E,2)==0x3FFF
    try:check.write(0xFFFFF75E,0,1)
    except ValueError:pass
    else:raise AssertionError('Missing bounded PLDR width rejection')
    results=[]
    for phase in [0,1,2,3,4,5,255]:
        e=Outer();e.registers[0xFFFFF74E]=1;e.run(0xCA94)
        w(e,0x651C,phase);w(e,0x652D,2);e.write(0xFFFFD800,2,4)
        preserved=e.r[8:16].copy()
        try:e.run(0x2BCE6,0xFFFFD800,limit=1000000);status='returned'
        except (ValueError,RuntimeError,NotImplementedError,TerminalEntry) as exc:status=type(exc).__name__+': '+str(exc)
        results.append(dict(initial_phase=phase,status=status,pc=e.pc,phase=r(e,0x651C),pending=r(e,0x652D),
                            preserved=e.r[8:16]==preserved,entries=e.outer_entries,tail=e.tail,registers=e.r,
                            accesses=e.accesses,monitor_boundaries=e.boundaries))
    (ROOT/'control-outer-event-probe.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,results=results),indent=2)+'\n')
    for x in results:print(x['initial_phase'],x['status'],hex(x['pc']),x['phase'],[hex(e['pc']) for e in x['entries']])


if __name__=='__main__':main()
