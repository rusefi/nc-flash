"""One explicit timer arrival preempts actual task4 before event2 callback.

Original IRQ/timer, higher-priority acquisition task and scheduler reselection
execute. Arrival is a chosen instruction boundary, with synthetic stack and
hardware frame/entry mask; no physical timing or interrupt-acceptance claim.
"""
import json
from pathlib import Path
from sh_control_interrupt import ControlInterrupt, execute_to
from probe_control_interrupt_timer import timer
from probe_control_timer_event2 import main as sequence
from probe_control_task_dispatch import IdleBoundary
from verify_control_interrupt import put, state
from verify_control_contributions import r


class PreemptBoundary(Exception):
    pass


class Preempted(ControlInterrupt):
    def __init__(self, selector=2):
        super().__init__()
        self.selector = selector
        self.armed = True
        self.preemptions = []

    def instruction(self, pc):
        if (self.armed and pc == 0xDCBA and self.r[2] == 0x2BCE6
                and (self.selector is None or self.read(self.r[9], 4) == self.selector)):
            self.armed = False
            raise PreemptBoundary
        return super().instruction(pc)


def preempt(e, cycle):
    assert e.pc == 0xDCBA and r(e, 0x12B4, 2) == 4
    selector = e.read(e.r[9], 4)
    assert e.selector is None or selector == e.selector
    assert e.sr & 0xF0 == 0 and r(e, 0x12B8, 4) == 0
    assert not any([e.decode_pending, e.qualification_pending,
                    e.consume_pending, e.queue2_pending])
    registers, saved, pr, sr = e.r.copy(), state(e), e.pr, e.sr
    task_sp = registers[15]
    start = len(e.rte_transfers)
    io_start = len(e.cmt_io)
    e.r[15] -= 8
    e.write(e.r[15], 0xDCBA, 4)
    e.write(e.r[15]+4, sr, 4)
    e.sr = 0xF0
    e.cmt_active, e.cmt_samples = True, [0xC0]
    try:
        assert execute_to(e, 0x2F78, {0x32D8}, 1000000) == 0x32D8
    finally:
        e.cmt_active = False
    assert not e.cmt_samples and r(e, 0x12B8, 4) == 1
    assert r(e, 0x12B6, 2) == 7
    # Model the entire epilogue RAM transformation after the real callback.
    want = e.ram.copy()
    gbr, mach, macl, fr, fpul, fpscr = saved
    pushed = [sr, 0xDCBA, registers[0], *registers[8:13], gbr,
              registers[13], mach, registers[14], macl, *fr[12:16],
              *fr[:11], fpscr, fr[11], fpul, *registers[1:8], pr]
    assert len(pushed) == 39
    for index, value in enumerate(pushed, 1):
        put(want, task_sp-4*index, value)
    saved_sp = task_sp-156
    put(want, 0xFFFF12B8, 0x100)
    put(want, 0xFFFF12BC, saved_sp)
    put(want, 0xFFFF11C8, 12, 1)
    assert execute_to(e, 0x32D8, {0x3D10}) == 0x3D10
    assert e.ram == want and e.r[4:6] == [0xFFFF12B0, 7]
    # No selected-index/stack write here: task7 runs, terminates and the
    # original scheduler selects and restores suspended task4 itself.
    assert execute_to(e, 0x3D10, {0xDCBA}, 2000000) == 0xDCBA
    assert e.r == registers and state(e) == saved and e.pr == pr and e.sr == sr
    assert r(e, 0x12B4, 2) == r(e, 0x12B6, 2) == r(e, 0x45CC, 2) == 4
    assert r(e, 0x12B8, 4) == 0
    transfers = e.rte_transfers[start:]
    assert [row['target'] for row in transfers] == [0xE26C, 0xDCBA]
    assert [row['pc'] for row in transfers] == [0x3F3C, 0x3F00]
    accesses = e.cmt_io[io_start:]
    assert accesses == [['read', 0xFFFFF718, 2, 0xC0], ['write', 0xFFFFF718, 2, 0x40]]
    e.preemptions.append(dict(cycle=cycle, pc=0xDCBA, selector=selector, before_registers=registers,
        after_registers=e.r.copy(), before_state=saved, after_state=state(e),
        pr=pr, sr=sr, saved_sp=saved_sp, epilogue_whole_ram=True,
        resumed_task=4, higher_priority_task=7, rte=transfers, mmio=accesses,
        wheel=r(e, 0x51E0, 2), divider=r(e, 0x51E2)))


def scheduler(e, cycle):
    try:
        execute_to(e, 0x32D8, {0x3D0C}, 2000000)
    except PreemptBoundary:
        preempt(e, cycle)
        assert execute_to(e, 0xDCBA, {0x3D0C}, 2000000) == 0x3D0C
    assert r(e, 0x12B8, 4) == 0x80000000
    assert e.r[15] == e.read(0x4078, 4) and e.sr == 0 and not e.queue2_pending
    e.irq_active = False
    e.irq_trace[-1].update(after_idle_stack=e.r[15], final_nesting=r(e, 0x12B8, 4),
        queue2_checks=len(e.queue2_checks))
    raise IdleBoundary


def main(selector=2, name='control-preemption-prefix10.json', cycles=10):
    e, result = sequence(cycles, name, lambda: Preempted(selector), timer, scheduler)
    result.update(preemption_scope=__doc__, preemptions=e.preemptions,
        interrupts=e.irq_trace, queue2_checks=e.queue2_checks,
        queue2_callbacks=e.queue2_callbacks, requested_selector=selector)
    Path(__file__).with_name(name).write_text(json.dumps(result, indent=2)+'\n')
    print('Preemptions', len(e.preemptions), result['status'], flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selector', choices=['1', '2', 'any'], default='2')
    parser.add_argument('--filename', default='control-preemption-prefix10.json')
    parser.add_argument('--cycles', type=int, default=10)
    args = parser.parse_args()
    main(None if args.selector == 'any' else int(args.selector), args.filename, args.cycles)
