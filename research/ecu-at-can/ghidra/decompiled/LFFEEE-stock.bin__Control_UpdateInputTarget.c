/* Ghidra analysis output; verify against original SH instructions. */

/* If7016exact1 andabs6DB4>.9765625,806C=max(RTZ(RTZ(80BC*7020)/6DB4),807C);elsebaseline80BC. */

uint Control_UpdateInputTarget(void)

{
  char cVar2;
  uint uVar1;
  float fVar3;
  undefined4 extraout_fr0;
  
  fVar3 = (float)(*(code *)PTR_FUN_00058930)(PTR_DAT_0005892c);
  cVar2 = (*(code *)PTR_FUN_00058950)(fVar3,0,DAT_0005894c);
  uVar1 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058954);
  uVar1 = uVar1 & 0xff;
  if ((uVar1 == 1) && (cVar2 != '\0')) {
    uVar1 = (*(code *)PTR_FUN_00058920)
                      ((*(float *)PTR_DAT_0005895c * *(float *)PTR_Control_BaselineInput_00058958) /
                       fVar3,*(undefined4 *)PTR_Control_ActiveInputLimit_00058948);
    *(undefined4 *)PTR_Control_InputTarget_00058960 = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_Control_InputTarget_00058960 =
         *(undefined4 *)PTR_Control_BaselineInput_00058958;
  }
  return uVar1;
}

