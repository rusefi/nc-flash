/* Ghidra analysis output; verify against original SH instructions. */

/* 7BB8=orderedRTZsum80C4,80DC,80FC,8118,813C,822C. Calledby5844E; cancellation-ordercases verified.
    */

void Control_SumRatioMapContributions(void)

{
  *(float *)PTR_Control_RatioContributionSum_000512d4 =
       *(float *)PTR_Control_MappedBaselineContribution_000512f0 +
       *(float *)PTR_Control_LatchGatedBaselineContribution_000512ec +
       *(float *)PTR_Control_MagnitudeBaselineContribution_000512f4 + *(float *)PTR_DAT_000512f8 +
       *(float *)PTR_DAT_000512fc + *(float *)PTR_DAT_00051300;
  return;
}

