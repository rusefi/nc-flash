"""Original TCU interrupt prefixes on one conditional peripheral-clock timeline.

Explicit fixtures: epoch/count zero, zero service latency, A edges every24320
phi; B edges restart one period after boundaries0/48/80/128 application periods,
with periods11780/12980/8860/18240. Both inputs stop before280*81920.
Tie order CMT0,CMT1,A,B,application. CAN/diagnostic remain once/application.
No full boot, hardware IRQ acceptance, pin identity or physical timing claim.
"""
import heapq

import probe_tcu_application_clock as application
import probe_tcu_initialized_requests as task
from probe_tcu_cmt0_delivery import Observed as ClockMachine, state as clock_state

APP_PERIOD = 81920
LOSS_TIME = 280 * APP_PERIOD
B_SEGMENTS = [(0,48,11780),(48,80,12980),(80,128,8860),(128,280,18240)]


def edges(channel):
    segments = [(0,280,24320)] if channel == 'A' else B_SEGMENTS
    for first,last,period in segments:
        time = first * APP_PERIOD + period
        while time < last * APP_PERIOD:
            yield time
            time += period


class Timeline:
    """Own the next arrival of each independent source; no firmware state."""
    def __init__(self,extra_periods=()):
        # Tuple iterators preserve their cursor when the application oracle
        # deep-copies the machine; Python generators cannot be deep-copied.
        self.captures = {2:iter(tuple(edges('A'))),3:iter(tuple(edges('B')))}
        self.periods = {0:20000,1:40960}
        for rank,period in extra_periods:
            assert rank >= 4 and rank not in self.periods and period > 0
            self.periods[rank] = period
        self.pending = [(period,rank) for rank,period in self.periods.items()]
        for rank, stream in self.captures.items():
            self.pending.append((next(stream),rank))
        heapq.heapify(self.pending)

    def through(self, target):
        while self.pending and self.pending[0][0] <= target:
            time, rank = heapq.heappop(self.pending)
            if rank in self.periods:
                following = time + self.periods[rank]
            else:
                following = next(self.captures[rank],None)
            if following is not None:
                heapq.heappush(self.pending,(following,rank))
            yield time,rank


class Observed(application.Observed):
    def clock_delivery(self):
        self.supplied_clock_requests += 1
        if self.supplied_clock_requests % 100 != 1:
            return
        for time,rank in self.timeline.through((self.application_number+1)*APP_PERIOD):
            number = self.deliver_arrival(time,rank)
            self.arrival_order.append([time,rank,number])

    def deliver_arrival(self,time,rank):
        if rank == 0:
            before = clock_state(self)
            ClockMachine.clock_delivery(self)
            self.clock_edges.append(dict(time=time,number=self.clock_number,
                before=before,after=clock_state(self),interrupt=self.clock_last))
            self.clock_order.append([time,0,self.clock_number])
            return self.clock_number
        if rank == 1:
            application.primary.Observed.primary_delivery(self)
            self.primary_events[-1]['peripheral_match_time'] = time
            self.clock_order.append([time,1,self.primary_number])
            return self.primary_number
        assert rank in [2,3]
        start = len(self.source_rows)
        self.capture_delivery(0x179A8 if rank == 2 else 0x17A58,
                              (time // 2) & 0xFFFFFFFF)
        self.capture_events[-1].update(peripheral_edge_time=time,number=self.capture_number,
            source_boundaries=self.source_rows[start:])
        return self.capture_number

    def application_delivery(self):
        super().application_delivery()
        rank = getattr(self,'application_rank',4)
        self.arrival_order.append([self.application_number*APP_PERIOD,rank,self.application_number])


def fixture():
    t = application.fixture()
    t.__class__ = Observed
    t.timeline = Timeline()
    # Suppress the old once/task callback hook; actual edges are delivered above.
    t.capture_enabled = lambda call,entry: False
    t.arrival_order = []
    t.clock_edges = []
    return t


def before_task(t,call):
    t.arrival_order = []
    t.clock_edges = []
    application.before_task(t,call)


def after_task(t,call):
    out = application.after_task(t,call)
    assert t.arrival_order == sorted(t.arrival_order)
    assert not t.source_pending
    # The next interval appends capture observations before the legacy hook
    # replaces source_rows. Freeze this completed application's list now.
    out['source_boundaries'] = list(out['source_boundaries'])
    out.update(arrival_order=t.arrival_order,cmt0_edges=t.clock_edges,
               capture_schedule=dict(counter_epoch=0,counter_divisor=2,
                   loss_time=LOSS_TIME,b_phase_restart=True,zero_service_latency=True))
    # The inherited field described obsolete once/task deltas, not actual edges.
    out.pop('capture_intervals')
    return out


def main(cycles=8,filename='tcu-capture-timeline-prefix8.json'):
    task.main(cycles=cycles,timer=True,filename=filename,machine_factory=fixture,
              before_task=before_task,after_task=after_task,scope=__doc__)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycles',type=int,default=8)
    parser.add_argument('--filename',default='tcu-capture-timeline-prefix8.json')
    args = parser.parse_args()
    main(args.cycles,args.filename)
