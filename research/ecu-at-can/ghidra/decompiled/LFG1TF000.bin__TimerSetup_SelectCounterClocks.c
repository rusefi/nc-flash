/* Ghidra analysis output; verify against original SH instructions. */

/* 16 bytewrites; F62B/F62A/F521/F520=0 select direct prescaled clock. F521 reached through register
   arithmetic. See tcu-timer-configuration.txt. */

void TimerSetup_SelectCounterClocks(void)

{
  undefined1 *puVar1;
  
  *(undefined1 *)(int)DAT_00014534 = 4;
  puVar1 = (undefined1 *)(int)DAT_00014536;
  *puVar1 = 4;
  *(undefined1 *)(int)DAT_00014538 = 0;
  *(undefined1 *)(int)DAT_0001453a = 0;
  puVar1[0x50] = 4;
  *(undefined1 *)(int)DAT_0001453c = 5;
  *(undefined1 *)(int)DAT_0001453e = 4;
  puVar1[0xc5] = 0;
  *(undefined1 *)(int)DAT_00014540 = 0;
  *(undefined1 *)(int)DAT_00014542 = 0;
  puVar1[0x144] = 0;
  *(undefined1 *)(int)DAT_00014544 = 0x53;
  *(undefined1 *)(int)DAT_00014546 = 0;
  *(undefined1 *)(int)DAT_00014548 = 0;
  *(undefined1 *)(int)DAT_0001454a = 0;
  *(undefined1 *)(int)DAT_0001454c = 0;
  return;
}

