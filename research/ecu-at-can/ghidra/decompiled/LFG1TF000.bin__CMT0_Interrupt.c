/* Ghidra analysis output; verify against original SH instructions. */

/* 516 differentialRAM prefixes through16DB6 beforeRTE: F712bit80 admission, secondstatusread
   ANDFF7F,123C2 callback; profile12, register/MMIO checks. No hardwaredelivery/cadence proof;
   tcu-cmt0-interrupt.txt. Joined320pairs execute32000 prefixes; independent320 recordedclock/wheel
   boundaries PASS. Latecaptureloss280 setsreferenceholdbit; tcu-cmt0-delivery.txt
   andtcu-clock-hold.txt. */

undefined8 CMT0_Interrupt(void)

{
  undefined *puVar1;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar2;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016dc4)(0xc,0);
  puVar1 = PTR_CMT0_AdmitTickAndTimerService_00016dcc;
  puVar2 = (ushort *)(int)DAT_00016dc0;
  if ((*puVar2 & 0x80) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_00016dc8;
    (*(code *)puVar1)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016dd0)(0xc);
  return CONCAT44(in_r1,in_r0);
}

