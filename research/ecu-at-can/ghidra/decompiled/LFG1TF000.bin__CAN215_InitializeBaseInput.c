/* Ghidra analysis output; verify against original SH instructions. */

/* Static initialization:5FD50=9240 ->80B4; A538=0. Initialization not executed by new feedback
   verifier. */

void CAN215_InitializeBaseInput(void)

{
  SparkRequest_BaseInput = *DAT_00051780;
  *PTR_CAN215_BaseSelectionStatus_00051784 = 0;
  return;
}

