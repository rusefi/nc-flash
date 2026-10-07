/* Ghidra analysis output; verify against original SH instructions. */

/* Executed rowmask/state1,2,4; returns0 ifselectedbit,22hex ifothermaskbit,11hex
   invalidstate/emptypermission. */

int Diagnostic_CheckPermissionMask(uint param_1,char param_2)

{
  byte bVar1;
  int iVar2;
  
  bVar1 = 0;
  iVar2 = 0;
  if (param_2 == '\x01') {
    bVar1 = 1;
  }
  else if (param_2 == '\x02') {
    bVar1 = 2;
  }
  else if (param_2 == '\x04') {
    bVar1 = 4;
  }
  else {
    iVar2 = 0x11;
  }
  if (iVar2 == 0) {
    if ((PTR_DAT_00056108[(param_1 & 0xff) * 2] & bVar1) == 0) {
      if ((~bVar1 & PTR_DAT_00056108[(param_1 & 0xff) * 2]) == 0) {
        iVar2 = 0x11;
      }
      else {
        iVar2 = 0x22;
      }
    }
  }
  return iVar2;
}

