/* Ghidra analysis output; verify against original SH instructions. */

/* Originalprefix through16CCA beforeRTE: TSR0bit0 admission, secondwordread ANDFFFE, ICR0A32-bit
   ->179A8.512 pairedA/B differentialRAM/register/MMIO cases plus6rejections; profilingindex5.
   HardwareRTE/cadence/wiring unproved; tcu-capture-interrupts.txt. Joined320 recovery pairs
   execute560 originalcaptureISRprefixes with differentialRAM/register/MMIO checks; exactpriortrace
   afteronlynewobservations andcallbackPR normalization. See tcu-capture-delivery.txt; no
   hardwareadmission/cadence proof. Nativeinitialized3traces now291CMT1/423captureA/870captureB
   prefixes PASS withactualenablegating; no postadmissionhistoryreset.
   tcu-native-capture-startup.txt retainsfixtures/correctedA-onlygatedefect. */

undefined8 Capture0A_Interrupt(void)

{
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar1;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016cd4)(5,0);
  puVar1 = (ushort *)(int)DAT_00016cd0;
  if ((*puVar1 & 1) != 0) {
    *puVar1 = *puVar1 & (ushort)PTR_DAT_00016cd8;
    (*(code *)PTR_Capture0A_ProcessCapturedCount_00016cdc)(*(undefined4 *)(int)DAT_00016cd2);
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016ce0)(5);
  return CONCAT44(in_r1,in_r0);
}

