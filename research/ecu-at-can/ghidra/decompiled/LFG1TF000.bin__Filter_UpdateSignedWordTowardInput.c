/* Ghidra analysis output; verify against original SH instructions. */

/* Signed16 input delta*128/divisor with original10D0C saturation; divisor signed minimum128;
   nonzero delta enforces +/-1 minimumstep. Stock45BA0 divisor512.392 helper cases. */

int Filter_UpdateSignedWordTowardInput(short param_1,short param_2,int param_3)

{
  short sVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  if ((int)(short)param_3 < (int)DAT_00010ffe) {
    param_3 = (int)DAT_00010ffe;
  }
  iVar3 = (int)param_2 - (int)param_1;
  iVar4 = 0;
  if (iVar3 != 0) {
    iVar2 = 1;
    if (iVar3 < 0) {
      iVar2 = -1;
    }
    sVar1 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00011000)(iVar3 * 0x80,param_3);
    iVar4 = (int)sVar1;
    if (sVar1 == 0) {
      iVar4 = iVar2;
    }
  }
  return param_1 + iVar4;
}

