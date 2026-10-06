/* Ghidra analysis output; verify against original SH instructions. */

/* Elapsed>=threshold AND(code!=9 OR signed80D8<64). Stock773E0=64;384 boundarycases verified.
   Physical role of80D8 open. See tcu-request-dispatch.txt. */

undefined4 SparkRequest_CheckHoldTime(int param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if ((param_2 <= param_1) &&
     ((*(char *)(param_3 + 1) != '\t' || (Request_Code9HoldSource < *(short *)PTR_DAT_0004d864)))) {
    uVar1 = 1;
  }
  return uVar1;
}

