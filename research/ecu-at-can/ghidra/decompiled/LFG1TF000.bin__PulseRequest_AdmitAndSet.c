/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:permission5604C(service4),wordrequest+8==0,predicate53520;success535B4->23DC0 sets9418.
   Errors11/12/22 through541CC;return0 can also mean suppressed rejection. tcu-pulse-request.txt. */

undefined4 PulseRequest_AdmitAndSet(int param_1)

{
  uint uVar1;
  char cVar3;
  undefined4 uVar2;
  
  uVar1 = (*(code *)PTR_Diagnostic_CheckServiceState_00054b58)(4);
  if ((uVar1 & 0xff) == 0) {
    if (*(short *)(param_1 + 8) == 0) {
      cVar3 = (*(code *)PTR_PulseRequest_CheckQualifiedInputs_00054b5c)();
      if (cVar3 == '\0') {
        uVar1 = 0x22;
      }
      else {
        (*(code *)PTR_PulseRequest_SetLatchThunk_00054b60)();
      }
    }
    else {
      uVar1 = 0x12;
    }
  }
  uVar2 = 0;
  if ((uVar1 & 0xff) != 0) {
    uVar2 = (*(code *)PTR_Diagnostic_RecordOrSuppressError_00054b64)(uVar1,0);
  }
  return uVar2;
}

