"""Bounded execution probe of126EC after ADC/port support; no full-task oracle.

A successful return is execution coverage, NOT verified semantic behavior.
Synthetic initialRAM/ADC/timer values are fixtures, not startup or hardware.
"""
import hashlib
import json
from pathlib import Path
import verify_tcu_output_pin_switch as pins

ROOT=Path(__file__).resolve().parent

def main():
    rows=[]
    for mode,stage,phase in [(m,0,0) for m in [0,1,3]]+[(3,1,0)]+[(3,2,i) for i in range(8)]:
        t=pins.fixture(mode);pins.setup.configure(t)
        pins.checked(t,0x147FE,pins.port_init_model)
        for address in t.timer:
            low=address-0xFFFF0000
            if low in t.configuration:t.timer[address]=t.configuration[low]
        t.configuring=False
        for a,v in [(0x8007,mode),(0x84F5,stage),(0x84F4,phase),(0xA5A1,0),(0xA5A2,0),(0x8A19,0)]:pins.w(t,a,v)
        t.configuration_trace=[];t.visited.clear()
        try:
            t.run(0x126EC,limit=300000);status='returned';error=None
        except (ValueError,RuntimeError,AssertionError,KeyError,ZeroDivisionError) as e:
            status='rejected';error=type(e).__name__+': '+str(e)
        rows.append(dict(mode=mode,stage=stage,phase=phase,status=status,error=error,pc=hex(t.pc),instructions=len(t.visited),
                         visited=[hex(a) for a in sorted(t.visited)],adc_reads=[hex(a) for a in t.adc_reads],
                         port_trace=t.configuration_trace,timer_trace=t.timer_trace))
    (ROOT/'tcu-output-pin-switch-task-probe.json').write_text(json.dumps(dict(scope=__doc__,rom_sha256=hashlib.sha256(pins.TCU).hexdigest(),rows=rows),indent=2)+'\n')
    print([{k:v for k,v in row.items() if k in ['mode','stage','phase','status','error','pc','instructions','adc_reads']} for row in rows])

if __name__=='__main__':main()
