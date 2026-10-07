/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1296finitecases:6D40->8FE0
   and6D20->8FDF,stock>=-777sets1,<-782clears0,deadbandholdsbyte.154BCplainfloatgetter.
   Doesnotwrite8FD8. control-activity-conditions.txt. */

undefined4 Control_UpdateActivityThresholdFlags(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  float fVar3;
  float extraout_fr0;
  float extraout_fr0_00;
  
  puVar1 = PTR_FUN_0006f4e0;
  fVar3 = (float)(*(code *)PTR_FUN_0006f4e0)(PTR_Control_RawSecondPublished_0006f4e4);
  if (fVar3 < *(float *)PTR_DAT_0006f4e8) {
    fVar3 = (float)(*(code *)puVar1)(PTR_Control_RawSecondPublished_0006f4e4);
    if (fVar3 < *(float *)PTR_DAT_0006f4e8 - *(float *)PTR_DAT_0006f4f0) {
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

