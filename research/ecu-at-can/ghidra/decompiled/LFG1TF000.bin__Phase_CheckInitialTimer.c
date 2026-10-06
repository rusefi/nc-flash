/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x000318d8) */
/* WARNING: Removing unreachable block (ram,0x0003194e) */
/* WARNING: Type propagation algorithm not settling */
/* Ascending: stock9-count delay (threshold18), zeroed when admitted followingascending timerready,
   or nonzerooperation with precedingphysicalslot directiondescending (evenathead).6480
   neighbor/wrap/bank cases. Descending prior1260 cases retained; tcu-ascending-phase.txt. */

bool Phase_CheckInitialTimer(short param_1)

{
  undefined1 uVar1;
  int iVar2;
  undefined *puVar3;
  short sVar5;
  char cVar6;
  int iVar4;
  ushort uVar7;
  uint uVar8;
  int *piVar9;
  int *piVar10;
  undefined4 local_3c;
  int local_38 [7];
  
  puVar3 = PTR_Phase_RecordRing_00031908;
  local_38[4] = (int)param_1;
  piVar10 = local_38 + 1;
  piVar9 = local_38 + 1;
  iVar2 = local_38[4] * 0xf;
  uVar1 = PTR_Phase_RecordRing_00031908[iVar2 + 10];
  sVar5 = ApplicationCode_SelectThresholdFamily(uVar1);
  local_38[5] = (int)(short)(param_1 - (ushort)(byte)puVar3[DAT_00031902]) + 0x10U & 0xf;
  local_38[3] = (int)(byte)puVar3[(short)(param_1 + 0xfU & 0xf) * 0xf + 10];
  uVar7 = param_1 + 0x11U & 0xf;
  local_38[2] = (int)(byte)puVar3[(short)uVar7 * 0xf + 10];
  cVar6 = Phase_ClassifyDirection(uVar1);
  if (cVar6 == '\0') {
    local_38[1] = (int)DAT_ffff808d;
    uVar8 = (uint)(byte)PTR_Phase_AscendingInitialDelays_0003190c[local_38[1] + sVar5 * 6];
    iVar4 = ApplicationCode_SelectThresholdFamily(local_38[2]);
    local_38[1] = (int)(byte)PTR_Phase_AscendingInitialDelays_0003190c[local_38[1] + iVar4 * 6];
    cVar6 = Phase_ClassifyDirection(local_38[2]);
    piVar9 = local_38 + 1;
    if ((((int)(local_38[5] + 1U) < (int)(uint)(byte)puVar3[DAT_00031904]) &&
        (piVar9 = local_38 + 1, cVar6 == '\0')) &&
       (piVar9 = local_38 + 1,
       local_38[1] << 1 <= (int)*(short *)(PTR_Phase_InitialTimers_00031910 + (short)uVar7 * 2))) {
      local_38[0] = 0;
      local_3c = DAT_00031914;
      piVar9 = &local_3c;
      sVar5 = (*(code *)PTR_FUN_0003191c)();
      uVar8 = (uint)sVar5;
    }
    cVar6 = Phase_ClassifyDirection(piVar9[2]);
    if ((puVar3[iVar2 + 0xb] == '\0') || (piVar10 = piVar9, cVar6 != '\x01')) goto LAB_0003195e;
  }
  else {
    uVar8 = (uint)(byte)PTR_Phase_DescendingInitialDelays_00031a54[(uint)DAT_ffff808c + sVar5 * 5];
    if (puVar3[iVar2 + 0xb] == '\0') goto LAB_0003195e;
  }
  piVar10[0xffffffff] = 0;
  piVar10[0xfffffffe] = DAT_00031a58;
  piVar9 = piVar10 + 0xfffffffe;
  sVar5 = (*(code *)PTR_FUN_00031a60)();
  uVar8 = (uint)sVar5;
LAB_0003195e:
  return (int)(uVar8 << 1) <= (int)*(short *)(PTR_Phase_InitialTimers_00031a64 + piVar9[3] * 2);
}

