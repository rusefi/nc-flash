/* Ghidra analysis output; verify against original SH instructions. */

/* 40A1zero copies4096/409A to4078/407A then explicit ADC23/11 samples to4098/409C and sets409E=1.
   Nonzero skips without clearing ready. No physical source/units claim. */

void Acquisition_CaptureAlternatePair(void)

{
  undefined *puVar1;
  undefined *puVar2;
  
  puVar1 = PTR_DAT_00005ea4;
  if (*PTR_Acquisition_AlternateCaptureInhibit_00005e98 == '\0') {
    *(undefined2 *)PTR_DAT_00005e9c =
         *(undefined2 *)PTR_Acquisition_AlternateInitialSample23_00005ea0;
    puVar2 = PTR_Acquisition_AlternateFollowupSample23_00005eac;
    *(undefined2 *)puVar1 = *(undefined2 *)PTR_DAT_00005ea8;
    *(undefined2 *)puVar2 = *(undefined2 *)(int)DAT_00005e7c;
    *(undefined2 *)PTR_DAT_00005eb0 = *(undefined2 *)(int)DAT_00005e7e;
    *PTR_Acquisition_AlternatePairReady_00005eb4 = 1;
  }
  return;
}

