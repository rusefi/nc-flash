/* Ghidra analysis output; verify against original SH instructions. */

/* Set959C=1 and81D7=FF. */

void Transition_InitializeState959C(void)

{
  undefined2 uVar1;
  
  uVar1 = DAT_0002f28c;
  *(undefined1 *)(int)DAT_0002f28a = 1;
  *PTR_DAT_0002f294 = (char)uVar1;
  return;
}

