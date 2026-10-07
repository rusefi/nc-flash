/* Ghidra analysis output; verify against original SH instructions. */

/* 8988 direct/13 retained/8 corrected consumerreplays; consumerconfigure movedbefore
   offsetproduction.12 originalqueue traces nowcomplete on producedphase1. Accepteddecrease
   cancapture beforetailtimerreset. See tcu-adjustment-queue.txt; cadence/physicalidentity unproved.
    */

void StoredAdjustment_RunLifecycle(void)

{
  undefined *puVar1;
  char cVar2;
  undefined1 uVar3;
  byte bVar4;
  short *psVar5;
  byte *pbVar6;
  char cVar7;
  
  bVar4 = CAN231_SixStateSource;
  cVar7 = *(char *)(int)DAT_00049bc6;
  StoredAdjustment_UpdateEventHistory();
  StoredAdjustment_UpdateTransitionHistory();
  cVar2 = StoredAdjustment_AdmitLifecycle();
  if (cVar2 == '\x01') {
    if (cVar7 == '\0') {
      cVar2 = StoredAdjustment_AdmitCapture();
      if (cVar2 == '\x01') {
        psVar5 = (short *)(int)DAT_00049bc8;
        *psVar5 = (short)DAT_ffff8089;
        *(undefined2 *)(int)DAT_00049bca = DAT_ffff80ea;
        *(undefined2 *)(int)DAT_00049bcc = Phase_MeasuredSourceSample;
        uVar3 = (*(code *)PTR_ApplicationPhase_ReadForCode_00049bd8)((int)*psVar5);
        *(undefined1 *)(int)DAT_00049bce = uVar3;
        cVar7 = '\x01';
      }
      goto LAB_00049b84;
    }
    if (cVar7 != '\x01') goto LAB_00049b84;
    StoredAdjustment_RetainSignedPeak();
    cVar2 = StoredAdjustment_ShouldAbort();
    if (cVar2 != '\x01') {
      cVar2 = StoredAdjustment_DetectCompletion();
      if (cVar2 != '\x01') goto LAB_00049b84;
      StoredAdjustment_UpdateFromCapturedInputs();
    }
  }
  cVar7 = '\0';
LAB_00049b84:
  pbVar6 = (byte *)(int)DAT_00049bd0;
  if (bVar4 < *pbVar6) {
    *PTR_StoredAdjustment_CaptureQualificationTimer_00049bdc = 0;
  }
  puVar1 = PTR_Phase_HasPendingWork_00049be0;
  *(char *)(int)DAT_00049bc6 = cVar7;
  *pbVar6 = bVar4;
  uVar3 = (*(code *)puVar1)();
  *(undefined1 *)(int)DAT_00049bd2 = uVar3;
  pbVar6 = (byte *)(int)DAT_00049bd4;
  if ((*PTR_DAT_00049be4 & 1) == 0) {
    bVar4 = *pbVar6 & 0xfe;
  }
  else {
    bVar4 = *pbVar6 | 1;
  }
  *pbVar6 = bVar4;
  return;
}

