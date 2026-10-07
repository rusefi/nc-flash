/* Ghidra analysis output; verify against original SH instructions. */

/* 256 original wholeRAM cases PASS:84EC=1,8450=FF via empty128F4/16E6C. Retained ADC-B/CMT0 chain
   reaches3 without forcing readiness. tcu-capture-readiness.txt. */

void Capture_InitializeReadiness(void)

{
  undefined *puVar1;
  
  (*(code *)PTR_FUN_00012350)();
  puVar1 = PTR_FUN_00012358;
  *PTR_Capture_ReadinessState_00012354 = 1;
  (*(code *)puVar1)();
  *PTR_Capture_ReadinessAge_0001235c = (char)DAT_0001234e;
  return;
}

