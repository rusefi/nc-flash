/* Ghidra analysis output; verify against original SH instructions. */

/* OriginalwordF710=0.96component/32caller15608..15614 cases verifyorderedMMIO/unchangedRAM.
   tcu-cmt-configuration.txt; fullboot admission notproved. */

void CMT_StopBothChannels(void)

{
  *(undefined2 *)(int)DAT_00014706 = 0;
  return;
}

