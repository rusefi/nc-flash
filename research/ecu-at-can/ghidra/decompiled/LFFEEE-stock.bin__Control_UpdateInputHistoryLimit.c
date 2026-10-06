/* Ghidra analysis output; verify against original SH instructions. */

/* StockD9F24/28 andA35C8allzero:qualified path retains8078,otherpathfloorsold8078at0. Explicitgates
   andhistoryoracle; control-input-history.txt. */

undefined4 Control_UpdateInputHistoryLimit(void)

{
  undefined *puVar1;
  char cVar3;
  undefined4 uVar2;
  undefined4 uVar4;
  undefined4 extraout_fr0;
  undefined4 extraout_fr0_00;
  
  puVar1 = PTR_Control_RetainedInputLimit_00058908;
  if (((*PTR_Control_InputHistoryHoldoff_0005890c == '\0') &&
      (cVar3 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058910), cVar3 == '\x01')) &&
     (cVar3 = (*(code *)PTR_FUN_00058914)(PTR_DAT_00058918), cVar3 == '\x01')) {
    uVar4 = (*(code *)PTR_FUN_00058920)(*(undefined4 *)puVar1,*(undefined4 *)PTR_DAT_0005891c);
    uVar2 = (*(code *)PTR_FUN_00058928)(*(float *)puVar1 + *(float *)PTR_DAT_00058924,uVar4);
    uVar4 = extraout_fr0;
  }
  else {
    uVar4 = (*(code *)PTR_FUN_00058930)(PTR_DAT_0005892c);
    uVar4 = (*(code *)PTR_Lookup_FloatCurve_00058938)(uVar4,DAT_00058934);
    uVar2 = (*(code *)PTR_FUN_00058920)(*(float *)puVar1 - *(float *)PTR_DAT_00058924,uVar4);
    uVar4 = extraout_fr0_00;
  }
  *(undefined4 *)puVar1 = uVar4;
  return uVar2;
}

