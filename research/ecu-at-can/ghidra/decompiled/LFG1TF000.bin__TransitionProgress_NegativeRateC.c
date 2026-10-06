/* Ghidra analysis output; verify against original SH instructions. */

/* Negative ofarithmetic((signed770C6*signed9718)>>6);stock256,code4 branch. */

int TransitionProgress_NegativeRateC(void)

{
  return -((int)*(short *)PTR_TransitionProgress_NegativeCConstant_00032c7c *
           (int)*(short *)(int)DAT_00032c4a >> 6);
}

