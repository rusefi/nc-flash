/* Ghidra analysis output; verify against original SH instructions. */

/* If9858nonzero,9889bit6 selects2 or0; zero stays0. Whole helpers and retained original sequences
   checked. */

void ClassAdjustment_QualifyUniform(void)

{
  char cVar1;
  undefined1 uVar2;
  
  uVar2 = 0;
  if (*(char *)(int)DAT_000368e0 != '\0') {
    uVar2 = 0;
    cVar1 = FUN_00036930();
    if (cVar1 == '\x01') {
      uVar2 = 2;
    }
  }
  *(undefined1 *)(int)DAT_000368e0 = uVar2;
  return;
}

