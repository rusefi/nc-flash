/* Ghidra analysis output; verify against original SH instructions. */

/* Protected8070=806C,8064=8060;called1D710 in another task. Once-per-cycle test publication is
   explicit,not proven production rate. */

void Control_PublishInputHistory(void)

{
  (*(code *)PTR_FUN_000586f4)
            (*(undefined4 *)PTR_Control_InputTarget_000586f0,
             PTR_Control_ProtectedPriorInputTarget_000586fc);
  (*(code *)PTR_FUN_000586f4)
            (*(undefined4 *)PTR_Control_FilteredInputTarget_000586ec,
             PTR_Control_ProtectedPriorFilteredInput_00058700);
  return;
}

