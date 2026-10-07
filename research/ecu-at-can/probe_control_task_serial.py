"""Original mode0 tasks with explicit SCI0 ready status and zero reply bytes.

The synthetic serial input is not an OEM controller response. No startup,
wire exchange, hardware time or valid operating state is established.
"""
import hashlib
import json
from pathlib import Path
from sh_control_task_serial import TaskSerial
from verify_control_contributions import ECU, w, r

ROOT = Path(__file__).resolve().parent


def main():
    rows = []
    for phase in range(8):
        e = TaskSerial(); e.sci0_status = 0xC0; e.sci0_rx.extend([0]*4096)
        w(e, 0x5360, phase); stack = e.r[15]
        try:
            e.run(0x18DC8, limit=1000000)
            assert e.r[15] == stack
            status = 'returned'
        except (ValueError, AssertionError, NotImplementedError, RuntimeError) as exc:
            status = type(exc).__name__ + ': ' + str(exc)
        rows.append(dict(phase=phase, status=status, pc=e.pc, final_phase=r(e, 0x5360),
                         tail=e.tail, direct_calls=e.calls, entries=e.entries,
                         sci0_tx=e.sci0_tx, received=4096-len(e.sci0_rx),
                         peripheral_accesses=e.accesses, registers=e.r))
        print(phase, status, hex(e.pc), 'calls', len(e.calls), 'serial bytes', len(e.sci0_tx), flush=True)
    (ROOT/'control-task-serial-probe.json').write_text(json.dumps(dict(
        scope=__doc__, rom_sha256=hashlib.sha256(ECU).hexdigest(), rows=rows), indent=2)+'\n')


if __name__ == '__main__':
    main()
