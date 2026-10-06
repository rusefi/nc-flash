/* Ghidra analysis output; verify against original SH instructions. */

/* 8018=max(0,RTZ(RTZ(8028-801C)-RTZ(6C20/60))).100 directcases and220
   serialcycles;upstream6C20/sourceprovenanceopen. */

void Control_UpdateSourceRemainder(void)

{
  float fVar1;
  undefined4 uVar2;
  float fVar3;
  
  fVar3 = *(float *)PTR_Control_RetainedSourceRatio_00058308 -
          *(float *)PTR_Control_SourceOffset_00058304;
  fVar1 = (float)(*(code *)PTR_FUN_00058310)(PTR_DAT_0005830c);
  uVar2 = (*(code *)PTR_FUN_00058318)(fVar3 - fVar1 / DAT_00058314,0);
  *(undefined4 *)PTR_Control_SourceRemainder_0005831c = uVar2;
  return;
}

