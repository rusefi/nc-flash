/* Ghidra analysis output; verify against original SH instructions. */

/* Retirement callback1; if95C2 nonzero and code matches u16 95C4, restore95C2=1. Original callback
   body executes in retirement fixtures. */

void Phase_RetireCapturedSource(short param_1)

{
  if ((*(char *)(int)DAT_00030c0a != '\0') && (*(short *)(int)DAT_00030c0c == param_1)) {
    *(char *)(int)DAT_00030c0a = '\x01';
  }
  return;
}

