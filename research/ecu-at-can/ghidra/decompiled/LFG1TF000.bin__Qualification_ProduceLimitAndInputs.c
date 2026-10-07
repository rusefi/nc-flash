/* Ghidra analysis output; verify against original SH instructions. */

/* Shifts15/25 histories; ratio80EE/80E8 ->939C, curve70331/2 ->93F2; signed92E2 ->939E
   plus6400,92E4/6 ->80F6/8108. Fault92CBbit1 publishes sentinels. Falls through2378A;6860 direct
   cases and4 paired bounded probes; tcu-qualification-limit.txt. */

void Qualification_ProduceLimitAndInputs(void)

{
  byte bVar1;
  bool bVar2;
  undefined *puVar3;
  int iVar4;
  uint uVar5;
  short sVar7;
  undefined *puVar6;
  char cVar8;
  char cVar9;
  ushort uVar12;
  undefined1 *puVar10;
  short *psVar11;
  undefined2 *puVar13;
  ushort uVar14;
  undefined2 uVar15;
  undefined2 *puVar16;
  undefined2 uVar17;
  undefined1 uVar18;
  short sVar19;
  undefined1 uVar20;
  undefined2 *puVar21;
  undefined *puVar22;
  undefined *puVar23;
  uint uVar24;
  ushort uVar25;
  undefined2 uStack_2c;
  undefined2 uStack_28;
  byte local_24;
  
  iVar4 = (int)CAN201_Word0ApplicationValue;
  puVar13 = (undefined2 *)(PTR_Qualification_InputHistory15_0002366c + 0x1a);
  puVar16 = (undefined2 *)(PTR_Qualification_InputHistory15_0002366c + 0x1e);
  puVar21 = (undefined2 *)(PTR_Qualification_InputHistory15_0002366c + 4);
  do {
    puVar16 = puVar16 + -1;
    *puVar16 = *puVar13;
    puVar13 = puVar13 + -1;
  } while (puVar21 <= puVar16);
  *(undefined2 *)PTR_Qualification_InputHistory15_0002366c = DAT_ffff80f6;
  puVar13 = (undefined2 *)(PTR_Qualification_SecondHistory25_00023670 + 0x2e);
  puVar16 = (undefined2 *)(PTR_Qualification_SecondHistory25_00023670 + 0x32);
  puVar21 = (undefined2 *)(PTR_Qualification_SecondHistory25_00023670 + 4);
  do {
    puVar16 = puVar16 + -1;
    *puVar16 = *puVar13;
    puVar13 = puVar13 + -1;
  } while (puVar21 <= puVar16);
  *(undefined2 *)PTR_Qualification_SecondHistory25_00023670 = DAT_ffff8108;
  puVar6 = PTR_DAT_00023674;
  uVar5 = (*(code *)PTR_FUN_00023678)((int)Phase_MeasuredSourceSample << 0xf,iVar4);
  puVar3 = PTR_Qualification_RatioFactorCurve_00023680;
  puVar22 = (undefined *)((uVar5 & 0xffff) * (int)puVar6 >> 0xf);
  if (puVar6 < puVar22) {
    puVar22 = puVar6;
  }
  *(short *)PTR_Qualification_MeasurementRatio_0002367c = (short)puVar22;
  uVar5 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00023684)(puVar22,puVar3);
  puVar6 = PTR_Arithmetic_GuardedSignedDivision_00023688;
  sVar19 = (short)((uVar5 & 0xffff) >> 1);
  *(short *)(int)DAT_00023662 = sVar19;
  iVar4 = (*(code *)puVar6)((int)*(short *)PTR_SparkRequest_BaseValue_0002368c * (int)sVar19,
                            (int)DAT_00023664);
  puVar3 = PTR_DAT_00023690;
  puVar22 = (undefined *)(iVar4 << 1);
  if ((int)PTR_DAT_00023690 < iVar4 << 1) {
    puVar22 = PTR_DAT_00023690;
  }
  puVar23 = (undefined *)(int)DAT_00023666;
  if ((int)puVar22 < (int)puVar23) {
    puVar22 = puVar23;
  }
  uVar12 = DAT_00023668 + (short)puVar22;
  uStack_2c = (undefined2)((int)puVar22 >> 1);
  iVar4 = (*(code *)puVar6)((int)*(short *)PTR_DAT_00023694 * (int)sVar19,(int)DAT_00023664);
  puVar22 = (undefined *)(iVar4 << 1);
  if ((int)puVar3 < iVar4 << 1) {
    puVar22 = puVar3;
  }
  if ((int)puVar22 < (int)puVar23) {
    puVar22 = puVar23;
  }
  uStack_28 = (undefined2)((int)puVar22 >> 1);
  iVar4 = (*(code *)puVar6)((int)*(short *)PTR_DAT_00023698 * (int)sVar19,(int)DAT_00023664);
  puVar22 = (undefined *)(iVar4 << 1);
  if ((int)puVar3 < iVar4 << 1) {
    puVar22 = puVar3;
  }
  if ((int)puVar22 < (int)puVar23) {
    puVar22 = puVar23;
  }
  uVar24 = 6;
  uVar17 = SUB42(puVar22 + DAT_00023668,0);
  uVar5 = (uint)(uVar12 >> 8);
  if (uVar5 < (byte)PTR_Qualification_CategoryThresholds_0002369c[6]) {
    for (uVar24 = 0; (byte)PTR_Qualification_CategoryThresholds_0002369c[uVar24] <= uVar5;
        uVar24 = uVar24 + 1) {
    }
  }
  if (((uVar24 & 0xff) < (uint)(byte)*PTR_Qualification_InputCategory_000236e0) &&
     ((int)((uint)(byte)PTR_Qualification_CategoryThresholds_0002369c[uVar24] -
           (uint)(byte)*PTR_DAT_000236e4) <= (int)uVar5)) {
    uVar24 = uVar24 + 1;
  }
  uVar18 = (undefined1)uVar24;
  uVar5 = ((uint)(puVar22 + DAT_00023668) & 0xffff) >> 8;
  uVar24 = 6;
  if (uVar5 < (byte)PTR_Qualification_CategoryThresholds_0002369c[6]) {
    for (uVar24 = 0; (byte)PTR_Qualification_CategoryThresholds_0002369c[uVar24] <= uVar5;
        uVar24 = uVar24 + 1) {
    }
  }
  if (((uVar24 & 0xff) < (uint)*(byte *)(int)DAT_000237f8) &&
     ((int)((uint)(byte)PTR_Qualification_CategoryThresholds_0002369c[uVar24] -
           (uint)(byte)*PTR_DAT_00023808) <= (int)uVar5)) {
    uVar24 = uVar24 + 1;
  }
  uVar20 = (undefined1)uVar24;
  sVar7 = (*(code *)PTR_Qualification_CalculateCorrection_0002380c)();
  puVar6 = (undefined *)(*(code *)puVar6)((int)sVar7 * (int)sVar19,(int)DAT_000237fa);
  if ((int)puVar3 < (int)puVar6) {
    puVar6 = puVar3;
  }
  if ((int)puVar6 < (int)DAT_000237fc) {
    puVar6 = (undefined *)(int)DAT_000237fc;
  }
  uVar15 = (short)((int)puVar6 >> 1);
  if ((*PTR_DAT_00023810 & 2) != 0) {
    uVar18 = 6;
    uVar17 = SUB42(PTR_DAT_00023814,0);
    uVar20 = 6;
    uStack_2c = DAT_000237fe;
    uStack_28 = DAT_000237fe;
    uVar15 = DAT_000237fe;
  }
  DAT_ffff80f6 = uStack_2c;
  DAT_ffff8108 = uStack_28;
  puVar10 = (undefined1 *)(int)DAT_000237f8;
  *(undefined2 *)PTR_Qualification_ProducedLimit_00023818 = uVar17;
  *puVar10 = uVar20;
  puVar6 = PTR_Qualification_ScaledCorrection_00023820;
  *PTR_Qualification_InputCategory_0002381c = uVar18;
  *(undefined2 *)puVar6 = uVar15;
  puVar6 = PTR_Qualification_StableInputTimer_0002382c;
  uVar5 = (uint)(short)uVar12;
  uVar14 = *(ushort *)PTR_Qualification_RetainedAscendingInput_00023824;
  if ((*(short *)PTR_DAT_00023830 <= *(short *)PTR_Primary_HistoryChange_00023828) ||
     (*(short *)PTR_Primary_HistoryChange_00023828 < *(short *)PTR_DAT_00023834)) {
    *PTR_Qualification_StableInputTimer_0002382c = 0;
  }
  sVar19 = Comparison_ApplicationInput;
  uVar17 = DAT_00023802;
  if (*(char *)(int)DAT_00023800 == '\x01') {
    *PTR_Qualification_CapturedTimer_00023838 = *puVar6;
    *PTR_Qualification_ComparisonTimer_0002383c = (char)uVar17;
    *(short *)(int)DAT_00023804 = sVar19;
  }
  cVar8 = (*(code *)PTR_Phase_HasPendingWork_00023840)();
  cVar9 = DAT_ffff8089;
  uVar25 = uVar12;
  if (cVar8 != '\0') {
    local_24 = *PTR_DAT_00023844;
    uStack_28._0_1_ = *PTR_DAT_00023940;
    sVar7 = (short)DAT_ffff8089;
    cVar8 = (*(code *)PTR_Phase_ClassifyDirection_00023944)((int)DAT_ffff8089);
    bVar1 = PTR_DAT_00023948[cVar9];
    if (cVar8 == '\0') {
      local_24 = *PTR_DAT_0002394c;
      uStack_28._0_1_ = *PTR_DAT_00023950;
    }
    bVar2 = false;
    if ((*(short *)PTR_DAT_00023954 <= (short)(*(short *)(int)DAT_00023936 - sVar19)) ||
       ((short)(*(short *)(int)DAT_00023936 - sVar19) <= *(short *)PTR_DAT_00023958)) {
      bVar2 = true;
      psVar11 = (short *)(int)DAT_00023936;
      *PTR_Qualification_ComparisonTimer_0002395c = 0;
      *psVar11 = sVar19;
    }
    if (((local_24 <= (byte)*PTR_Qualification_CapturedTimer_00023960) &&
        (((*(char *)(int)DAT_00023938 == '\0' || ((*(byte *)(int)DAT_0002393a & 1) == 1)) &&
         (uStack_28._0_1_ <= (byte)*PTR_Qualification_ComparisonTimer_0002395c)))) && (!bVar2)) {
      uVar18 = *PTR_Qualification_RetainedCategory_00023964;
      if (cVar8 == '\x01') {
        uVar5 = Qualification_SlewUnsignedDifference
                          ((int)*(short *)(int)DAT_0002393c,uVar5,
                           (uint)(byte)PTR_Qualification_DescendingSlewFactors_00023968[bVar1] << 7)
        ;
      }
      cVar9 = (*(code *)PTR_ApplicationPhase_ReadForCode_0002396c)((int)sVar7);
      if ('\0' < cVar9) {
        uVar5 = (uint)*(short *)(int)DAT_0002393c;
      }
    }
    uVar25 = (ushort)uVar5;
    if (((cVar8 == '\0') &&
        (uVar14 = uVar25, PTR_Qualification_AscendingMaximumFlags_00023970[bVar1 - 1] == '\x01')) &&
       ((uVar5 & 0xffff) <= (uint)uVar12)) {
      uVar14 = uVar12;
    }
  }
  puVar6 = PTR_Qualification_RetainedCategory_00023a34;
  AscendingRequest_LiveMapAxis = uVar25;
  if ((*PTR_DAT_00023974 & 2) != 0) {
    uVar18 = 6;
    uVar14 = (ushort)PTR_DAT_00023a30;
    AscendingRequest_LiveMapAxis = uVar14;
  }
  *(ushort *)(int)DAT_00023a28 = AscendingRequest_LiveMapAxis;
  *puVar6 = uVar18;
  puVar10 = (undefined1 *)(int)DAT_00023a2a;
  *(ushort *)PTR_Qualification_RetainedAscendingInput_00023a38 = uVar14;
  *puVar10 = 0;
  *(byte *)(int)DAT_00023a2c = *(byte *)(int)DAT_00023a2c & 0xfe;
  return;
}

