/* Ghidra analysis output; verify against original SH instructions. */

/* Clears9414..941A and8280; preserves82B9/82BA untilrequests.16fullRAMcases. See
   tcu-inhibit-writers.txt. */

void ModePulse_Initialize(void)

{
  undefined *puVar1;
  undefined1 *puVar2;
  
  puVar1 = PTR_ModePulse_SecondState_00023e90;
  *PTR_ModePulse_FirstState_00023e8c = 0;
  *puVar1 = 0;
  puVar2 = (undefined1 *)(int)DAT_00023e82;
  *PTR_ModePulse_ThirdState_00023e94 = 0;
  *puVar2 = 0;
  puVar2 = (undefined1 *)(int)DAT_00023e86;
  *(undefined1 *)(int)DAT_00023e84 = 0;
  *puVar2 = 0;
  puVar1 = PTR_DAT_00023e98;
  *(undefined1 *)(int)DAT_00023e88 = 0;
  *puVar1 = 0;
  return;
}

