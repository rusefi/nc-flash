/* Ghidra analysis output; verify against original SH instructions. */

/* GBR+2 exact1->3; othersretain; tailcall124AA.256modebytes executed, real interruptdelivery open.
   See tcu-cycle-callback.txt. */

void OutputCycle_ModeCallback(void)

{
  if (DAT_ffff8002 == '\x01') {
    DAT_ffff8002 = '\x03';
  }
  (*(code *)PTR_OutputCycle_UpdateInputs_00011f9c)();
  return;
}

