/* Ghidra analysis output; verify against original SH instructions. */

/* Five ordered up/down comparisons from8084,80EA,9B1E/9B14; writes pointer pair only.3072 direct
   cases plus retained full44CFE observation. tcu-transition-classification.txt. */

void Selection_ScanProposalThresholds(byte *param_1,undefined1 *param_2)

{
  byte bVar1;
  int iVar2;
  undefined1 uVar3;
  uint uVar4;
  
  uVar4 = (uint)Selection_ApplicationIndex;
  uVar3 = *PTR_DAT_00045154;
  iVar2 = 9;
  bVar1 = Selection_ApplicationIndex;
  do {
    if ((int)uVar4 < 5) {
      if ((*(ushort *)(PTR_Selection_ProposalThresholds_00045158 + uVar4 * 2) <= DAT_ffff80ea) &&
         (bVar1 != 5)) {
        bVar1 = bVar1 + 1;
        uVar3 = PTR_Selection_ThresholdOperations_0004515c[uVar4];
      }
    }
    else if ((DAT_ffff80ea < *(ushort *)(PTR_Selection_ProposalThresholds_00045158 + iVar2 * 2)) &&
            (bVar1 != 0)) {
      bVar1 = bVar1 - 1;
      uVar3 = PTR_Selection_ThresholdOperations_0004515c[iVar2];
    }
    iVar2 = iVar2 + -1;
    uVar4 = uVar4 + 1;
  } while (4 < iVar2);
  *param_2 = uVar3;
  *param_1 = bVar1;
  return;
}

