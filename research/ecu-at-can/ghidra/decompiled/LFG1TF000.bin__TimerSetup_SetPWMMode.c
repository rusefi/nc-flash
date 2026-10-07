/* Ghidra analysis output; verify against original SH instructions. */

/* F526=0; compatiblemanual on-duty non-complementary6A..D. Pinpolarity remains dependent
   onPBIR/resetcontext. See tcu-timer-configuration.txt. */

void TimerSetup_SetPWMMode(void)

{
  *(undefined1 *)(int)DAT_000149d4 = 0;
  return;
}

