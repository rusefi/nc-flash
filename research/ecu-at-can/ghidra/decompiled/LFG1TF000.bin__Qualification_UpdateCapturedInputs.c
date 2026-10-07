/* Ghidra analysis output; verify against original SH instructions. */

/* Fall-through tail of23544; pending-work,93F4/8 capture and8159/B timers select retained/slewed
   values. Delta uses809C, NOT80EA. Writes80F8/93F6/9398/939A; clears capture flags.4536 direct
   cases. */

void Qualification_UpdateCapturedInputs(uint param_1,undefined1 param_2)

{
  byte bVar1;
  bool bVar2;
  undefined *puVar3;
  short sVar4;
  char cVar7;
  short sVar6;
  uint uVar5;
  char cVar8;
  short *psVar9;
  undefined1 *puVar10;
  uint uVar11;
  undefined2 uVar12;
  byte bStack_28;
  byte bStack_24;
  
  puVar3 = PTR_Qualification_StableInputTimer_0002382c;
  uVar11 = (uint)*(short *)PTR_Qualification_RetainedAscendingInput_00023824;
  if ((*(short *)PTR_DAT_00023830 <= *(short *)PTR_Primary_HistoryChange_00023828) ||
     (*(short *)PTR_Primary_HistoryChange_00023828 < *(short *)PTR_DAT_00023834)) {
    *PTR_Qualification_StableInputTimer_0002382c = 0;
  }
  sVar4 = Comparison_ApplicationInput;
  uVar12 = DAT_00023802;
  if (*(char *)(int)DAT_00023800 == '\x01') {
    *PTR_Qualification_CapturedTimer_00023838 = *puVar3;
    *PTR_Qualification_ComparisonTimer_0002383c = (char)uVar12;
    *(short *)(int)DAT_00023804 = sVar4;
  }
  cVar7 = (*(code *)PTR_Phase_HasPendingWork_00023840)();
  cVar8 = DAT_ffff8089;
  uVar5 = param_1;
  if (cVar7 != '\0') {
    bStack_24 = *PTR_DAT_00023844;
    bStack_28 = *PTR_DAT_00023940;
    sVar6 = (short)DAT_ffff8089;
    cVar7 = (*(code *)PTR_Phase_ClassifyDirection_00023944)((int)DAT_ffff8089);
    bVar1 = PTR_DAT_00023948[cVar8];
    if (cVar7 == '\0') {
      bStack_24 = *PTR_DAT_0002394c;
      bStack_28 = *PTR_DAT_00023950;
    }
    bVar2 = false;
    if ((*(short *)PTR_DAT_00023954 <= (short)(*(short *)(int)DAT_00023936 - sVar4)) ||
       ((short)(*(short *)(int)DAT_00023936 - sVar4) <= *(short *)PTR_DAT_00023958)) {
      bVar2 = true;
      psVar9 = (short *)(int)DAT_00023936;
      *PTR_Qualification_ComparisonTimer_0002395c = 0;
      *psVar9 = sVar4;
    }
    if (((bStack_24 <= (byte)*PTR_Qualification_CapturedTimer_00023960) &&
        (((*(char *)(int)DAT_00023938 == '\0' || ((*(byte *)(int)DAT_0002393a & 1) == 1)) &&
         (bStack_28 <= (byte)*PTR_Qualification_ComparisonTimer_0002395c)))) && (!bVar2)) {
      param_2 = *PTR_Qualification_RetainedCategory_00023964;
      if (cVar7 == '\x01') {
        uVar5 = Qualification_SlewUnsignedDifference
                          ((int)*(short *)(int)DAT_0002393c,param_1,
                           (uint)(byte)PTR_Qualification_DescendingSlewFactors_00023968[bVar1] << 7)
        ;
      }
      cVar8 = (*(code *)PTR_ApplicationPhase_ReadForCode_0002396c)((int)sVar6);
      if ('\0' < cVar8) {
        uVar5 = (uint)*(short *)(int)DAT_0002393c;
      }
    }
    if (((cVar7 == '\0') &&
        (uVar11 = uVar5, PTR_Qualification_AscendingMaximumFlags_00023970[bVar1 - 1] == '\x01')) &&
       ((uVar5 & 0xffff) <= (param_1 & 0xffff))) {
      uVar11 = param_1;
    }
  }
  puVar3 = PTR_Qualification_RetainedCategory_00023a34;
  uVar12 = (undefined2)uVar11;
  AscendingRequest_LiveMapAxis = (short)uVar5;
  if ((*PTR_DAT_00023974 & 2) != 0) {
    param_2 = 6;
    uVar12 = SUB42(PTR_DAT_00023a30,0);
    AscendingRequest_LiveMapAxis = uVar12;
  }
  *(undefined2 *)(int)DAT_00023a28 = AscendingRequest_LiveMapAxis;
  *puVar3 = param_2;
  puVar10 = (undefined1 *)(int)DAT_00023a2a;
  *(undefined2 *)PTR_Qualification_RetainedAscendingInput_00023a38 = uVar12;
  *puVar10 = 0;
  *(byte *)(int)DAT_00023a2c = *(byte *)(int)DAT_00023a2c & 0xfe;
  return;
}

