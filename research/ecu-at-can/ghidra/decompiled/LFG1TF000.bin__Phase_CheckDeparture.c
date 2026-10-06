/* Ghidra analysis output; verify against original SH instructions. */

/* 92C6 bits1/4 inhibit. After317E4 ready: ascending requires measured STRICTLY<from-reference-128;
   descending measured>=from-reference+128.1575 ascending boundary/flag cases; phase0 can instead
   advance through targetqualifier. */

undefined4 Phase_CheckDeparture(undefined2 param_1,uint param_2)

{
  byte bVar1;
  char cVar4;
  short sVar3;
  int iVar2;
  char cVar5;
  int iVar6;
  undefined4 uVar7;
  
  bVar1 = PTR_DAT_00032528[param_2 & 0xffff];
  cVar4 = (*(code *)PTR_Phase_ClassifyDirection_0003252c)(param_2);
  sVar3 = (*(code *)PTR_ApplicationCode_SelectThresholdFamily_00032530)(param_2);
  iVar2 = (int)Phase_MeasuredSourceSample;
  iVar6 = *(int *)(PTR_Phase_ProducedReferenceWords_00032534 + (uint)bVar1 * 4);
  uVar7 = 0xffffffff;
  if (((*PTR_ApplicationFaultFlags92C6_00032538 & 0x10) == 0) &&
     ((*PTR_ApplicationFaultFlags92C6_00032538 & 2) == 0)) {
    cVar5 = (*(code *)PTR_Phase_CheckInitialTimer_0003253c)(param_1);
    if (cVar4 == '\0') {
      if (cVar5 != '\x01') {
        return 0xffffffff;
      }
      if (iVar6 - *(short *)(PTR_Phase_DepartureThresholds_00032540 + sVar3 * 2) <= iVar2) {
        return 0xffffffff;
      }
    }
    else {
      if (cVar5 != '\x01') {
        return 0xffffffff;
      }
      if (iVar2 < *(short *)(PTR_Phase_DepartureThresholds_00032540 + (sVar3 + 5) * 2) + iVar6) {
        return 0xffffffff;
      }
    }
    uVar7 = 1;
  }
  return uVar7;
}

