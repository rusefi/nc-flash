/* Ghidra analysis output; verify against original SH instructions. */

/* 128 original wholeRAM/register/MMIO cases clear UBBR EC08. Zero cycle conditions prevent
   userbreak matching; UBCR0 itself enables requests. tcu-basic-hardware-startup.txt. */

void Startup_ClearUserBreakCycleConditions(void)

{
  *(undefined2 *)(int)DAT_0001451a = 0;
  return;
}

