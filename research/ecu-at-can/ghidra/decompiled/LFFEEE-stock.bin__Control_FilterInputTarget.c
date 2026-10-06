/* Ghidra analysis output; verify against original SH instructions. */

/* Mode1 usesoriginal2508 withinput806C,old8088,weight1-D9F1C andeps.000244140625;else8060=80BC. RTZ
   intermediateoracle. */

uint Control_FilterInputTarget(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  
  uVar1 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058954);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 1) {
    uVar1 = (*(code *)PTR_FUN_00058970)
                      (*(undefined4 *)PTR_Control_InputTarget_00058960,
                       *(undefined4 *)PTR_Control_PriorFilteredInputSnapshot_0005896c,
                       1.0 - *(float *)PTR_DAT_00058964,DAT_00058968);
    *(undefined4 *)PTR_Control_FilteredInputTarget_00058974 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_FilteredInputTarget_00058974 =
         *(undefined4 *)PTR_Control_BaselineInput_00058958;
  }
  return uVar1;
}

