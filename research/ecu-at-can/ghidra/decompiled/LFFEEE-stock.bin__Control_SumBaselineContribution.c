/* Ghidra analysis output; verify against original SH instructions. */

/* 80C4=RTZ(80C8+80CC). Bothcontributors nowproduced inretainedpaired pipeline. */

void Control_SumBaselineContribution(void)

{
  *(float *)PTR_Control_MappedBaselineContribution_00059118 =
       *(float *)PTR_Control_TwoInputBaselineMap_00059114 +
       *(float *)PTR_Control_OptionalBaselineExtra_00059110;
  return;
}

