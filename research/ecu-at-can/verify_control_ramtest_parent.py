"""Whole-RAM oracle for original10022 RAM-test/backup/restore/clear parent.

Explicit SH7058 SYSCR2/SDSR and bounded DMA fixtures; not full reset or timing.
"""
import hashlib
import json
from pathlib import Path
from sh_control_initialize_syscr import SystemStartup
from verify_control_contributions import ECU
from verify_control_raw_inputs import application, expected_write

ROOT=Path(__file__).resolve().parent


def main():
    rows=[]
    for seed in range(3):
        e=SystemStartup()
        for address in range(0xFFFF0000,0xFFFFBFA4):e.write(address,(address*37+seed*19)%255+1,1)
        want=application(e)
        for address in range(0x4000,0xBFA0):expected_write(want,address,0,1)
        saved=e.r[8:16].copy();gbr=e.gbr;sr=e.sr
        try:
            e.run(0x10022,limit=2000000)
            actual=application(e)
            delta=[dict(address=hex(a),actual=actual.get(a,0),expected=want.get(a,0))
                   for a in sorted(actual.keys()|want.keys()) if actual.get(a,0)!=want.get(a,0)]
            assert not delta,delta[:20]
            assert e.r[8:16]==saved and e.gbr==gbr and e.sr&0xF0==sr&0xF0
            assert e.syscr2==1 and len(e.dma_transfers)==1
            status='returned'
        except (ValueError,RuntimeError,NotImplementedError,AssertionError) as exc:
            status=type(exc).__name__+': '+str(exc)
        row=dict(seed=seed,status=status,pc=e.pc,tail=e.tail,dma=e.dma_transfers,accesses=e.accesses)
        rows.append(row)
        (ROOT/'control-ramtest-parent-verification.json').write_text(json.dumps(dict(
            rom_sha256=hashlib.sha256(ECU).hexdigest(),scope=__doc__,rows=rows),indent=2)+'\n')
        print(seed,status,flush=True)
        assert status=='returned'


if __name__=='__main__':main()
