/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned word increments unlessFFFF; boundary cases executed. */

void Timer_IncrementWordUntilFFFF(ushort *param_1)

{
  if ((undefined *)(uint)*param_1 != PTR_DAT_000112c8) {
    *param_1 = *param_1 + 1;
  }
  return;
}

