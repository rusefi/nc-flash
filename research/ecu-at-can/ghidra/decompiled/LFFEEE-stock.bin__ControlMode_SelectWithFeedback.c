/* Ghidra analysis output; verify against original SH instructions. */

/* Priorityone-bit695B=80/40/20/10/08/04/02/01hex. Reads693E/F
   andpositive6914/16;entrymode/69AD/current6560
   controlssticky6956pair.10918direct/108caller/450retained/320pairedcycles;
   control-mode-feedback.txt. */

uint ControlMode_SelectWithFeedback(void)

{
  char cVar1;
  char cVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  undefined *puVar6;
  uint uVar7;
  undefined1 uVar8;
  float extraout_fr0;
  
  puVar6 = PTR_ControlMode_SelectedBit_00030240;
  cVar1 = *PTR_DAT_00030370;
  cVar2 = *PTR_DAT_00030374;
  bVar3 = *PTR_DAT_00030378;
  bVar4 = *PTR_DAT_0003037c;
  bVar5 = *PTR_DAT_00030380;
  if ((*PTR_DAT_00030384 & 0x10) == 0) {
    (*(code *)PTR_FUN_0003036c)(PTR_TargetRamp_FallSelector_00030368,0);
  }
  else if ((((*PTR_ControlMode_SelectedBit_00030240 & 0x10) != 0) &&
           (*PTR_ControlMode_PreviousSourceByte_00030454 == '\x01')) && (cVar1 == '\0')) {
    (*(code *)PTR_FUN_0003045c)(PTR_TargetRamp_FallSelector_00030458,1);
  }
  if (cVar2 == '\0') {
    if ((bVar3 == 0) &&
       (uVar7 = (*(code *)PTR_FUN_00030464)(PTR_SpeedCandidate_ProtectedSelected_00030460),
       *(float *)PTR_DAT_00030468 <= extraout_fr0)) {
      *puVar6 = (char)DAT_00030450;
      goto LAB_000304fe;
    }
    if (*PTR_DAT_0003046c != '\x01') goto LAB_000303f6;
    uVar8 = 0x40;
  }
  else {
LAB_000303f6:
    if ((cVar2 == '\0') && (*PTR_DAT_00030470 == '\x01')) {
      uVar8 = 0x20;
    }
    else {
      uVar7 = (uint)bVar4;
      if ((uVar7 != 0) || ((cVar2 != '\0' || (bVar3 != 1)))) {
LAB_000304b0:
        if (uVar7 == 1) {
          if (((cVar2 == '\0') && (bVar5 == 0)) && (bVar3 == 1)) {
            uVar8 = 4;
          }
          else {
            if (((cVar2 != '\0') || (uVar7 = (uint)bVar5, uVar7 != 1)) ||
               (uVar7 = (uint)bVar3, uVar7 != 1)) goto LAB_000304fa;
            uVar8 = 2;
          }
          uVar7 = (uint)bVar3;
          *puVar6 = uVar8;
        }
        else {
LAB_000304fa:
          *puVar6 = 1;
        }
        goto LAB_000304fe;
      }
      if ((*PTR_TargetFollow_FirstRetainedFlag_00030474 == '\x01') &&
         ((*(short *)PTR_ControlMode_FirstAdmissionCountdown_00030478 != 0 && (cVar1 == '\x01')))) {
        uVar8 = 0x10;
      }
      else {
        if ((*PTR_TargetFollow_SecondRetainedFlag_000305ec != '\x01') ||
           (*(short *)PTR_ControlMode_SecondAdmissionCountdown_000305f0 == 0)) goto LAB_000304b0;
        uVar8 = 8;
      }
    }
  }
  uVar7 = 1;
  *puVar6 = uVar8;
LAB_000304fe:
  *PTR_ControlMode_PreviousSourceByte_000305f4 = cVar1;
  return uVar7;
}

