/* Ghidra analysis output; verify against original SH instructions. */

/* Channel<30 returns byte at FFFF8818+5*channel; otherwiseFF. */

int Input_GetFilteredState(byte param_1)

{
  int iVar1;
  
  iVar1 = (int)DAT_00017402;
  if (param_1 < 0x1e) {
    iVar1 = (int)(char)PTR_DAT_00017404[(uint)param_1 * 5];
  }
  return iVar1;
}

