"""Original10022 -> CA94 ->1619A then40 explicitly sampled outer events.

High10/low15/high15; each transition is sampled twice by originalCADE.
This executes selected original startup routines, not the full reset chain.
"""
from verify_control_clear_startup import run_sequence


if __name__=='__main__':
    run_sequence(0x10022,'control-ramtest-startup-verification.json',__doc__,
                 samples=[1]*10+[0]*15+[1]*15)
