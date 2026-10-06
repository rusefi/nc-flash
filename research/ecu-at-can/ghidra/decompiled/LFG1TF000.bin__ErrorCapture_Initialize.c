/* Ghidra analysis output; verify against original SH instructions. */

/* Sets95C2=1; real expanded initialization enables capture30B28. Other capture fields retained. */

void ErrorCapture_Initialize(void)

{
  *(undefined1 *)(int)DAT_00030c0a = 1;
  return;
}

