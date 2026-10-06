/* Ghidra analysis output; verify against original SH instructions. */

/* 80FC=RTZ(RTZ(80F4*8110)*max(8108,810C)); originaloutputsfeed58F10baselineand51286ratiofactor.
   8108canpreservebaselinewith7242zero. */

void Control_CombineMagnitudeBaseline(void)

{
  float fVar1;
  
  fVar1 = (float)(*(code *)PTR_FUN_000594cc)
                           (*(undefined4 *)PTR_Control_FirstMagnitudeAmount_000594c8,
                            *(undefined4 *)PTR_Control_SecondMagnitudeAmount_000594c4);
  *(float *)PTR_Control_MagnitudeBaselineContribution_000594d4 =
       *(float *)PTR_Control_MagnitudeBaselineScale_000594d0 *
       *(float *)PTR_Control_MagnitudeInputFactor_000594c0 * fVar1;
  return;
}

