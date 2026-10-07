"""Compare zero-state and original CA94-initialized complete ECU tasks.

PFDR bit0 is an explicit peripheral fixture, not an identified physical input.
CA94 executes normally; filtered input is held afterward. Actual sampling
cadence and boot remain unproved. Stop cases end at terminal entry.
"""
import hashlib
import json
from pathlib import Path
from verify_control_task_stop import StopProbe, TerminalEntry, core, monitor_model
from verify_control_contributions import ECU,r
from sh_integer_arithmetic import SHIntegerArithmetic

ROOT=Path(__file__).resolve().parent


class Observed(StopProbe):
    # SH7058 table11.3 PDFzero257: TSR9, word R/(W). Explicit zero
    # status sample; writes logged only, no event counter/interrupt model.
    WIDTHS={**StopProbe.WIDTHS,0xFFFFF69E:2,0xFFFFF480:2,0xFFFFF482:2,0xFFFFF4EB:1,**{0xFFFF0000+a:2 for a in [0xF4E0,0xF4E2,0xF4E4,0xF4E6,0xF4E8]}}
    def __init__(self):
        super().__init__();self.writes=[];self.guard=None;self.boundaries=[]
        self.sci0_rx.extend([0]*256)

    def write(self,a,v,size):
        if a in [0xFFFFF69E,0xFFFFF480] and size==2:
            self.accesses.append(('write',a,v&65535,size))
            return
        if a<=0xFFFF722A<a+size or a<=0xFFFF735C<a+size:
            self.writes.append(dict(pc=self.pc,address=a,value=v,size=size))
        return super().write(a,v,size)

    def instruction(self,pc):
        # Renesas SH-2E REJ09B0316-0200, sections 7.2.26 and 7.2.58.
        opcode=self.read(pc,2); n=(opcode>>8)&15
        if opcode&0xF00F==0x0007:
            return SHIntegerArithmetic.instruction(self,pc)
        operation=opcode&0xF0FF
        if operation in [0x4013,0x401E,0x4017]:
            if operation==0x4013:  # STC.L GBR,@-Rn
                self.r[n]=(self.r[n]-4)&0xFFFFFFFF
                self.write(self.r[n],self.gbr,4)
            elif operation==0x401E:  # LDC Rn,GBR
                self.gbr=self.r[n]
            else:  # LDC.L @Rn+,GBR
                self.gbr=self.read(self.r[n],4)
                self.r[n]=(self.r[n]+4)&0xFFFFFFFF
            self.visited.add(pc)
            return pc+2,False
        if self.guard is not None and (pc==self.guard['return_pc'] or pc in [0xF8D6,0xF972]):
            saved=self.guard
            assert core(self)==saved.pop('expected')
            assert (pc if pc in [0xF8D6,0xF972] else None)==saved['terminal']
            saved['after']=core(self);self.boundaries.append(saved);self.guard=None
        if pc==0x2C4FC:
            assert self.guard is None
            want,target,_=monitor_model(self)
            self.guard=dict(expected=want,terminal=target,return_pc=self.pr,before=core(self))
        return super().instruction(pc)


