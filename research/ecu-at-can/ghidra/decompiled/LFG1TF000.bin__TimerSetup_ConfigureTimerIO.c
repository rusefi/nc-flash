/* Ghidra analysis output; verify against original SH instructions. */

/* 16 exact timer-I/O bytewrites verified; original initialization caller executed. See
   tcu-timer-configuration.txt. */

void TimerSetup_ConfigureTimerIO(void)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  
  puVar2 = (undefined1 *)(int)DAT_000146a6;
  *puVar2 = 0;
  puVar1 = (undefined1 *)(int)DAT_000146a8;
  *puVar1 = 0;
  *(undefined1 *)(int)DAT_000146aa = 0;
  puVar2[0x31] = 0;
  puVar1[1] = 0;
  puVar1 = (undefined1 *)(int)DAT_000146ac;
  *puVar1 = 1;
  *(undefined1 *)(int)DAT_000146ae = 0;
  *(undefined1 *)(int)DAT_000146b0 = 0;
  puVar1[1] = 0;
  *(undefined1 *)(int)DAT_000146b2 = 1;
  *(undefined1 *)(int)DAT_000146b4 = 0;
  puVar1 = (undefined1 *)(int)DAT_000146b6;
  *puVar1 = 0;
  *(undefined1 *)(int)DAT_000146b8 = 0x10;
  *(undefined1 *)(int)DAT_000146ba = 0x11;
  puVar1[0x1f] = 0;
  *(undefined1 *)(int)DAT_000146bc = 1;
  return;
}

