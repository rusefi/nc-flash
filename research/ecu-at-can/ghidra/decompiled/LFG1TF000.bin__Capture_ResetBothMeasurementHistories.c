/* Ghidra analysis output; verify against original SH instructions. */

/* Original calls17A40,17990,20658,211C4 executed inside122F4; independent wholeRAM history oracle
   checks counters,18/24long histories,heads,invalid values. tcu-capture-readiness.txt. */

void Capture_ResetBothMeasurementHistories(void)

{
  (*(code *)PTR_FUN_00012918)();
  (*(code *)PTR_FUN_0001291c)();
  (*(code *)PTR_Reference_InitializeCaptureHistory_00012920)();
  (*(code *)PTR_Measurement_InitializeCaptureHistory_00012924)();
  return;
}

