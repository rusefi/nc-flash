"""Preserve the retained mode0 failure with a frozen TCNT0 fixture."""
import json
from pathlib import Path
from sh_control_task_serial import TaskSerial
from verify_control_contributions import r

def main():
    e=TaskSerial();e.sci0_status=0xC0;e.sci0_rx.extend([0]*128);rows=[]
    for i in range(32):
        try:e.run(0x18DC8,limit=1000000);status='returned'
        except (RuntimeError,ValueError,NotImplementedError) as exc:
            status=type(exc).__name__+': '+str(exc)
        rows.append(dict(call=i,status=status,phase=r(e,0x5360),serial_bytes=len(e.sci0_tx),
                         pc=e.pc,tail=e.tail.copy(),registers=e.r.copy()))
        if status!='returned':break
    Path(__file__).with_name('control-task-retained-probe.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(len(rows),rows[-1]['status'])

if __name__=='__main__':main()
