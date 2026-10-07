/* Ghidra analysis output; verify against original SH instructions. */

/* 2816 isolatedcases plus93actual12712returnwholeRAM/MMIO checks in3nativecallertraces PASS. ADC-B3
   admitsreset/captureenable/age0/state2;age>=20->3. SubsequentapplicationIRQadmitsmode3.
   Explicitforeground/timestamp/cadence,no fullboot.
   tcu-capture-readiness.txt/tcu-readiness-admission.txt. */

void Capture_UpdateReadiness(void)

{
  undefined *UNRECOVERED_JUMPTABLE;
  char cVar1;
  
  cVar1 = *PTR_Capture_ReadinessState_00012354;
  if (cVar1 == '\x01') {
    if (*PTR_Startup_AdcBReadinessState_00012360 == '\x03') {
      (*(code *)PTR_Capture_ResetBothMeasurementHistories_00012364)();
      *PTR_Capture_ReadinessAge_0001235c = 0;
      cVar1 = '\x02';
      (*(code *)PTR_Capture0A_InitializeRisingEdge_00012368)();
      (*(code *)PTR_Capture0B_InitializeRisingEdge_0001236c)();
    }
  }
  else if ((cVar1 == '\x02') && (0x13 < (byte)*PTR_Capture_ReadinessAge_0001235c)) {
    cVar1 = '\x03';
  }
  UNRECOVERED_JUMPTABLE = PTR_LAB_00012370;
  *PTR_Capture_ReadinessState_00012354 = cVar1;
                    /* WARNING: Could not recover jumptable at 0x0001234a. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*(code *)UNRECOVERED_JUMPTABLE)();
  return;
}

