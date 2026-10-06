/* Ghidra analysis output; verify against original SH instructions. */

/* Requiresdistance>record+32 and>=20584 deadline. Complete assertion/release matrix and exact
   boundary tests execute. */

undefined4 Output_AdmitMode1Release(int param_1,int param_2)

{
  int iVar1;
  uint uVar2;
  
  uVar2 = param_1 + 0x10;
  while( true ) {
    if (param_1 + 0x28U <= uVar2) {
      return 1;
    }
    if ((param_2 <= *(int *)(uVar2 + 0x10)) ||
       (iVar1 = Output_CalculateMode1Boundary(uVar2), param_2 < iVar1)) break;
    uVar2 = uVar2 + 0x18;
  }
  return 0;
}

