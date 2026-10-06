/* Ghidra analysis output; verify against original SH instructions. */

/* Select current8081 if low-byte r4 zero,else low-byte r5 proposal. Run48D70; selected0 uses
   exact9C82==1 and stock4925C,1 uses9B40 values10/17,2 uses produced9C83,other0. Writes
   boolean8086;3024 direct and180 selector cases,386 lifecycle calls. tcu-phase-mode.txt. */

void PhaseMode_ProduceQualificationMode(char param_1,uint param_2)

{
  char cVar1;
  char cVar2;
  
  cVar1 = *PTR_Selection_SourceCode_00049340;
  if (param_1 == '\0') {
    param_2 = (uint)(char)CAN231_SixStateSource;
  }
  (*(code *)PTR_PhaseMode_UpdateLocalFlags_00049344)(param_2);
  cVar2 = PhaseMode_AllowSourceLatch();
  param_2 = param_2 & 0xff;
  if (param_2 == 0) {
    if (*PTR_PhaseMode_SourceLatch_00049348 != '\x01') {
      Phase_AscendingQualificationMode = 0;
      return;
    }
  }
  else {
    if (param_2 == 1) {
      if (cVar1 == '\n') {
        Phase_AscendingQualificationMode = 1;
        return;
      }
      if (cVar1 == '\x11') {
        Phase_AscendingQualificationMode = 1;
        return;
      }
      Phase_AscendingQualificationMode = 0;
      return;
    }
    if (param_2 != 2) {
      Phase_AscendingQualificationMode = 0;
      return;
    }
    cVar2 = *PTR_PhaseMode_QualifiedRequest_0004934c;
  }
  if (cVar2 == '\x01') {
    Phase_AscendingQualificationMode = 1;
    return;
  }
  Phase_AscendingQualificationMode = 0;
  return;
}

