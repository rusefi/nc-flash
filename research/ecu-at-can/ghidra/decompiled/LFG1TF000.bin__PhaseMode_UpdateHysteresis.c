/* Ghidra analysis output; verify against original SH instructions. */

/* Request9C84bit0 enables retained9C8Abit1: set when s16(80EA)<2793,clear at>=2980 or request
   absent; preserve other bits. tcu-phase-mode.txt. */

void PhaseMode_UpdateHysteresis(void)

{
  byte bVar1;
  char cVar2;
  byte *pbVar3;
  
  pbVar3 = (byte *)(int)DAT_000491b6;
  cVar2 = -(((*pbVar3 & 2) == 0) + -1);
  if ((DAT_ffff80ea < *(short *)PTR_PhaseMode_HysteresisSetThreshold_000491bc) &&
     ((*PTR_PhaseMode_RequestFlags_000491b8 & 1) == 1)) {
    cVar2 = '\x01';
  }
  if ((*(short *)PTR_PhaseMode_HysteresisClearThreshold_000491c0 <= DAT_ffff80ea) ||
     ((*PTR_PhaseMode_RequestFlags_000491b8 & 1) == 0)) {
    cVar2 = '\0';
  }
  if (cVar2 == '\0') {
    bVar1 = *pbVar3 & 0xfd;
  }
  else {
    bVar1 = *pbVar3 | 2;
  }
  *pbVar3 = bVar1;
  return;
}

