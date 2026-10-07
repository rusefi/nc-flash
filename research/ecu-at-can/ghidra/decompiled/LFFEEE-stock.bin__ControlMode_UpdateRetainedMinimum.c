/* Ghidra analysis output; verify against original SH instructions. */

/* Only70F0exact1 updates67D8=min(old,current67D0) through23F8; otherwiseholds.400finitecases
   andretaineddecrease/rise behavior. */

uint ControlMode_UpdateRetainedMinimum(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  
  uVar1 = (uint)(byte)*PTR_DAT_00030618;
  if (uVar1 == 1) {
    uVar1 = (*DAT_0003061c)(*(undefined4 *)PTR_ControlMode_BiasedInput_00030600,
                            *(undefined4 *)PTR_ControlMode_RetainedMinimum_00030614);
    *(undefined4 *)PTR_ControlMode_RetainedMinimum_00030614 = extraout_fr0;
  }
  return uVar1;
}

