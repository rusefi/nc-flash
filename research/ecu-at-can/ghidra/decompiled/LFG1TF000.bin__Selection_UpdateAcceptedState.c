/* Ghidra analysis output; verify against original SH instructions. */

/* 488F4 candidatehold ->47B3C nextindex ->48174 acceptance. Updates8081
   onlypending/admittedchange;8085=next evenwhenblocked.144 pairedTCU-CAN231-ECU cases,7 gate and8
   delay checkpoints; selection-reporting.txt. */

void Selection_UpdateAcceptedState(void)

{
  undefined *puVar1;
  byte bVar2;
  byte bVar3;
  byte bVar8;
  uint uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined1 uVar9;
  char cVar10;
  byte bVar11;
  char *pcVar12;
  byte *pbVar13;
  byte *pbVar14;
  
  bVar2 = TransmissionStateClass;
  bVar8 = (*(code *)PTR_Selection_AdmitDelayedCandidate_00048d38)();
  bVar3 = CAN231_SixStateSource;
  pbVar13 = (byte *)(int)DAT_00048d2a;
  bVar11 = *pbVar13;
  if (bVar8 != DAT_00048d2c) {
    bVar11 = bVar8;
  }
  *pbVar13 = bVar11;
  pcVar12 = (char *)(int)DAT_00048d2e;
  uVar4 = (*(code *)PTR_FUN_00048d3c)((int)*pcVar12,(int)(char)*pbVar13);
  uVar5 = (*(code *)PTR_Transition_SelectOperation_00048d40)((int)*pcVar12,uVar4);
  uVar6 = (*(code *)PTR_Transition_ClassifyProposal_00048d44)(uVar5,uVar4);
  puVar1 = PTR_Transition_SelectOperation_00048d40;
  pbVar13 = (byte *)(int)DAT_00048d30;
  pbVar14 = (byte *)(int)DAT_00048d32;
  if ((uVar4 & 0xff) != (uint)*pbVar14) {
    *pbVar13 = *pbVar13 | 1;
    *pbVar14 = (byte)uVar4;
    uVar5 = (*(code *)puVar1)((int)*pcVar12,(int)(char)*pbVar14);
    uVar6 = (*(code *)PTR_Transition_ClassifyProposal_00048d44)(uVar5,(int)(char)*pbVar14);
    *(char *)(int)DAT_00048d34 = (char)uVar5;
  }
  PhaseMode_UpdateSourceLatch(uVar6);
  uVar7 = (*(code *)PTR_Selection_CheckTransitionAcceptance_00048d48)(uVar6,uVar5);
  (*(code *)PTR_PhaseMode_ProduceQualificationMode_00048d4c)(uVar7,(int)(char)*pbVar14);
  if ((((*pbVar13 & 1) == 1) && ((char)uVar7 == '\x01')) &&
     (*pbVar13 = *pbVar13 & 0xfe, bVar3 != *pbVar14)) {
    *pcVar12 = (char)uVar6;
    *(char *)(int)DAT_00048d34 = (char)uVar5;
    *PTR_DAT_00048d50 = bVar3;
    CAN231_SixStateSource = *pbVar14;
    if (bVar2 != 0xff) {
      uVar9 = FUN_00048d84();
      *PTR_DAT_00048d54 = uVar9;
      Transition_BuildWorkRecords();
    }
  }
  if (5 < CAN231_SixStateSource) {
    CAN231_SixStateSource = 5;
  }
  (*(code *)PTR_StateCache_WriteByte_00048d58)(0x13,(int)(char)CAN231_SixStateSource);
  cVar10 = (*(code *)PTR_Phase_HasPendingWork_00048d5c)();
  if ((bVar2 == 0xff) && (cVar10 != '\0')) {
    (*(code *)PTR_FUN_00048d60)();
  }
  Selection_NextIndex = *pbVar14;
  return;
}

