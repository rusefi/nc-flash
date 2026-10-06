/* Ghidra analysis output; verify against original SH instructions. */

/* deadline-current;if nonpositive add02D00000 once.20290 subsequently rejects negative signed
   result; not unrestricted modular arithmetic. */

int Output_ForwardPositionDistance(int param_1,int param_2)

{
  param_2 = param_2 - param_1;
  if (param_2 < 1) {
    param_2 = param_2 + DAT_000201a4;
  }
  return param_2;
}

