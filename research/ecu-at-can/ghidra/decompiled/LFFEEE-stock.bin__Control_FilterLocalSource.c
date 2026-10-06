/* Ghidra analysis output; verify against original SH instructions. */

/* 2508:stockhalfblend6CB4/old536C,epsilon~1e-5snap;1600finitefilterchecks. Relativecallscheduling
   andnonfinite behavioropen. */

void Control_FilterLocalSource(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_0001df10)
                    (*(undefined4 *)PTR_Control_LocalFilterInput_0001df00,
                     *(undefined4 *)PTR_Control_FilteredLocalSource_0001df04,
                     *(undefined4 *)PTR_DAT_0001df0c,DAT_0001df08);
  *(undefined4 *)PTR_Control_FilteredLocalSource_0001df04 = uVar1;
  return;
}

