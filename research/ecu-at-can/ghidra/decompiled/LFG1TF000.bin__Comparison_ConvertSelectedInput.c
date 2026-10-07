/* Ghidra analysis output; verify against original SH instructions. */

/* WARNING: Removing unreachable block (ram,0x000233cc) */
/* 92D5mask88 selects3200; otherwiseu16 89B0*256/10 throughsigned16saturation, uppercap25600
   viaoriginal5BBEC(25600.5).2816 cases, no arithmetic stubs. */

int Comparison_ConvertSelectedInput
              (undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  short sVar1;
  int extraout_r3;
  int iVar2;
  
  iVar2 = (int)*(short *)PTR_DAT_00023468;
  if ((((int)(char)PTR_DAT_0002346c[1] & 0x80U) == 0) && ((PTR_DAT_0002346c[1] & 8) == 0)) {
    iVar2 = (*(code *)PTR_FixedPoint_DivideToSignedWord_00023474)
                      ((uint)*(ushort *)PTR_Comparison_SelectedCANValue_00023470 << 8,10);
  }
  sVar1 = (*(code *)PTR_FUN_00023480)(1,iVar2,param_3,param_4,DAT_00023478,0);
  if (sVar1 < extraout_r3) {
    sVar1 = (*(code *)PTR_FUN_00023480)();
    iVar2 = (int)sVar1;
  }
  return iVar2;
}

