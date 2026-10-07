/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00023064) */
/* WARNING: Removing unreachable block (ram,0x00023004) */
/* WARNING: Removing unreachable block (ram,0x000230d0) */
/* Four-wordhistory9346,23406 result809A,50F78 publication,categories933D/C,mirror933A.
   Shortchange>=25600 resets8198;long>=2560 latches9344bit0. Long<2560,timer>=6
   clears.933E=longchange unlesslatched.1800 paired cases. */

void Primary_UpdateInputAndHistory(void)

{
  undefined *puVar1;
  short sVar2;
  short sVar3;
  short sVar4;
  int extraout_r3;
  char cVar6;
  short sVar5;
  char cVar7;
  byte *pbVar8;
  short *psVar9;
  
  psVar9 = (short *)(int)DAT_00023038;
  psVar9[3] = psVar9[2];
  psVar9[2] = psVar9[1];
  psVar9[1] = *psVar9;
  puVar1 = PTR_Primary_ConvertCANInput_0002303c;
  *psVar9 = Primary_ApplicationInput;
  sVar2 = (*(code *)puVar1)();
  Primary_ApplicationInput = sVar2;
  (*(code *)PTR_Primary_PublishValueAndStatus_00023040)();
  cVar6 = '\f';
  if (sVar2 < (short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023044[0xc] << 7)) {
    cVar6 = '\0';
    while ((short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023044[cVar6] << 7) <= sVar2) {
      cVar6 = cVar6 + '\x01';
    }
  }
  if ((cVar6 < (char)*PTR_Primary_InputCategory_0002304c) &&
     ((short)((ushort)(byte)PTR_Comparison_CategoryThresholds_00023044[cVar6] * 0x80 -
             *(short *)PTR_DAT_00023048) <= sVar2)) {
    cVar6 = cVar6 + '\x01';
  }
  *PTR_Primary_InputCategory_0002304c = cVar6;
  puVar1 = PTR_Primary_InputMirror_00023054;
  cVar7 = cVar6 >> 1;
  if ('\t' < cVar6) {
    cVar7 = cVar6 + -5;
  }
  *PTR_Primary_CompressedCategory_00023050 = cVar7;
  *(short *)puVar1 = sVar2;
  sVar5 = sVar2 - *psVar9;
  sVar4 = sVar5;
  sVar3 = (*(code *)PTR_FUN_00023060)();
  if (sVar4 < sVar3) {
    sVar5 = -sVar4;
  }
  sVar2 = sVar2 - psVar9[3];
  sVar4 = sVar2;
  sVar3 = (*(code *)PTR_FUN_00023148)();
  if (extraout_r3 < sVar3) {
    sVar2 = -sVar4;
  }
  pbVar8 = (byte *)(int)DAT_00023140;
  if ((*(short *)PTR_DAT_0002314c <= sVar5) &&
     (*PTR_Primary_ChangeLatchTimer_00023150 = 0, *(short *)PTR_DAT_00023154 <= sVar2)) {
    *pbVar8 = *pbVar8 | 1;
  }
  if ((sVar2 < *(short *)PTR_DAT_00023154) && (5 < (byte)*PTR_Primary_ChangeLatchTimer_00023150)) {
    *pbVar8 = *pbVar8 & 0xfe;
  }
  if ((*pbVar8 & 1) == 1) {
    sVar4 = (*(code *)PTR_FUN_00023148)();
  }
  *(short *)PTR_Primary_HistoryChange_0002315c = sVar4;
  return;
}

