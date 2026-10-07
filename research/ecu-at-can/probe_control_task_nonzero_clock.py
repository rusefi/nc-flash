"""Explicit coarse TCNT0 samples distinguish a wait from a terminal loop."""
from collections import deque
import json
from pathlib import Path
from sh_control_task_serial import TaskSerial
from verify_control_contributions import w

def main():
    e=TaskSerial();w(e,0x535C,1,4);e.sci0_status=0xC0;e.sci0_rx.extend([0]*128)
    e.timer_samples=deque(i*16000 for i in range(1000))
    try:e.run(0x18DC8,limit=1000000);status='returned'
    except (ValueError,RuntimeError,NotImplementedError) as exc:status=type(exc).__name__+': '+str(exc)
    out=dict(status=status,pc=e.pc,delays=e.delays,remaining_timer_samples=len(e.timer_samples),
             registers=e.r,tail=e.tail,calls=e.calls,terminal_entries=e.terminal_entries)
    Path(__file__).with_name('control-task-nonzero-clock-probe.json').write_text(json.dumps(out,indent=2)+'\n')
    assert status.startswith('RuntimeError: Instruction limit') and e.terminal_entries
    print(status,'terminal entries',e.terminal_entries)

if __name__=='__main__':main()
