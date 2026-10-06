/* Ghidra analysis output; verify against original SH instructions. */

/* Counter96EF[index] saturates255 on qualified sample, else resets. Band
   lower-inclusive/upper-exclusive; code8/9/10 low-value alternative and code11 lower-only/bypass.
   Threshold70B14 family/gate9410bit1, operation5 code8/9 override70B22. See tcu-phase-policy.txt.
    */

undefined1 Phase_QualifyDescendingTarget(ushort param_1,short param_2)

{
  bool bVar1;
  bool bVar2;
  undefined1 uVar3;
  int iVar4;
  short sVar5;
  char cVar6;
  byte *pbVar7;
  byte bVar8;
  byte bVar9;
  
  iVar4 = (int)Phase_MeasuredSourceSample;
  bVar1 = false;
  bVar2 = false;
  if (param_2 == 0xb) {
    if ((*(int *)(int)DAT_000327fc <= iVar4) &&
       (bVar1 = true,
       *(short *)PTR_Phase_Code11BypassThreshold_00032808 <=
       *(short *)PTR_TransitionProgress_AccumulatorC_00032804)) {
      bVar2 = true;
    }
  }
  else if (((iVar4 < *(int *)(int)DAT_000328dc) && (*(int *)(int)DAT_000327fc <= iVar4)) ||
          ((param_2 != 7 &&
           (((param_2 != 6 && (param_2 != 5)) && (iVar4 < *(short *)PTR_DAT_000328e4)))))) {
    bVar1 = true;
  }
  sVar5 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_000328e8)((int)param_2);
  bVar9 = -(((*PTR_Request_EnableFlags_000328ec & 2) == 0) + -1);
  cVar6 = (*(code *)PTR_Selection_ReadOperation_000328f0)();
  iVar4 = (int)DAT_000328de;
  uVar3 = 0;
  pbVar7 = (byte *)((uint)param_1 + iVar4);
  if (bVar1) {
    if ((short)(ushort)*pbVar7 < DAT_000328e0) {
      *pbVar7 = *pbVar7 + 1;
    }
    bVar8 = PTR_Phase_DescendingQualificationCounts_000328f4[(uint)bVar9 + sVar5 * 2];
    if (((cVar6 == '\x05') && (bVar9 == 1)) && ((param_2 == 9 || (param_2 == 8)))) {
      bVar8 = PTR_Phase_Operation5QualificationCounts_000328f8[param_2 == 9];
    }
    if ((bVar8 <= *(byte *)(iVar4 + (uint)param_1)) || (bVar2)) {
      uVar3 = 1;
    }
  }
  else {
    *pbVar7 = 0;
  }
  return uVar3;
}

