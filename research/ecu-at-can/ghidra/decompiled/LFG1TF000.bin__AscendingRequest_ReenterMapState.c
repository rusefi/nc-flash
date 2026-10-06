/* Ghidra analysis output; verify against original SH instructions. */

/* Sets record+8bit10, clears8276, returns3; preservesnumeric+4/+6. Canrepeatwhilealready state3.768
   allflag/timer cases. Bit10 bypasses initial map scaling. */

undefined4 AscendingRequest_ReenterMapState(undefined4 param_1,int param_2)

{
  undefined *puVar1;
  
  puVar1 = PTR_AscendingRequest_ScaleTimer_0004df28;
  *(byte *)(param_2 + 8) = *(byte *)(param_2 + 8) | 0x10;
  *puVar1 = 0;
  return 3;
}

