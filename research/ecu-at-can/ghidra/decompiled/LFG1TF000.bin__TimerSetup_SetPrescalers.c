/* Ghidra analysis output; verify against original SH instructions. */

/* Writes1 toF404/F406/F408/F40A; compatibleSH7055S prescalers Pphi/2. Absolute clock unproved. See
   tcu-timer-configuration.txt. */

void TimerSetup_SetPrescalers(void)

{
  undefined1 *puVar1;
  
  puVar1 = (undefined1 *)(int)DAT_0001452e;
  *puVar1 = 1;
  *(undefined1 *)(int)DAT_00014530 = 1;
  *(undefined1 *)(int)DAT_00014532 = 1;
  puVar1[6] = 1;
  return;
}

