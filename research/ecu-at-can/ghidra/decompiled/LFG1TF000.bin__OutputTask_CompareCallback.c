/* Ghidra analysis output; verify against original SH instructions. */

/* Promotes8008 mode1 to3 iff84A0=8007=84F8=3 thenfull127BA.750 callbackcases;160 retainedIRQ
   bodies. See tcu-output-task.txt. */

void OutputTask_CompareCallback(void)

{
  if ((((DAT_ffff8008 == '\x01') && (*PTR_Startup_AdcAReadinessState_000122c8 == '\x03')) &&
      (DAT_ffff8007 == '\x03')) && (*PTR_DAT_000122cc == '\x03')) {
    (*(code *)PTR_FUN_000122d0)();
    DAT_ffff8008 = '\x03';
  }
  (*(code *)PTR_OutputTask_Dispatch_000122d4)();
  return;
}

