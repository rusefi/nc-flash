/* Ghidra analysis output; verify against original SH instructions. */

/* Word4 !=FFFF:88E4=clip16(10*(raw-512)),88E6=2. Invalid holds old number and sets validity1. */

void CAN215_ConvertOffset(void)

{
  uint uVar1;
  int iVar2;
  undefined1 uVar3;
  undefined2 uVar4;
  
  uVar4 = *(undefined2 *)PTR_CAN215_ConvertedOffset_00017828;
  uVar3 = 1;
  uVar1 = (*(code *)PTR_CAN215_ReadWord4_00017830)();
  if ((undefined *)(uVar1 & 0xffff) != PTR_DAT_00017834) {
    iVar2 = (*(code *)PTR_FUN_00017840)(uVar1,PTR_DAT_0001783c,PTR_DAT_00017838);
    if (DAT_00017824 < iVar2) {
      iVar2 = (int)DAT_00017824;
    }
    if (iVar2 < DAT_00017826) {
      iVar2 = (int)DAT_00017826;
    }
    uVar4 = (undefined2)iVar2;
    uVar3 = 2;
  }
  *(undefined2 *)PTR_CAN215_ConvertedOffset_00017828 = uVar4;
  *PTR_CAN215_OffsetValidity_0001782c = uVar3;
  return;
}

