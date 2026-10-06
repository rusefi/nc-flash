/* Ghidra analysis output; verify against original SH instructions. */

/* Two per-index saturating counters96CF/96DF selected bycode/8086; shared971Abit1 remembers
   measured>=lower. Band path and below-upper-plus-latch path use distinct counttables.22400 cases
   and111 retainedmanager oraclechecks; tcu-ascending-phase.txt. */

undefined4 Phase_QualifyAscendingTarget(ushort param_1,short param_2,short param_3)

{
  byte bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  char cVar5;
  int iVar6;
  short sVar7;
  uint uVar8;
  undefined4 uVar9;
  byte bVar10;
  
  cVar5 = Phase_AscendingQualificationMode;
  iVar6 = (int)Phase_MeasuredSourceSample;
  bVar2 = false;
  if (((((param_2 == 2) || (param_2 == 3)) || (param_2 == 4)) ||
      (((param_2 == 0 || (param_2 == 1)) && (Phase_AscendingQualificationMode == '\x01')))) &&
     ((iVar6 < *(int *)(int)DAT_00032714 && (*(int *)(int)DAT_00032716 <= iVar6)))) {
    bVar2 = true;
  }
  if ((*(int *)(int)DAT_00032716 <= iVar6) && ((*(byte *)(int)DAT_00032718 & 2) == 0)) {
    *(byte *)(int)DAT_00032718 = *(byte *)(int)DAT_00032718 | 2;
  }
  bVar3 = false;
  if ((((param_2 == 0) || (param_2 == 1)) && (cVar5 == '\0')) && (iVar6 < *(int *)(int)DAT_00032714)
     ) {
    bVar3 = true;
  }
  sVar7 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_00032720)((int)param_2);
  bVar4 = false;
  iVar6 = (int)DAT_0003271a;
  bVar1 = *PTR_Request_EnableFlags_00032724;
  uVar8 = (uint)param_1;
  if (bVar2) {
    if ((short)(ushort)*(byte *)(iVar6 + uVar8) < DAT_0003271c) {
      *(char *)(iVar6 + uVar8) = *(char *)(iVar6 + uVar8) + '\x01';
    }
    bVar10 = PTR_Phase_AscendingBandQualificationCounts_00032728[(uint)(bVar1 & 1) + sVar7 * 2];
    if ((param_3 == 0x12) || (param_3 == 0x13)) {
      bVar10 = *PTR_Phase_AscendingOperationCount_0003272c;
    }
    if (bVar10 <= *(byte *)(iVar6 + uVar8)) {
      bVar4 = true;
    }
  }
  else {
    *(undefined1 *)(iVar6 + uVar8) = 0;
  }
  iVar6 = (int)DAT_000327f6;
  bVar2 = false;
  if (bVar3) {
    if ((short)(ushort)*(byte *)(iVar6 + uVar8) < DAT_000327f8) {
      *(char *)(iVar6 + uVar8) = *(char *)(iVar6 + uVar8) + '\x01';
    }
    if (((byte)PTR_Phase_AscendingBelowUpperCounts_00032800[(uint)(bVar1 & 1) + sVar7 * 2] <=
         *(byte *)(iVar6 + uVar8)) && ((*(byte *)(int)DAT_000327fa & 2) != 0)) {
      bVar2 = true;
    }
  }
  else {
    *(undefined1 *)(iVar6 + uVar8) = 0;
  }
  uVar9 = 0;
  if ((bVar4) || (bVar2)) {
    uVar9 = 1;
    *(byte *)(int)DAT_000327fa = *(byte *)(int)DAT_000327fa & 0xfd;
  }
  return uVar9;
}

