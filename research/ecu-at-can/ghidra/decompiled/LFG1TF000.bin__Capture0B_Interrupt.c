/* Ghidra analysis output; verify against original SH instructions. */

/* Originalprefix through16B92 beforeRTE: TSR0bit1 admission, secondwordread ANDFFFD, ICR0B32-bit
   ->17A58.512 pairedA/B differentialRAM/register/MMIO cases plus6rejections; profilingindex6.
   HardwareRTE/cadence/wiring unproved; tcu-capture-interrupts.txt. Joined320 recovery pairs
   execute560 originalcaptureISRprefixes with differentialRAM/register/MMIO checks; exactpriortrace
   afteronlynewobservations andcallbackPR normalization. See tcu-capture-delivery.txt; no
   hardwareadmission/cadence proof. Nativeinitialized3traces now291CMT1/423captureA/870captureB
   prefixes PASS withactualenablegating; no postadmissionhistoryreset.
   tcu-native-capture-startup.txt retainsfixtures/correctedA-onlygatedefect. */

undefined8 Capture0B_Interrupt(void)

{
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar1;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016b9c)(6,0);
  puVar1 = (ushort *)(int)DAT_00016b98;
  if ((*puVar1 & 2) != 0) {
    *puVar1 = *puVar1 & (ushort)PTR_DAT_00016ba0;
    (*(code *)PTR_Capture0B_ProcessCapturedCount_00016ba4)(*(undefined4 *)(int)DAT_00016b9a);
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016ba8)(6);
  return CONCAT44(in_r1,in_r0);
}

