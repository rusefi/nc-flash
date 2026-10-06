/* Ghidra analysis output; verify against original SH instructions. */

/* Executed stock one-priority FIFO first nonsentinel; all-sentinel selects last active index, empty
   indexFF. General multi-priority behavior not verified. */

void RequestList_SelectCandidate(int param_1,byte *param_2,short *param_3,undefined1 *param_4)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  short sVar8;
  uint uVar9;
  uint uVar10;
  undefined1 uVar7;
  
  sVar8 = *(short *)(param_2 + 2);
  uVar2 = (uint)*param_2;
  uVar4 = (uint)DAT_00030582;
  uVar6 = uVar4;
  do {
    do {
      uVar2 = uVar2 - 1;
      uVar7 = (undefined1)uVar6;
      if ((int)uVar2 < 0) goto LAB_000305bc;
      uVar9 = (uint)*(byte *)(uVar2 * 4 + param_1 + 1);
    } while (uVar9 == uVar2);
    for (iVar3 = 0; uVar5 = uVar6, iVar3 < (int)(uint)param_2[1]; iVar3 = iVar3 + 1) {
      iVar1 = uVar9 * 4 + param_1;
      sVar8 = *(short *)(iVar1 + 2);
      uVar10 = (uint)*(byte *)(iVar1 + 1);
      uVar5 = uVar9;
      uVar4 = uVar9;
      if ((sVar8 != *(short *)(param_2 + 2)) || (uVar10 == uVar2)) break;
      uVar9 = uVar10;
    }
    uVar7 = (undefined1)uVar4;
    uVar6 = uVar5;
  } while (sVar8 == *(short *)(param_2 + 2));
LAB_000305bc:
  *param_3 = sVar8;
  *param_4 = uVar7;
  return;
}

