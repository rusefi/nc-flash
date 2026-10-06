/* Ghidra analysis output; verify against original SH instructions. */

/* 8020reload113
   if8194zero,7012exact1,7346zero,or8023zeroand7020+100>6DB4;elsedecrementnonzero.972cases;control-history.txt.
    */

uint Control_UpdateRetainedDecayTimer(void)

{
  undefined *puVar1;
  undefined *puVar2;
  char cVar5;
  uint uVar3;
  uint uVar4;
  float extraout_fr0;
  float fVar6;
  
  puVar2 = PTR_FUN_00058244;
  puVar1 = PTR_Control_RetainedDecayTimer_00058230;
  fVar6 = *(float *)PTR_DAT_00058240 + *(float *)PTR_DAT_0005823c;
  cVar5 = (*(code *)PTR_FUN_00058244)(PTR_DAT_00058248);
  uVar4 = 0;
  if (cVar5 != '\0') {
    cVar5 = (*(code *)puVar2)(PTR_DAT_0005824c);
    uVar4 = 1;
    if (cVar5 != '\x01') {
      uVar3 = (*(code *)puVar2)(PTR_DAT_00058250);
      uVar4 = 0;
      if (((uVar3 & 0xff) != 0) &&
         ((uVar4 = uVar3 & 0xff, *PTR_Control_RetainedSourceHysteresis_00058254 != '\0' ||
          (uVar4 = (*(code *)PTR_FUN_000581fc)(PTR_DAT_00058258), fVar6 <= extraout_fr0)))) {
        if (*(short *)puVar1 == 0) {
          return uVar4;
        }
        *(short *)puVar1 = *(short *)puVar1 + (short)DAT_00058260;
        return uVar4;
      }
    }
  }
  *(undefined2 *)puVar1 = *(undefined2 *)PTR_DAT_0005825c;
  return uVar4;
}

