"""Original10022 with bounded SYSCR2 and documented SH7058 SDSR sample.

No callee stubs; module/clock samples do not identify a physical ECU chip.
"""
from sh_control_initialize_syscr import SystemStartup
from probe_control_initialize_fpu import run_probe


if __name__=='__main__':
    run_probe(SystemStartup,'control-initialize-syscr-probe.json',__doc__,
              entry=0x10022,instruction_limit=2000000)
