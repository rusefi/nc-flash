/* Ghidra analysis output; verify against original SH instructions. */

/* If985Czero, writes1 and clears821E. Original helper starts120call retained stock trace; admission
   never advances to2. */

void ClassAdjustment_StartAdmission(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_DAT_00036a54;
  if (*(char *)(int)DAT_00036a4c == '\0') {
    *(char *)(int)DAT_00036a4c = '\x01';
    *puVar1 = 0;
  }
  return;
}

