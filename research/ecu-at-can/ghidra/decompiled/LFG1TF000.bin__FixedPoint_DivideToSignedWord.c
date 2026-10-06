/* Ghidra analysis output; verify against original SH instructions. */

/* Signed32 numerator divided by signed16 denominator, truncate toward0 then clamp[-32768,32767].
   Zero denominator gives0 for0 numerator, signed endpoint otherwise.25 original helper cases in
   ascending-release verifier. */

int FixedPoint_DivideToSignedWord(int param_1,short param_2)

{
  int iVar1;
  int iVar2;
  
  iVar2 = (int)DAT_00010d1e;
  if (param_2 == 0) {
    if (param_1 == 0) {
      return 0;
    }
    if (0 < param_1) {
      return iVar2;
    }
  }
  else {
    iVar1 = (*(code *)PTR_FUN_00010e50)();
    if (iVar2 < iVar1) {
      iVar1 = iVar2;
    }
    if (DAT_00010e4c <= iVar1) {
      return iVar1;
    }
  }
  return (int)DAT_00010e4c;
}

