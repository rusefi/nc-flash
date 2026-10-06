/* Ghidra analysis output; verify against original SH instructions. */

/* Retirement callback2; if95BE nonzero and signed code matches95BF, restore95BE=1. Original body
   executes. */

void Phase_RetireDifferenceCapture(char param_1)

{
  if ((*(char *)(int)DAT_00030b12 != '\0') && (*(char *)(int)DAT_00030b14 == param_1)) {
    *(char *)(int)DAT_00030b12 = '\x01';
  }
  return;
}

