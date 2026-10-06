/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00020a20) */
/* WARNING: Removing unreachable block (ram,0x00020a00) */
/* WARNING: Removing unreachable block (ram,0x00020a9c) */
/* Runs20CBC/20FAC then fallback(9194bit0/91A6bit4),hold(bit0),stale(ages>=14),or history.
   Healthy80EA uses18 entries;80EC window extends while cumulative<9238 or selectedcount<5
   unless92C6bit4.900 branch cases; all original helpers, no stubs. See tcu-reference-source.txt. */

int Reference_SelectMeasuredOrHistorySource(void)

{
  undefined *puVar1;
  char cVar5;
  short sVar3;
  undefined2 uVar4;
  undefined4 uVar2;
  byte bVar6;
  uint uVar7;
  byte bVar8;
  byte *pbVar9;
  undefined4 uVar10;
  int iVar11;
  int iVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  byte *pbVar16;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined1 local_2c;
  
  local_2c = 0;
  Reference_UpdateHoldAndFaultGates();
  Reference_UpdateDiscrepancyLatch();
  cVar5 = (*(code *)PTR_Phase_HasPendingWork_00020a7c)();
  pbVar9 = PTR_Reference_IdleSettlingTimer_00020a80;
  if (cVar5 != '\0') {
    *PTR_Reference_IdleSettlingTimer_00020a80 = 0;
  }
  bVar6 = CAN231_SixStateSource;
  local_38 = 0;
  local_3c = DAT_00020a84;
  bVar8 = TransmissionStateClass;
  sVar3 = (*(code *)PTR_FUN_00020a8c)();
  iVar14 = (int)sVar3;
  local_40 = 0;
  local_44 = DAT_00020a84;
  sVar3 = (*(code *)PTR_FUN_00020a8c)();
  iVar13 = (int)sVar3;
  uVar10 = 0xffffffff;
  local_44 = CONCAT13(*(undefined1 *)(int)DAT_00020a78,local_44._1_3_);
  iVar12 = (int)*(short *)(int)DAT_00020a7a;
  uVar7 = 1;
  pbVar16 = (byte *)&local_44;
  if ((cVar5 == '\0') &&
     (pbVar16 = (byte *)&local_44, (uint)(byte)*PTR_DAT_00020a90 <= (uint)*pbVar9 << 2)) {
    iVar12 = (int)Phase_MeasuredSourceSample;
    local_44 = CONCAT13(bVar6,local_44._1_3_);
    uVar7 = 0;
    pbVar16 = (byte *)&local_44;
    if ((byte)*PTR_DAT_00020a98 <= (byte)*PTR_Measurement_CurrentCaptureAge_00020a94) {
      local_48 = 0;
      local_4c = DAT_00020a84;
      pbVar16 = (byte *)&local_4c;
      sVar3 = (*(code *)PTR_FUN_00020b0c)();
      iVar12 = (int)sVar3;
    }
  }
  *(short *)(int)DAT_00020b04 = (short)iVar12;
  puVar1 = PTR_DAT_00020bfc;
  if (((*PTR_Reference_SourceStatus_00020b10 & 1) == 0) &&
     ((*(byte *)(int)DAT_00020b06 & 0x10) == 0)) {
    if ((*(byte *)(int)DAT_00020b06 & 1) == 0) {
      if (((byte)*PTR_DAT_00020b14 < (byte)*PTR_DAT_00020b18) &&
         ((byte)*PTR_DAT_00020b1c < (byte)*PTR_DAT_00020b18)) {
        iVar14 = (int)DAT_00020bf6;
        *(byte *)(int)DAT_00020bf4 = *(byte *)(int)DAT_00020bf4 & 0xfb;
        uVar4 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00020c04)
                          ((int)(short)(ushort)(byte)*puVar1 * (int)*(short *)PTR_DAT_00020c00,
                           iVar14);
        *(undefined2 *)(pbVar16 + 4) = uVar4;
        iVar15 = 0;
        sVar3 = 0;
        pbVar16[0xc] = 0;
        pbVar16[0xd] = 0;
        pbVar16[0xe] = 0;
        pbVar16[0xf] = 0;
        iVar11 = *(int *)PTR_Measurement_NormalizedPeriod_00020c08;
        uVar10 = (*(code *)PTR_FUN_00020c0c)();
        bVar6 = *(byte *)(int)DAT_00020bf8;
        iVar14 = (int)*(short *)(pbVar16 + 4);
        iVar12 = 0;
        if (0 < iVar14) {
          do {
            iVar15 = iVar15 + *(int *)(PTR_Reference_CaptureHistory_00020c10 + (uint)bVar6 * 4);
            if (bVar6 == 0) {
              bVar6 = *PTR_DAT_00020bfc;
            }
            bVar6 = bVar6 - 1;
            if ((iVar15 < iVar11) || (sVar3 < 5)) {
              sVar3 = sVar3 + 1;
              *(int *)(pbVar16 + 0xc) = iVar15;
            }
            iVar12 = iVar12 + 1;
          } while (iVar12 < iVar14);
        }
        (*(code *)PTR_FUN_00020c14)(uVar10);
        uVar10 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_00020c18)
                           (iVar15,*PTR_DAT_00020bfc,0);
        uVar10 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020c1c)(uVar10,iVar14);
        iVar14 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020c1c)(DAT_00020c20,uVar10);
        if ((*PTR_ApplicationFaultFlags92C6_00020c24 & 0x10) == 0) {
          *(int *)(pbVar16 + -4) = (int)sVar3;
          uVar2 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_00020c18)
                            (*(undefined4 *)(pbVar16 + 0xc),*PTR_DAT_00020bfc,0);
          uVar2 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020c1c)
                            (uVar2,*(undefined4 *)(pbVar16 + -4));
          iVar13 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020c1c)(DAT_00020c20,uVar2);
          pbVar16[8] = 1;
        }
      }
      else {
        *(byte *)(int)DAT_00020b06 = *(byte *)(int)DAT_00020b06 | 4;
        Reference_ResetCaptureHistory();
      }
    }
    else {
      iVar14 = (int)DAT_ffff80ea;
      iVar13 = (int)Phase_ReferenceSourceSample;
      pbVar16[8] = 1;
      uVar10 = *(undefined4 *)PTR_Reference_FullNormalizedPeriod_00020c28;
    }
  }
  else if (bVar8 != 0) {
    if (bVar8 == 0xff) {
      bVar6 = 6;
    }
    if ((uVar7 & 0xff) == 1) {
      bVar6 = *pbVar16;
    }
    sVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00020d18)
                      (iVar12 << 0xc,
                       (int)*(short *)(PTR_Phase_ReferenceScalesQ12_00020d14 + (uint)bVar6 * 2));
    iVar14 = (int)sVar3;
  }
  iVar12 = (int)DAT_00020d06;
  *(undefined4 *)PTR_Reference_FullNormalizedPeriod_00020d1c = uVar10;
  if (iVar12 < iVar14) {
    iVar14 = iVar12;
  }
  if (iVar14 < 0) {
    iVar14 = 0;
  }
  if (pbVar16[8] == 1) {
    if (iVar12 < iVar13) {
      iVar13 = iVar12;
    }
    if (iVar13 < 0) {
      iVar13 = 0;
    }
    Phase_ReferenceSourceSample = (short)iVar13;
  }
  else {
    Phase_ReferenceSourceSample = (short)iVar14;
  }
  *(byte *)(int)DAT_00020d08 = *pbVar16;
  if ((*(byte *)(int)DAT_00020d0a & 4) == 0) {
    bVar6 = *PTR_Reference_SourceStatus_00020d20 & 0xfd;
  }
  else {
    bVar6 = *PTR_Reference_SourceStatus_00020d20 | 2;
  }
  *PTR_Reference_SourceStatus_00020d20 = bVar6;
  return iVar14;
}

