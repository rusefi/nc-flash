/* Ghidra analysis output; verify against original SH instructions. */

/* All256 byte inputs executed; increments unlessFF. */

void Timer_IncrementByteUntilFF(byte *param_1)

{
  if (*param_1 != DAT_000112ba) {
    *param_1 = *param_1 + 1;
  }
  return;
}

