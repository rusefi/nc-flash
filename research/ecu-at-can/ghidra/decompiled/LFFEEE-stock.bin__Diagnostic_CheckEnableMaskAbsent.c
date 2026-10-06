/* Ghidra analysis output; verify against original SH instructions. */

/* Executed bitmask1 with groups43/44: E1AD3/E1AD4=1 returns0. Enable alone does not imply report
   admission. */

bool Diagnostic_CheckEnableMaskAbsent(uint param_1,byte param_2)

{
  return (param_2 & *(byte *)((param_1 & 0xffff) + DAT_00090374)) == 0;
}

