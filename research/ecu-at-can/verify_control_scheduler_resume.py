"""Original 3D10 dispatch/hook/table selection of a saved stock type4 task.

Reuses independently checked nonidle-save frames; selected index and caller
stack are explicit. No intervening higher-priority body or native reselection.
"""
import json
from pathlib import Path
from sh_control_interrupt import execute_to
from verify_control_interrupt import put, state
from verify_control_interrupt_nonidle import main as cases
from verify_control_contributions import ECU, w


def resume(e, task, saved_sp, return_pc):
    registers, saved, pr, sr = e.r.copy(), state(e), e.pr, e.sr
    descriptor = 0x40D0+task*16
    task_ram = int.from_bytes(ECU[descriptor+4:descriptor+8], 'big')
    w(e, 0x12B4, 17, 2)
    w(e, 0x12B6, task, 2)
    w(e, 0x12C4, 0xFFFF1230, 4)
    w(e, 0x12C8, 0x41E0, 4)
    caller_sp = 0xFFFEB000
    e.r[4:6] = [0xFFFF12B0, task]
    e.r[15], e.pr, e.sr = caller_sp, 0x13572468, 0xB0
    want = e.ram.copy()
    for address, value, size in [(0xFFFF12B4, task, 2),
            (0xFFFF12C4, task_ram, 4), (0xFFFF12C8, descriptor, 4),
            (0xFFFF12B8, 0, 4), (0xFFFF45CC, task, 2),
            (caller_sp-4, e.pr, 4), (caller_sp-8, 0x3D36, 4)]:
        put(want, address, value, size)
    start = len(e.rte_transfers)
    assert execute_to(e, 0x3D10, {return_pc}) == return_pc
    assert e.ram == want, (task, 'dispatcher whole RAM')
    assert e.r == registers and state(e) == saved and e.pr == pr and e.sr == sr
    assert e.rte_transfers[start:] == [dict(pc=0x3F00,
        sp=registers[15]-8, target=return_pc, status=sr, restored_sr=sr)]
    assert e.read(0xFFFF12BC, 4) == saved_sp and e.read(task_ram, 1) == 12


def main():
    filename = 'control-scheduler-resume-verification.json'
    result = cases(resume, filename)
    result.update(resume_scope=__doc__, original_dispatch_restore_cases=512,
        hook='3D10 -> 36F0 -> E7D4 -> 38B4 publishes task index45CC',
        table='423C + state12 - stocktype4 = 4244 -> 3EB4',
        resume_limits='Selected index/caller stack explicit; no intervening task body/native reselection/physical IRQ.')
    Path(__file__).with_name(filename).write_text(json.dumps(result, indent=2)+'\n')
    print('PASS original dispatcher/hook/context restore', result['original_dispatch_restore_cases'])


if __name__ == '__main__':
    main()
