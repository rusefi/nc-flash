/* Ghidra analysis output; verify against original SH instructions. */

/* IncrementsFFFF84D0 via CMT0 interrupt chain. */

void Tick_Increment(void)

{
  *(int *)(int)DAT_00011954 = *(int *)(int)DAT_00011954 + 1;
  return;
}

