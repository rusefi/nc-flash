/* Ghidra analysis output; verify against original SH instructions. */

/* Reads800A; ONLY3 calls11864,1E506,11A64.768 mode/counter cases verify91AC and84D0 increments.
   Direct wrapper execution, not CMT0 hardware emulation. See tcu-reference-policy.txt. */

uint Scheduler_ServiceCaptureElapsedWhenMode3(void)

{
  uint uVar1;
  
  uVar1 = (uint)DAT_ffff800a;
  if ((uVar1 != 1) && (uVar1 == 3)) {
    (*(code *)PTR_Tick_Increment_000128e8)();
    (*(code *)PTR_Reference_ServiceElapsedCaptureCounter_000128ec)();
    uVar1 = (*(code *)PTR_FUN_000128f0)();
    return uVar1;
  }
  return uVar1;
}

