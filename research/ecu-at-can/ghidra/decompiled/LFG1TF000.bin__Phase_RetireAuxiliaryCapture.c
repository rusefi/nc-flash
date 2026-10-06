/* Ghidra analysis output; verify against original SH instructions. */

/* Retirement callback3; restore nonzero95D0 to1. Original body executes. */

void Phase_RetireAuxiliaryCapture(void)

{
  if (*(char *)(int)DAT_00031178 != '\0') {
    *(char *)(int)DAT_00031178 = '\x01';
  }
  return;
}

