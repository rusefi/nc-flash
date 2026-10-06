/* Ghidra analysis output; verify against original SH instructions. */

/* Clear809C ifA3A4==1 orboth7012/80A8zero; elsemax(old809C,80A0). Does not check7346: targetclear
   alone can retain old source. */

undefined4 Control_RaiseRetainedBaselineSource(void)

{
  undefined *puVar1;
  char cVar3;
  undefined4 uVar2;
  undefined4 extraout_fr0;
  
  puVar1 = PTR_Control_RetainedBaselineSource_00058dc0;
  cVar3 = (*(code *)PTR_FUN_00058dc8)(PTR_DAT_00058dc4);
  uVar2 = 1;
  if ((cVar3 != '\x01') &&
     ((cVar3 = (*(code *)PTR_FUN_00058dc8)(PTR_DAT_00058dcc), cVar3 != '\0' ||
      (uVar2 = 0, *PTR_Control_BaselineSourceCountdown_00058dd0 != '\0')))) {
    uVar2 = (*(code *)PTR_FUN_00058dd4)
                      (*(undefined4 *)puVar1,
                       *(undefined4 *)PTR_Control_BaselineSourceTarget_00058dbc);
    *(undefined4 *)puVar1 = extraout_fr0;
    return uVar2;
  }
  *(undefined4 *)puVar1 = 0;
  return uVar2;
}

