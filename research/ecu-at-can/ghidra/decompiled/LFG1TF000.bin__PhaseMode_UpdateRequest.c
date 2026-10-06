/* Ghidra analysis output; verify against original SH instructions. */

/* 9C84bit0=request when selected state2 AND(9B40 in10/17/13/14 OR9ACDbit4 OR9C00bit4). Other bits
   preserved; tcu-phase-mode.txt. */

void PhaseMode_UpdateRequest(char param_1)

{
  char cVar1;
  bool bVar2;
  byte bVar3;
  
  cVar1 = *PTR_Selection_SourceCode_00049340;
  bVar2 = false;
  if (((((cVar1 == '\n') || (cVar1 == '\x11')) || (cVar1 == '\r')) ||
      (((cVar1 == '\x0e' || ((*PTR_DAT_00049350 & 0x10) != 0)) || ((*PTR_DAT_00049354 & 0x10) != 0))
      )) && (param_1 == '\x02')) {
    bVar2 = true;
  }
  if (bVar2) {
    bVar3 = *PTR_PhaseMode_RequestFlags_00049358 | 1;
  }
  else {
    bVar3 = *PTR_PhaseMode_RequestFlags_00049358 & 0xfe;
  }
  *PTR_PhaseMode_RequestFlags_00049358 = bVar3;
  return;
}

