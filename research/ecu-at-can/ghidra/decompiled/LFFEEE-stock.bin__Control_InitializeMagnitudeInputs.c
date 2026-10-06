/* Ghidra analysis output; verify against original SH instructions. */

/* Original protected72B4/72BC zero initialization and72C4clear. Nine cases/checksums;
   callers169C8/199C8. Subsequentproducer/CANattribution unproved; control-magnitude.txt. */

void Control_InitializeMagnitudeInputs(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  (*(code *)PTR_FUN_00041a5c)(0,PTR_Control_FirstMagnitudeInput_00041a58);
  (*(code *)PTR_FUN_00041a5c)(uVar1,PTR_Control_SecondMagnitudeInput_00041a60);
  *PTR_Control_MagnitudeInitializationFlag_00041a64 = 0;
  return;
}

