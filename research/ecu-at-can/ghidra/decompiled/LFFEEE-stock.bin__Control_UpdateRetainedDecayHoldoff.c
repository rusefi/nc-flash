/* Ghidra analysis output; verify against original SH instructions. */

/* Ifcurrent8020zeroand(previous8024nonzeroorhold8022zero),load3;elsedecrement8022nonzero.
   Savecurrent8020to8024. Repeatedzero producesfourcallcadence. */

void Control_UpdateRetainedDecayHoldoff(void)

{
  short sVar1;
  undefined *puVar2;
  
  puVar2 = PTR_Control_PreviousRetainedDecayTimer_00058264;
  sVar1 = *(short *)PTR_Control_RetainedDecayTimer_00058230;
  if (((*(short *)PTR_Control_PreviousRetainedDecayTimer_00058264 == 0) || (sVar1 != 0)) &&
     ((*PTR_Control_RetainedDecayHoldoff_00058234 != '\0' || (sVar1 != 0)))) {
    if (*PTR_Control_RetainedDecayHoldoff_00058234 != '\0') {
      *PTR_Control_RetainedDecayHoldoff_00058234 =
           *PTR_Control_RetainedDecayHoldoff_00058234 + (char)DAT_00058300;
    }
  }
  else {
    *PTR_Control_RetainedDecayHoldoff_00058234 = *PTR_DAT_00058268;
  }
  *(short *)puVar2 = sVar1;
  return;
}

