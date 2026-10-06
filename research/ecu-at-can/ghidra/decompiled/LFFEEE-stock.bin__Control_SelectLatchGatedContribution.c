/* Ghidra analysis output; verify against original SH instructions. */

/* 80DC=0unless67ACexact1 and7978zero. Else original2508 blends80E8 toward80E4 using80EC
   andepsilon~1e-5. CAN211bit13->6A20->original4E80C latch nowexecutesbeforethisconsumer;
   control-contributions.txt. */

uint Control_SelectLatchGatedContribution(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  
  uVar1 = (*(code *)PTR_FUN_0005933c)(PTR_DAT_00059338);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 1) {
    uVar1 = (*(code *)PTR_FUN_0005933c)(PTR_Control_RetainedLatch7978_00059340);
    uVar1 = uVar1 & 0xff;
    if (uVar1 == 0) {
      uVar1 = (*(code *)PTR_FUN_00059354)
                        (*(undefined4 *)PTR_Control_SecondGatedContributionMap_00059350,
                         *(undefined4 *)PTR_Control_FirstGatedContributionMap_0005934c,
                         1.0 - *(float *)PTR_Control_ContributionBlendWeight_00059344,DAT_00059348);
      *(undefined4 *)PTR_Control_LatchGatedBaselineContribution_00059358 = extraout_fr0;
      return uVar1;
    }
  }
  *(undefined4 *)PTR_Control_LatchGatedBaselineContribution_00059358 = 0;
  return uVar1;
}

