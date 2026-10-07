/* Ghidra analysis output; verify against original SH instructions. */

/* Mode01 permission5604C; synthetic90B6=1 admits request context. Calls54284 PID dispatcher; PID01
   body verified, transport header not executed. */

uint OBD_Service01(int param_1)

{
  uint uVar1;
  uint uVar2;
  
  uVar2 = 0;
  uVar1 = (*(code *)PTR_Diagnostic_CheckServiceState_000542f4)(1);
  if (((uVar1 & 0xff) == 0) &&
     ((6 < *(ushort *)(param_1 + 8) ||
      (uVar2 = OBD_DispatchCurrentDataPIDs(param_1), (uVar2 & 0xffff) == 0)))) {
    uVar1 = 0x12;
  }
  if ((uVar1 & 0xff) != 0) {
    uVar2 = (*(code *)PTR_Diagnostic_RecordOrSuppressError_000542f8)(uVar1,0);
  }
  return uVar2;
}

