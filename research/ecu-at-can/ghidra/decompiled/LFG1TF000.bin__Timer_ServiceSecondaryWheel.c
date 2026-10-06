/* Ghidra analysis output; verify against original SH instructions. */

/* Original16-slot table5C130 and phase8498; primary phase15, executed. */

void Timer_ServiceSecondaryWheel(void)

{
  int iVar1;
  int *piVar2;
  
  piVar2 = (int *)(int)DAT_00011204;
  (**(code **)(PTR_Timer_SecondaryWheelTable_00011210 + *piVar2 * 4))();
  iVar1 = *piVar2;
  *piVar2 = iVar1 + 1;
  if (iVar1 + 1 == 0x10) {
    *piVar2 = 0;
  }
  return;
}

