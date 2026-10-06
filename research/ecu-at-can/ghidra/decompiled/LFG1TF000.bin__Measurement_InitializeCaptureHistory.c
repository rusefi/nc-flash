/* Ghidra analysis output; verify against original SH instructions. */

/* Sets810C=9244=FF;21482 resets24 history entries/head;9238=7FFFFFFF.5 initialization/SR fixtures
   verified. See tcu-measurement.txt. */

void Measurement_InitializeCaptureHistory(void)

{
  undefined1 uVar1;
  
  uVar1 = (undefined1)DAT_000212a8;
  *PTR_Measurement_CurrentCaptureAge_000212b0 = uVar1;
  *(undefined1 *)(int)DAT_000212aa = uVar1;
  Measurement_ResetHistory();
  *(undefined4 *)PTR_Measurement_NormalizedPeriod_000212b8 = DAT_000212b4;
  return;
}

