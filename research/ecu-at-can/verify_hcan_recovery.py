"""Execute TCU HCAN error-handler body and recovery task with explicit registers.

Register samples are fixtures, not a CAN peripheral simulation. Original
instructions execute through the error-handler body up to (excluding) RTE.
Hardware reset acknowledgement, timer ticks and task order are supplied.
"""
import itertools
import json

from sh_software_arithmetic import SHSoftwareArithmetic
from verify_can201_cut_loop import TCU, w, r, receive, engine_response


class HCANSamples(SHSoftwareArithmetic):
    """Only MCR/GSR samples and observed MCR/IRR writes are admitted."""
    def __init__(self):
        super().__init__(TCU)
        self.mcr = 0
        self.gsr = 0
        self.register_writes = []

    def read(self, addr, size):
        addr &= 0xFFFFFFFF
        if (addr, size) == (0xFFFFE400, 2):
            return self.mcr*256+self.gsr
        if (addr, size) == (0xFFFFE400, 1):
            return self.mcr
        if (addr, size) == (0xFFFFE401, 1):
            return self.gsr
        return super().read(addr, size)

    def write(self, addr, value, size):
        addr &= 0xFFFFFFFF
        if (addr, size) == (0xFFFFE400, 1):
            self.mcr = value & 255
        elif (addr, size) != (0xFFFFE412, 2):
            return super().write(addr, value, size)
        self.register_writes.append([hex(addr), value & ((1 << (8*size))-1), size])

    def error_handler_body(self):
        # Stop before RTE: no exception entry/return or interrupt timing model.
        before = self.r[:8], self.r[15], self.pr
        self.pc = 0x1B3E8
        for _ in range(20000):
            if self.pc == 0x1B422:
                assert (self.r[:8], self.r[15], self.pr) == before
                return
            nxt, delay = self.instruction(self.pc)
            if delay:
                _, nested = self.instruction(self.pc+2)
                assert not nested
            self.pc = nxt
        raise RuntimeError("Error-handler body did not reach RTE")


def initial():
    t = HCANSamples()
    t.run(0x5327C)
    t.run(0x1A164, 0)
    w(t, 0xA939, 1)
    w(t, 0x8464, 200, 2)
    w(t, 0x868C, 1)
    receive(t, 16000)
    return t


def step(t, tick, gsr):
    t.gsr = gsr
    w(t, 0x84D0, tick, 4)
    t.run(0x1A164, 1)
    t.run(0x56908, 0x35)
    t.run(0x57F50)
    for fn in [0x570F6, 0x57258, 0x21C1C, 0x2055C, 0x24FA0]:
        t.run(fn)
    count = t.run(0x558CC, 0xFFFFB000)
    return {"tick": tick, "gsr_sample": gsr, "state": r(t, 0x8BD9),
            "retry_count": r(t, 0x8BCE), "recovery_active": r(t, 0x8BCD),
            "deadline": r(t, 0x8BD4, 4), "raw_group35": r(t, 0xA76B),
            "active_group35": r(t, 0xA721), "aggregate": r(t, 0xA98E),
            "mcr": t.mcr, "cut_request": r(t, 0x9454),
            "ecu_commands": engine_response(t),
            "report": bytes(r(t, 0xB000+i) for i in range(count*3)).hex(" ")}


