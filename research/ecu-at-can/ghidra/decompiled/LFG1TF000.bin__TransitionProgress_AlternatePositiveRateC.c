/* Ghidra analysis output; verify against original SH instructions. */

/* Curve70B34(u16(2*80FA))>>8 multipliedbysigned9718,arithmetic>>6. Selectedforcode9
   orcode11with9410bit1. */

int TransitionProgress_AlternatePositiveRateC(void)

{
  ushort extraout_var;
  
  (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00032c5c)
            ((int)DAT_ffff80fa << 1,PTR_TransitionProgress_AlternateCCurve_00032c78);
  return (int)(short)(extraout_var & 0xff) * (int)*(short *)(int)DAT_00032c4a >> 6;
}

