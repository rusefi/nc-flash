/* Ghidra analysis output; verify against original SH instructions. */

/* 128 prefix cases through14458 clearUBCR EC0A;256 fullfunction cases also write
   BCR1EC20=000F/BCR2EC22=0007. WholeRAM/register/MMIO checks; no externalbus cycles.
   tcu-basic-hardware-startup.txt. */

void Startup_ConfigureUserBreakAndBus(void)

{
  *(undefined2 *)(int)DAT_0001451c = 0;
  *(undefined2 *)(int)DAT_0001451e = 0xf;
  *(undefined2 *)(int)DAT_00014520 = 7;
  return;
}

