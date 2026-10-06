/* Ghidra analysis output; verify against original SH instructions. */

/* Tentative +/-one history toward accepted using signed80EE and reference9218 +/-128. Reset to
   accepted if no pending work, signed80EA<256 or8080FF.1340 cases incl signed/wrapped references;
   tcu-transition-classification.txt. */

uint Transition_AdjustReferenceHistory(uint param_1,byte param_2)

{
  int iVar1;
  short sVar2;
  char cVar4;
  short sVar3;
  int *piVar5;
  byte *pbVar6;
  char *pcVar7;
  char local_20 [8];
  undefined4 local_18;
  undefined4 local_14;
  byte local_10 [8];
  
  iVar1 = (int)Phase_MeasuredSourceSample;
  piVar5 = (int *)(PTR_Phase_ProducedReferenceWords_000476d0 + (param_1 & 0xff) * 4);
  local_10[0] = param_2;
  if ((param_1 & 0xff) < (uint)param_2) {
    local_14 = 0;
    local_18 = DAT_000476d4;
    sVar2 = (*(code *)PTR_FUN_000476d8)();
    pbVar6 = (byte *)&local_18;
    if (iVar1 <= (int)sVar2 + piVar5[1]) {
      param_1 = param_1 + 1;
      pbVar6 = (byte *)&local_18;
    }
  }
  else {
    pbVar6 = local_10;
    if ((uint)param_2 < (param_1 & 0xff)) {
      local_14 = 0;
      local_18 = DAT_000476d4;
      sVar2 = (*(code *)PTR_FUN_000476d8)();
      pbVar6 = (byte *)&local_18;
      if (*piVar5 - (int)sVar2 < iVar1) {
        param_1 = param_1 - 1;
        pbVar6 = (byte *)&local_18;
      }
    }
  }
  cVar4 = (*(code *)PTR_Phase_HasPendingWork_000476dc)();
  sVar2 = DAT_ffff80ea;
  pcVar7 = (char *)pbVar6;
  if (cVar4 != '\0') {
    *(undefined4 *)(pbVar6 + -4) = 0;
    *(undefined4 *)(pbVar6 + -8) = DAT_000476e0;
    sVar3 = (*(code *)PTR_FUN_000476d8)();
    pcVar7 = (char *)(pbVar6 + -8);
    if ((sVar3 <= sVar2) && (pcVar7 = (char *)(pbVar6 + -8), TransmissionStateClass != 0xff)) {
      return param_1;
    }
  }
  return (int)*pcVar7;
}

