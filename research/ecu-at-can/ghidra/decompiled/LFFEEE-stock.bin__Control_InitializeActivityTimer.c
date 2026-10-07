/* Ghidra analysis output; verify against original SH instructions. */

/* 64wholeRAMcases:stock8FD4=640(sum E0862/64/66),8FD6/7=E0860=40,thenfalls
   through6F2C8thresholdflags. ActualinitializerPR1712C verified. Doesnotreset9158/915E/915C. */

undefined4 Control_InitializeActivityTimer(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  undefined2 uVar3;
  float fVar4;
  float extraout_fr0;
  float extraout_fr0_00;
  
  uVar2 = (*(code *)PTR_FUN_0006f4c8)
                    ((int)*(short *)PTR_DAT_0006f4c4,(int)*(short *)PTR_DAT_0006f4c0);
  uVar3 = (*(code *)PTR_FUN_0006f4c8)(uVar2,(int)*(short *)PTR_DAT_0006f4cc);
  *(undefined2 *)PTR_Control_ActivityHoldCounter_0006f4d0 = uVar3;
  puVar1 = PTR_DAT_0006f4d4;
  *PTR_DAT_0006f4d8 = *PTR_DAT_0006f4d4;
  *PTR_DAT_0006f4dc = *puVar1;
  puVar1 = PTR_FUN_0006f4e0;
  fVar4 = (float)(*(code *)PTR_FUN_0006f4e0)(PTR_Control_RawSecondPublished_0006f4e4);
  if (fVar4 < *(float *)PTR_DAT_0006f4e8) {
    fVar4 = (float)(*(code *)puVar1)(PTR_Control_RawSecondPublished_0006f4e4);
    if (fVar4 < *(float *)PTR_DAT_0006f4e8 - *(float *)PTR_DAT_0006f4f0) {
      *PTR_Control_ActivityFirstThresholdFlag_0006f4ec = 0;
    }
  }
  else {
    *PTR_Control_ActivityFirstThresholdFlag_0006f4ec = 1;
  }
  uVar2 = (*(code *)puVar1)(PTR_Control_RawFirstPublished_0006f4f4);
  if (extraout_fr0 < *(float *)PTR_DAT_0006f4f8) {
    uVar2 = (*(code *)puVar1)(PTR_Control_RawFirstPublished_0006f4f4);
    if (extraout_fr0_00 < *(float *)PTR_DAT_0006f4f8 - *DAT_0006f500) {
      *PTR_Control_ActivitySecondThresholdFlag_0006f4fc = 0;
    }
  }
  else {
    *PTR_Control_ActivitySecondThresholdFlag_0006f4fc = 1;
  }
  return uVar2;
}

