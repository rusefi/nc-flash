/* Ghidra analysis output; verify against original SH instructions. */

/* 8030 from8048*6DB4 /60 *CC028(~.0012) *CA974(1998) /2, RTZ eachoperation. Pairednumerator cases
   andserialcycles. */

void Control_ScaleCurrentRatioNumerator(void)

{
  float fVar1;
  
  fVar1 = (float)(*(code *)PTR_FUN_000585a0)(PTR_DAT_0005859c);
  *(float *)PTR_Control_CurrentRatioNumerator_00058594 =
       (((*(float *)PTR_Control_CurrentRatioInput_000585a4 * fVar1) / DAT_000585a8) *
        *(float *)PTR_DAT_000585ac * *(float *)PTR_DAT_000585b0) / 2.0;
  return;
}

