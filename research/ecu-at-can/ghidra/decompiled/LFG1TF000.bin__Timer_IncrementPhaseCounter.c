/* Ghidra analysis output; verify against original SH instructions. */

/* u16 RAM90C8 increments wrapping; called on even primary wheel slots. Does not call1E5F6;
   pending-work interpretation unproved. */

void Timer_IncrementPhaseCounter(void)

{
  *(short *)(int)DAT_0001e6ec = *(short *)(int)DAT_0001e6ec + 1;
  return;
}

