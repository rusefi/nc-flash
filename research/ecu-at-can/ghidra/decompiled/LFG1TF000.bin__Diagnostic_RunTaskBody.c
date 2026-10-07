/* Ghidra analysis output; verify against original SH instructions. */

/* Originalfullbody invokes producers then56658,57F50,570F6,57258,tail57B9C.
   Executesseparatelyfrom126EC in64pairfixture. Callingbodyalone doesnotsetA936/A939. */

void Diagnostic_RunTaskBody(void)

{
  (*(code *)PTR_FUN_000571e0)();
  (*(code *)PTR_FUN_000571e4)();
  (*(code *)PTR_FUN_000571e8)();
  (*(code *)PTR_FUN_000571ec)();
  (*(code *)PTR_CAN_ProduceValidityDiagnosticGroups_000571f0)();
  (*(code *)PTR_FUN_000571f4)();
  (*(code *)PTR_FUN_000571f8)();
  (*(code *)PTR_FUN_000571fc)();
  (*(code *)PTR_FUN_00057200)();
  (*(code *)PTR_FUN_00057204)();
  (*(code *)PTR_Selector_ProduceDiagnosticGroups_00057208)();
  (*(code *)PTR_FUN_0005720c)();
  (*(code *)PTR_FUN_00057210)();
  (*(code *)PTR_FUN_00057214)();
  (*(code *)PTR_FUN_00057218)();
  (*(code *)PTR_FUN_0005721c)();
  (*(code *)PTR_FUN_00057220)();
  (*(code *)PTR_Diagnostic_ProcessGroups_00057224)();
  (*(code *)PTR_Diagnostic_UpdateHealthyRecovery_00057228)();
  Diagnostic_BuildMappedSummary();
  Diagnostic_BuildCombinedSummaries();
  (*(code *)PTR_FUN_0005722c)();
  return;
}

