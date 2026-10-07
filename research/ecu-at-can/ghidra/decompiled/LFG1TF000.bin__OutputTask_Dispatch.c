/* Ghidra analysis output; verify against original SH instructions. */

/* Mode8008=1 historyscan17B1A;3 active127FC;othersskip. Always84F8 zero->3 elsebyte decrement.1536
   fullmode/phase cases. See tcu-output-task.txt. */

uint OutputTask_Dispatch(void)

{
  uint uVar1;
  
  (*(code *)PTR_FUN_00012864)();
  uVar1 = (uint)DAT_ffff8008;
  if (uVar1 == 1) {
    uVar1 = (*(code *)PTR_OutputTask_ScanInputHistory_00012868)();
  }
  else if (uVar1 == 3) {
    uVar1 = OutputTask_ActiveFeedbackService();
  }
  if (*PTR_DAT_00012850 != '\0') {
    *PTR_DAT_00012850 = *PTR_DAT_00012850 + -1;
    return uVar1;
  }
  *PTR_DAT_00012850 = 3;
  return uVar1;
}

