/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x00021068) */
/* Six raw91A2 samples; oldest-current>=998 setsbit4. Converted-minus-raw >=128 and
   >=converted5percent resets91C6; otherwise saturating increment, uninhibited>=7 clearsbit4.1764
   policy and768 boundary cases. Actual stoppedcapture task setsbit4 using retained10865/index0;
   tcu-recovery-reference.txt. */

void Reference_UpdateDiscrepancyLatch(void)

{
  char cVar2;
  short sVar1;
  byte bVar3;
  short *psVar4;
  uint uVar5;
  byte *pbVar6;
  int iVar7;
  int iVar8;
  char cVar9;
  byte bVar11;
  byte *pbVar10;
  int *piVar12;
  undefined4 local_30;
  undefined4 local_2c;
  int local_28;
  int local_24;
  
  bVar11 = CAN231_SixStateSource;
  pbVar6 = (byte *)(int)DAT_0002104c;
  sVar1 = *(short *)PTR_Motion_PeriodDerivedValue_00021054;
  cVar9 = -(((*pbVar6 & 0x10) == 0) + -1);
  cVar2 = (*(code *)PTR_Phase_HasPendingWork_00021058)();
  local_24 = (int)sVar1;
  psVar4 = (short *)(int)DAT_00021050;
  bVar3 = *(byte *)(int)DAT_0002104e;
  local_28 = *psVar4 - local_24;
  *psVar4 = psVar4[1];
  psVar4[1] = psVar4[2];
  psVar4[2] = psVar4[3];
  psVar4[3] = psVar4[4];
  psVar4[4] = psVar4[5];
  psVar4[5] = sVar1;
  psVar4 = (short *)(int)DAT_00021052;
  iVar7 = (int)*psVar4;
  uVar5 = 1;
  piVar12 = &local_28;
  if (cVar2 == '\0') {
    iVar7 = (int)Phase_MeasuredSourceSample;
    uVar5 = 0;
    piVar12 = &local_28;
    bVar3 = bVar11;
    if ((byte)*PTR_DAT_00021060 <= (byte)*PTR_Measurement_CurrentCaptureAge_0002105c) {
      local_2c = 0;
      local_30 = DAT_00021064;
      piVar12 = &local_30;
      sVar1 = (*(code *)PTR_FUN_00021144)();
      iVar7 = (int)sVar1;
    }
  }
  *psVar4 = (short)iVar7;
  if (TransmissionStateClass == 0xff) {
    bVar11 = 6;
  }
  if ((uVar5 & 0xff) == 1) {
    bVar11 = bVar3;
  }
  sVar1 = (*(code *)PTR_FixedPoint_DivideToSignedWord_0002114c)
                    (iVar7 << 0xc,
                     (int)*(short *)(PTR_Phase_ReferenceScalesQ12_00021148 + (uint)bVar11 * 2));
  pbVar10 = (byte *)(int)DAT_0002113a;
  if ((int)*(short *)PTR_DAT_00021150 <= *piVar12) {
    *pbVar10 = 0;
    cVar9 = '\x01';
  }
  iVar8 = (int)sVar1 - piVar12[1];
  (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_00021158)
            ((int)sVar1,(int)*(short *)PTR_DAT_00021154,8);
  iVar7 = (*(code *)PTR_FUN_0002115c)();
  if ((iVar8 < *(short *)PTR_DAT_00021160) || (iVar8 < iVar7)) {
    if (*pbVar10 != DAT_0002113c) {
      *pbVar10 = *pbVar10 + 1;
    }
  }
  else {
    *pbVar10 = 0;
  }
  if ((((*PTR_Reference_SourceStatus_00021164 & 1) == 0) &&
      ((*PTR_ApplicationFaultFlags92C6_00021168 & 0x10) == 0)) &&
     ((byte)*PTR_DAT_0002116c <= *(byte *)(int)DAT_0002113a)) {
    cVar9 = '\0';
  }
  *(byte *)(int)DAT_0002113e = bVar3;
  if (cVar9 == '\0') {
    bVar3 = *pbVar6 & 0xef;
  }
  else {
    bVar3 = *pbVar6 | 0x10;
  }
  *pbVar6 = bVar3;
  return;
}

