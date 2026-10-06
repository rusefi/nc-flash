/* Ghidra analysis output; verify against original SH instructions. */

/* Only868C!=0 permits class-dependent recovery, clearing8EE2 record bit via1A454/1A598. Does not
   establish DTC recovery completion. */

void CAN_ReceiveRecordRecovery(uint param_1)

{
  char cVar1;
  undefined4 uVar2;
  
  if (*(char *)(int)DAT_00019e52 != '\0') {
    cVar1 = PTR_DAT_00019e5c[(param_1 & 0xff) * 0x1c];
    if (cVar1 == '\0') {
      uVar2 = 4;
    }
    else if (cVar1 == '\x01') {
      uVar2 = 3;
    }
    else {
      if (cVar1 != '\x02') {
        return;
      }
      uVar2 = 2;
    }
    (*(code *)PTR_FUN_00019e60)(uVar2,param_1);
  }
  return;
}

