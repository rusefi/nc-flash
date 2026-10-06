/* Ghidra analysis output; verify against original SH instructions. */

/* Executed stock one-priority lists: node0 active head,node1 free head, four-byte nodes
   prev/next/value; sentinel7FFF. */

void RequestList_Initialize(int param_1,byte *param_2,undefined2 *param_3)

{
  uint uVar1;
  undefined1 *puVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  
  uVar4 = (uint)*param_2 + (uint)param_2[1];
  uVar5 = uVar4 + 1;
  *param_3 = *(undefined2 *)(param_2 + 2);
  for (iVar3 = 0; iVar3 < (int)(uint)*param_2; iVar3 = iVar3 + 1) {
    puVar2 = (undefined1 *)(iVar3 * 4 + param_1);
    puVar2[1] = (char)iVar3;
    *puVar2 = (char)iVar3;
    *(undefined2 *)(puVar2 + 2) = *(undefined2 *)(param_2 + 2);
  }
  uVar6 = *param_2 + 1;
  uVar1 = (uint)*param_2;
  puVar2 = (undefined1 *)(param_1 + uVar1 * 4);
  if (uVar1 < uVar5) {
    do {
      puVar2[1] = (char)uVar6;
      *puVar2 = (char)uVar4;
      *(undefined2 *)(puVar2 + 2) = *(undefined2 *)(param_2 + 2);
      uVar6 = uVar6 + 1;
      uVar4 = uVar4 + 1;
      if ((int)uVar5 <= (int)uVar6) {
        uVar6 = (uint)*param_2;
      }
      uVar1 = uVar1 + 1;
      if ((int)uVar5 <= (int)uVar4) {
        uVar4 = (uint)*param_2;
      }
      puVar2 = puVar2 + 4;
    } while ((int)uVar1 < (int)uVar5);
  }
  return;
}

