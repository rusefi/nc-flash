/* Ghidra analysis output; verify against original SH instructions. */

/* 2816 isolatedgatecases plus108actualapplicationISRprefixes in3initializedstartup traces PASS.
   Mode1 admits126DA onlyif84A0/84D8/84EC all3,thenmode3. Capturebecomes3 during126EC,soadmission
   requiresNEXTapplicationinterrupt. No forcedreadyflags/fullboot. tcu-readiness-admission.txt. */

void Task_AdmitApplicationMode(void)

{
  if ((((DAT_ffff8007 == '\x01') && (*PTR_Startup_AdcAReadinessState_00012258 == '\x03')) &&
      (*PTR_Startup_AdcBReadinessState_0001225c == '\x03')) &&
     (*PTR_Capture_ReadinessState_00012260 == '\x03')) {
    (*(code *)PTR_Task_AdmitInitializedApplication_00012264)();
    DAT_ffff8007 = '\x03';
  }
  (*(code *)PTR_Task_ServiceApplicationMode_00012268)();
  return;
}

