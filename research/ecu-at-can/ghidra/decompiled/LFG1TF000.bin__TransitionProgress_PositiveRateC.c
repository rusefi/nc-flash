/* Ghidra analysis output; verify against original SH instructions. */

/* Curve70B24(u16(2*80FE))>>8 multipliedbysigned9718,arithmetic>>6. */

int TransitionProgress_PositiveRateC(void)

{
  ushort extraout_var;
  
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00032c5c)
            ((int)DAT_ffff80fe << 1,PTR_TransitionProgress_PositiveCCurve_00032c58);
  return (int)(short)(extraout_var & 0xff) * (int)*(short *)(int)DAT_00032c4a >> 6;
}

