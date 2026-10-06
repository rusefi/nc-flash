/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004d0d4) */
/* WARNING: Removing unreachable block (ram,0x0004d050) */
/* WARNING: Removing unreachable block (ram,0x0004d02e) */
/* WARNING: Removing unreachable block (ram,0x0004d0ae) */
/* WARNING: Removing unreachable block (ram,0x0004d0fa) */
/* Executed4D554 components,subtract then signed16lower clamp4D274;92D5bit2 or9410bit1clear
   forceszero. Store+4,set+18bit80iffpositive,real4C6DA publish. Stock offset curves zero. */

void SparkRequest_UpdateFirstListFromMaps(undefined4 param_1,int param_2)

{
  short sVar1;
  undefined2 uVar2;
  int *piVar3;
  undefined4 *puVar4;
  int aiStack_40 [7];
  int iStack_24;
  int iStack_20;
  undefined4 uStack_1c;
  int iStack_10;
  
  uStack_1c = 0;
  iStack_20 = DAT_0004d24c;
  iStack_10 = param_2;
  sVar1 = (*(code *)PTR_FUN_0004d254)();
  iStack_20 = (int)sVar1;
  iStack_24 = 0;
  aiStack_40[6] = DAT_0004d24c;
  piVar3 = aiStack_40 + 6;
  sVar1 = (*(code *)PTR_FUN_0004d254)();
  iStack_24 = (int)sVar1;
  (*(code *)PTR_SparkRequest_CalculateFirstListMapComponents_0004d258)
            (aiStack_40 + 6,&iStack_24,iStack_20);
  aiStack_40[6] = aiStack_40[6] - iStack_24;
  sVar1 = SparkRequest_ClampSignedNonnegative(aiStack_40[6]);
  aiStack_40[6] = (int)sVar1;
  if (((*PTR_ApplicationFaultFlags92D5_0004d25c & 4) != 0) ||
     ((*PTR_Request_EnableFlags_0004d260 & 2) == 0)) {
    aiStack_40[5] = 0;
    aiStack_40[4] = DAT_0004d24c;
    piVar3 = aiStack_40 + 4;
    sVar1 = (*(code *)PTR_FUN_0004d254)();
    aiStack_40[4] = (int)sVar1;
  }
  *(undefined2 *)(param_2 + 4) = *(undefined2 *)((int)piVar3 + 2);
  *(undefined4 *)((int)piVar3 + -4) = 0;
  *(int *)((int)piVar3 + -8) = DAT_0004d24c;
  puVar4 = (undefined4 *)((int)piVar3 + -8);
  sVar1 = (*(code *)PTR_FUN_0004d254)();
  if (sVar1 < *(short *)(param_2 + 4)) {
    *(byte *)(param_2 + 0x12) = *(byte *)(param_2 + 0x12) | 0x80;
  }
  else {
    *(undefined4 *)((int)piVar3 + -0xc) = 0;
    *(int *)((int)piVar3 + -0x10) = DAT_0004d24c;
    puVar4 = (undefined4 *)((int)piVar3 + -0x10);
    uVar2 = (*(code *)PTR_FUN_0004d254)();
    *(undefined2 *)(param_2 + 4) = uVar2;
    *(byte *)(param_2 + 0x12) = *(byte *)(param_2 + 0x12) & 0x7f;
  }
  (*(code *)PTR_SparkRequest_SetFirstListEntry_0004d264)
            ((int)*(char *)(param_2 + 2),*puVar4,
             -((((int)*(char *)(param_2 + 0x12) & 0x80U) == 0) - 1));
  return;
}

