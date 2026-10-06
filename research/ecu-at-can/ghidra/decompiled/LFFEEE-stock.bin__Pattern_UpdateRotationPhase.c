/* Ghidra analysis output; verify against original SH instructions. */

/* Eligible level1..6 reload74F3=40 ifzero;elseposition7 decrements. Resultzero
   advances74F2,3->0.2160 cases and1280-event synthetic lifecycle. */

void Pattern_UpdateRotationPhase(void)

{
  undefined *puVar1;
  
  puVar1 = PTR_Pattern_RotationCountdown_0004637c;
  if ((*PTR_Pattern_Level_0004636c == 0) || (6 < (byte)*PTR_Pattern_Level_0004636c)) {
    *PTR_Pattern_RotationCountdown_0004637c = 0;
  }
  else if (*PTR_Pattern_RotationCountdown_0004637c == '\0') {
    *PTR_Pattern_RotationCountdown_0004637c = *PTR_DAT_00046380;
  }
  else if (*PTR_Pattern_EventPosition_00046384 == '\a') {
    *PTR_Pattern_RotationCountdown_0004637c =
         *PTR_Pattern_RotationCountdown_0004637c + (char)DAT_00046360;
  }
  if (*puVar1 == '\0') {
    if (*DAT_00046388 == '\x03') {
      *DAT_00046388 = '\0';
    }
    else {
      *DAT_00046388 = *DAT_00046388 + '\x01';
    }
  }
  return;
}

