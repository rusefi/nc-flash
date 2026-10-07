/* Ghidra analysis output; verify against original SH instructions. */

/* Three originalinitializedstartup traces
   include108actualapplicationISRprefixes,93capture-return/216command-pin RAMchecks. Mode1
   invokes122F4;mode3 invokes12726/1E5F6 afterstageinit. NextIRQ aftercapture3 admitsmode3.
   Nativeforegroundpollperiod/epoch remainfixtures. tcu-readiness-admission.txt. */

void Task_ServiceApplicationMode(void)

{
  (*(code *)PTR_FUN_00012780)();
  (*(code *)PTR_Diagnostic_SelectActiveOutput_00012784)();
  if (DAT_ffff8007 == '\x01') {
    (*(code *)PTR_Capture_UpdateReadiness_00012788)();
  }
  else if (DAT_ffff8007 == '\x03') {
    Task_DispatchApplicationPhase();
  }
  (*(code *)PTR_OutputPins_ArbitrateSources_0001278c)();
  (*(code *)PTR_OutputPins_ApplyCommand_00012790)();
  return;
}

