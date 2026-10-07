/* Ghidra analysis output; verify against original SH instructions. */

/* 128 original wholeRAM/register/MMIO cases clear UBARH/L EC00/02. Bounded configuration only; no
   break matching/interrupts. tcu-basic-hardware-startup.txt. */

void Startup_ClearUserBreakAddress(void)

{
  *(undefined2 *)(int)DAT_00014512 = 0;
  *(undefined2 *)(int)DAT_00014514 = 0;
  return;
}

