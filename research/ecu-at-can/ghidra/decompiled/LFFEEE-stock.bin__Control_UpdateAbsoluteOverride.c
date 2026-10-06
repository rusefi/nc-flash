/* Ghidra analysis output; verify against original SH instructions. */

/* Stage5634>=3 plus previous565A0/current5635exact1 resets timer; otherwise old timer<=63
   follows8248+closed and increments, >63 ramps~0.008. Always upper cap closed+6. Updates even if
   enable zero; control-overrides.txt. */

void Control_UpdateAbsoluteOverride(void)

{
  char cVar1;
  undefined *puVar2;
  undefined2 uVar3;
  float fVar4;
  float fVar5;
  undefined4 uVar6;
  
  fVar4 = (float)(*(code *)PTR_FUN_000246c0)(PTR_Control_BoundedOverrideSource_000246bc);
  fVar5 = (float)(*(code *)PTR_FUN_000246a4)
                           (*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_0002469c,
                            PTR_DAT_000246a0);
  puVar2 = PTR_Control_AbsoluteOverrideTimer_000246b8;
  cVar1 = *PTR_DAT_000246c4;
  fVar4 = fVar4 + fVar5;
  if ((((byte)*PTR_DAT_000246c8 < 3) ||
      (*PTR_Control_PreviousAbsoluteOverrideEnable_000246cc != '\0')) || (cVar1 != '\x01')) {
    if (*(ushort *)PTR_DAT_000246d0 < *(ushort *)PTR_Control_AbsoluteOverrideTimer_000246b8) {
      fVar4 = (float)(*(code *)PTR_FUN_000246c0)(PTR_Control_AbsoluteOverrideValue_000246ac);
      fVar4 = fVar4 + *(float *)PTR_DAT_000246d8;
    }
    else {
      uVar3 = (*(code *)PTR_FUN_000246d4)
                        ((int)(short)*(ushort *)PTR_Control_AbsoluteOverrideTimer_000246b8,1);
      *(undefined2 *)puVar2 = uVar3;
    }
  }
  else {
    *(undefined2 *)PTR_Control_AbsoluteOverrideTimer_000246b8 = 0;
  }
  uVar6 = (*(code *)PTR_FUN_000246dc)(*(float *)PTR_DAT_000246a8 + fVar5,fVar4);
  (*(code *)PTR_FUN_000246b0)(uVar6,PTR_Control_AbsoluteOverrideValue_000246ac);
  *PTR_Control_PreviousAbsoluteOverrideEnable_000246cc = cVar1;
  return;
}

