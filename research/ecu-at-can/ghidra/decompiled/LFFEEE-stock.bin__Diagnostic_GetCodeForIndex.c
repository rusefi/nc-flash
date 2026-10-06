/* Ghidra analysis output; verify against original SH instructions. */

/* Executed E1770 unsigned word lookup: index43->0704,44->0850; definitions corroborate
   clutch/neutral names. */

int Diagnostic_GetCodeForIndex(ushort param_1)

{
  return (int)*(short *)(DAT_0009036c + (uint)param_1 * 2);
}

