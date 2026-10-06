/* Ghidra analysis output; verify against original SH instructions. */

/* Negative ofarithmetic((signed770CC*signed9718)>>6);stockconstant256. */

int TransitionProgress_NegativeRateA(void)

{
  return -((int)*(short *)PTR_TransitionProgress_NegativeAConstant_00032af4 *
           (int)*(short *)(int)DAT_00032ada >> 6);
}

