/* Ghidra analysis output; verify against original SH instructions. */

/* Copy80BC to8060/806C;clear protected804C/8070/8064. Executed initialization;
   control-input-history.txt. */

void Control_InitializeInputHistory(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  puVar1 = PTR_Control_BaselineInput_000586e8;
  uVar2 = 0;
  *(undefined4 *)PTR_Control_FilteredInputTarget_000586ec =
       *(undefined4 *)PTR_Control_BaselineInput_000586e8;
  *(undefined4 *)PTR_Control_InputTarget_000586f0 = *(undefined4 *)puVar1;
  puVar1 = PTR_FUN_000586f4;
  (*(code *)PTR_FUN_000586f4)(0,PTR_Control_ProtectedInputBase_000586f8);
  (*(code *)puVar1)(uVar2,PTR_Control_ProtectedPriorInputTarget_000586fc);
  (*(code *)puVar1)(uVar2,PTR_Control_ProtectedPriorFilteredInput_00058700);
  return;
}

