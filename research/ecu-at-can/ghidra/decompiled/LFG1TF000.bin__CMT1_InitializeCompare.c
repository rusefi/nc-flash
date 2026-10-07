/* Ghidra analysis output; verify against original SH instructions. */

/* Original16CE4 writes04FF toFFFFF71C thenORbit1 intoFFFFF710.256lowbyte samples
   verifyorderedMMIO/unchangedRAM; full12374 initadds256cases. No hardwareclockrate proof;
   tcu-cmt1-delivery.txt. */

void CMT1_InitializeCompare(void)

{
  *(undefined2 *)(int)DAT_00016d44 = DAT_00016d42;
  *(ushort *)(int)DAT_00016d46 = *(ushort *)(int)DAT_00016d46 | 2;
  return;
}

