/* Ghidra analysis output; verify against original SH instructions. */

/* Signed83C0[index] >=signed ROM770C0=8 returns3, otherwise-1;112 cases across16 slots. Counts are
   not milliseconds. */

undefined4 Phase_CheckCompletionTimer(uint param_1)

{
  undefined4 uVar1;
  
  uVar1 = 0xffffffff;
  if (*(short *)PTR_Phase_CompletionTimerThreshold_00032610 <=
      *(short *)(PTR_Phase_CompletionTimers_0003260c + (param_1 & 0xffff) * 2)) {
    uVar1 = 3;
  }
  return uVar1;
}

