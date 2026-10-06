/* Ghidra analysis output; verify against original SH instructions. */

/* After24910,increment5668saturatingu16 only5670exact1;elseclear.
   Originalretainedlifecyclesandboundarycasesverified. */

uint Control_UpdateRelativeOverrideTimer(void)

{
  undefined *puVar1;
  uint uVar2;
  
  puVar1 = PTR_Control_RelativeOverrideTimer_00024c28;
  uVar2 = (*(code *)PTR_FUN_00024bdc)(PTR_DAT_00024c1c);
  uVar2 = uVar2 & 0xff;
  if (uVar2 == 1) {
    uVar2 = (*(code *)PTR_FUN_00024c2c)((int)*(short *)puVar1,1);
    *(short *)puVar1 = (short)uVar2;
  }
  else {
    *(undefined2 *)puVar1 = 0;
  }
  return uVar2;
}

