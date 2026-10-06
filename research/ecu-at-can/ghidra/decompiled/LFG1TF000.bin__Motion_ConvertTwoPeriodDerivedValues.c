/* Ghidra analysis output; verify against original SH instructions. */

/* Static: calibration76E78/7A/7C and9330 bit0 form factor;10B74 converts80EA and91A2, clampsFF00
   into932C/932E then50F26. Full execution stops at unsupported MULS.W22DFE; units unproved. */

void Motion_ConvertTwoPeriodDerivedValues(void)

{
  ushort uVar1;
  undefined *puVar2;
  ushort uVar4;
  undefined2 uVar5;
  undefined *puVar3;
  
  uVar1 = DAT_00022e60;
  if ((*PTR_DAT_00022e64 & 1) == 1) {
    uVar1 = *(ushort *)PTR_DAT_00022e68;
  }
  uVar4 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00022e74)
                    ((int)*(short *)PTR_DAT_00022e70 * (int)DAT_00022e62,
                     (int)*(short *)PTR_DAT_00022e6c);
  uVar5 = (*(code *)PTR_FUN_00022e78)((uint)uVar4 * (uint)DAT_00022e60,(int)(short)uVar1);
  puVar3 = (undefined *)(*(code *)PTR_FUN_00022e7c)((int)DAT_ffff80ea,uVar5,8);
  puVar2 = PTR_DAT_00022e80;
  if (PTR_DAT_00022e80 < puVar3) {
    puVar3 = PTR_DAT_00022e80;
  }
  *(short *)PTR_DAT_00022e84 = (short)puVar3;
  DAT_ffff800e = (undefined1)((uint)puVar3 >> 8);
  puVar3 = (undefined *)
           (*(code *)PTR_FUN_00022e7c)
                     ((int)*(short *)PTR_Motion_PeriodDerivedValue_00022e88,uVar5,8);
  if (puVar2 < puVar3) {
    puVar3 = puVar2;
  }
  *(short *)PTR_DAT_00022e8c = (short)puVar3;
  (*(code *)PTR_Diagnostic_ScaleTwoApplicationWords_00022e90)();
  return;
}

