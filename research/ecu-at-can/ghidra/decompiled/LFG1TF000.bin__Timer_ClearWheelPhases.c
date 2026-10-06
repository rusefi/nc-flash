/* Ghidra analysis output; verify against original SH instructions. */

/* Clears u32 RAM8494,8498,849C; executed through12880. See tcu-request-timing.txt. */

void Timer_ClearWheelPhases(void)

{
  undefined4 *puVar1;
  
  puVar1 = (undefined4 *)(int)DAT_000110ec;
  *(undefined4 *)(int)DAT_000110ea = 0;
  *puVar1 = 0;
  *(undefined4 *)(int)DAT_000110ee = 0;
  return;
}

