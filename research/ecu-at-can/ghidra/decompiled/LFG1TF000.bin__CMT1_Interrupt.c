/* Ghidra analysis output; verify against original SH instructions. */

/* Originalprefix through16D3E beforeRTE; status admission/promote8009/wheel/profile13.1024
   independentwholeRAM cases. Joined320pairs/2560prefixes PASS with32000CMT0,560capture,80actualhold
   returns; exactprior320. Supplied100:8 schedule differs fromconditionalconfigured256:125;
   nohardwarecadence proof. tcu-cmt1-delivery.txt andtcu-cmt-configuration.txt.
   Nativeinitialized3traces now291CMT1/423captureA/870captureB prefixes PASS withactualenablegating;
   no postadmissionhistoryreset. tcu-native-capture-startup.txt
   retainsfixtures/correctedA-onlygatedefect. */

undefined8 CMT1_Interrupt(void)

{
  undefined *puVar1;
  undefined4 in_r0;
  undefined4 in_r1;
  ushort *puVar2;
  
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016d4c)(0xd,0);
  puVar1 = PTR_Timer_PromoteAndServiceMode_00016d54;
  puVar2 = (ushort *)(int)DAT_00016d48;
  if ((*puVar2 & 0x80) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_00016d50;
    (*(code *)puVar1)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016d58)(0xd);
  return CONCAT44(in_r1,in_r0);
}

