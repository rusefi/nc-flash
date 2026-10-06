/* Ghidra analysis output; verify against original SH instructions. */

/* 7242zero clears8100;nonzero withold8114=0and8104=0
   pulses80F8*.1*8110*(8040exact1?.9:1);elsedecay.005floor0.
   Exact7242=1andold8114=0reloads8104=12evenifpulseblocked;elsecountdown. Savesraw7242to8114. */

uint Control_UpdateMagnitudePulse(void)

{
  undefined *puVar1;
  byte bVar2;
  uint uVar3;
  undefined4 uVar4;
  float fVar5;
  
  bVar2 = (*(code *)PTR_FUN_000594dc)(PTR_DAT_000594d8);
  puVar1 = PTR_Control_MagnitudeActivationCorrection_000594e0;
  uVar3 = (uint)bVar2;
  if (uVar3 == 0) {
    *(undefined4 *)PTR_Control_MagnitudeActivationCorrection_000594e0 = 0;
  }
  else if ((*PTR_Control_PreviousMagnitudeGate_000594e4 == '\0') &&
          (*PTR_Control_MagnitudeRetriggerHoldoff_000594e8 == '\0')) {
    if (*PTR_DAT_000594ec == '\x01') {
      fVar5 = *(float *)PTR_DAT_000594f0;
    }
    else {
      fVar5 = 1.0;
    }
    *(float *)PTR_Control_MagnitudeActivationCorrection_000594e0 =
         *(float *)PTR_Control_MagnitudePulseScale_000594f8 * *(float *)PTR_DAT_000594f4 *
         *(float *)PTR_Control_MagnitudeInputFactor_000594c0 * fVar5;
  }
  else {
    uVar4 = (*(code *)PTR_FUN_000594cc)
                      (*(float *)PTR_Control_MagnitudeActivationCorrection_000594e0 -
                       *(float *)PTR_DAT_000594fc,0);
    *(undefined4 *)puVar1 = uVar4;
  }
  if ((uVar3 == 1) && (*PTR_Control_PreviousMagnitudeGate_000594e4 == '\0')) {
    uVar3 = (uint)(char)*PTR_DAT_00059500;
    *PTR_Control_MagnitudeRetriggerHoldoff_000594e8 = *PTR_DAT_00059500;
  }
  else if (*PTR_Control_MagnitudeRetriggerHoldoff_000594e8 != '\0') {
    *PTR_Control_MagnitudeRetriggerHoldoff_000594e8 =
         *PTR_Control_MagnitudeRetriggerHoldoff_000594e8 + (char)DAT_000594ae;
  }
  *PTR_Control_PreviousMagnitudeGate_000594e4 = bVar2;
  return uVar3;
}

