/* Ghidra analysis output; verify against original SH instructions. */

/* Uses previous signed9BF6/9BF8 before fresh capture. Stock A>=32000 sets, A<14720 clears,
   intermediate retains9BF5bit3; B drops out because paired A thresholds equal. Updates9AEA bit2 and
   active writes source6.300 cases; source publication independent of later admission. */

void Selection_UpdateOverlayHysteresis(void)

{
  short sVar1;
  byte bVar2;
  char cVar3;
  byte *pbVar4;
  
  pbVar4 = (byte *)(int)DAT_00046606;
  sVar1 = *(short *)(int)DAT_00046608;
  cVar3 = -(((*pbVar4 & 8) == 0) + -1);
  if ((*(short *)PTR_Selection_OverlayHysteresisCalibration_0004660c <= sVar1) ||
     ((*(short *)PTR_Selection_OverlayHysteresisCalibration_1__00046610 <= sVar1 &&
      (*(short *)PTR_Selection_OverlayHysteresisCalibration_2__00046614 <=
       *(short *)(int)DAT_0004660a)))) {
    cVar3 = '\x01';
  }
  if ((sVar1 < *(short *)PTR_Selection_OverlayHysteresisCalibration_3__00046618) ||
     ((sVar1 < *(short *)PTR_Selection_OverlayHysteresisCalibration_4__0004661c &&
      (*(short *)(int)DAT_0004660a <
       *(short *)PTR_Selection_OverlayHysteresisCalibration_5__00046620)))) {
    cVar3 = '\0';
  }
  if (cVar3 == '\0') {
    bVar2 = *pbVar4 & 0xf7;
  }
  else {
    bVar2 = *pbVar4 | 8;
  }
  *pbVar4 = bVar2;
  if (cVar3 == '\x01') {
    *PTR_Selection_SourceCode_00046624 = 6;
  }
  if (cVar3 == '\0') {
    bVar2 = *PTR_DAT_00046628 & 0xfb;
  }
  else {
    bVar2 = *PTR_DAT_00046628 | 4;
  }
  *PTR_DAT_00046628 = bVar2;
  return;
}

