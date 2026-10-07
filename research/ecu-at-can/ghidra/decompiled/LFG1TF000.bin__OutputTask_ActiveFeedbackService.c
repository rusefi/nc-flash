/* Ghidra analysis output; verify against original SH instructions. */

/* Always188FC feedbackacquisition. Phase3 calls18830 adaptation and17B1A scan; phase<4
   service530C8/52EDC/18816 selectedchannel. Complete originaltask executed. See
   tcu-output-task.txt. */

void OutputTask_ActiveFeedbackService(void)

{
  byte bVar1;
  
  bVar1 = *PTR_DAT_00012850;
  (*(code *)PTR_OutputHandoff_AcquireSamples_0001286c)();
  if (bVar1 == 3) {
    (*(code *)PTR_OutputAdaptation_Dispatch_00012870)();
    (*(code *)PTR_OutputTask_ScanInputHistory_00012868)();
  }
  if (bVar1 < 4) {
    (*(code *)PTR_OutputRecord_ServiceChannel_00012874)(bVar1);
    (*(code *)PTR_OutputDriver_PrepareChannel_00012878)();
                    /* WARNING: Could not recover jumptable at 0x00012840. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (*(code *)PTR_OutputHandoff_ServiceChannel_0001287c)((int)(char)(bVar1 + 1));
    return;
  }
  return;
}

