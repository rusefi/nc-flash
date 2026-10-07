/* Ghidra analysis output; verify against original SH instructions. */

/* Originaltask3queuecallback callsCADE/B31C/D3FC/D770 then215C6->event2queue3/task4, tailsD02E.
   Full600timerdrainsPASS withboundedSCI4/peripheralfixtures; all120monitoredtractionfields
   exactpriortrace. No serialpeer/controllerproof orallnestedbodyoracle. control-timer-event2.txt.
    */

void Control_RunPeriodicEventProducer(void)

{
  (*(code *)PTR_Input_UpdateLocalFilters_0000e6e4)();
  (*(code *)PTR_LAB_0000e6e8)();
  (*(code *)PTR_LAB_0000e6ec)();
  (*(code *)PTR_LAB_0000e6f0)();
  (*(code *)PTR_Control_RequestEvent2Wrapper_0000e6f4)();
                    /* WARNING: Could not recover jumptable at 0x0000e61e. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)PTR_LAB_0000e6f8)();
  return;
}

