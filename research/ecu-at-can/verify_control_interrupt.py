"""Independent FPU stack operations, original timer IRQ entry and return gate.

Explicit hardware PC/SR frame and context values. No hardware acceptance,
VBR selection, callback-body or nonidle contextsave execution in this component.
Original idle branch33F0 executes to task-dispatch boundary3D10.
"""
import hashlib
import itertools
import json
import random
from pathlib import Path
from sh_control_interrupt import ControlInterrupt,execute_to
from verify_control_contributions import ECU,r,w


def put(memory,address,value,size=4):
    memory.update({address+i:v for i,v in enumerate((value&((1<<(size*8))-1)).to_bytes(size,'big'))})


def state(e):
    return (e.gbr,e.mach,e.macl,e.fr.copy(),e.fpul,e.fpscr)


def main():
    instructions=entries=returns=idle_handoffs=0;branches={hex(v):0 for v in [0x3D0C,0x334C,0x33F0]}
    bits=[5,6,10,11,15,16]
    for n,pattern,kind in itertools.product(range(16),range(64),[0x4052,0x4056,0x4062,0x4066]):
        e=ControlInterrupt();e.rom=(kind+n*256).to_bytes(2,'big')
        e.r=[0xA0000000+i for i in range(16)];e.r[n]=0xFFFED000;e.sr=0x3F3
        writable=sum(1<<bit for i,bit in enumerate(bits) if pattern&(1<<i))
        value=writable|0xFFFE739F;e.fpscr=writable|0x40001;e.fpul=value
        e.write(0xFFFECFFC,0xDEADBEEF,4);e.write(0xFFFED000,value,4)
        want=e.ram.copy();registers=e.r.copy();saved=state(e);fpscr=e.fpscr;fpul=e.fpul
        if kind in [0x4052,0x4062]:
            registers[n]-=4;put(want,registers[n],fpul if kind==0x4052 else fpscr)
        else:
            registers[n]+=4
            if kind==0x4056:fpul=value
            else:fpscr=writable|0x40001
        assert e.instruction(0)==(2,False)
        assert e.r==registers and e.ram==want and e.sr==0x3F3
        assert state(e)==saved[:4]+(fpul,fpscr)
        instructions+=1
    pr_cases=0
    for n,value in itertools.product(range(16),[0,1,0x32D8,0x7FFFFFFF,0x80000000,0xFFFFFFFF]):
        e=ControlInterrupt();e.rom=(0x402A+n*256).to_bytes(2,'big');e.r[n]=value
        registers=e.r.copy();memory=e.ram.copy();saved=state(e);status=e.sr
        assert e.instruction(0)==(2,False) and e.pr==value
        assert e.r==registers and e.ram==memory and state(e)==saved and e.sr==status
        pr_cases+=1
    rejected=0
    for kind,address in itertools.product([0x4052,0x4056,0x4062,0x4066],[0xFFFED001,0xFFFFF000]):
        e=ControlInterrupt();e.rom=kind.to_bytes(2,'big');e.r[0]=address
        original=(e.r.copy(),e.ram.copy(),state(e),e.sr)
        try:e.instruction(0)
        except ValueError:rejected+=1
        else:raise AssertionError('unsupported transfer accepted')
        assert (e.r,e.ram,state(e),e.sr)==original
    for seed,(nest,mask,ready,current,task_state) in enumerate(itertools.product(
        [0,1,255,0x7FFFFFFF,0x80000000,0xFFFFFFFF],[0,0x10,0xF0],[0,1,3,255],[0,1,3,255],[0,1])):
        e=ControlInterrupt();rng=random.Random(seed)
        e.r=[rng.randrange(1<<32) for _ in range(16)];e.r[15]=0xFFFECFF8
        e.fr=[rng.randrange(1<<32) for _ in range(16)];e.fpul=rng.randrange(1<<32)
        e.fpscr=(rng.randrange(1<<32)&0x18C60)|0x40001;e.pr=rng.randrange(1<<32);e.sr=(seed%16)*16|(seed&1)|(0x300 if seed&2 else 0)
        e.gbr=0xFFFF8000;e.macl=seed*3;e.mach=seed*7
        w(e,0x12B8,nest,4);w(e,0x12C0,0xB0,4);w(e,0x12B0,ready);w(e,0x12B6,seed%19,2)
        w(e,0x12C8,0xFFFF11A8,4);w(e,0x12C4,0xFFFF11B0,4)
        w(e,0x11A9,task_state);w(e,0x11B1,current)
        return_sr=mask|0x301;return_pc=0x3D0C
        e.write(e.r[15],return_pc,4);e.write(e.r[15]+4,return_sr,4)
        want=e.ram.copy();saved=state(e);original=e.r.copy();original_pr=e.pr;original_sr=e.sr
        stack=[original[0],original_pr,original[1],original[2],*original[3:8],*e.fr[:11],e.fpscr,e.fr[11],e.fpul]
        assert len(stack)==23
        for index,value in enumerate(stack):put(want,original[15]-4*(index+1),value)
        put(want,0xFFFF12B8,nest+1)
        assert execute_to(e,0x2F78,{0xF28C})==0xF28C
        expected=original.copy();expected[:3]=[0x32D8,0xF28C,original_sr];expected[15]-=92
        assert e.r==expected and e.ram==want and state(e)==saved and e.sr==original_sr and e.pr==0x32D8
        entries+=1
        # Perturb only callback-volatile registers; the body itself is not simulated.
        e.r[:8]=[rng.randrange(1<<32) for _ in range(8)]
        e.fr[:12]=[rng.randrange(1<<32) for _ in range(12)];e.fpul=0xDEADBEEF;e.fpscr=0x40001
        e.sr=0xF0;e.pr=0x32D8
        combined=nest|mask
        if combined&0x7FFFFFFF or ready==255:target=0x3D0C
        elif combined&0x80000000:target=0x33F0
        elif task_state==1:target=0x3D0C
        elif ready>current:target=0x334C
        else:target=0x3D0C
        assert execute_to(e,0x32D8,{0x3D0C,0x334C,0x33F0})==target,(nest,mask,ready,current,task_state)
        put(want,0xFFFF12B8,nest)
        assert e.ram==want and state(e)==saved
        if target==0x3D0C:
            expected=original.copy();expected[15]+=8
            assert e.r==expected and e.sr==return_sr and e.pr==original_pr
            assert e.rte_transfers[-1]['pc']==0x333E and e.rte_transfers[-1]['target']==return_pc
        else:
            assert e.r[3:15]==original[3:15] and e.r[15]==original[15]-16
            assert not e.rte_transfers
        if target==0x33F0:
            memory=e.ram.copy();registers=e.r.copy();saved=state(e);prior_pr=e.pr
            put(memory,0xFFFF12B8,0x100)
            registers[0]=seed%19;registers[1]=0x3D10;registers[4]=0xFFFF12B0
            registers[5]=seed%19;registers[15]=int.from_bytes(ECU[0x4078:0x407C],'big')
            assert execute_to(e,0x33F0,{0x3D10})==0x3D10
            assert e.ram==memory and e.r==registers and state(e)==saved and e.pr==prior_pr
            assert e.sr==0xB0 and not e.rte_transfers
            idle_handoffs+=1
        returns+=1;branches[hex(target)]+=1
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        instruction_cases=instructions,pr_instruction_cases=pr_cases,rejected_transfers=rejected,original_entry_cases=entries,
        original_return_gate_cases=returns,return_boundaries=branches,idle_scheduler_handoffs=idle_handoffs,
        limits='Explicit exceptionframe/nesting/context, no actual IRQ acceptance or taskexecution after3D10 or nonidle334C contextsave.')
    Path(__file__).with_name('control-interrupt-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
