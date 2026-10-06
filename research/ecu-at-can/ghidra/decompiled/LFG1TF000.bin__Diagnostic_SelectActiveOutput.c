/* Ghidra analysis output; verify against original SH instructions. */

/* 8464 unsigned>=stock5FD64(200) clears startup latchA664; otherwise forcesA665=1. Afterward532D8
   selectsA666 or overrideA667.72 sender gate cases verified. */

void Diagnostic_SelectActiveOutput(void)

{
  undefined *puVar1;
  undefined1 uVar2;
  
  puVar1 = PTR_DAT_000532f8;
  if (*(ushort *)PTR_DAT_00053300 <= *(ushort *)PTR_DAT_000532f4) {
    *PTR_DAT_000532f8 = 0;
  }
  if (*puVar1 == '\x01') {
    uVar2 = 1;
  }
  else {
    uVar2 = Diagnostic_GetActiveOutputOverride();
  }
  *PTR_DAT_000532fc = uVar2;
  return;
}

