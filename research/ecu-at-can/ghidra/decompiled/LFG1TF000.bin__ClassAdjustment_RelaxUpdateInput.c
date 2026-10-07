/* Ghidra analysis output; verify against original SH instructions. */

/* 36D1Astockargs:98DCabove-527subtract24,below-701add24,thenclamp+/-30464. Original10C1C executes;
   entryinputusedforbothcomparisons. No generalnonstockargumentclaim. */

int ClassAdjustment_RelaxUpdateInput(short param_1,short param_2,short param_3,short param_4)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  iVar1 = (*(code *)PTR_FUN_0003a008)((int)param_3,(int)param_4,10);
  iVar2 = (int)*(short *)PTR_ClassAdjustment_UpdateInput_0003a00c;
  iVar3 = iVar2;
  if ((int)param_1 + (int)param_2 < iVar2) {
    iVar3 = iVar2 - iVar1;
  }
  if (iVar2 < (int)param_2 - (int)param_1) {
    iVar3 = iVar3 + iVar1;
  }
  if (iVar3 < *(short *)PTR_DAT_0003a010 * -2) {
    iVar3 = *(short *)PTR_DAT_0003a010 * -2;
  }
  if ((int)*(short *)PTR_DAT_0003a010 << 1 < iVar3) {
    iVar3 = (int)*(short *)PTR_DAT_0003a010 << 1;
  }
  *(short *)PTR_ClassAdjustment_UpdateInput_0003a00c = (short)iVar3;
  return iVar1;
}

