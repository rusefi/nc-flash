/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned target-old difference, scaled128/max(s16factor,128); signed16 step clamp and minimum
   nonzero step. Returns signed16old plus step;200 direct cases. */

int Qualification_SlewUnsignedDifference(ushort param_1,uint param_2,int param_3)

{
  short sVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  if ((int)(short)param_3 < (int)DAT_00023a2e) {
    param_3 = (int)DAT_00023a2e;
  }
  iVar3 = (param_2 & 0xffff) - (uint)param_1;
  iVar4 = 0;
  if (iVar3 != 0) {
    iVar2 = 1;
    if (iVar3 < 0) {
      iVar2 = -1;
    }
    sVar1 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00023a40)(iVar3 * 0x80,param_3);
    iVar4 = (int)sVar1;
    if (sVar1 == 0) {
      iVar4 = iVar2;
    }
  }
  return (short)param_1 + iVar4;
}

