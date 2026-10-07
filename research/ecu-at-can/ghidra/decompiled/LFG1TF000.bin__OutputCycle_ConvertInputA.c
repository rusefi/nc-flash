/* Ghidra analysis output; verify against original SH instructions. */

/* 300+signed32(u16count*64000)/2976 trunczero; clamp0..22000,state2ifunchangedelse1 viaR5pointer.
   All1024ADCcounts+wrapboundaries executed. See tcu-cycle-callback.txt. */

int OutputCycle_ConvertInputA(uint param_1,undefined1 *param_2)

{
  int iVar1;
  int iVar2;
  undefined1 uVar3;
  int iVar4;
  
  iVar1 = (*(code *)PTR_FUN_00017058)((param_1 & 0xffff) << 6);
  iVar4 = (int)DAT_00017040;
  iVar2 = (*(code *)PTR_FUN_0001705c)(iVar4 + iVar1,0,(int)DAT_00017042);
  uVar3 = 1;
  if (iVar4 + iVar1 == iVar2) {
    uVar3 = 2;
  }
  *param_2 = uVar3;
  return iVar2;
}

