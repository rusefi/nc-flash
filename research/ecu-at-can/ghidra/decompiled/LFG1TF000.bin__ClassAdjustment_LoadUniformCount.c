/* Ghidra analysis output; verify against original SH instructions. */

/* Original2457A cacheindex3 ->word985A. Executed alongside count helper; unrelated
   storedclasses0..2 remain unchanged. */

void ClassAdjustment_LoadUniformCount(void)

{
  undefined2 uVar1;
  
  uVar1 = (*DAT_000368e4)(3);
  *(undefined2 *)(int)DAT_000368de = uVar1;
  return;
}

