/* Ghidra analysis output; verify against original SH instructions. */

/* Original1217C calls empty12678,writes8006=1,tail167E4. Three
   independentwholeRAM/exact18MMIO/registerchecks PASS beforeinitializedreadiness traces.
   Initializerordering/epoch remainfixture,notcomplete1168A/reset. tcu-diagnostic-startup.txt. */

void DiagnosticTask_InitializeModeAndTimer(void)

{
  (*(code *)PTR_FUN_000121e0)();
  DAT_ffff8006 = 1;
  (*DAT_000121e4)();
  return;
}

