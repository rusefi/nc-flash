/* Ghidra analysis output; verify against original SH instructions. */

/* 256 cases: wordF716=624, wordF710=old|1, exactorderedMMIO andunchangedRAM. Clockperiod unproved;
   tcu-cmt0-interrupt.txt. */

void CMT0_InitializeCompare(void)

{
  *(undefined2 *)(int)DAT_00016dbc = DAT_00016dba;
  *(ushort *)(int)DAT_00016dbe = *(ushort *)(int)DAT_00016dbe | 1;
  return;
}

