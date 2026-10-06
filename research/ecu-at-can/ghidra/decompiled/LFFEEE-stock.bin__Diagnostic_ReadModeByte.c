/* Ghidra analysis output; verify against original SH instructions. */

/* Index0 highbyteof99D8;index1 lowbytewhenconsumertruncates;otherindex0. Executed9A43A modepair
   checks. */

uint Diagnostic_ReadModeByte(char param_1)

{
  uint uVar1;
  
  uVar1 = (uint)(short)*(ushort *)PTR_DAT_00091764;
  if (param_1 == '\0') {
    uVar1 = (uint)(*(ushort *)PTR_DAT_00091764 >> 8);
  }
  else if (param_1 != '\x01') {
    uVar1 = 0;
  }
  return uVar1;
}

