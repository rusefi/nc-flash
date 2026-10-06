/* Ghidra analysis output; verify against original SH instructions. */

/* Real3206E lookup then signedbyte95E1+15*index,FF ifabsent. Used in4CD18 activationgate;
   phase-record production not establishedhere. See tcu-request-dispatch.txt. */

int ApplicationPhase_ReadForCode(void)

{
  short sVar1;
  int iVar2;
  
  sVar1 = ApplicationPhase_FindCode();
  iVar2 = -1;
  if (-1 < sVar1) {
    iVar2 = (int)(char)PTR_DAT_00031704[sVar1 * 0xf];
  }
  return iVar2;
}

