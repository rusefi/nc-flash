/* Ghidra analysis output; verify against original SH instructions. */

/* Mode1 writes805C=max(0,RTZ(806C-8060));othermodeszero. */

uint Control_UpdateInputPositiveGap(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  undefined4 uVar2;
  
  uVar2 = 0;
  uVar1 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058954);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 1) {
    uVar1 = (*(code *)PTR_FUN_00058920)
                      (*(float *)PTR_Control_InputTarget_00058960 -
                       *(float *)PTR_Control_FilteredInputTarget_00058974,uVar2);
    *(undefined4 *)PTR_Control_PositiveInputGap_00058978 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_PositiveInputGap_00058978 = uVar2;
  }
  return uVar1;
}

