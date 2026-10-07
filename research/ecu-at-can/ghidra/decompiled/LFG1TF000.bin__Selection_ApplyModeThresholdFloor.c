/* Ghidra analysis output; verify against original SH instructions. */

/* Slots2..4 max incoming withmode-selectedbyte*64 andbytecurve/4 floor. Allstockfloorconstants/maps
   zero;588directcases preserve input. Mode captured92D1bit3 andcurrent9AE9bit0. */

uint Selection_ApplyModeThresholdFloor(int param_1,uint param_2,int param_3,char param_4)

{
  short sVar2;
  uint uVar1;
  uint uVar3;
  
  sVar2 = (short)param_3;
  uVar3 = 0;
  if (param_4 != '\x02') {
    param_3 = param_1 + -2;
    uVar3 = (uint)(byte)PTR_DAT_00045114[param_3] << 6;
  }
  if ((param_4 != '\x01') && (param_1 != 2)) {
    uVar1 = (*(code *)PTR_Lookup_ByteCurveToFixedPoint_0004511c)
                      ((int)sVar2,PTR_DAT_00045118 + (param_1 + -3) * 7,param_3,param_4,param_1 + -3
                      );
    uVar1 = (uVar1 & 0xffff) >> 2;
    if (uVar3 < uVar1) {
      uVar3 = uVar1;
    }
  }
  if ((param_2 & 0xffff) < uVar3) {
    param_2 = uVar3;
  }
  return param_2;
}

