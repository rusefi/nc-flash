/* Ghidra analysis output; verify against original SH instructions. */

/* OriginalwordF714=0,F71A=0. Actual1560Ccall betweenstop/configure executed; exactRAM/MMIO. No
   hardwarecounteroperation claim; tcu-cmt-configuration.txt. */

void CMT_ClearBothCounters(void)

{
  *(undefined2 *)(int)DAT_0001470c = 0;
  *(undefined2 *)(int)DAT_0001470e = 0;
  return;
}

