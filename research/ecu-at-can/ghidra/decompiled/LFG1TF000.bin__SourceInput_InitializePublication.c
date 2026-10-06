/* Ghidra analysis output; verify against original SH instructions. */

/* Zero89A4/89A5 input25 publication state; tcu-source-selection.txt. */

void SourceInput_InitializePublication(void)

{
  undefined1 *puVar1;
  
  puVar1 = (undefined1 *)(int)DAT_00017d78;
  *(undefined1 *)(int)DAT_00017d76 = 0;
  *puVar1 = 0;
  return;
}