def main():
    multiply_cases=0
    values=[0,1,2,0xFFFF,0x10000,0x7FFFFFFF,0x80000000,0x80000001,0xFFFFFFFE,0xFFFFFFFF]
    for a in values:
        for b in values:
            for n in [0,4,15]:
                for m in [0,5,15]:
                    for t in [0,1]:
                        e=Observed();e.rom=(0x0007|n<<8|m<<4).to_bytes(2,'big')
                        e.r[n]=a;e.r[m]=b;e.sr=0x3F0|t;e.mach=0xA55AA55A
                        want=e.r.copy()
                        def signed(v):return int.from_bytes(v.to_bytes(4,'big'),'big',signed=True)
                        product=signed(want[n])*signed(want[m])
                        assert e.instruction(0)==(2,False)
                        assert e.r==want and e.sr==0x3F0|t and e.mach==0xA55AA55A
                        assert e.macl==product%2**32 and e.visited=={0}
                        multiply_cases+=1
    isa_cases=0
    for n in range(16):
        for value in [0,1,0xFFFF,0x10000,0x7FFFFFFF,0x80000000,0xFFFFFFFE,0xFFFFFFFF]:
            for t in [0,1]:
                for opcode in [0x4013,0x401E,0x4017]:
                    e=Observed();e.rom=(opcode|n<<8).to_bytes(2,'big')
                    e.r=[0xABC00000+i for i in range(16)];e.sr=0x3F0|t
                    e.r[n]=value if opcode==0x401E else 0xFFFF1004
                    e.gbr=value if opcode==0x4013 else 0x12345678
                    if opcode==0x4017:e.write(e.r[n],value,4)
                    want=e.r.copy()
                    if opcode==0x4013:want[n]-=4
                    if opcode==0x4017:want[n]+=4
                    assert e.instruction(0)==(2,False)
                    assert e.r==want and e.sr==0x3F0|t and e.gbr==value
                    if opcode==0x4013:assert e.read(want[n],4)==value
                    assert e.visited=={0}
                    isa_cases+=1
    probe=Observed(); rejections=0
    for address in [0xFFFFF69E,0xFFFFF480]:
        probe.write(address,0xFFFF,2);assert probe.read(address,2)==0
    for address,size in [(0xFFFFF482,2),(0xFFFFF4EB,1)]+[(0xFFFF0000+a,2) for a in [0xF4E0,0xF4E2,0xF4E4,0xF4E6,0xF4E8]]:
        probe.write(address,0x12345,size)
        assert probe.read(address,size)==0x12345%2**(8*size)
    for address,size in [(0xFFFFF69E,1),(0xFFFFF480,1),(0xFFFFF482,1),(0xFFFFF4EB,2),(0xFFFFF4E0,1),(0xFFFFF4E2,1)]:
        try:probe.read(address,size)
        except ValueError:rejections+=1
        else:raise AssertionError('Unexpected peripheral width')
    scenarios=[]
    for initialized in [False,True]:
        e=Observed();e.registers[0xFFFFF74E]=int(initialized)
        if initialized:
            sp=e.r[15];e.run(0xCA94)
            assert e.r[15]==sp and r(e,0x44A2,2)==r(e,0x44AC,2)==1
        rows=[]
        for i in range(32 if initialized else 17):
            before=len(e.writes);boundary=len(e.boundaries);sp=e.r[15];gbr=e.gbr
            try:e.run(0x18DC8,limit=1000000);status='returned'
            except TerminalEntry:status=hex(e.stop)
            except (ValueError,RuntimeError,NotImplementedError) as exc:
                (ROOT/'control-task-stop-retained-limit.json').write_text(json.dumps(dict(
                    call=i,initialized=initialized,status=type(exc).__name__+': '+str(exc),
                    pc=e.pc,tail=e.tail,registers=e.r,completed=rows),indent=2)+'\n')
                raise
            assert e.guard is None and len(e.boundaries)==boundary+1
            assert status==('returned' if initialized or i<16 else '0xf8d6')
            if status=='returned':assert e.r[15]==sp and e.gbr==gbr
            writes=e.writes[before:]
            assert [(x['pc'],x['address'],x['value'],x['size']) for x in writes]==[
                (0x154CA,0xFFFF722A,0x1FE if initialized else 0xFF,2),
                (0x42AE4 if initialized else 0x42ADE,0xFFFF735C,int(initialized),1)]
            rows.append(dict(call=i,status=status,phase=r(e,0x5360),writes=writes,
                             monitor=e.boundaries[-1]))
        scenarios.append(dict(ca94_initialized=initialized,pfdr_initial=int(initialized),rows=rows))
    result=dict(rom_sha256=hashlib.sha256(ECU).hexdigest(),complete_tasks=48,
                terminal_entries=1,verified_monitor_boundaries=49,gbr_instruction_cases=isa_cases,multiply_cases=multiply_cases,peripheral_rejections=rejections,scenarios=scenarios,scope=__doc__)
    (ROOT/'control-task-stop-retained-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    legacy=[dict(call=x['call'],status=x['status'],phase=x['phase'],entries=[x['monitor']['before']],writes=x['writes']) for x in scenarios[0]['rows']]
    (ROOT/'control-task-stop-trace.json').write_text(json.dumps(legacy,indent=2)+'\n')
    print('48 complete tasks;49 monitor boundaries;one expected terminal entry')


if __name__=='__main__':main()
