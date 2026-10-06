/* Ghidra analysis output; verify against original SH instructions. */

/* Valid word0 and88E6==2:88E8=clip16(10*(raw0-512)-signed88E4),88EA=2. Else holds number; validity1
   for invalid dependency, otherwise3. */

uint CAN215_ConvertDifference(void)

{
  uint uVar1;
  uint uVar2;
  undefined1 uVar3;
  int iVar4;
  undefined2 uVar5;
  
  uVar5 = *(undefined2 *)PTR_CAN215_ConvertedDifference_000178c8;
  uVar3 = 3;
  uVar1 = (*(code *)PTR_CAN215_ReadWord0_000178d0)();
  uVar2 = uVar1;
  if ((undefined *)(uVar1 & 0xffff) != PTR_DAT_000178d4) {
    uVar2 = (uint)(byte)*PTR_CAN215_OffsetValidity_000178d8;
    if (uVar2 == 2) {
      uVar2 = (*(code *)PTR_FUN_000178e4)(uVar1,PTR_DAT_000178e0,PTR_DAT_000178dc);
      iVar4 = uVar2 - (int)*(short *)PTR_CAN215_ConvertedOffset_000178e8;
      if ((int)DAT_000178c0 < (int)(uVar2 - (int)*(short *)PTR_CAN215_ConvertedOffset_000178e8)) {
        iVar4 = (int)DAT_000178c0;
      }
      uVar3 = 2;
      if (iVar4 < DAT_000178c2) {
        iVar4 = (int)DAT_000178c2;
      }
      uVar5 = (undefined2)iVar4;
      goto LAB_000178b0;
    }
    if (((undefined *)(uVar1 & 0xffff) != PTR_DAT_000178d4) &&
       (uVar2 = (uint)(byte)*PTR_CAN215_OffsetValidity_000178d8, uVar2 != 1)) goto LAB_000178b0;
  }
  uVar3 = 1;
LAB_000178b0:
  *(undefined2 *)PTR_CAN215_ConvertedDifference_000178c8 = uVar5;
  *PTR_CAN215_DifferenceValidity_000178cc = uVar3;
  return uVar2;
}

