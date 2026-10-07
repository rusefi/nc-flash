/* Ghidra analysis output; verify against original SH instructions. */

/* Original protected6D5C/6D68 zero; six history floats retained. Initialization verified under
   three nonzero SR masks. */

void SpeedCandidate_InitializeProtectedInput(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  (*(code *)PTR_FUN_0003a214)(0,PTR_SpeedCandidate_ProtectedSelected_0003a210);
  (*(code *)PTR_FUN_0003a214)(uVar1,PTR_SpeedCandidate_HistoryDifference_0003a218);
  return;
}

