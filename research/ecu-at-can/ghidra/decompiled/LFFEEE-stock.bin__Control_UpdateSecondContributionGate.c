/* Ghidra analysis output; verify against original SH instructions. */

/* 812B clears6818<0,sets6818>=A36E8(8120),otherwisehold.1080cases. */

undefined4 Control_UpdateSecondContributionGate(void)

{
  undefined4 uVar1;
  float fVar2;
  float extraout_fr0;
  
  fVar2 = (float)(*(code *)PTR_FUN_000599a4)(PTR_Control_ScaledErrorTerm_000599a0);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_00059994)
                    (*(undefined4 *)PTR_Control_FilteredContributionInput_0005998c,
                     PTR_Model_FloatCurve_ARRAY_000599a8);
  if (*(float *)PTR_DAT_000599b0 <= fVar2) {
    if (extraout_fr0 <= fVar2) {
      *PTR_Control_SecondContributionGate_000599ac = 1;
    }
  }
  else {
    *PTR_Control_SecondContributionGate_000599ac = 0;
  }
  return uVar1;
}

