/* Ghidra analysis output; verify against original SH instructions. */

/* Adds signedword error times gain to signed32 accumulator, wraps then compares negative bound
   first and positive bound second without sorting. Bound is s16(D)*1000; nested signed division
   executes. */

int OutputHandoff_AccumulateError(short param_1,uint param_2,int param_3,short param_4)

{
  int iVar1;
  
  param_3 = param_3 + (int)param_1 * (param_2 & 0xffff);
  iVar1 = (int)param_4 * (int)DAT_00018edc;
  if (param_3 < -iVar1) {
    return -iVar1;
  }
  if (iVar1 < param_3) {
    return iVar1;
  }
  return param_3;
}

