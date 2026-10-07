/* Ghidra analysis output; verify against original SH instructions. */

/* Same numericconversion as16FF6; completeoriginalhelper executed. Physicalsensor/units not
   inferred. See tcu-cycle-callback.txt. */

int OutputCycle_ConvertInputB(uint param_1,undefined1 *param_2)

{
  int iVar1;
  int iVar2;
  undefined1 uVar3;
  int iVar4;
  
  iVar1 = (*(code *)PTR_FUN_00016f60)((param_1 & 0xffff) << 6);
  iVar4 = (int)DAT_00016f48;
  iVar2 = (*(code *)PTR_FUN_00016f64)(iVar4 + iVar1,0,(int)DAT_00016f4a);
  uVar3 = 1;
  if (iVar4 + iVar1 == iVar2) {
    uVar3 = 2;
  }
  *param_2 = uVar3;
  return iVar2;
}

