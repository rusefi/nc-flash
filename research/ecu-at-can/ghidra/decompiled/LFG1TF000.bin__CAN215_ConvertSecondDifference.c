/* Ghidra analysis output; verify against original SH instructions. */

/* BEword2 via1C83C minus converted offset88E4:clip16(10*(raw-512)-signed88E4). Invalid/unready
   holds number;88EE2/1/3.400 callback and20 dependency cases. */

uint CAN215_ConvertSecondDifference(void)

{
  uint uVar1;
  uint uVar2;
  int iVar3;
  undefined1 uVar5;
  undefined2 uVar4;
  
  uVar1 = (*(code *)PTR_CAN215_ReadWord2_00017974)();
  uVar4 = *(undefined2 *)PTR_CAN215_ConvertedSecondDifference_0001796c;
  uVar5 = 3;
  uVar2 = uVar1;
  if ((undefined *)(uVar1 & 0xffff) != PTR_DAT_00017978) {
    uVar2 = (uint)(byte)*PTR_CAN215_OffsetValidity_0001797c;
    if (uVar2 == 2) {
      uVar2 = (*(code *)PTR_FUN_00017988)(uVar1,PTR_DAT_00017984,PTR_DAT_00017980);
      iVar3 = uVar2 - (int)*(short *)PTR_CAN215_ConvertedOffset_0001798c;
      if ((int)DAT_00017964 < (int)(uVar2 - (int)*(short *)PTR_CAN215_ConvertedOffset_0001798c)) {
        iVar3 = (int)DAT_00017964;
      }
      uVar5 = 2;
      if (iVar3 < DAT_00017966) {
        iVar3 = (int)DAT_00017966;
      }
      uVar4 = (undefined2)iVar3;
      goto LAB_00017958;
    }
    if (((undefined *)(uVar1 & 0xffff) != PTR_DAT_00017978) &&
       (uVar2 = (uint)(byte)*PTR_CAN215_OffsetValidity_0001797c, uVar2 != 1)) goto LAB_00017958;
  }
  uVar5 = 1;
LAB_00017958:
  *(undefined2 *)PTR_CAN215_ConvertedSecondDifference_0001796c = uVar4;
  *PTR_CAN215_SecondDifferenceValidity_00017970 = uVar5;
  return uVar2;
}

