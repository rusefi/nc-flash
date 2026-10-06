/* Ghidra analysis output; verify against original SH instructions. */

/* Word increments unless7FFF; negatives increment normally andFFFF wraps0; boundary cases executed.
    */

void Timer_IncrementWordUntil7FFF(short *param_1)

{
  if (*param_1 != DAT_000112bc) {
    *param_1 = *param_1 + 1;
  }
  return;
}

