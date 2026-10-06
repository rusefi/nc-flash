/* Ghidra analysis output; verify against original SH instructions. */

/* Only8020/8022bothzero:protected2310 decreasesbyD9E80~0.05 withfloor0
   via152FE;elseoriginalrecordheld. Invalidreaddefaults0.108cases andretained220serialcycles. */

int Control_DecayRetainedSource(void)

{
  int iVar1;
  float extraout_fr0;
  float fVar2;
  
  iVar1 = (*(code *)PTR_FUN_0005821c)
                    (*(undefined4 *)PTR_DAT_000581f0,PTR_Control_RetainedSourceFloor_000581e8);
  if ((*(short *)PTR_Control_RetainedDecayTimer_00058230 == 0) &&
     (iVar1 = (int)(char)*PTR_Control_RetainedDecayHoldoff_00058234, iVar1 == 0)) {
    if (extraout_fr0 <= *(float *)PTR_DAT_00058238) {
      fVar2 = 0.0;
    }
    else {
      fVar2 = extraout_fr0 - *(float *)PTR_DAT_00058238;
    }
    iVar1 = (*(code *)PTR_Protected_WriteFloatUnderInterruptMask_000581f4)
                      (fVar2,PTR_Control_RetainedSourceFloor_000581e8);
    return iVar1;
  }
  return iVar1;
}

