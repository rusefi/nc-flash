/* Ghidra analysis output; verify against original SH instructions. */

/* Builds bytes4..7;9454 ->byte7 bit5. Executed byte4 signed80EE/96 clamp; speedA5AC cap30000,
   change limit1000, offset10000; fault92C6bit2 ->FFFF/reset limiter. */

void CAN216_BuildStatus(char param_1)

{
  undefined *puVar1;
  short sVar2;
  undefined1 *puVar3;
  int iVar4;
  undefined2 *puVar5;
  short sVar6;
  uint uVar7;
  uint uVar8;
  char cVar9;
  char *pcVar10;
  ushort *puVar11;
  int unaff_r10;
  uint unaff_r11;
  undefined *unaff_r12;
  int unaff_r13;
  char local_30;
  char cStack_2c;
  char cStack_28;
  char cStack_24;
  
  cVar9 = (char)DAT_00019014;
  pcVar10 = (char *)(int)DAT_00019010;
  puVar11 = (ushort *)(int)DAT_00019012;
  if (param_1 == '\0') {
    param_1 = '\0';
    unaff_r12 = (undefined *)(int)DAT_00019016;
    unaff_r11 = 0;
    unaff_r13 = 0;
    unaff_r10 = 0;
    cStack_2c = '\0';
    cStack_28 = '\0';
    cStack_24 = '\0';
    local_30 = '\0';
    *puVar11 = 0;
    *pcVar10 = '\0';
    goto LAB_000190de;
  }
  if (param_1 == '\x10') {
    unaff_r11 = 0;
    unaff_r13 = 0;
    unaff_r10 = 0;
    cStack_2c = '\0';
    cStack_28 = '\0';
    cStack_24 = '\0';
    local_30 = '\0';
    unaff_r12 = PTR_DAT_0001901c;
    param_1 = cVar9;
    goto LAB_000190de;
  }
  if (param_1 != '\x01') goto LAB_000190de;
  unaff_r12 = PTR_DAT_0001901c;
  if ((*PTR_ApplicationFaultFlags92C6_0001902c & 0x20) == 0) {
    sVar2 = (*(code *)PTR_FUN_00019070)();
    sVar6 = DAT_0001906c;
    if ((sVar2 <= DAT_0001906c) && (sVar6 = sVar2, sVar2 < 0)) {
      sVar6 = 0;
    }
    cVar9 = (char)sVar6;
  }
  if ((*PTR_ApplicationFaultFlags92C6_00019074 & 4) == 0) {
    uVar7 = (int)(short)*(ushort *)PTR_CAN216_SpeedCandidate_00019174;
    if ((int)DAT_00019156 < (int)(uint)*(ushort *)PTR_CAN216_SpeedCandidate_00019174) {
      uVar7 = (int)DAT_00019156;
    }
    if (*pcVar10 != '\0') {
      uVar8 = (uint)*puVar11 + (int)DAT_00019158;
      if ((int)(uVar7 & 0xffff) <= (int)uVar8) {
        uVar8 = (uint)*puVar11 + (int)DAT_0001915a;
        if ((int)uVar8 < 0) {
          uVar8 = 0;
        }
        if ((int)uVar8 <= (int)(uVar7 & 0xffff)) goto LAB_000190ae;
      }
      uVar7 = uVar8;
    }
LAB_000190ae:
    iVar4 = (int)DAT_0001915c;
    *puVar11 = (ushort)uVar7;
    *pcVar10 = '\x01';
    unaff_r12 = (undefined *)(uVar7 + iVar4);
  }
  else {
    *puVar11 = (ushort)unaff_r12;
    *pcVar10 = '\0';
  }
  unaff_r13 = (int)(char)*PTR_DAT_0001917c;
  unaff_r11 = (int)(char)*PTR_DAT_00019178 & 1;
  unaff_r10 = (int)(char)*PTR_CAN216_CylinderCutRequestSource_00019180;
  cStack_2c = '\0';
  cStack_28 = '\0';
  cStack_24 = '\0';
  local_30 = *(char *)(int)DAT_0001915e;
  param_1 = cVar9;
LAB_000190de:
  puVar5 = (undefined2 *)(int)DAT_00019162;
  *(char *)(int)DAT_00019160 = param_1;
  *puVar5 = (short)unaff_r12;
  puVar3 = (undefined1 *)(int)DAT_00019166;
  *(char *)(int)DAT_00019164 = (char)unaff_r11;
  *puVar3 = (char)unaff_r13;
  pcVar10 = (char *)(int)DAT_0001916a;
  *(char *)(int)DAT_00019168 = (char)unaff_r10;
  *pcVar10 = cStack_2c;
  pcVar10 = (char *)(int)DAT_0001916e;
  *(char *)(int)DAT_0001916c = cStack_28;
  *pcVar10 = cStack_24;
  puVar1 = PTR_FUN_00019184;
  *(char *)(int)DAT_00019170 = local_30;
  (*(code *)puVar1)();
  (*(code *)PTR_CAN216_SetWord5_00019188)(unaff_r12);
  (*(code *)PTR_FUN_0001918c)(unaff_r11);
  (*(code *)PTR_FUN_00019190)(unaff_r13);
  (*(code *)PTR_FUN_00019194)(unaff_r10);
  (*(code *)PTR_FUN_00019198)((int)cStack_2c);
  (*(code *)PTR_FUN_0001919c)((int)cStack_28);
  (*(code *)PTR_FUN_000191a0)((int)cStack_24);
                    /* WARNING: Could not recover jumptable at 0x00019152. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_000191a4)((int)local_30);
  return;
}

