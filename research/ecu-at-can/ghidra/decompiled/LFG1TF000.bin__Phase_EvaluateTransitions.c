/* Ghidra analysis output; verify against original SH instructions. */

/* State/code5D474 dispatch through5D464; state0 falls back to state1 predicate and maps return2
   to1. Descending original lifecycles verified; ascending/composite context remains open. See
   tcu-phase-policy.txt. */

int Phase_EvaluateTransitions(char param_1,short param_2,uint param_3,short param_4,short param_5)

{
  int iVar1;
  
  iVar1 = (**(code **)(PTR_Phase_PredicateCallbacks_00032248 +
                      (char)PTR_Phase_CodeStateColumns_00032244
                            [(int)param_1 + (param_3 & 0xffff) * 3] * 4))
                    ((int)param_2,param_3,(int)param_4,(int)param_5,
                     (int)(char)PTR_Phase_CodeStateColumns_00032244
                                [(int)param_1 + (param_3 & 0xffff) * 3]);
  if ((param_1 == '\0') && (iVar1 != 1)) {
    iVar1 = (**(code **)(PTR_Phase_PredicateCallbacks_00032248 +
                        (char)PTR_Phase_CodeStateColumns_1__0003224c[(param_3 & 0xffff) * 3] * 4))
                      ((int)param_2,param_3,(int)param_4,(int)param_5,
                       (int)(char)PTR_Phase_CodeStateColumns_1__0003224c[(param_3 & 0xffff) * 3]);
    if (iVar1 == 2) {
      iVar1 = 1;
    }
  }
  return iVar1;
}

