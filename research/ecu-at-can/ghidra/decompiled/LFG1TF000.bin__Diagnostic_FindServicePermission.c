/* Ghidra analysis output; verify against original SH instructions. */

/* Executed lowbyteargument search22 two-byte rows5EB28;returnsrowindex or22. */

uint Diagnostic_FindServicePermission(char param_1)

{
  bool bVar1;
  uint uVar2;
  
  uVar2 = 0;
  bVar1 = false;
  while ((!bVar1 && ((uVar2 & 0xff) < 0x16))) {
    if (param_1 == PTR_DAT_00056104[(uVar2 & 0xff) * 2]) {
      bVar1 = true;
    }
    else {
      uVar2 = uVar2 + 1;
    }
  }
  return uVar2;
}

