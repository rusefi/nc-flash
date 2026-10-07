/* Ghidra analysis output; verify against original SH instructions. */

/* Curve7035C(80E8)/4-9600;92D1bit2 subtract7036F curve correction;bit3 subtract70382 map(80E8,92F6)
   correction; subtract9310*16.252 cases; caller truncates return to16 for MULS.W. */

int Qualification_CalculateCorrection(void)

{
  int iVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  
  iVar1 = (int)CAN201_Word0ApplicationValue;
  iVar3 = (int)DAT_00023abc;
  uVar2 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00023ac4)
                    (iVar1,PTR_Qualification_BaseCorrectionCurve_00023ac0);
  iVar4 = ((uVar2 & 0xffff) >> 2) + iVar3;
  if ((*PTR_DAT_00023ac8 & 4) != 0) {
    uVar2 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_00023ac4)
                      (iVar1,PTR_Qualification_OptionalCorrectionCurve_00023acc);
    iVar4 = iVar4 - (((uVar2 & 0xffff) >> 2) + iVar3);
  }
  if ((*PTR_DAT_00023ac8 & 8) != 0) {
    uVar2 = (*(code *)PTR_Lookup_ByteGrid2D_Q8_00023ad8)
                      (iVar1,(int)*(short *)PTR_DAT_00023ad4,
                       PTR_Qualification_OptionalCorrectionMap_00023ad0);
    iVar4 = iVar4 - (((uVar2 & 0xffff) >> 2) + iVar3);
  }
  return iVar4 + (uint)(byte)*PTR_DAT_00023adc * -0x10;
}

