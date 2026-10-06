/* Ghidra analysis output; verify against original SH instructions. */

/* Protected wordread/bitclear whenR6zero,elsebitset;restoresSR. Used forTIER8 cancellation branch.
    */

void Register_UpdateMaskedWord(ushort *param_1,ushort param_2,short param_3)

{
  if (param_3 == 0) {
    *param_1 = *param_1 & ~param_2;
    return;
  }
  *param_1 = *param_1 | param_2;
  return;
}

