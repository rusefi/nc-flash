/* Ghidra analysis output; verify against original SH instructions. */

/* Curve70B49(u16(2*80FE))>>8 multipliedbysigned9718,arithmetic>>6. Stockcurveidenticalto70B40. */

int TransitionProgress_PositiveRateB(void)

{
  ushort extraout_var;
  
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00032af0)
            ((int)DAT_ffff80fe << 1,PTR_TransitionProgress_PositiveBCurve_00032af8);
  return (int)(short)(extraout_var & 0xff) * (int)*(short *)(int)DAT_00032ada >> 6;
}

