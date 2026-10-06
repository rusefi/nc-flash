/* Ghidra analysis output; verify against original SH instructions. */

/* Updates9C82 and previous-source9C89 using9B40 values10/17,9C91,transition classifier49110 and
   signed80EA thresholds558/1211.6048 cases; tcu-phase-mode.txt. */

void PhaseMode_UpdateSourceLatch(undefined1 param_1)

{
  char cVar1;
  char cVar2;
  char cVar3;
  undefined1 uVar4;
  
  uVar4 = *PTR_PhaseMode_SourceLatch_000490fc;
  cVar1 = *PTR_Selection_SourceCode_00049100;
  cVar2 = *PTR_SourcePolicy_AdjustmentState_00049104;
  cVar3 = PhaseMode_ClassifyTransition(param_1);
  if (((cVar1 != '\n') && (cVar1 != '\x11')) || ((cVar2 == '\x02' && (cVar3 == '\x02')))) {
    uVar4 = 0;
  }
  if (((cVar1 == '\n') || (cVar1 == '\x11')) &&
     (((*(char *)(int)DAT_000490fa != '\n' && (*(char *)(int)DAT_000490fa != '\x11')) ||
      (((*(short *)PTR_PhaseMode_SourceHighThreshold_00049108 <= DAT_ffff80ea ||
        (DAT_ffff80ea < *(short *)PTR_PhaseMode_SourceLowThreshold_0004910c)) || (cVar2 == '\x01')))
      ))) {
    uVar4 = 1;
  }
  *(char *)(int)DAT_000490fa = cVar1;
  *PTR_PhaseMode_SourceLatch_000490fc = uVar4;
  return;
}

