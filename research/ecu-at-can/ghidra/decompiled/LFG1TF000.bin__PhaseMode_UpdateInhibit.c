/* Ghidra analysis output; verify against original SH instructions. */

/* 9C8Abit2 =request9C84bit0 AND9BFCbit5 AND(s16(80EA)>=12198 OR9B40 not10/17). Preserve other bits;
   tcu-phase-mode.txt. */

void PhaseMode_UpdateInhibit(void)

{
  bool bVar1;
  byte bVar2;
  byte *pbVar3;
  
  bVar1 = false;
  if (((*PTR_DAT_0004924c & 0x20) != 0) &&
     (((*(short *)PTR_PhaseMode_InhibitThreshold_00049250 <= DAT_ffff80ea ||
       ((*PTR_Selection_SourceCode_00049248 != '\n' &&
        (*PTR_Selection_SourceCode_00049248 != '\x11')))) &&
      ((*PTR_PhaseMode_RequestFlags_00049254 & 1) == 1)))) {
    bVar1 = true;
  }
  pbVar3 = (byte *)(int)DAT_00049246;
  if (bVar1) {
    bVar2 = *pbVar3 | 4;
  }
  else {
    bVar2 = *pbVar3 & 0xfb;
  }
  *pbVar3 = bVar2;
  return;
}

