"""Original ECU CMT1 startup and background re-enable register transactions.

Finite word accesses only; no timer evolution or hardware status side effects.
CompatibleSH7058 CMCSR CKS0 selectsPphi/8, compare2499 =>20000phi per match.
"""
import json
from pathlib import Path
from sh_rotate import SHRotate
from verify_control_contributions import ECU


class Configuration(SHRotate):
    def __init__(self,samples):
        super().__init__(ECU);self.samples=list(samples);self.accesses=[]
    def read(self,a,n):
        a &= 0xFFFFFFFF
        if a>=0xFFFFE000:
            if (a,n)!=(0xFFFFF718,2) or not self.samples:raise ValueError('unsupported finite CMT read')
            value=self.samples.pop(0);self.accesses.append(['read',a,n,value]);return value
        return super().read(a,n)
    def write(self,a,v,n):
        a &= 0xFFFFFFFF
        if a>=0xFFFFE000:
            if n!=2 or a not in [0xFFFFF710,0xFFFFF718,0xFFFFF71A,0xFFFFF71C]:raise ValueError('unsupported CMT write')
            self.accesses.append(['write',a,n,v&65535]);return
        return super().write(a,v,n)


def main():
    count=0
    for entry in [0x105FC,0x1061A]:
        for i in range(256):
            sample=i*257;e=Configuration([sample] if entry==0x105FC else [])
            e.r[15]=0xFFFED000;e.sr=0xF0;saved=e.r[8:16].copy();gbr=e.gbr;memory=e.ram.copy()
            expected=([['write',0xFFFFF710,2,0],['read',0xFFFFF718,2,sample],
                ['write',0xFFFFF718,2,192],['write',0xFFFFF71C,2,2499],
                ['write',0xFFFFF71A,2,0],['write',0xFFFFF710,2,2]] if entry==0x105FC else
                [['write',0xFFFFF710,2,2],['write',0xFFFFF718,2,192],['write',0xFFFFF71C,2,2499]])
            e.run(entry)
            assert e.accesses==expected and not e.samples
            assert e.ram==memory and e.r[8:16]==saved and e.gbr==gbr and e.sr==0xF0
            count+=1
    rejected=0
    for a,n,writing in [(0xFFFFF718,1,False),(0xFFFFF710,2,False),(0xFFFFF716,2,True),(0xFFFFF71A,4,True)]:
        e=Configuration([192])
        try:e.write(a,0,n) if writing else e.read(a,n)
        except ValueError:rejected+=1
        else:raise AssertionError('missing rejection')
    result=dict(status='PASS',scope=__doc__,original_cases=count,rejected_accesses=rejected,
        compatible_cmt1_period_peripheral_clocks=20000,
        compatible_event2_request_period_peripheral_clocks=100000,
        limits='Isolated routines and compatiblemanual. No reset/background reachability, interruptvector/delivery, chipclock frequency or physicalelapsedtime.')
    Path(__file__).with_name('control-cmt1-configuration-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result)


if __name__=='__main__':main()
