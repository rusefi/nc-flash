/* Ghidra analysis output; verify against original SH instructions. */

/* Group0..2 from9C9E otherwise0. Halfopen signed16(80EA-9CA0) admission; signed9C9C-centered
   error/division update, deadband,clamp[-512,192/256/320]
   ->storedindices6/7/8.13098cases,18retained,24consumerreplays. 49B08 caller now executed;
   scheduling unproved. See tcu-adjustment-lifecycle.txt. */

void StoredAdjustment_UpdateFromCapturedInputs(void)

{
  byte bVar1;
  short sVar3;
  short sVar4;
  undefined *puVar2;
  short sVar5;
  int iVar6;
  int iVar7;
  short sVar8;
  int iVar9;
  uint uVar10;
  
  sVar5 = *(short *)(int)DAT_0004a0f4;
  sVar3 = DAT_ffff80ea - *(short *)(int)DAT_0004a0f6;
  uVar10 = 0;
  if (*(ushort *)(int)DAT_0004a0f8 < 3) {
    uVar10 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_0004a0fc)();
  }
  if (((short)((ushort)(byte)PTR_DAT_0004a100[uVar10 & 0xff] << 6) <= sVar3) &&
     (sVar3 < (short)((ushort)(byte)PTR_DAT_0004a104[uVar10 & 0xff] << 6))) {
    bVar1 = PTR_DAT_0004a108[uVar10 & 0xff];
    iVar7 = (uVar10 & 0xff) * 2;
    sVar3 = *(short *)(PTR_PTR_0004a110 + iVar7);
    sVar8 = sVar5 + (ushort)(byte)PTR_DAT_0004a10c[uVar10 & 0xff] * -0x40;
    sVar4 = (*(code *)PTR_StoredWord_ReadSignedAdjustment_0004a114)((int)sVar3);
    iVar9 = (int)sVar4;
    puVar2 = PTR_DAT_0004a120;
    if (((short)((ushort)bVar1 << 6) <= sVar5) ||
       ((((*PTR_DAT_0004a11c & 1) == 1 ||
         (iVar6 = (uVar10 & 0xff) * 2, puVar2 = PTR_DAT_0004a12c,
         sVar8 < *(short *)(PTR_DAT_0004a124 + iVar6))) ||
        (*(short *)(PTR_DAT_0004a128 + iVar6) <= sVar8)))) {
      sVar5 = (*(code *)PTR_FixedPoint_DivideToSignedWord_0004a130)
                        ((int)(short)((ushort)(byte)puVar2[uVar10 & 0xff] << 4) * (int)sVar8,
                         (int)*(short *)(PTR_Phase_ReferenceScalesQ12_0004a118 + iVar7));
      iVar9 = iVar9 - sVar5;
    }
    iVar7 = (uVar10 & 0xff) * 2;
    if (*(short *)(PTR_DAT_0004a134 + iVar7) < iVar9) {
      iVar9 = (int)*(short *)(PTR_DAT_0004a134 + iVar7);
    }
    if (iVar9 < *(short *)(PTR_DAT_0004a138 + iVar7)) {
      iVar9 = (int)*(short *)(PTR_DAT_0004a138 + iVar7);
    }
    (*(code *)PTR_StoredWord_WriteAdjustment_0004a13c)((int)sVar3,iVar9);
  }
  return;
}

