/* Ghidra analysis output; verify against original SH instructions. */

/* Original285AE admission then285F0 monitor;972 cases and30 actualserial/application loss/recovery
   calls. Faultsets26,gatecloses27;goodreply alone cannotadvance recovery. */

void SCI1_ServiceMissingFeedbackMonitor(void)

{
  SCI1_AdmitMissingFeedbackMonitor();
  SCI1_UpdateMissingFeedbackMonitor();
  return;
}

