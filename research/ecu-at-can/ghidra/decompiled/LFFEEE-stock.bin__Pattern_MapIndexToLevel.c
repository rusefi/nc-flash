/* Ghidra analysis output; verify against original SH instructions. */

/* Index0 returns0;else clamp4 and read C4FD4 if6542==0,otherwiseC4FD8. Executed within40660. */

int Pattern_MapIndexToLevel(uint param_1)

{
  undefined *puVar1;
  int iVar2;
  
  if ((param_1 & 0xff) == 0) {
    iVar2 = 0;
  }
  else {
    if ((uint)(byte)*PTR_DAT_0004638c < (param_1 & 0xff)) {
      param_1 = (int)(char)*PTR_DAT_0004638c;
    }
    puVar1 = PTR_DAT_00046398;
    if (*PTR_DAT_00046390 == '\0') {
      puVar1 = PTR_DAT_00046394;
    }
    iVar2 = (int)(char)puVar1[param_1 + (int)DAT_00046360 & 0xff];
  }
  return iVar2;
}

