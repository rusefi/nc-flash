/* Ghidra analysis output; verify against original SH instructions. */

/* 803C=RTZ(RTZ(6DC4*353.016296)/RTZ(RTZ(6D40+273)*101319.9921875)). Finitecases;6D40=-273
   stopsboundedinterpreter,hardwareexceptionbehavioropen. */

void Control_UpdateRatioEnvironmentFactor(void)

{
  float fVar1;
  float fVar2;
  
  fVar1 = (float)(*(code *)PTR_FUN_000585a0)(PTR_DAT_000585f4);
  fVar1 = fVar1 * DAT_000585f8;
  fVar2 = (float)(*(code *)PTR_FUN_000585a0)(PTR_Control_RawSecondPublished_000585fc);
  *(float *)PTR_Control_RatioEnvironmentFactor_00058570 =
       fVar1 / ((fVar2 + DAT_00058600) * DAT_00058604);
  return;
}

