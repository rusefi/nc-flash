/* Ghidra analysis output; verify against original SH instructions. */

/* Reads MCR/GSR word, shifts8, writes MCR byte with bit0 set/clear according to action==1. Register
   fixtures verify preserved otherbits/GSR. */

uint HCAN_SetResetRequest(short param_1)

{
  uint uVar1;
  
  uVar1 = FUN_00019ab6((int)DAT_00019abe);
  uVar1 = (uVar1 & 0xffff) >> 8;
  if (param_1 == 1) {
    uVar1 = uVar1 | 1;
  }
  else {
    uVar1 = uVar1 & (int)DAT_00019ac0;
  }
  FUN_00019aca((int)DAT_00019abe,uVar1);
  return uVar1;
}

