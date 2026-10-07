/* Ghidra analysis output; verify against original SH instructions. */

/* Fullstock priority/body verification:4991 totaldispatcher/localgate cases;32pairedTCU/CAN/serial
   lifecycle. Thresholdstates,bypass,firstnonzero priority andretained5675
   checked;control-admission.txt. */

void Control_DispatchCommandOverrides(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  short sVar4;
  undefined *puVar5;
  undefined4 uVar6;
  char cVar7;
  char cVar8;
  char cVar9;
  char cVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  uint uVar14;
  int iVar15;
  float fVar16;
  float fVar17;
  float fVar18;
  undefined1 local_2c;
  
  fVar16 = (float)(*(code *)PTR_FUN_000249f0)(PTR_Control_RawFirstPublished_000249ec);
  fVar17 = (float)(*(code *)PTR_FUN_000249f0)(PTR_DAT_000249f4);
  fVar18 = *(float *)PTR_Control_FilteredLocalSource_000249f8;
  if (fVar18 < *(float *)PTR_DAT_000249fc) {
    if (fVar18 < *(float *)PTR_DAT_000249fc - *(float *)PTR_DAT_00024a04) {
      *PTR_Control_ThresholdState_568A_00024a00 = 0;
    }
  }
  else {
    *PTR_Control_ThresholdState_568A_00024a00 = 1;
  }
  if (fVar18 < *(float *)PTR_DAT_00024a08) {
    if (fVar18 < *(float *)PTR_DAT_00024a10) {
      *PTR_Control_ThresholdState_568B_00024a0c = 0;
    }
  }
  else {
    *PTR_Control_ThresholdState_568B_00024a0c = 1;
  }
  fVar18 = DAT_00024a18;
  if (fVar16 < *(float *)PTR_DAT_00024a1c) {
    if (fVar16 < *(float *)PTR_DAT_00024a1c + DAT_00024a18) {
      *PTR_Control_ThresholdState_568D_00024a14 = 0;
    }
  }
  else {
    *PTR_Control_ThresholdState_568D_00024a14 = 1;
  }
  if (fVar16 < *(float *)PTR_DAT_00024a24) {
    if (fVar16 < *(float *)PTR_DAT_00024a24 + fVar18) {
      *PTR_Control_ThresholdState_568E_00024a20 = 0;
    }
  }
  else {
    *PTR_Control_ThresholdState_568E_00024a20 = 1;
  }
  if (fVar17 < *(float *)PTR_DAT_00024a2c) {
    if (fVar17 < *(float *)PTR_DAT_00024a2c - *(float *)PTR_DAT_00024bd4) {
      *PTR_Control_ThresholdState_568C_00024a28 = 0;
    }
  }
  else {
    *PTR_Control_ThresholdState_568C_00024a28 = 1;
  }
  uVar6 = (*(code *)PTR_FUN_00024bdc)(PTR_Control_FilteredModeInput_00024bd8);
  puVar5 = PTR_Protected_ReadByteOrDefault_00024be4;
  cVar1 = *PTR_Control_QualifiedSerialFeedback_00024be0;
  cVar7 = (*(code *)PTR_Protected_ReadByteOrDefault_00024be4)(PTR_DAT_00024be8,0);
  cVar8 = (*(code *)puVar5)(PTR_DAT_00024bec,0);
  cVar9 = (*(code *)puVar5)(PTR_SCI1_MissingFeedbackFault_00024bf0,0);
  uVar14 = 0;
  uVar11 = 0;
  cVar2 = *PTR_Control_ModeZeroTimerEligible_00024bf4;
  uVar12 = 0;
  uVar13 = 0;
  cVar3 = *PTR_DAT_00024bf8;
  iVar15 = (int)*(short *)PTR_Control_ModeZeroTimer_00024bfc;
  sVar4 = *(short *)PTR_Control_ModeOneTimer_00024c00;
  local_2c = 0;
  cVar10 = Control_CheckOverrideBypass(uVar6,iVar15,(int)cVar3);
  if (cVar10 == '\0') {
    uVar14 = Control_AdmitHighestPriorityOverride
                       (fVar17,uVar6,iVar15,(int)cVar1,(int)cVar7,(int)cVar9);
    if ((uVar14 & 0xff) == 0) {
      uVar11 = Control_AdmitFeedbackOverride
                         (uVar6,iVar15,(int)sVar4,(int)cVar1,(int)cVar9,(int)cVar7,(int)cVar8,
                          (int)(char)*PTR_Control_ThresholdState_568A_00024c04,(int)cVar2);
      if ((uVar11 & 0xff) == 0) {
        uVar12 = Control_AdmitRelativeOverride
                           (uVar6,iVar15,(int)sVar4,(int)cVar7,(int)cVar8,
                            (int)(char)*PTR_Control_ThresholdState_568B_00024c08,(int)cVar2,
                            (int)cVar3);
        if (((uVar12 & 0xff) == 0) &&
           (uVar13 = Control_ReadAbsoluteOverrideRequest(), (uVar13 & 0xff) == 0)) {
          local_2c = 1;
        }
      }
    }
  }
  *PTR_Control_OverrideBypassResult_00024c0c = cVar10;
  puVar5 = PTR_FUN_00024c10;
  (*(code *)PTR_FUN_00024c10)(PTR_DAT_00024c14,uVar14);
  (*(code *)puVar5)(PTR_Control_FeedbackOverrideEnabled_00024c18,uVar11);
  (*(code *)puVar5)(PTR_DAT_00024c1c,uVar12);
  (*(code *)puVar5)(PTR_DAT_00024c20,uVar13);
  *PTR_Control_NoOverrideRequested_00024c24 = local_2c;
  return;
}

