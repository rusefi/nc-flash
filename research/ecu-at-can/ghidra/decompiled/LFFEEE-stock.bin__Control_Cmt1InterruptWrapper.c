/* Ghidra analysis output; verify against original SH instructions. */

/* 576originalentry cases PASS, completeRAM/23stackwords andGPR/FPUstate.
   PushR0/PR/R1,3290save,nativeF28C withPR32D8. Retained10idleIRQcycles matchpriordirectrows
   afteronlyentryR4/PR accounting. VBRFFC50+300 points here; physicaladmission unproved.
   control-interrupt-timer.txt. */

void Control_Cmt1InterruptWrapper(void)

{
  (*(code *)PTR_Scheduler_SaveInterruptContext_00002f8c)();
                    /* WARNING: Could not recover jumptable at 0x00002f84. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_Control_Cmt1TimerCallback_00002f88)();
  return;
}

