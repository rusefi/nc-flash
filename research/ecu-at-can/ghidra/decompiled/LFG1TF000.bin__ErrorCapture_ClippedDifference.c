/* Ghidra analysis output; verify against original SH instructions. */

/* Signed32 wrap of s16(80EE)-s32(9218[95C6]), clamp[-16319,16319];658 signed/boundary/index cases.
   Actual produced reference range is much narrower than32-bit boundary tests. */

int ErrorCapture_ClippedDifference(void)

{
  int iVar1;
  
  iVar1 = (int)Phase_MeasuredSourceSample -
          *(int *)(PTR_Phase_ProducedReferenceWords_00030c50 + (uint)*(byte *)(int)DAT_00030c48 * 4)
  ;
  if ((int)DAT_00030c4a <
      (int)Phase_MeasuredSourceSample -
      *(int *)(PTR_Phase_ProducedReferenceWords_00030c50 + (uint)*(byte *)(int)DAT_00030c48 * 4)) {
    iVar1 = (int)DAT_00030c4a;
  }
  if (iVar1 < DAT_00030c4c) {
    iVar1 = (int)DAT_00030c4c;
  }
  return iVar1;
}

