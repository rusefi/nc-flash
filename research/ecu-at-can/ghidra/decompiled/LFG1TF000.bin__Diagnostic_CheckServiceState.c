/* Ghidra analysis output; verify against original SH instructions. */

/* Executed1D246 state90B6,5607A search22 rows5EB28,560AC mask. Service4 mask1 permitsstate1 only;
   errors11/22hex. */

undefined4 Diagnostic_CheckServiceState(char param_1)

{
  char cVar3;
  uint uVar1;
  undefined4 uVar2;
  
  cVar3 = (*(code *)PTR_Diagnostic_ReadServiceState_00056100)();
  uVar1 = Diagnostic_FindServicePermission((int)param_1);
  if ((uVar1 & 0xff) < 0x16) {
    uVar2 = Diagnostic_CheckPermissionMask(uVar1,(int)cVar3);
  }
  else {
    uVar2 = 0x11;
  }
  return uVar2;
}

