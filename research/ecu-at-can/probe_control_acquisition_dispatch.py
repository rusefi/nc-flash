"""Original3D10 index7 dispatch prefix, stopping before unsupported RTE.

Context stack/mask are explicit samples from ROM defaults. The firmware
installs its own selected descriptor; no task body or yield is skipped.
"""
import hashlib,json
from pathlib import Path
from probe_control_acquisition_task import AcquisitionTask
from verify_control_contributions import ECU,w,r


class RteBoundary(Exception):pass


class DispatchPrefix(AcquisitionTask):
    def instruction(self,pc):
        if pc==0x3F3C:raise RteBoundary
        return super().instruction(pc)


def main():
    e=DispatchPrefix();e.sr=0xF0;e.stage='dispatch-prefix'
    stack=int.from_bytes(ECU[0x4078:0x407C],'big')
    w(e,0x12BC,stack,4);w(e,0x12C0,int.from_bytes(ECU[0x4054:0x4058],'big'),4)
    e.r[5]=7
    try:e.run(0x3D10,0xFFFF12B0,limit=100000);status='unexpected-return'
    except RteBoundary:status='RTE boundary'
    except (ValueError,RuntimeError,NotImplementedError) as exc:status=type(exc).__name__+': '+str(exc)
    row=dict(scope=__doc__,status=status,rom_sha256=hashlib.sha256(ECU).hexdigest(),pc=e.pc,
        registers=e.r,sr=e.sr,pr=e.pr,tail=e.tail,
        context={hex(a):r(e,a,n) for a,n in [(0x12B4,2),(0x12B8,4),(0x12BC,4),(0x12C0,4),(0x12C4,4),(0x12C8,4)]},
        descriptor=[r(e,0x11E0+i) for i in range(8)],frame=[e.read(e.r[15]+i*4,4) for i in range(2)])
    Path(__file__).with_name('control-acquisition-dispatch-probe.json').write_text(json.dumps(row,indent=2)+'\n')
    print(status,hex(e.pc),row['context'],row['frame'])


if __name__=='__main__':main()
