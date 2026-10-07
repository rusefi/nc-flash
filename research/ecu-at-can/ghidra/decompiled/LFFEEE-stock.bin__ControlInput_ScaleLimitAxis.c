/* Ghidra analysis output; verify against original SH instructions. */

/* 67DC=RTZ(6DB4*DB144), stock2.4200000763.12direct plus72original14callsegments/320retainedcycles.
   control-input-gates.txt; physicalunits unproved. */

void ControlInput_ScaleLimitAxis(void)

{
  float fVar1;
  
  fVar1 = (float)(*(code *)PTR_FUN_00030cb4)(PTR_DAT_00030cb0);
  *(float *)PTR_ControlInput_ScaledLimitAxis_00030cd4 = *(float *)PTR_DAT_00030cd0 * fVar1;
  return;
}

