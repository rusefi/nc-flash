/* Ghidra analysis output; verify against original SH instructions. */

/* Original12880->11004 resets8494/8498/849C; sets8009=1 then16CE4compare/start.256wholeRAM/MMIO
   initcases; preserves84D0/91AC/90C8. FirstadmittedISR promotes3. tcu-cmt1-delivery.txt. */

void CMT1_InitializePrimaryWheel(void)

{
  (*(code *)PTR_Timer_InitializeWheel_000123a4)();
  DAT_ffff8009 = 1;
  (*(code *)PTR_CMT1_InitializeCompare_000123a8)();
  return;
}

