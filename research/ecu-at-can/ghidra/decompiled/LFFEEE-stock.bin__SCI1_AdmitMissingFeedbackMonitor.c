/* Ghidra analysis output; verify against original SH instructions. */

/* 57CC=(99D8bit15)&&(567A==1)&&(protected20A8/default0==0),stockB4 policy mask00800000.
   Gatebeforemonitor/reset;24E06/567A producer verified
   incontrol-admission.txt;earlierinputs/taskorderopen. */

undefined4 SCI1_AdmitMissingFeedbackMonitor(void)

{
  char cVar1;
  
  cVar1 = (*(code *)PTR_Diagnostic_CheckIndexedPolicyInhibit_0002864c)((int)DAT_0002862a);
  if (((cVar1 == '\0') && (*PTR_Control_LocalMissingFeedbackEnable_00028650 == '\x01')) &&
     (cVar1 = (*(code *)PTR_Protected_ReadByteOrDefault_00028634)
                        (PTR_SCI1_MissingFeedbackFault_00028638,0), cVar1 == '\0')) {
    *PTR_SCI1_MissingFeedbackMonitorEnabled_00028654 = 1;
    return 0;
  }
  *PTR_SCI1_MissingFeedbackMonitorEnabled_00028654 = 0;
  return 0;
}

