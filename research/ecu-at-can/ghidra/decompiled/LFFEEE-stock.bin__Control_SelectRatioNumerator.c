/* Ghidra analysis output; verify against original SH instructions. */

/* 7016 exact1 clamps8030 to[8034,RTZ(8034+9.5)];otherwise8034. Original207C and96 directcases;
   control-ratio-inputs.txt. */

uint Control_SelectRatioNumerator(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  float fVar2;
  
  fVar2 = *(float *)PTR_Control_BaselineRatioNumerator_00058584;
  uVar1 = (*(code *)PTR_FUN_0005858c)(PTR_DAT_00058588);
  uVar1 = uVar1 & 0xff;
  if (uVar1 == 1) {
    uVar1 = (*(code *)PTR_FUN_00058598)
                      (*(undefined4 *)PTR_Control_CurrentRatioNumerator_00058594,fVar2,
                       *(float *)PTR_DAT_00058590 + fVar2);
    *(undefined4 *)PTR_Control_SelectedRatioNumerator_0005855c = extraout_fr0;
  }
  else {
    *(float *)PTR_Control_SelectedRatioNumerator_0005855c = fVar2;
  }
  return uVar1;
}

