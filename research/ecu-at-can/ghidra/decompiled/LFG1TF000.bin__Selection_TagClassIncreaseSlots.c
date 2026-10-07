/* Ghidra analysis output; verify against original SH instructions. */

/* If0<signedprevious<signedcurrent, tags upper indicesprevious-1..current-2 operation4/kind7
   without pointer changes. Can tag primary-restored curves on increase to6. Full4530C base rebuild
   removes transient tags on next unchanged-class call. */

void Selection_TagClassIncreaseSlots(char param_1,char param_2)

{
  undefined *puVar1;
  undefined *puVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  
  puVar2 = PTR_Selection_ThresholdOperations_00047408;
  puVar1 = PTR_DAT_00047404;
  iVar5 = (int)param_1;
  if (((0 < iVar5) && ('\0' < param_2)) && (iVar5 < param_2)) {
    iVar4 = 0;
    iVar5 = param_2 - iVar5;
    iVar3 = (-(6 - param_2) - iVar5) + 5;
    if (0 < iVar5) {
      do {
        puVar2[iVar3] = 4;
        iVar4 = iVar4 + 1;
        puVar1[iVar3] = 7;
        iVar3 = iVar3 + 1;
      } while (iVar4 < iVar5);
    }
  }
  return;
}

