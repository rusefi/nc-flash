/* Ghidra analysis output; verify against original SH instructions. */

/* 6938clear when67DC<RTZ(DB180-DB184),set when>=DB180,else retainrawbyte. Upper equality
   sets;36cases. DB180~859.37,DB184~58.59.314F8 requires exact1. */

void ControlInput_UpdateScaleHysteresis(void)

{
  if (*(float *)PTR_DAT_00030850 - *(float *)PTR_DAT_00030854 <=
      *(float *)PTR_ControlInput_ScaledLimitAxis_00030858) {
    if (*(float *)PTR_DAT_00030850 <= *(float *)PTR_ControlInput_ScaledLimitAxis_00030858) {
      *PTR_ControlInput_ScaleHysteresisGate_0003085c = 1;
    }
  }
  else {
    *PTR_ControlInput_ScaleHysteresisGate_0003085c = 0;
  }
  return;
}

