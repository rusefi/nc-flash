/* Ghidra analysis output; verify against original SH instructions. */

/* Negative ofarithmetic((signed770D0*signed9718)>>6);stock256,selectedby95AEbit0 forcertaincodes.
    */

int TransitionProgress_AlternateNegativeRateB(void)

{
  return -((int)*(short *)PTR_TransitionProgress_AlternateNegativeBConstant_00032c50 *
           (int)*(short *)(int)DAT_00032c4a >> 6);
}

