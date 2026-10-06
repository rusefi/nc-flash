/* Ghidra analysis output; verify against original SH instructions. */

/* Returns0 without31720 pending work; otherwise dispatches5DEB8[previous_code*6+next]. Observed
   code1/next1 executes47762->8 in phase0. Other dispatch paths not independently modeled;
   tcu-transition-classification.txt. */

undefined1 Transition_SelectOperation(byte param_1,byte param_2)

{
  char cVar1;
  undefined1 uVar2;
  
  cVar1 = (*(code *)PTR_Phase_HasPendingWork_000474b8)();
  uVar2 = 0;
  if (cVar1 != '\0') {
    uVar2 = (**(code **)(PTR_PTR_000474bc + (uint)param_2 * 4 + (uint)param_1 * 0x18))();
  }
  return uVar2;
}

