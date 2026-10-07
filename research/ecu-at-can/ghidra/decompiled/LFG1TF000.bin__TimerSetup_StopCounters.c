/* Ghidra analysis output; verify against original SH instructions. */

/* Writes0 toF401/F400/F402. Exact original writes and selected155C8 caller executed. See
   tcu-timer-configuration.txt. */

void TimerSetup_StopCounters(void)

{
  *(undefined1 *)(int)DAT_00014528 = 0;
  *(undefined1 *)(int)DAT_0001452a = 0;
  *(undefined1 *)(int)DAT_0001452c = 0;
  return;
}

