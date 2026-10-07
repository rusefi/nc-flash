"""Original nonidle IRQ context save and direct saved-context restoration.

Stock task descriptors, explicit hardware frame and higher-priority ready task.
Callback volatile registers are perturbed; callback body and task interleaving
are not executed. No hardware interrupt acceptance or elapsed-time claim.
"""
import hashlib
import json
import random
from pathlib import Path
from sh_control_interrupt import ControlInterrupt, execute_to
from verify_control_contributions import ECU, r, w
from verify_control_interrupt import put, state


def main(after_restore=None, filename='control-interrupt-nonidle-verification.json'):
    cases = 0
    tasks = [i for i in range(19) if ECU[0x40D2 + 16*i] < 4]
    for task in tasks:
        descriptor = 0x40D0 + 16*task
        task_ram = int.from_bytes(ECU[descriptor+4:descriptor+8], 'big')
        assert ECU[descriptor] == 4 and ECU[descriptor+1] == 0
        for seed in range(32):
            e = ControlInterrupt()
            rng = random.Random(task*32 + seed)
            e.r = [rng.randrange(1 << 32) for _ in range(16)]
            task_sp = 0xFFFED000
            e.r[15] = task_sp
            e.fr = [rng.randrange(1 << 32) for _ in range(16)]
            e.fpul = rng.randrange(1 << 32)
            e.fpscr = (rng.randrange(1 << 32) & 0x18C60) | 0x40001
            e.gbr, e.mach, e.macl, e.pr = [rng.randrange(1 << 32) for _ in range(4)]
            saved_registers = e.r.copy()
            saved_state, saved_pr = state(e), e.pr
            saved_sr = (seed & 1) | ((seed & 6) << 7)
            return_pc = 0x2000
            for a in range(task_sp-192, task_sp):
                e.write(a, rng.randrange(256), 1)
            w(e, 0x12B0, 4)
            w(e, 0x12B4, task, 2)
            w(e, 0x12B6, 17, 2)
            w(e, 0x12B8, 0, 4)
            w(e, 0x12BC, task_sp, 4)
            w(e, 0x12C0, 0xB0, 4)
            w(e, 0x12C4, task_ram, 4)
            w(e, 0x12C8, descriptor, 4)
            e.write(task_ram, 0, 1)
            e.write(task_ram+1, ECU[descriptor+2], 1)
            e.r[15] -= 8
            e.write(e.r[15], return_pc, 4)
            e.write(e.r[15]+4, saved_sr, 4)
            e.sr = (seed % 16)*16 | (seed & 1)
            # Independent final stack layout, in push order, including the
            # supplied hardware PC/SR frame. All 156 bytes are checked.
            want = e.ram.copy()
            pushed = [saved_sr, return_pc, saved_registers[0],
                      *saved_registers[8:13], e.gbr, saved_registers[13],
                      e.mach, saved_registers[14], e.macl,
                      *e.fr[12:16], *e.fr[:11], e.fpscr, e.fr[11], e.fpul,
                      *saved_registers[1:8], saved_pr]
            assert len(pushed) == 39
            for index, value in enumerate(pushed, 1):
                put(want, task_sp-4*index, value)
            saved_sp = task_sp-156
            put(want, 0xFFFF12B8, 0x100)
            put(want, 0xFFFF12BC, saved_sp)
            put(want, task_ram, 12, 1)
            assert execute_to(e, 0x2F78, {0xF28C}) == 0xF28C
            assert r(e, 0x12B8, 4) == 1
            e.r[:8] = [rng.randrange(1 << 32) for _ in range(8)]
            e.fr[:12] = [rng.randrange(1 << 32) for _ in range(12)]
            e.fpul, e.fpscr, e.pr, e.sr = 0xDEADBEEF, 0x40001, 0x32D8, 0xF0
            assert execute_to(e, 0x32D8, {0x3D10}) == 0x3D10
            assert e.ram == want, (task, seed, 'context RAM')
            expected = saved_registers.copy()
            expected[0:2] = [17, 0x3D10]
            expected[4:6] = [0xFFFF12B0, 17]
            expected[8:12] = [0xFFFF12B0, descriptor, task_ram, saved_sr]
            expected[15] = saved_sp
            assert e.r == expected, (task, seed, 'registers')
            assert state(e) == saved_state and e.pr == saved_pr and e.sr == 0xB0
            assert not e.rte_transfers
            # Explicit restore entry; no claimed execution of the intervening
            # task17 body or scheduler reselection of the preempted task.
            e.r = [rng.randrange(1 << 32) for _ in range(16)]
            e.fr = [rng.randrange(1 << 32) for _ in range(16)]
            e.gbr, e.mach, e.macl, e.fpul, e.fpscr, e.pr = [0]*6
            e.r[4] = saved_sp
            e.sr = 0xF0
            assert execute_to(e, 0x3EB4, {return_pc}) == return_pc
            assert e.r == saved_registers and state(e) == saved_state
            assert e.pr == saved_pr and e.sr == saved_sr and e.ram == want
            assert e.rte_transfers == [dict(pc=0x3F00, sp=task_sp-8,
                target=return_pc, status=saved_sr, restored_sr=saved_sr)]
            if after_restore is not None:
                after_restore(e, task, saved_sp, return_pc)
            cases += 1
    result = dict(status='PASS', scope=__doc__,
        rom_sha256=hashlib.sha256(ECU).hexdigest(), task_indices=tasks,
        original_nonidle_save_cases=cases, original_direct_restore_cases=cases,
        stack_bytes=156, entry_masks=list(range(0, 256, 16)),
        limits='Explicit frame, callback perturbation and restore entry. Stock type4 only; no task17 body, scheduler reselection, hardware IRQ or timing.')
    Path(__file__).with_name(filename).write_text(json.dumps(result, indent=2)+'\n')
    print(result)
    return result


if __name__ == '__main__':
    main()
