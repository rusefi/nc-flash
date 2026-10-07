"""Bounded original10022 RAM-test/clear parent; no skipped firmware helpers.

Uses established DMA/peripheral fixtures; missing SYSCR2 behavior stays a
recorded limit. Does not establish full reset or successful parent return.
"""
from sh_control_initialize_dma import RamFillStartup
from probe_control_initialize_fpu import run_probe


if __name__=='__main__':
    run_probe(RamFillStartup,'control-initialize-dma-parent-probe.json',__doc__,
              entry=0x10022,instruction_limit=500000)
