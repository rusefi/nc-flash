/* Ghidra analysis output; verify against original SH instructions. */

/* 9C9C=max_signed16(old,current80EE), executed before abort/completion.36 edges and retained
   traces. */

int StoredAdjustment_RetainSignedPeak(void)

{
  int iVar1;
  
  iVar1 = (int)Phase_MeasuredSourceSample;
  if (*(short *)(int)DAT_00049fba < Phase_MeasuredSourceSample) {
    *(short *)(int)DAT_00049fba = Phase_MeasuredSourceSample;
  }
  return iVar1;
}

