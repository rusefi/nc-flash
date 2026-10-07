/* Ghidra analysis output; verify against original SH instructions. */

/* Calls4643A then reads73F20+index:policy0 permits,policy1 requirespredicate1,other policies deny.
   Stock three bytes all1; patched-calibration branches not claimed executed. */

undefined4 Selection_AdmitOverlayLatch(byte param_1)

{
  char cVar1;
  undefined4 uVar2;
  
  uVar2 = 0;
  cVar1 = Selection_TestOverlayThresholdCrossing((int)(char)param_1);
  if ((PTR_Selection_OverlayLatchPolicies_000464a4[param_1] == '\0') ||
     ((PTR_Selection_OverlayLatchPolicies_000464a4[param_1] == '\x01' && (cVar1 == '\x01')))) {
    uVar2 = 1;
  }
  return uVar2;
}

