/* Ghidra analysis output; verify against original SH instructions. */

/* Original allocator executed for20-byte request records; first fixture allocation9F40. General
   fragmentation/exhaustion not newly verified. See tcu-request-dispatch.txt. */

undefined * Heap_AllocateRequestStorage(short param_1)

{
  int iVar1;
  undefined1 *puVar2;
  undefined *puVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  
  puVar3 = PTR_DAT_0004bff0;
  iVar6 = 0;
  iVar5 = param_1 + 3 >> 2;
  iVar4 = -1;
  for (iVar1 = 0; (iVar4 == -1 && (iVar1 != -1)); iVar1 = (int)(char)PTR_DAT_0004bff0[iVar1 * 4 + 3]
      ) {
    if ((PTR_DAT_0004bff0[iVar1 * 4] == '\0') && (iVar5 <= (char)(PTR_DAT_0004bff0 + iVar1 * 4)[1]))
    {
      iVar4 = iVar1;
    }
  }
  if (iVar4 == -1) {
    puVar3 = (undefined *)0x0;
    *(undefined1 *)(int)DAT_0004bfec = 1;
  }
  else {
    iVar1 = iVar4 * 4;
    if ((char)PTR_DAT_0004bff0[iVar1 + 1] != iVar5) {
      iVar6 = iVar4 + iVar5 + 1;
      puVar2 = PTR_DAT_0004bff0 + iVar6 * 4;
      *puVar2 = 0;
      puVar2[1] = (puVar3[iVar1 + 1] - (char)iVar5) + -1;
      puVar2[2] = (char)iVar4;
      puVar2[3] = puVar3[iVar1 + 3];
      puVar3[iVar1 + 3] = (char)iVar6;
      puVar3[iVar1 + 1] = (char)iVar5;
      if ((char)puVar2[3] != -1) {
        puVar3[(char)puVar2[3] * 4 + 2] = (char)iVar6;
      }
    }
    puVar3[iVar1] = 0xff;
    puVar3 = puVar3 + (iVar4 + 1) * 4;
    if ((int)(uint)*(byte *)(int)DAT_0004bfea < iVar6 + 1) {
      *(byte *)(int)DAT_0004bfea = (char)iVar6 + 1;
    }
  }
  return puVar3;
}

