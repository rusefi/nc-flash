/* Ghidra analysis output; verify against original SH instructions. */

/* Mode1 returns; modes3/5 tail57002/56F80. Three originalinitializedtraces verify
   exactentrysequence, first5diagnosticIRQs wait, sixthadmits, next2continue. No
   forcedmode3/fullboot/physicalIRQ. tcu-diagnostic-startup.txt. */

uint Task_RunDiagnosticsForMode(void)

{
  uint uVar1;
  
  uVar1 = (uint)DAT_ffff8006;
  if (uVar1 == 1) {
    return 1;
  }
  if ((uVar1 != 3) && (uVar1 != 5)) {
    return uVar1;
  }
  uVar1 = (*(code *)PTR_FUN_000126a8)();
  return uVar1;
}

