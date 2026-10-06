/* Ghidra analysis output; verify against original SH instructions. */

/* Generic event/state dispatcher executed forB038: guard before state predicate, then handler
   forselected state; storetransition afterward. Events1/4 run state handler, release state1 skips
   numeric callback. See tcu-request-dispatch.txt. */

void CallbackState_Dispatch(short param_1,undefined4 *param_2,int *param_3)

{
  char cVar1;
  short sVar2;
  int iVar3;
  char *pcVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  int unaff_r12;
  char *pcVar8;
  
  iVar7 = -1;
  if ((param_1 == 1) || (param_1 == 2)) {
    unaff_r12 = (int)*(char *)(param_2 + 1);
  }
  else if (param_1 == 3) {
    unaff_r12 = (int)*(char *)(param_2 + 1);
  }
  else {
    if (param_1 != 4) {
      pcVar8 = (char *)0x0;
      goto LAB_0002ff44;
    }
    unaff_r12 = (int)*(char *)(param_2 + 1);
  }
  pcVar8 = (char *)*param_2;
LAB_0002ff44:
  pcVar4 = (char *)param_3[5];
  if (pcVar8 != (char *)0x0) {
    pcVar4 = pcVar8;
  }
  cVar1 = *(char *)param_3[5];
  if (param_1 == 0) {
    if (*(int *)*param_3 != 0) {
      sVar2 = (**(code **)*param_3)(0,0,0);
      iVar7 = (int)sVar2;
    }
  }
  else if (param_1 == 1) {
    if ((cVar1 != '\0') && (*(int *)(*param_3 + 4) != 0)) {
      if (pcVar8 != (char *)0x0) {
        *pcVar4 = cVar1;
      }
      sVar2 = (**(code **)(*param_3 + 4))
                        (unaff_r12,*(undefined1 *)((int)param_2 + 5),
                         *(undefined1 *)((int)param_2 + 6),pcVar8);
      iVar7 = (int)sVar2;
    }
  }
  else if (param_1 == 2) {
    if ((cVar1 != '\0') && (*(int *)(*param_3 + 8) != 0)) {
      sVar2 = (**(code **)(*param_3 + 8))(unaff_r12,*(undefined1 *)((int)param_2 + 5),0,pcVar8);
      iVar7 = (int)sVar2;
    }
  }
  else if (param_1 == 3) {
    if ((cVar1 != '\0') && (*(int *)(*param_3 + 0xc) != 0)) {
      sVar2 = (**(code **)(*param_3 + 0xc))(unaff_r12,*(undefined1 *)((int)param_2 + 5),0,pcVar8);
      iVar7 = (int)sVar2;
    }
  }
  else if ((param_1 == 4) && (cVar1 != '\0')) {
    for (iVar6 = 0; iVar6 < (int)(uint)*(byte *)((int)param_3 + 0x1a); iVar6 = iVar6 + 1) {
      if (*(int *)(iVar6 * 4 + param_3[1]) != 0) {
        (**(code **)(iVar6 * 4 + param_3[1]))(unaff_r12,pcVar8);
      }
    }
    for (iVar6 = 0; iVar3 = iVar7, iVar6 < (int)(uint)*(byte *)((int)param_3 + 0x19);
        iVar6 = iVar6 + 1) {
      iVar5 = iVar6 * 8;
      if ((*(int *)(param_3[2] + iVar5) != 0) &&
         (sVar2 = (**(code **)(param_3[2] + iVar5))(unaff_r12,pcVar8), sVar2 != 0)) {
        iVar3 = -1;
        if (*(int *)(param_3[2] + iVar5 + 4) != 0) {
          sVar2 = (**(code **)(param_3[2] + iVar5 + 4))(unaff_r12,pcVar8);
          iVar3 = (int)sVar2;
        }
        if (iVar3 != -1) break;
      }
    }
    iVar7 = iVar3;
    iVar6 = (int)*pcVar4;
    if ((((iVar7 == -1) && (1 < iVar6)) && (iVar6 < (int)(uint)*(byte *)(param_3 + 6))) &&
       ((*(int *)((iVar6 + -2) * 8 + param_3[3]) != 0 &&
        (*(int *)((iVar6 + -2) * 8 + param_3[3] + 4) != 0)))) {
      iVar6 = (iVar6 + -2) * 8;
      sVar2 = (**(code **)(param_3[3] + iVar6))(unaff_r12,pcVar8);
      if (sVar2 != 0) {
        sVar2 = (**(code **)(param_3[3] + iVar6 + 4))(unaff_r12,pcVar8);
        iVar7 = (int)sVar2;
      }
    }
  }
  if ((param_1 == 1) || (param_1 == 4)) {
    iVar6 = iVar7;
    if (iVar7 == -1) {
      iVar6 = (int)*pcVar4;
    }
    if (((1 < iVar6) && (iVar6 < (int)(uint)*(byte *)(param_3 + 6))) &&
       (*(int *)((iVar6 + -2) * 4 + param_3[4]) != 0)) {
      (**(code **)((iVar6 + -2) * 4 + param_3[4]))(unaff_r12,pcVar8);
    }
  }
  if (iVar7 != -1) {
    *pcVar4 = (char)iVar7;
  }
  return;
}

