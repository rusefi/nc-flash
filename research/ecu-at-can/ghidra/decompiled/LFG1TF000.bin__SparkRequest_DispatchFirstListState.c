/* Ghidra analysis output; verify against original SH instructions. */

/* Tailcalls2FEF8 with startup-copied descriptorB038. Full creation,state2/3/4/5 andrelease
   executed. This is a dispatcher wrapper, not only an initializer. See tcu-request-dispatch.txt. */

void SparkRequest_DispatchFirstListState(undefined4 param_1,undefined4 param_2)

{
  (*(code *)PTR_CallbackState_Dispatch_0004ccdc)(param_1,param_2,DAT_0004ccd8);
  return;
}

