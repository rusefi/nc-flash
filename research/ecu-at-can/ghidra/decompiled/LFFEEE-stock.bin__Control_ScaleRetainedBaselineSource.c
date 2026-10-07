/* Ghidra analysis output; verify against original SH instructions. */

/* 8098=RTZ(809C*A35E0(6D5C));80B4 stores factor. Stock seven knots all1. Full original body;
   control-baseline-source.txt. */

void Control_ScaleRetainedBaselineSource(void)

{
  undefined4 uVar1;
  float fVar2;
  
  uVar1 = (*(code *)PTR_FUN_00058c54)(PTR_SpeedCandidate_ProtectedSelected_00058c50);
  fVar2 = (float)(*(code *)PTR_Lookup_FloatCurve_00058c5c)(uVar1,DAT_00058c58);
  *(float *)PTR_Control_BaselineSourceScale_00058c60 = fVar2;
  *(float *)PTR_Control_ScaledRetainedBaselineSource_00058c68 =
       *(float *)PTR_Control_RetainedBaselineSource_00058c64 * fVar2;
  return;
}

