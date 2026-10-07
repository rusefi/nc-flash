/* Ghidra analysis output; verify against original SH instructions. */

/* Executed:90C6word=500 iff90B6!=1 or90A8bit7;otherwisehold. Units/cadenceunproved. */

uint Diagnostic_ConditionallyReloadTimer(void)

{
  uint uVar1;
  
  uVar1 = (uint)(byte)*PTR_Diagnostic_ServiceState_0001d8e0;
  if ((uVar1 != 1) || (uVar1 = -((((int)(char)*PTR_DAT_0001d8d4 & 0x80U) == 0) - 1), uVar1 == 1)) {
    *(undefined2 *)PTR_DAT_0001d8e4 = DAT_0001d8c4;
  }
  return uVar1;
}

