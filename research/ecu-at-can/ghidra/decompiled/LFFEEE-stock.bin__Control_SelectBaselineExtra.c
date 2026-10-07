/* Ghidra analysis output; verify against original SH instructions. */

/* If6D30<DA474=-200,80CC=A3650(80D0);else0. Stockcurveallzero; threshold andlookup paths executed.
    */

undefined4 Control_SelectBaselineExtra(void)

{
  undefined4 uVar1;
  float extraout_fr0;
  undefined4 extraout_fr0_00;
  
  uVar1 = (*(code *)PTR_FUN_00059120)(PTR_Control_RawFirstSnapshot_0005911c);
  if (*(float *)PTR_DAT_00059130 <= extraout_fr0) {
    *(undefined4 *)PTR_Control_OptionalBaselineExtra_00059110 = 0;
  }
  else {
    uVar1 = (*(code *)PTR_Lookup_FloatCurve_0005913c)
                      (*(undefined4 *)PTR_Control_RetainedBaselineAverage_00059134,
                       PTR_Control_BaselineExtraDescriptor_00059138);
    *(undefined4 *)PTR_Control_OptionalBaselineExtra_00059110 = extraout_fr0_00;
  }
  return uVar1;
}

