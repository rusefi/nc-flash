/* Ghidra analysis output; verify against original SH instructions. */

/* Writes605C+index foru16index<010D, else626E+index-010D.1536 byte/sentinelcases. Index12=606E
   requested,13=606F acceptedstate. NoEEPROMclaim. */

undefined4 StateCache_WriteByte(uint param_1,undefined1 param_2)

{
  if ((int)(param_1 & 0xffff) < (int)DAT_000245be) {
    *(undefined1 *)((param_1 & 0xffff) + DAT_000245c8) = param_2;
  }
  else {
    *(undefined1 *)((param_1 & 0xffff) + (int)DAT_000245c0 + DAT_000245cc) = param_2;
  }
  return 0;
}

