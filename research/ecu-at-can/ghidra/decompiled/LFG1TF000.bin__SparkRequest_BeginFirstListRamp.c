/* Ghidra analysis output; verify against original SH instructions. */

/* Executed record+4 copied to+6;8115[record+12]=0;returns5. Full dispatch and timer service remain
   open. */

undefined4 SparkRequest_BeginFirstListRamp(undefined4 param_1,int param_2)

{
  undefined *puVar1;
  
  puVar1 = PTR_Request_RampTimerSlots_0004cffc;
  *(undefined2 *)(param_2 + 6) = *(undefined2 *)(param_2 + 4);
  puVar1[*(byte *)(param_2 + 0xc)] = 0;
  return 5;
}

