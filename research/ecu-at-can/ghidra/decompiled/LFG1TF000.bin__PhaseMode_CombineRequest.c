/* Ghidra analysis output; verify against original SH instructions. */

/* 9C83 boolean=request9C84bit0 AND neither9C8Abit1 norbit2. Executed inside full49260;
   tcu-phase-mode.txt. */

void PhaseMode_CombineRequest(void)

{
  undefined1 uVar1;
  
  uVar1 = 0;
  if ((((*PTR_PhaseMode_RequestFlags_00049254 & 1) == 1) && ((*(byte *)(int)DAT_00049246 & 2) == 0))
     && ((*(byte *)(int)DAT_00049246 & 4) == 0)) {
    uVar1 = 1;
  }
  *PTR_PhaseMode_QualifiedRequest_00049258 = uVar1;
  return;
}

