/* Ghidra analysis output; verify against original SH instructions. */

/* OnadmittedCMT0 status, promotes800A1->3, preservesothermodes, tails128B6. Onlyinitial1/3
   executetick/elapsed/mixedtimer.516 ISRprefix differentialRAM andindependentmode/counter checks;
   tcu-cmt0-interrupt.txt. */

void CMT0_AdmitTickAndTimerService(void)

{
  if (DAT_ffff800a == '\x01') {
    DAT_ffff800a = '\x03';
  }
  (*(code *)PTR_Scheduler_ServiceCaptureElapsedWhenMode3_000123e8)();
  return;
}

