/* Ghidra analysis output; verify against original SH instructions. */

/* STATIC: writes04FF toFFFFF71C; ORs bit1 intoFFFFF710. Physical frequency and hardware execution
   unproved. */

void Timer_StartCMT1Lead(void)

{
  *(undefined2 *)(int)DAT_00016d44 = DAT_00016d42;
  *(ushort *)(int)DAT_00016d46 = *(ushort *)(int)DAT_00016d46 | 2;
  return;
}

