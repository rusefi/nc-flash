/* Ghidra analysis output; verify against original SH instructions. */

/* Original caller executes A61A8,A4B98,A6238,A6490,A4FF8 in order;12 paired TCU/ECU fixtures. Only
   final conversion independently modeled;control-conversion.txt. */

void Control_RunFiveStageCalculation(void)

{
  (*(code *)PTR_Control_SnapshotConversionInputs_000a47d8)();
  (*(code *)PTR_thunk_FUN_000a4b98_000a47dc)();
  (*(code *)PTR_thunk_FUN_000a6238_000a47e0)();
  (*(code *)PTR_Control_CombineCANNumericInputs_000a47e4)();
  (*(code *)PTR_Control_InvertAndBlendMaps_000a47e8)();
  return;
}

