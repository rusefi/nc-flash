/* Ghidra analysis output; verify against original SH instructions. */

/* 8023 clearswhen8018>=RTZ(protected2310+50);sets1when8018<=2310;middleholdsrawoldbyte.
   Protecteddefault0;108cases. */

undefined4 Control_UpdateRetainedSourceHysteresis(void)

{
  undefined4 uVar1;
  float fVar2;
  float extraout_fr0;
  float fVar3;
  
  fVar2 = (float)(*(code *)PTR_FUN_0005832c)
                           (*(undefined4 *)PTR_DAT_00058324,PTR_Control_RetainedSourceFloor_00058328
                           );
  fVar3 = *(float *)PTR_Control_SourceRemainder_0005831c;
  if (fVar3 < fVar2 + *(float *)PTR_DAT_00058330) {
    uVar1 = (*(code *)PTR_FUN_0005832c)
                      (*(undefined4 *)PTR_DAT_00058324,PTR_Control_RetainedSourceFloor_00058328);
    if (fVar3 <= extraout_fr0) {
      *PTR_Control_RetainedSourceHysteresis_00058334 = 1;
    }
  }
  else {
    uVar1 = 0;
    *PTR_Control_RetainedSourceHysteresis_00058334 = 0;
  }
  return uVar1;
}

