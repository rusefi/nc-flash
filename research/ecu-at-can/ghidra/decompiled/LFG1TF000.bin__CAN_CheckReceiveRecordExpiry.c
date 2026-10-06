/* Ghidra analysis output; verify against original SH instructions. */

/* On deadline expiry refreshes deadline and sets8EE2 record bit via class-dependent actions.
   Downstream diagnostics remain open. */

uint CAN_CheckReceiveRecordExpiry(uint param_1)

{
  uint uVar1;
  undefined4 uVar2;
  
  uVar1 = CAN_RecordDeadlineExpired(param_1,0);
  if ((uVar1 & 0xff) != 0) {
    CAN_SetRecordDeadline(param_1,0);
    uVar1 = (uint)(byte)PTR_DAT_00019e5c[(param_1 & 0xff) * 0x1c];
    if (uVar1 == 0) {
      uVar2 = 7;
    }
    else if (uVar1 == 1) {
      uVar2 = 6;
    }
    else {
      if (uVar1 != 2) {
        return uVar1;
      }
      uVar2 = 5;
    }
    uVar1 = (*(code *)PTR_FUN_00019e60)(uVar2,param_1);
  }
  return uVar1;
}

