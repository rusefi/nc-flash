/* Ghidra analysis output; verify against original SH instructions. */

/* Signed32 division; zero divisor returns0 for zero numerator,7FFFFFFF positive,80000000
   negative.49 boundary/sign/zero cases; original integer overflow behavior retained. See
   tcu-measurement.txt. */

undefined4 Arithmetic_GuardedSignedDivision(int param_1,int param_2)

{
  undefined4 uVar1;
  
  if (param_2 == 0) {
    if (param_1 == 0) {
      uVar1 = 0;
    }
    else {
      uVar1 = DAT_00010e5c;
      if (0 < param_1) {
        uVar1 = DAT_00010e58;
      }
    }
  }
  else {
    uVar1 = (*(code *)PTR_FUN_00010e50)();
  }
  return uVar1;
}

