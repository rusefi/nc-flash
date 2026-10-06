/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x0004d28a) */
/* Compares signed low16 argument withzero; returns original32-bit argument ifnonnegative,elsezero.
   Real5BBEC(0.5) conversion executed. */

int SparkRequest_ClampSignedNonnegative(int param_1)

{
  short sVar1;
  int extraout_r3;
  
  sVar1 = (*(code *)PTR_FUN_0004d2cc)();
  if (extraout_r3 < sVar1) {
    sVar1 = (*(code *)PTR_FUN_0004d2cc)();
    param_1 = (int)sVar1;
  }
  return param_1;
}

