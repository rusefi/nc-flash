/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00023224) */
/* WARNING: Removing unreachable block (ram,0x000231da) */
/* WARNING: Removing unreachable block (ram,0x00023296) */
/* Wholebody shifts4-wordhistory934E, publishes23380 result to809C and50AC8 status;
   categories9338/9; signedwrapped changes,latch9344bit1,timer8199;25-wordhistory9358
   andphase/code-conditioned9342.1600 randomized cases. */

void Comparison_UpdateInputAndHistory(void)

{
  undefined *puVar1;
  short sVar2;
  short sVar3;
  undefined1 uVar4;
  char cVar5;
  int extraout_r1;
  int extraout_r3;
  char cVar8;
  short sVar7;
  byte *pbVar6;
  short *psVar9;
  short sVar11;
  int iVar10;
  short *psVar12;
  short *psVar13;
  char *pcVar14;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  
  psVar13 = (short *)(int)DAT_00023142;
  psVar13[3] = psVar13[2];
  psVar13[2] = psVar13[1];
  psVar13[1] = *psVar13;
  puVar1 = PTR_Comparison_ConvertSelectedInput_00023160;
  *psVar13 = Comparison_ApplicationInput;
  sVar2 = (*(code *)puVar1)();
  Comparison_ApplicationInput = sVar2;
  (*(code *)PTR_Comparison_PublishValueAndStatus_00023164)();
  cVar8 = '\f';
  if (sVar2 < (short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023168[0xc] << 7)) {
    cVar8 = '\0';
    while ((short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023168[cVar8] << 7) <= sVar2) {
      cVar8 = cVar8 + '\x01';
    }
  }
  if ((cVar8 < (char)*PTR_Comparison_InputCategory_00023210) &&
     ((short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023168[cVar8] * 0x80 -
             *(short *)PTR_DAT_0002320c) <= sVar2)) {
    cVar8 = cVar8 + '\x01';
  }
  cVar5 = cVar8 >> 1;
  *PTR_Comparison_InputCategory_00023210 = cVar8;
  if ('\t' < cVar8) {
    cVar5 = cVar8 + -5;
  }
  *PTR_Comparison_CompressedCategory_00023214 = cVar5;
  sVar7 = sVar2 - *psVar13;
  local_1c = 0;
  local_20 = DAT_00023218;
  sVar11 = sVar7;
  sVar3 = (*(code *)PTR_FUN_00023220)();
  if (extraout_r1 < sVar3) {
    sVar7 = -sVar11;
  }
  sVar2 = sVar2 - psVar13[3];
  local_24 = 0;
  local_28 = DAT_00023218;
  pcVar14 = (char *)&local_28;
  sVar11 = sVar2;
  sVar3 = (*(code *)PTR_FUN_00023320)();
  if (extraout_r3 < sVar3) {
    sVar11 = -sVar2;
  }
  pbVar6 = (byte *)(int)DAT_00023316;
  if ((*(short *)PTR_DAT_00023324 <= sVar7) &&
     (*PTR_DAT_00023328 = 0, *(short *)PTR_DAT_0002332c <= sVar11)) {
    *pbVar6 = *pbVar6 | 2;
  }
  if ((sVar11 < *(short *)PTR_DAT_0002332c) && (5 < (byte)*PTR_DAT_00023328)) {
    *pbVar6 = *pbVar6 & 0xfd;
  }
  if ((*pbVar6 & 2) != 0) {
    local_2c = 0;
    local_30 = DAT_00023330;
    pcVar14 = (char *)&local_30;
    sVar2 = (*(code *)PTR_FUN_00023320)();
  }
  psVar12 = (short *)(int)DAT_00023318;
  *(short *)PTR_Comparison_HistoryChange_00023334 = sVar2;
  psVar13 = psVar12 + 0x17;
  psVar9 = psVar12 + 0x19;
  do {
    psVar9 = psVar9 + -1;
    *psVar9 = *psVar13;
    puVar1 = PTR_Phase_HasPendingWork_00023338;
    psVar13 = psVar13 + -1;
  } while (psVar12 + 2 <= psVar9);
  *psVar12 = sVar2;
  uVar4 = (*(code *)puVar1)();
  cVar8 = DAT_ffff8089;
  *pcVar14 = uVar4;
  cVar5 = (*(code *)PTR_ApplicationPhase_ReadForCode_0002333c)((int)DAT_ffff8089);
  puVar1 = PTR_Comparison_RetainedHistoryChange_0002337c;
  sVar11 = sVar2;
  if ((*pcVar14 == '\0') || (*(char *)(int)DAT_0002331a != cVar8)) {
    if (*(char *)(int)DAT_0002331a != cVar8) {
      iVar10 = 1;
      psVar12 = psVar12 + 1;
      *(short **)pcVar14 = psVar12;
      psVar13 = psVar12;
      while (iVar10 <= (int)(uint)(byte)*PTR_DAT_00023378) {
        iVar10 = iVar10 + 1;
        if (sVar11 < *psVar12) {
          sVar11 = *psVar13;
        }
        psVar13 = psVar13 + 1;
        psVar12 = psVar12 + 1;
      }
    }
  }
  else {
    sVar11 = *(short *)PTR_Comparison_RetainedHistoryChange_00023340;
    if ((cVar5 < '\x01') && (sVar11 < sVar2)) {
      sVar11 = sVar2;
    }
  }
  *(char *)(int)DAT_00023374 = cVar8;
  *(short *)puVar1 = sVar11;
  return;
}

