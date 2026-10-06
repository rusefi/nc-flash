/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0002154c) */
/* Updates8098 and shifts four history words92BA..92C0. Jump thresholds15360/2560 latch92C2bit0,
   suppress92B8 change; timer8197>=6 and small long delta clear.600 histories verified. */

void CAN201_UpdateByte6History(void)

{
  undefined *puVar1;
  short sVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  short *psVar6;
  byte *pbVar7;
  
  psVar6 = (short *)(int)DAT_00021600;
  psVar6[3] = psVar6[2];
  psVar6[2] = psVar6[1];
  psVar6[1] = *psVar6;
  puVar1 = PTR_CAN201_SelectByte6ApplicationValue_00021604;
  *psVar6 = CAN201_Byte6ApplicationValue;
  sVar2 = (*(code *)puVar1)();
  CAN201_Byte6ApplicationValue = sVar2;
  (*(code *)PTR_CAN201_PublishByte6ValueAndStatus_00021608)();
  iVar4 = (int)sVar2;
  iVar3 = iVar4 - *psVar6;
  iVar5 = iVar3;
  sVar2 = (*(code *)PTR_FUN_00021614)();
  if (iVar3 < sVar2) {
    iVar5 = -iVar3;
  }
  iVar4 = iVar4 - psVar6[3];
  iVar3 = iVar4;
  sVar2 = (*(code *)PTR_FUN_00021614)();
  if (iVar4 < sVar2) {
    iVar3 = -iVar4;
  }
  pbVar7 = (byte *)(int)DAT_00021602;
  if ((*(short *)PTR_DAT_00021618 <= iVar5) &&
     (*PTR_CAN201_Byte6JumpTimer_0002161c = 0, *(short *)PTR_DAT_00021620 <= iVar3)) {
    *pbVar7 = *pbVar7 | 1;
  }
  if ((iVar3 < *(short *)PTR_DAT_00021620) && (5 < (byte)*PTR_CAN201_Byte6JumpTimer_0002161c)) {
    *pbVar7 = *pbVar7 & 0xfe;
  }
  if ((*pbVar7 & 1) == 1) {
    sVar2 = (*(code *)PTR_FUN_00021614)();
    iVar4 = (int)sVar2;
  }
  *(short *)PTR_CAN201_Byte6HistoryChange_00021624 = (short)iVar4;
  return;
}

