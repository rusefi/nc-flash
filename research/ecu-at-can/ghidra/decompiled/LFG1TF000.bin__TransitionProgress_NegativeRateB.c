/* Ghidra analysis output; verify against original SH instructions. */

/* Negative ofarithmetic((signed770CE*signed9718)>>6);stockconstant256. */

int TransitionProgress_NegativeRateB(void)

{
  return -((int)*(short *)PTR_TransitionProgress_NegativeBConstant_00032c54 *
           (int)*(short *)(int)DAT_00032c4a >> 6);
}

