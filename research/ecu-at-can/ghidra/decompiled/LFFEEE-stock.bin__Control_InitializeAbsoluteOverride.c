/* Ghidra analysis output; verify against original SH instructions. */

/* Writes protected5650=closed2114+6 and timer5658=FFFF; leaves previous565A unchanged. Executed
   default/valid record cases. */

void Control_InitializeAbsoluteOverride(void)

{
  float fVar1;
  
  fVar1 = (float)(*(code *)PTR_FUN_000246a4)
                           (*(undefined4 *)PTR_ThrottleCandidate_DefaultClosedOffset_0002469c,
                            PTR_DAT_000246a0);
  (*(code *)PTR_FUN_000246b0)
            (fVar1 + *(float *)PTR_DAT_000246a8,PTR_Control_AbsoluteOverrideValue_000246ac);
  *(short *)PTR_Control_AbsoluteOverrideTimer_000246b8 = (short)DAT_000246b4;
  return;
}

