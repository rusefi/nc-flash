/* Ghidra analysis output; verify against original SH instructions. */

/* Originalentry576cases PASS:saveR2..R7/FR0..11/FPSCR/FPUL,context12B8++mod32 under12C0
   mask,restoreincomingSR,R0=32D8.92bytes totalincludingwrapper beforeexplicit8bytehardwareframe.
   Notfullhardwareinterruptmodel. control-interrupt-timer.txt. */

undefined * Scheduler_SaveInterruptContext(void)

{
  *(int *)(PTR_DAT_000032d0 + 8) = *(int *)(PTR_DAT_000032d0 + 8) + 1;
  return PTR_Scheduler_RestoreInterruptContextAndSelect_000032d4;
}

