/* Ghidra analysis output; verify against original SH instructions. */

/* Returns0 for codes0..4,1 otherwise; descending codes5..11 exercised via real phase predicates. */

undefined4 Phase_ClassifyDirection(short param_1)

{
  undefined4 uVar1;
  
  uVar1 = 1;
  if ((((param_1 == 0) || (param_1 == 1)) || (param_1 == 2)) || ((param_1 == 3 || (param_1 == 4))))
  {
    uVar1 = 0;
  }
  return uVar1;
}

