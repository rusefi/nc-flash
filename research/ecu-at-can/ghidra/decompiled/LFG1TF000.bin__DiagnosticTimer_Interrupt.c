/* Ghidra analysis output; verify against original SH instructions. */

/* 20isolatedprefixes,52operationaltimelineIRQs and24nativeinitializedstartupIRQs PASS.
   TSR3bit0clear,GR3A+15625,1218E,profileindex9; wholeRAMdifferential/exactMMIO/registerchecks.
   Startupmode3 producedbyoriginalcode; conditional500000phi/epoch/latency remainfixtures.
   tcu-diagnostic-startup.txt/tcu-diagnostic-timeline.txt. */

undefined8 DiagnosticTimer_Interrupt(void)

{
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar1;
  short *psVar2;
  
  psVar2 = (short *)(int)DAT_00016898;
  (*(code *)PTR_OutputTask_RecordInterruptEntry_000168a0)
            (9,(int)*(short *)(int)DAT_00016894 - (int)*psVar2);
  puVar1 = (ushort *)(int)DAT_00016892;
  if ((*puVar1 & 1) != 0) {
    *puVar1 = *puVar1 & (ushort)PTR_DAT_0001689c;
    *psVar2 = *psVar2 + DAT_00016896;
    (*(code *)PTR_DiagnosticTask_AdmitAndRun_000168a4)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_000168a8)(9);
  return CONCAT44(in_r1,in_r0);
}

