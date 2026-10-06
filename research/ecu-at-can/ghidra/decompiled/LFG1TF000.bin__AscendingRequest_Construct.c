/* Ghidra analysis output; verify against original SH instructions. */

/* Captures808D to+12,80C8/80D2/80D4 to+14/+16/+18; allocates first-list priority1 handle into+2;
   zeroes+4, returns2. Preserves+8.18 cases; tcu-ascending-map.txt. */

undefined4
AscendingRequest_Construct(undefined4 param_1,undefined1 param_2,undefined4 param_3,int param_4)

{
  undefined2 uVar1;
  undefined1 uVar2;
  
  *(undefined1 *)(param_4 + 1) = param_2;
  uVar1 = (*(code *)PTR_FUN_0004def8)();
  *(undefined2 *)(param_4 + 4) = uVar1;
  *(undefined1 *)(param_4 + 0xc) = DAT_ffff808d;
  *(undefined2 *)(param_4 + 0xe) = Request_CapturedMeasurementScaled;
  *(undefined2 *)(param_4 + 0x10) = AscendingRequest_CapturedThresholdSource;
  *(undefined2 *)(param_4 + 0x12) = AscendingRequest_CapturedMapSource;
  uVar2 = (*(code *)PTR_SparkRequest_AllocateFirstList_0004defc)(1);
  *(undefined1 *)(param_4 + 2) = uVar2;
  return 2;
}

