/* Ghidra analysis output; verify against original SH instructions. */

/* Separate91B6/91C8 cache refresh only idle and4*8196>=37; age810C>=5 thenzero.9194bit0/91A6bit4
   selects80EA, otherwiseclass0zero or coefficient-converted cache. Nonnegative clamp; refresh
   precedes gate.1764 paired policy plus216 dedicated cases. See tcu-reference-policy.txt. */

int Reference_SelectAlternateCachedValue(void)

{
  bool bVar1;
  byte bVar2;
  char cVar4;
  short sVar3;
  byte bVar5;
  byte bVar6;
  int iVar7;
  
  cVar4 = (*(code *)PTR_Phase_HasPendingWork_00020f6c)();
  bVar6 = CAN231_SixStateSource;
  bVar2 = TransmissionStateClass;
  bVar1 = true;
  iVar7 = (int)*(short *)(int)DAT_00020f50;
  bVar5 = *(byte *)(int)DAT_00020f4e;
  if ((cVar4 == '\0') &&
     ((uint)(byte)*PTR_DAT_00020f74 <= (uint)(byte)*PTR_Reference_IdleSettlingTimer_00020f70 << 2))
  {
    iVar7 = (int)Phase_MeasuredSourceSample;
    bVar1 = false;
    bVar5 = CAN231_SixStateSource;
    if ((byte)*PTR_DAT_00020f7c <= (byte)*PTR_Measurement_CurrentCaptureAge_00020f78) {
      iVar7 = 0;
    }
  }
  *(short *)(int)DAT_00020f50 = (short)iVar7;
  if (((*PTR_Reference_SourceStatus_00020f80 & 1) == 0) &&
     ((*(byte *)(int)DAT_00020f52 & 0x10) == 0)) {
    if (bVar2 == 0) {
      iVar7 = 0;
    }
    else {
      if (bVar2 == 0xff) {
        bVar6 = 6;
      }
      if (bVar1) {
        bVar6 = bVar5;
      }
      sVar3 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00020f5c)
                        (iVar7 << 0xc,
                         (int)*(short *)(PTR_Phase_ReferenceScalesQ12_00020f84 + (uint)bVar6 * 2));
      iVar7 = (int)sVar3;
    }
  }
  else {
    iVar7 = (int)DAT_ffff80ea;
  }
  if (DAT_00021048 < iVar7) {
    iVar7 = (int)DAT_00021048;
  }
  if (iVar7 < 0) {
    iVar7 = 0;
  }
  *(byte *)(int)DAT_0002104a = bVar5;
  return iVar7;
}

