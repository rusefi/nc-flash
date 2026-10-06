/* Ghidra analysis output; verify against original SH instructions. */

/* Executed allocation of first free node and insertion at requested priority head tail; FF if
   exhausted. Stock caller priority1. */

uint RequestList_Allocate(byte param_1,int param_2,byte *param_3)

{
  int iVar1;
  uint uVar2;
  
  uVar2 = (uint)DAT_00030582;
  iVar1 = (uint)*param_3 * 4 + param_2;
  if ((uint)*(byte *)(iVar1 + 1) != (uint)*param_3) {
    uVar2 = (uint)*(byte *)(iVar1 + 1);
    RequestList_Unlink(uVar2,param_2);
    RequestList_InsertBeforeHead(param_1 - 1,uVar2,param_2,(int)*(short *)(param_3 + 2),param_1 - 1)
    ;
  }
  return uVar2;
}

