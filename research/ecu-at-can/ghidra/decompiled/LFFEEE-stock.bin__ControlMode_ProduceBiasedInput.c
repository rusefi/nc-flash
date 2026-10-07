/* Ghidra analysis output; verify against original SH instructions. */

/* 67D0=RTZ(6CB4+DB1D4 approximately0.11). Replaces raw67D0 fixture before downstream gates
   in320cycle replay. Physicalidentityopen. */

void ControlMode_ProduceBiasedInput(void)

{
  *(float *)PTR_ControlMode_BiasedInput_00030600 =
       *(float *)PTR_Control_LocalFilterInput_000305fc + *DAT_000305f8;
  return;
}

