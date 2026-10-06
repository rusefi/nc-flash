/* Ghidra analysis output; verify against original SH instructions. */

/* DescriptorAD46C maskE0 gates960C mode; mode0 mirrors input to9638, mode7 returns9638==1, other
   modes preserve input. See warning-status.txt. */

uint Status_OverrideMILRequest(uint param_1)

{
  int iVar1;
  
  iVar1 = (int)DAT_0008b9b2;
  if ((*PTR_DAT_0008b9bc & PTR_DAT_0008b9b8[iVar1 + 8]) == 0) {
    **(undefined1 **)(PTR_DAT_0008b9b8 + iVar1 + 0xc) = 0;
  }
  if (**(char **)(PTR_PTR_0008b9c0 + iVar1) == '\0') {
    PTR_DAT_0008b9c4[0x14] = (param_1 & 0xff) == 1;
  }
  else if ((**(char **)(PTR_PTR_0008b9c0 + iVar1) == '\a') &&
          (param_1 = 0, PTR_DAT_0008b9c4[0x14] == '\x01')) {
    param_1 = 1;
  }
  return param_1;
}

