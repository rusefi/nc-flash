/* Ghidra analysis output; verify against original SH instructions. */

/* 256 independentwholeRAM initcases: reset84D0 and84D4/5/6, set800A1, then16D5C
   compare/startMMIO.91AC preserved. Originalinitializer availablefornativeclockjoin;
   tcu-cmt0-interrupt.txt. */

void CMT0_InitializeTickAndTimerService(void)

{
  (*(code *)PTR_FUN_000123e0)();
  DAT_ffff800a = 1;
  (*(code *)PTR_CMT0_InitializeCompare_000123e4)();
  return;
}

