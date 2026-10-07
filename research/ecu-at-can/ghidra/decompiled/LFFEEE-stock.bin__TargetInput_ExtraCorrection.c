/* Ghidra analysis output; verify against original SH instructions. */

/* 6960=RTZ(max(0,RTZ(raw6D20-86.1))*0.56), exactstockbinary32.154BCrawgetter; thresholdneighbors
   andcoupledretainedbehaviorverified. */

void TargetInput_ExtraCorrection(void)

{
  float fVar1;
  
  fVar1 = (float)(*(code *)PTR_FUN_00033c8c)(PTR_Control_RawFirstPublished_00033c88);
  fVar1 = (float)(*(code *)PTR_FUN_00033c94)(fVar1 - *(float *)PTR_DAT_00033c90,0);
  *(float *)PTR_TargetInput_ExtraTerm_00033c9c = *(float *)PTR_DAT_00033c98 * fVar1;
  return;
}

