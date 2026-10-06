/* Ghidra analysis output; verify against original SH instructions. */

/* Increments849C and on2 calls1125C then resets0; executed. */

void Timer_ServiceTertiaryDivider(void)

{
  int iVar1;
  int *piVar2;
  
  piVar2 = (int *)(int)DAT_000112b8;
  iVar1 = *piVar2;
  *piVar2 = iVar1 + 1;
  if (iVar1 + 1 == 2) {
    Timer_IncrementTertiaryWord();
    *piVar2 = 0;
  }
  return;
}

