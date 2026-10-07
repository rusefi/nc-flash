/* Ghidra analysis output; verify against original SH instructions. */

/* Original168AC helper clears RAM87F4. Interrupt1692E incrementsit; interruptdelivery/RTE bodies
   remainstaticleads. */

void OutputTimer_ClearPhase(void)

{
  *(undefined1 *)(int)DAT_00016a18 = 0;
  return;
}

