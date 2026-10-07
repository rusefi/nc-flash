/* Ghidra analysis output; verify against original SH instructions. */

/* 3072 isolatedgatecases plus24actualISRprefixes in3nativeinitializedtraces PASS. Mode1
   requires84A0/84D8/8007 all3 before1267C thenmode3;mode3 with84A0=4 becomes5. No forcedmode3
   innewstartup; diagnosticadmission3000000phi underexplicitpoll/epoch fixtures.
   tcu-diagnostic-startup.txt. */

void DiagnosticTask_AdmitAndRun(void)

{
  if (DAT_ffff8006 == '\x01') {
    if (((*PTR_Startup_AdcAReadinessState_000121e8 == '\x03') &&
        (*PTR_Startup_AdcBReadinessState_000121ec == '\x03')) && (DAT_ffff8007 == '\x03')) {
      (*(code *)PTR_Diagnostic_InitializeTaskState_000121f0)();
      DAT_ffff8006 = '\x03';
    }
  }
  else if ((DAT_ffff8006 == '\x03') && (*PTR_Startup_AdcAReadinessState_000121e8 == '\x04')) {
    DAT_ffff8006 = '\x05';
  }
  (*(code *)PTR_Task_RunDiagnosticsForMode_000121f4)();
  return;
}

