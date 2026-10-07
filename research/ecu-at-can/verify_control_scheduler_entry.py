"""Independent original3A38 mode admission and native stack/context prefix."""
import hashlib,itertools,json,random
from pathlib import Path
from sh_control_scheduler_entry import SchedulerEntry
from sh_control_interrupt import execute_to
from verify_control_interrupt import put,state
from verify_control_contributions import ECU


def main():
    transfers=admitted=rejected_modes=0
    for n,status in itertools.product(range(16),[0,1,0xB0,0xF0,0x3F3,0x0FFF0FFF]):
        e=SchedulerEntry();e.rom=(0x4003+n*256).to_bytes(2,'big');e.r[n]=0xFFFED000;e.sr=status
        registers=e.r.copy();registers[n]-=4;memory=e.ram.copy();put(memory,registers[n],status)
        saved=state(e);pr=e.pr
        assert e.instruction(0)==(2,False) and e.r==registers and e.ram==memory
        assert e.sr==status and state(e)==saved and e.pr==pr
        transfers+=1
    for high,low in itertools.product([0,0x100,0x80000000,0xFFFFFF00],range(256)):
        e=SchedulerEntry();rng=random.Random(high+low);e.r=[rng.randrange(1<<32) for _ in range(16)]
        e.r[15]=0xFFFED000;e.r[4]=high|low;e.pr=0x3D0C;e.sr=0x3F3
        registers=e.r.copy();memory=e.ram.copy();saved=state(e)
        signed=low if low<128 else low-256;registers[4]=signed&0xFFFFFFFF
        if low==0:
            put(memory,e.r[15]-4,e.sr&~1);put(memory,e.r[15]-8,e.pr)
            put(memory,0xFFFF12D8,e.r[15]-8);put(memory,0xFFFF12B8,256)
            registers[0]=0x3DD8;registers[2]=0xFFFF12B0;registers[15]=0xFFFF11A8
            target=0x3DD8;status=0xB0;admitted+=1
        else:
            registers[0]=0;target=0x3D0C;status=e.sr|1;rejected_modes+=1
        assert execute_to(e,0x3A38,{0x3DD8,0x3D0C})==target
        assert e.r==registers and e.ram==memory and state(e)==saved and e.pr==0x3D0C and e.sr==status
    bad=0
    for address in [0xFFFED001,0xFFFFF000]:
        e=SchedulerEntry();e.rom=bytes.fromhex('4003');e.r[0]=address
        before=(e.r.copy(),e.ram.copy(),e.sr)
        try:e.instruction(0)
        except ValueError:bad+=1
        else:raise AssertionError('invalid STC accepted')
        assert (e.r,e.ram,e.sr)==before
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        stc_instruction_cases=transfers,rejected_accesses=bad,admitted_mode_prefixes=admitted,
        rejected_mode_prefixes=rejected_modes,stock_mode_count=ECU[0x4050],
        limits='Explicit callerSR/PR/stack; first initialization instruction3DD8 not executed here.')
    Path(__file__).with_name('control-scheduler-entry-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
