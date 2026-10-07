/* Ghidra analysis output; verify against original SH instructions. */

/* Twelve wordwrites includingF630=1/F524=1. Does not prove CPU enable or hardware
   interruptdelivery. See tcu-timer-configuration.txt. */

void TimerSetup_EnableInterruptSources(void)

{
  undefined2 *puVar1;
  
  *(undefined2 *)(int)DAT_000146d0 = 0;
  *(undefined2 *)(int)DAT_000146d2 = 0;
  puVar1 = (undefined2 *)(int)DAT_000146d4;
  *puVar1 = 1;
  *(undefined2 *)(int)DAT_000146d6 = 1;
  *(undefined2 *)(int)DAT_000146d8 = 0;
  puVar1[0xf] = 0;
  *(undefined2 *)(int)DAT_000146da = 1;
  *(undefined2 *)(int)DAT_000146dc = 0;
  *(undefined2 *)(int)DAT_000146de = 0;
  *(undefined2 *)(int)DAT_000146e0 = 0;
  *(undefined2 *)(int)DAT_000146e2 = 0;
  *(undefined2 *)(int)DAT_000146e4 = 1;
  return;
}

