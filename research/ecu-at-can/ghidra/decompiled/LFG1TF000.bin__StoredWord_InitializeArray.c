/* Ghidra analysis output; verify against original SH instructions. */

/* Copy15words from pointers5D1C4 into616A..6186; stock allAD4E, initialized0 by15D04. Sentinels
   confirm bounds; persistence/boot scheduling unproved. */

void StoredWord_InitializeArray(void)

{
  int iVar1;
  uint uVar2;
  undefined4 *puVar3;
  
  iVar1 = DAT_000137dc;
  uVar2 = 0;
  puVar3 = (undefined4 *)PTR_PTR_000137d8;
  do {
    *(undefined2 *)(iVar1 + uVar2) = *(undefined2 *)*puVar3;
    uVar2 = uVar2 + 2;
    puVar3 = puVar3 + 1;
  } while (uVar2 < 0x1e);
  return;
}

