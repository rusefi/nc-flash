/* Ghidra analysis output; verify against original SH instructions. */

/* 128 original wholeRAM/register/MMIO cases clear UBAMRH/L EC04/06. All mask bits writable; no
   break matching. tcu-basic-hardware-startup.txt. */

void Startup_ClearUserBreakMask(void)

{
  *(undefined2 *)(int)DAT_00014516 = 0;
  *(undefined2 *)(int)DAT_00014518 = 0;
  return;
}

