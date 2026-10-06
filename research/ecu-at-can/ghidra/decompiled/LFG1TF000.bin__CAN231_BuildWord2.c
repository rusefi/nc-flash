/* Ghidra analysis output; verify against original SH instructions. */

/* Invalid -> FFFF; else clamp(s32[FFFFA5A8]-10,10,499). Units unresolved. */

int CAN231_BuildWord2(void)

{
  int iVar1;
  int iVar2;
  
  if ((((TransmissionStateClass == 0) || ((*PTR_DAT_00019948 & 1) == 1)) ||
      ((*PTR_ApplicationFaultFlags92C6_0001994c & 0x20) != 0)) ||
     ((*PTR_ApplicationFaultFlags92C6_0001994c & 4) != 0)) {
    iVar2 = -1;
  }
  else {
    iVar2 = (int)DAT_0001993e;
    iVar1 = *(int *)PTR_DAT_00019950 + -10;
    if ((iVar1 <= iVar2) && (iVar2 = iVar1, iVar1 < 10)) {
      iVar2 = 10;
    }
  }
  return iVar2;
}

