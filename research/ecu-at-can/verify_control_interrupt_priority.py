"""Original ECU AA4A priority setup and AA94 branch caller; strict word writes.

Existing INTC write-log fixture extended only to ICR ED18. Latches/logs do not
model pins, priority arbitration, reserved bits or acceptance side effects.
"""
import hashlib,json
from pathlib import Path
from verify_tcu_interrupt_setup import Machine
from verify_control_contributions import ECU

VALUES=[0x999,0x9000,0x900B,0x9099,0x990,0x9090,0x9099,0x9999,0x99B0,0x999,0x9909,0x9909,0xFF]


def main():
    count=0
    for entry in [0xAA4A,0xAA94]:
        for seed in range(128):
            e=Machine(ECU,seed);e.intc.values[0xFFFFED18]=(seed*373)&65535
            e.sr=seed&0xF1;e.r[8:15]=[seed*100+i for i in range(7)]
            saved=(e.r[8:16].copy(),e.gbr,e.macl,e.pr,e.sr,e.vbr);memory=e.ram.copy()
            expected=[['write',0xFFFFED00+i*2,2,v] for i,v in enumerate(VALUES)]
            e.run(entry)
            assert e.intc.accesses==expected and e.intc.values=={a:v for _,a,_,v in expected}
            assert e.ram==memory and (e.r[8:16],e.gbr,e.macl,e.pr,e.sr,e.vbr)==saved
            count+=1
    result=dict(status='PASS',scope=__doc__,rom_sha256=hashlib.sha256(ECU).hexdigest(),
        original_cases=count,ordered_word_writes=expected,
        cmt1_compatible_priority=(VALUES[9]>>4)&15,
        source='SH7058 table7.2 PDFzero145:ED12=IPRJ,ED18=ICR; table7.3 PDFzero155:CMTI1=IPRJbits7..4',
        limits='No fullstartup reachability, physicalchip, ICRpinbehavior, interrupt arbitration or entrySR.')
    Path(__file__).with_name('control-interrupt-priority-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
