/* Ghidra analysis output; verify against original SH instructions. */

/* Executed raw18-entry history inverse: both810D/9195<14, normalizedperiod=sat32(sum*18)/count;
   clamp(153600000/period,0,32767), else0.36 age cases plus450 full2086C callers; result91A2. See
   tcu-reference-source.txt. */

int Motion_CalculateRawPeriodValue(void)

{
  short sVar2;
  undefined4 uVar1;
  int iVar3;
  
  if (((byte)*PTR_DAT_00020e44 < (byte)*PTR_DAT_00020e40) &&
     ((byte)*PTR_DAT_00020e48 < (byte)*PTR_DAT_00020e40)) {
    sVar2 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00020f5c)
                      ((int)(short)(ushort)(byte)*PTR_DAT_00020f54 * (int)*(short *)PTR_DAT_00020f58
                       ,(int)DAT_00020f4a);
    uVar1 = Reference_SumCaptureHistory((int)*(short *)PTR_DAT_00020f58);
    uVar1 = (*(code *)PTR_Arithmetic_SaturatingMultiplyShift_00020f60)(uVar1,*PTR_DAT_00020f54,0);
    uVar1 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020f64)(uVar1,(int)sVar2);
    iVar3 = (*(code *)PTR_Arithmetic_GuardedSignedDivision_00020f64)(DAT_00020f68,uVar1);
  }
  else {
    iVar3 = 0;
  }
  if (DAT_00020f4c < iVar3) {
    iVar3 = (int)DAT_00020f4c;
  }
  if (iVar3 < 0) {
    iVar3 = 0;
  }
  return iVar3;
}

