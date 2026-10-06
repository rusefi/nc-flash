/* Ghidra analysis output; verify against original SH instructions. */

/* Original release clears payload and coalesces free blocks; complete request lifecycles
   restore9F3C=007FFFFF. See tcu-request-dispatch.txt. */

void Heap_ReleaseRequestStorage(undefined *param_1)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  
  puVar1 = PTR_DAT_0004bff0;
  iVar2 = -1;
  for (iVar3 = 0; (iVar2 == -1 && (iVar3 != -1)); iVar3 = (int)(char)PTR_DAT_0004bff0[iVar3 * 4 + 3]
      ) {
    if ((PTR_DAT_0004bff0[iVar3 * 4] == -1) && (PTR_DAT_0004bff0 + (iVar3 + 1) * 4 == param_1)) {
      iVar2 = iVar3;
    }
  }
  if (iVar2 != -1) {
    PTR_DAT_0004bff0[iVar2 * 4] = 0;
    for (iVar3 = 1; iVar3 <= (char)puVar1[iVar2 * 4 + 1]; iVar3 = iVar3 + 1) {
      *(undefined4 *)(puVar1 + (iVar3 + iVar2) * 4) = 0;
    }
    iVar3 = (int)(char)puVar1[iVar2 * 4 + 3];
    if ((iVar3 != -1) && (puVar1[iVar3 * 4] == '\0')) {
      puVar1[iVar2 * 4 + 1] = puVar1[iVar2 * 4 + 1] + puVar1[iVar3 * 4 + 1] + '\x01';
      puVar1[iVar2 * 4 + 3] = puVar1[iVar3 * 4 + 3];
      if ((char)puVar1[iVar3 * 4 + 3] != -1) {
        puVar1[(char)puVar1[iVar3 * 4 + 3] * 4 + 2] = (char)iVar2;
      }
      *(undefined4 *)(puVar1 + iVar3 * 4) = 0;
    }
    iVar3 = (int)(char)puVar1[iVar2 * 4 + 2];
    if ((iVar3 != -1) && (puVar1[iVar3 * 4] == '\0')) {
      puVar1[iVar3 * 4 + 1] = puVar1[iVar3 * 4 + 1] + puVar1[iVar2 * 4 + 1] + '\x01';
      puVar1[iVar3 * 4 + 3] = puVar1[iVar2 * 4 + 3];
      if ((char)puVar1[iVar2 * 4 + 3] != -1) {
        puVar1[(char)puVar1[iVar2 * 4 + 3] * 4 + 2] = puVar1[iVar2 * 4 + 2];
      }
      *(undefined4 *)(puVar1 + iVar2 * 4) = 0;
    }
  }
  return;
}

