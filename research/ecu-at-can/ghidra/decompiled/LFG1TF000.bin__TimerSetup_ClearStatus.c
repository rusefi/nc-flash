/* Ghidra analysis output; verify against original SH instructions. */

/* Eleven statusword writes0 includingF62C/F522; exact trace/fullRAM verified. See
   tcu-timer-configuration.txt. */

void TimerSetup_ClearStatus(void)

{
  undefined2 *puVar1;
  
  *(undefined2 *)(int)DAT_000146be = 0;
  *(undefined2 *)(int)DAT_000146c0 = 0;
  puVar1 = (undefined2 *)(int)DAT_000146c2;
  *puVar1 = 0;
  *(undefined2 *)(int)DAT_000146c4 = 0;
  *(undefined2 *)(int)DAT_000146c6 = 0;
  puVar1[0x10] = 0;
  *(undefined2 *)(int)DAT_000146c8 = 0;
  puVar1 = (undefined2 *)(int)DAT_000146ca;
  *puVar1 = 0;
  *(undefined2 *)(int)DAT_000146cc = 0;
  *(undefined2 *)(int)DAT_000146ce = 0;
  puVar1[0x14] = 0;
  return;
}