def main():
    helper_cases = 0
    for mcr, gsr in itertools.product([0, 1, 2, 3, 0x24, 0x80, 0xA4, 0xA7], range(16)):
        t = HCANSamples()
        t.mcr, t.gsr = mcr, gsr
        for fn, expected in [(0x19A14, bool(mcr & 2)), (0x19A30, bool(gsr & 8)),
                             (0x19A62, bool(gsr & 1)), (0x19A80, bool(gsr & 2))]:
            assert t.run(fn) == expected
            helper_cases += 1
        for fn, bit in [(0x199AC, 1), (0x199E0, 2)]:
            for value in [0, 1]:
                t.mcr = mcr
                t.run(fn, value)
                assert t.mcr == ((mcr | bit) if value else (mcr & ~bit))
                assert t.gsr == gsr
                helper_cases += 1
        t.mcr = mcr
        t.register_writes.clear()
        t.error_handler_body()
        assert r(t, 0x8BCF) == bool(gsr & 1)
        assert t.mcr == (mcr | 2 if gsr & 1 else mcr)
        assert t.register_writes == ([["0xffffe400", mcr | 2, 1]] if gsr & 1 else []) + [["0xffffe412", 0x6000, 2]]
    # Fail closed on any peripheral access beyond the explicitly admitted slice.
    rejected = 0
    for operation in [lambda: t.read(0xFFFFE402, 2),
                      lambda: t.write(0xFFFFE401, 0, 1),
                      lambda: t.read(0xFFFFE400, 4)]:
        try:
            operation()
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Unmodelled peripheral access admitted")

    boundary_cases = 0
    for old, tick, gsr, halt, latch in itertools.product(
            [0, 9, 10, 254, 255], [99, 100, 101], [0, 1, 2, 8], range(2), range(2)):
        t = initial()
        t.gsr, t.mcr = gsr, halt*2
        for address, value in [(0x8BD9, 2), (0x8BD8, 1), (0x8BCE, old),
                               (0x8BCF, latch), (0x8BCD, 1)]:
            w(t, address, value)
        w(t, 0x8BD4, 100, 4)
        w(t, 0x84D0, tick, 4)
        t.run(0x1A164, 1)
        if tick < 100:
            assert r(t, 0x8BD9) == 2 and r(t, 0x8BCE) == old
            assert t.mcr == halt*2
        elif halt or latch or gsr & 2:
            assert r(t, 0x8BD9) == 3 and r(t, 0x8BCE) == min(old+1, 255)
            assert t.mcr == 1
        else:
            assert r(t, 0x8BD9) == 1 and r(t, 0x8BCE) == 0
            assert r(t, 0x8BCD) == 0
        boundary_cases += 1

    acknowledgement_cases = 0
    for old, acknowledgement in itertools.product([0, 9, 10, 255], [0, 8]):
        t = initial()
        w(t, 0x8BD9, 3)
        w(t, 0x8BCE, old)
        t.mcr = 1
        for call in range(1, 5):
            t.gsr = acknowledgement
            t.run(0x1A164, 1)
            if acknowledgement or call == 4:
                assert r(t, 0x8BD9) == 4 and t.mcr == 0
                break
            assert r(t, 0x8BD9) == 3 and t.mcr == 1
        # Deadline advances from the old deadline, not the current tick.
        w(t, 0x8BD4, 500, 4)
        w(t, 0x84D0, 900, 4)
        t.gsr = 0
        t.run(0x1A164, 1)
        assert r(t, 0x8BD9) == 0
        assert r(t, 0x8BD4, 4) == 500+(40 if old < 10 else 1000)
        acknowledgement_cases += 1

    producer_cases = 0
    for old, ready, inhibit in itertools.product(range(256), range(2), range(2)):
        t = initial()
        w(t, 0x8BCE, old)
        w(t, 0x8BCD, 1)
        w(t, 0x8BCF, 1)
        w(t, 0xA939, ready)
        w(t, 0x9415, inhibit)
        t.run(0x1A4E4, 1)
        expected = (7 if old >= 10 else 1) if ready and not inhibit else 0
        assert r(t, 0xA76B) == expected
        if not ready or inhibit:
            assert [r(t, a) for a in [0x8BCE, 0x8BCD, 0x8BCF]] == [0, 0, 0]
        t.run(0x56908, 0x35)
        for fn in [0x570F6, 0x57258, 0x21C1C, 0x2055C, 0x24FA0]:
            t.run(fn)
        assert bool(r(t, 0xA98E) & 8) == (expected == 7)
        assert r(t, 0x9454) == (0 if expected == 7 else 1)
        producer_cases += 1

    monitor_gate_cases = 0
    for gsr, recovery_active, group35 in itertools.product([0, 8], range(2), [0, 2, 4, 6]):
        t = initial()
        t.run(0x1A082, 0)
        t.gsr = gsr
        w(t, 0x8BCD, recovery_active)
        w(t, 0xA721, group35)
        for a in [0xA76C, 0xA76D, 0xA76E]:
            w(t, a, 0x55)
        t.run(0x1A082, 1)
        skipped = gsr or recovery_active or group35 & 4
        assert all((r(t, a) == 0x55) == bool(skipped) for a in [0xA76C, 0xA76D, 0xA76E])
        monitor_gate_cases += 1

    t = initial()
    timeline = [step(t, 0, 0)]
    t.gsr = 1
    t.error_handler_body()
    timeline.append(step(t, 100, 1))
    now = 140
    for retry in range(1, 11):
        timeline.append(step(t, now, 1))
        assert r(t, 0x8BCE) == retry and r(t, 0x8BD9) == 3
        assert bool(r(t, 0xA98E) & 8) == (retry == 10)
        timeline.append(step(t, now+1, 8))
        timeline.append(step(t, now+2, 0))
        timeline.append(step(t, now+3, 0))
        now = r(t, 0x8BD4, 4)
        if retry != 10:
            t.gsr = 1
            t.error_handler_body()
    timeline.append(step(t, now, 0))
    for tick in [now+1, now+5000, now+5001, now+5002]:
        timeline.append(step(t, tick, 0))
        assert bool(r(t, 0xA98E) & 8) == (tick <= now+5000)
        assert timeline[-1]["report"] == "c0 73 ff"
    assert len(timeline) == 47 and now == 1500
    print(json.dumps({"scope": __doc__.strip(), "register_helper_cases": helper_cases,
                      "error_handler_cases": 128, "unmapped_access_rejections": rejected,
                      "deadline_and_retry_cases": boundary_cases,
                      "reset_acknowledgement_cases": acknowledgement_cases,
                      "diagnostic_producer_cases": producer_cases,
                      "receive_monitor_gate_cases": monitor_gate_cases,
                      "timeline": timeline,
                      "limits": "Explicit MCR/GSR samples and task/tick schedule; RTE excluded, no interrupt or CAN electrical model. ECU command fixtures restart at each checkpoint. Group3A, physical timer units, traction and roof internals remain unresolved."}, indent=2))


if __name__ == "__main__":
    main()
