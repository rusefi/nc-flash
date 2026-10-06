/* Ghidra analysis output; verify against original SH instructions. */

/* 5668<50 writes1; ==50 feedback5534 minus protected closed2114; >50 add~0.3 capped~11.6. Finite
   RTZ oracle and retained serial lifecycle; control-overrides.txt. */

void Control_UpdateRelativeOverride(void)

{
  float fVar1;
  float fVar2;
  
  if (*(ushort *)PTR_Control_RelativeOverrideTimer_00023a8c < *(ushort *)PTR_DAT_00023a90) {
    fVar2 = *(float *)PTR_DAT_00023a94;
  }
  else if (*(ushort *)PTR_Control_RelativeOverrideTimer_00023a8c == *(ushort *)PTR_DAT_00023a90) {
    fVar2 = (float)(*(code *)PTR_FUN_00023a9c)(PTR_SCI1_ProtectedFeedbackValue_00023a98);
    fVar1 = (float)(*(code *)PTR_FUN_00023aa8)
                             (*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_00023aa0,
                              PTR_DAT_00023aa4);
    fVar2 = fVar2 - fVar1;
  }
  else {
    fVar2 = (float)(*(code *)PTR_FUN_00023a9c)(PTR_Control_RelativeOverrideValue_00023a84);
    fVar2 = (float)(*(code *)PTR_FUN_00023ab4)
                             (*(undefined4 *)PTR_DAT_00023ab0,fVar2 + *(float *)PTR_DAT_00023aac);
  }
  (*(code *)PTR_FUN_00023a88)(fVar2,PTR_Control_RelativeOverrideValue_00023a84);
  return;
}

