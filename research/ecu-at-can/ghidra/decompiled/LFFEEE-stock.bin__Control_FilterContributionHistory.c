/* Ghidra analysis output; verify against original SH instructions. */

/* 8120 finiteRTZ blend from684C andold8120 usingDA774=.85;nearinput snaps.
   Physicalunits/taskcadenceopen. */

void Control_FilterContributionHistory(void)

{
  undefined4 uVar1;
  float fVar2;
  
  fVar2 = 1.0 - *(float *)PTR_DAT_00059874;
  uVar1 = (*(code *)PTR_FUN_0005983c)(PTR_ControlSecondary_ProtectedPublishedValue_00059878);
  uVar1 = (*(code *)PTR_FUN_00059884)
                    (uVar1,*(undefined4 *)PTR_Control_FilteredContributionInput_0005987c,fVar2,
                     DAT_00059880);
  *(undefined4 *)PTR_Control_FilteredContributionInput_0005987c = uVar1;
  return;
}

