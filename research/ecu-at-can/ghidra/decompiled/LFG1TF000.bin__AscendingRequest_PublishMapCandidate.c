/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004e06c) */
/* 4E3A8 candidate suppressed by92D5bit0 OR9410bit0clear; positive flag into+8bit80, value+4
   and4C6DA.120 gate cases and original manager/pairedECU path verified. */

void AscendingRequest_PublishMapCandidate(undefined4 param_1,int param_2)

{
  undefined *UNRECOVERED_JUMPTABLE;
  int iVar1;
  short sVar2;
  byte bVar3;
  int iVar4;
  int *piVar5;
  undefined4 uStack_18;
  undefined4 uStack_14;
  int aiStack_10 [2];
  
  piVar5 = aiStack_10;
  aiStack_10[0] = param_2;
  iVar1 = (*(code *)PTR_AscendingRequest_CalculateMapCandidate_0004e15c)(param_2);
  iVar4 = 1;
  if (((*PTR_ApplicationFaultFlags92D5_0004e160 & 1) == 1) ||
     ((*PTR_Request_EnableFlags_0004e164 & 1) == 0)) {
    uStack_14 = 0;
    uStack_18 = DAT_0004e148;
    piVar5 = &uStack_18;
    sVar2 = (*(code *)PTR_FUN_0004e150)();
    iVar1 = (int)sVar2;
  }
  if (iVar4 == 0) {
    *(undefined4 *)((int)piVar5 + -4) = 0;
    *(undefined4 *)((int)piVar5 + -8) = DAT_0004e14c;
  }
  else {
    *(undefined4 *)((int)piVar5 + -4) = 0;
    *(undefined4 *)((int)piVar5 + -8) = DAT_0004e148;
  }
  sVar2 = (*(code *)PTR_FUN_0004e150)();
  if (sVar2 < iVar1) {
    bVar3 = *(byte *)(param_2 + 8) | 0x80;
  }
  else {
    if (iVar4 == 0) {
      *(undefined4 *)((int)piVar5 + -0xc) = 0;
      *(undefined4 *)((int)piVar5 + -0x10) = DAT_0004e14c;
    }
    else {
      *(undefined4 *)((int)piVar5 + -0xc) = 0;
      *(undefined4 *)((int)piVar5 + -0x10) = DAT_0004e148;
    }
    sVar2 = (*(code *)PTR_FUN_0004e150)();
    iVar1 = (int)sVar2;
    bVar3 = *(byte *)(param_2 + 8) & 0x7f;
  }
  UNRECOVERED_JUMPTABLE = PTR_SparkRequest_SetFirstListEntry_0004e158;
  *(byte *)(param_2 + 8) = bVar3;
  *(short *)(param_2 + 4) = (short)iVar1;
                    /* WARNING: Could not recover jumptable at 0x0004e0ea. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)UNRECOVERED_JUMPTABLE)
            ((int)*(char *)(param_2 + 2),iVar1,-((((int)*(char *)(param_2 + 8) & 0x80U) == 0) - 1));
  return;
}

