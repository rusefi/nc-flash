/* Ghidra analysis output; verify against original SH instructions. */

/* 6937=(67D4>=DB170 OR67D0>=DB174). Stock~18.4711/15.9375.9exact-neighborboundarycases;
   caller/model order verified. */

void ControlSecondary_ProduceGate(void)

{
  if ((*(float *)PTR_DAT_00030848 <= *(float *)PTR_ControlMode_ScaledByteInput_00030828) ||
     (*(float *)PTR_DAT_0003084c <= *(float *)PTR_ControlMode_BiasedInput_00030830)) {
    *PTR_ControlSecondary_Gate_00030844 = 1;
  }
  else {
    *PTR_ControlSecondary_Gate_00030844 = 0;
  }
  return;
}

