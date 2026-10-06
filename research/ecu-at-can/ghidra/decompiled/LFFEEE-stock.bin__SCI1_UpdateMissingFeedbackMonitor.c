/* Ghidra analysis output; verify against original SH instructions. */

/* 5578==0 loss;57CCexact1 enablesbad/good counters. OLD25sets20A8;OLD250sets57CD.9462exact1
   resets.432cases+28transport/applicationlosssteps withgatefixture. */

uint SCI1_UpdateMissingFeedbackMonitor(void)

{
  char cVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar6;
  uint uVar5;
  
  puVar4 = PTR_SCI1_PresentFeedbackCounter_00028660;
  puVar3 = PTR_SCI1_MissingFeedbackCounter_0002865c;
  puVar2 = PTR_SCI1_FeedbackMissing_0002862c;
  cVar1 = *PTR_SCI1_ApplicationFeedbackReceived_00028658;
  cVar6 = (*(code *)PTR_FUN_00028668)(PTR_DAT_00028664);
  if (cVar6 == '\x01') {
    *(undefined2 *)puVar4 = 0;
    *(undefined2 *)puVar3 = 0;
    *puVar2 = 0;
    uVar5 = (*(code *)PTR_FUN_0002863c)(PTR_SCI1_MissingFeedbackFault_00028638,0);
    *PTR_SCI1_FeedbackRecoveryLatch_0002866c = 0;
  }
  else {
    if (cVar1 == '\0') {
      *puVar2 = 1;
    }
    else {
      *puVar2 = 0;
    }
    uVar5 = (uint)(byte)*PTR_SCI1_MissingFeedbackMonitorEnabled_000286e4;
    if (uVar5 == 1) {
      if (cVar1 == '\0') {
        if (*(ushort *)PTR_DAT_000286e8 <= *(ushort *)puVar3) {
          (*(code *)PTR_FUN_000286f0)(PTR_SCI1_MissingFeedbackFault_000286ec,1);
        }
        uVar5 = (*(code *)PTR_FUN_000286f4)((int)*(short *)puVar3,1);
        *(short *)puVar3 = (short)uVar5;
        *(undefined2 *)puVar4 = 0;
      }
      else {
        if (*(ushort *)PTR_DAT_000286f8 <= *(ushort *)puVar4) {
          *PTR_SCI1_FeedbackRecoveryLatch_000286fc = 1;
        }
        uVar5 = (*(code *)PTR_FUN_000286f4)((int)*(short *)puVar4,1);
        *(short *)puVar4 = (short)uVar5;
        *(undefined2 *)puVar3 = 0;
      }
    }
    else {
      *(undefined2 *)puVar4 = 0;
      *(undefined2 *)puVar3 = 0;
    }
  }
  return uVar5;
}

