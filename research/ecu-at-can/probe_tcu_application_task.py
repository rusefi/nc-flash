"""Compose prior explicit HCAN/ADC/port samples for bounded application probes.

No full-task semantic oracle. Return means coverage only; failure identifies
next unsupported access or missing initialization, never physical behavior.
"""
import hashlib
import json
from pathlib import Path
import verify_tcu_output_pin_switch as pins
from verify_tcu_output_pin_switch import w,r,TCU

ROOT=Path(__file__).resolve().parent
PORTS={0xFFFF0000+a for a in [0xF73E,0xF730,0xF734,0xF736,0xF738,0xF748,0xF74A,0xF74C,0xF74E]}


class ApplicationRegisters(pins.PinRegisters):
    def read(self,a,n):
        if a in self.digital_inputs:
            if n!=2:raise ValueError('Explicit digital input word required')
            value=self.digital_inputs[a];self.digital_trace.append((a,value));return value
        if a in PORTS:
            if n!=2:raise ValueError('Explicit port word required')
            value=self.configuration[a-0xFFFF0000]
            self.configuration_trace.append(('read',a-0xFFFF0000,n,value));return value
        if (a,n) in [(0xFFFFE400,2),(0xFFFFE400,1),(0xFFFFE401,1)]:
            value=self.mcr*256+self.gsr if n==2 else self.mcr if a==0xFFFFE400 else self.gsr
            self.hcan_trace.append(('read',a,n,value));return value
        return super().read(a,n)
    def write(self,a,v,n):
        if a in PORTS:
            if n!=2:raise ValueError('Explicit port word required')
            value=v&65535;self.configuration[a-0xFFFF0000]=value
            self.configuration_trace.append(('write',a-0xFFFF0000,n,value));return
        if (a,n) in [(0xFFFFE400,1),(0xFFFFE412,2)]:
            v &= (1<<(8*n))-1
            if a==0xFFFFE400:self.mcr=v
            self.hcan_trace.append(('write',a,n,v));return
        super().write(a,v,n)


def fixture(mode=3,stage=2,phase=0,gsr=0,source=0):
    t=pins.fixture(phase);t.__class__=ApplicationRegisters;t.mcr=0;t.gsr=gsr;t.hcan_trace=[]
    t.configuration[0xF73E]=0
    t.digital_inputs={0xFFFFF726:0,0xFFFFF778:0x3C,0xFFFFF76C:0,0xFFFFF746:0};t.digital_trace=[]
    pins.setup.configure(t);pins.checked(t,0x147FE,pins.port_init_model)
    for a in t.timer:
        low=a-0xFFFF0000
        if low in t.configuration:t.timer[a]=t.configuration[low]
    t.configuring=False
    for a,v in [(0x8007,mode),(0x84F5,stage),(0x84F4,phase),(0xA5A1,source),(0xA5A2,0),(0x8A19,0)]:w(t,a,v)
    t.configuration_trace=[];t.visited.clear();return t


def main():
    rows=[]
    for gsr in [0,8]:
        for phase in range(8):
            t=fixture(phase=phase,gsr=gsr)
            try:t.run(0x126EC,limit=300000);status='returned';error=None
            except (ValueError,RuntimeError,AssertionError,KeyError,ZeroDivisionError) as e:status='rejected';error=type(e).__name__+': '+str(e)
            rows.append(dict(phase=phase,gsr=gsr,status=status,error=error,pc=hex(t.pc),unique_instructions=len(t.visited),
                visited=[hex(a) for a in sorted(t.visited)],adc_reads=[hex(a) for a in t.adc_reads],hcan_trace=t.hcan_trace,
                port_trace=t.configuration_trace,timer_trace=t.timer_trace,digital_inputs=t.digital_inputs,digital_trace=t.digital_trace))
    (ROOT/'tcu-application-task-probe.json').write_text(json.dumps(dict(scope=__doc__,rom_sha256=hashlib.sha256(TCU).hexdigest(),rows=rows),indent=2)+'\n')
    print([{k:v for k,v in row.items() if k in ['phase','gsr','status','error','pc','unique_instructions']} for row in rows])


if __name__=='__main__':main()
