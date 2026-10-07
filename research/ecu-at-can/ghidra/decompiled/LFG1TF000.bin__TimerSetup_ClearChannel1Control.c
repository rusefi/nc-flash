/* Ghidra analysis output; verify against original SH instructions. */

/* Writes byte0 toF484 in original155C8 initialization sequence. See tcu-timer-configuration.txt. */

void TimerSetup_ClearChannel1Control(void)

{
  *(undefined1 *)(int)DAT_000149d2 = 0;
  return;
}

