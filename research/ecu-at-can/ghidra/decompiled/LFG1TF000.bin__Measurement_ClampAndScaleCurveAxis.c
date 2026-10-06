/* Ghidra analysis output; verify against original SH instructions. */

/* s16(input) clamped[0,16383] then multiplied4. Original helper executes within4E450 threshold
   verification, including sign and saturation boundaries. */

int Measurement_ClampAndScaleCurveAxis(short param_1)

{
  if (DAT_00020974 < param_1) {
    param_1 = DAT_00020974;
  }
  if (param_1 < 0) {
    param_1 = 0;
  }
  return (int)param_1 << 2;
}

