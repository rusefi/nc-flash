/* Ghidra analysis output; verify against original SH instructions. */

/* SourceFFFF9118 signed16 >>6 plus50; bounded0..254, invalid7FFF -> FF. */

void CAN218_BuildByte6(char param_1)

{
  undefined *UNRECOVERED_JUMPTABLE;
  int iVar1;
  
  UNRECOVERED_JUMPTABLE = PTR_CAN218_SetByte6_00019294;
  iVar1 = (int)DAT_00019280;
  if ((param_1 != '\0') && (param_1 != '\x10')) {
    if (param_1 != '\x01') goto LAB_000191e8;
    if ((int)*(short *)PTR_CAN218_Byte6Source_00019290 != (int)DAT_00019282) {
      iVar1 = ((int)*(short *)PTR_CAN218_Byte6Source_00019290 >> 6) + 0x32;
      if ((int)DAT_00019284 < (int)(short)iVar1) {
        iVar1 = (int)DAT_00019284;
      }
      if ((short)iVar1 < 0) {
        iVar1 = 0;
      }
    }
  }
  param_1 = (char)iVar1;
LAB_000191e8:
                    /* WARNING: Could not recover jumptable at 0x000191ec. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  *(char *)(int)DAT_00019286 = param_1;
  (*(code *)UNRECOVERED_JUMPTABLE)();
  return;
}

