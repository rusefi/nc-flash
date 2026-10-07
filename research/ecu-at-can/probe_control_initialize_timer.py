"""Startup with byte-only OCR10B/TCNT10B configuration and no AGCK events.

Initial FF/00 values are explicit fixtures matching documented reset values.
Writes latch; no external clock, compare event or interrupt is synthesized.
SH7058 REJ09B0046-0300H table11.3/printed216, details345/350.
"""
from probe_control_initialize_fpu import SelfTest, run_probe


class TimerStartup(SelfTest):
    WIDTHS = {**SelfTest.WIDTHS, 0xFFFFF6D8: 1, 0xFFFFF6C4: 1}

    def __init__(self):
        super().__init__()
        self.registers[0xFFFFF6D8] = 255
        self.registers[0xFFFFF6C4] = 0


if __name__ == '__main__':
    run_probe(TimerStartup, 'control-initialize-timer-probe.json', __doc__)
