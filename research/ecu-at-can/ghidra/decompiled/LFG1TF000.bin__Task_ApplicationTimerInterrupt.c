/* Ghidra analysis output; verify against original SH instructions. */

/* 26isolatedprefixes through16B00preRTE plus320retainedprefixes PASS;
   F460clear/F454+2560/1220A->126EC, independentprofile andexistingcommand/pin oracles.
   Conditional81920phi,1310CMT0/640CMT1,12comparewraps;
   explicitepoch/capture/CAN/diagnosticfixtures. Two creations/16acks; phaseindex1code5
   stillpending319. tcu-application-clock.txt; nofullboot/physicaltimingproof. */

undefined8 Task_ApplicationTimerInterrupt(void)

{
  undefined4 in_r0;
  byte bVar1;
  undefined4 in_r1;
  ushort *puVar2;
  short *psVar3;
  undefined4 uVar4;
  
  bVar1 = *PTR_Task_ApplicationPhaseCounter_00016b10 & 7;
  if (((*PTR_Task_ApplicationPhaseCounter_00016b10 & 7) != 0) && (bVar1 != 4)) {
    if ((bVar1 == 1) || (bVar1 == 5)) {
      uVar4 = 1;
      goto LAB_00016ab2;
    }
    if ((bVar1 == 2) || (bVar1 == 6)) {
      uVar4 = 2;
      goto LAB_00016ab2;
    }
    if (bVar1 == 3) {
      uVar4 = 3;
      goto LAB_00016ab2;
    }
    if (bVar1 == 7) {
      uVar4 = 4;
      goto LAB_00016ab2;
    }
  }
  uVar4 = 0;
LAB_00016ab2:
  psVar3 = (short *)(int)DAT_00016b0a;
  (*(code *)PTR_OutputTask_RecordInterruptEntry_00016b14)
            (uVar4,(int)*(short *)(int)DAT_00016b06 - (int)*psVar3);
  puVar2 = (ushort *)(int)DAT_00016b0c;
  if ((*puVar2 & 1) != 0) {
    *puVar2 = *puVar2 & (ushort)PTR_DAT_00016b18;
    *psVar3 = *psVar3 + DAT_00016b08;
    (*(code *)PTR_Task_AdmitApplicationMode_00016b1c)();
  }
  (*(code *)PTR_OutputTask_RecordInterruptExit_00016b20)(uVar4);
  return CONCAT44(in_r1,in_r0);
}

