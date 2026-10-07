/* Ghidra analysis output; verify against original SH instructions. */

/* Static caller sequence11F38,1217C,123B0,12374,11F6C,1226C,11FA0,121F8,122D8 then12018. Called
   from mainforegroundmode1/2. Completecaller notexecuted. tcu-capture-readiness.txt. */

void Startup_InitializeOperationalTasks(void)

{
  (*(code *)PTR_FUN_00011740)();
  (*(code *)PTR_DiagnosticTask_InitializeModeAndTimer_00011744)();
  (*(code *)PTR_CMT0_InitializeTickAndTimerService_00011748)();
  (*(code *)PTR_CMT1_InitializePrimaryWheel_0001174c)();
  (*(code *)PTR_FUN_00011750)();
  (*(code *)PTR_FUN_00011754)();
  (*(code *)PTR_CANTask_InitializeModeAndTimer_00011758)();
  (*(code *)PTR_Task_InitializeApplicationAndTimer_0001175c)();
  (*(code *)PTR_Capture_InitializeReadiness_00011760)();
                    /* WARNING: Could not recover jumptable at 0x000116c4. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_00011764)();
  return;
}

