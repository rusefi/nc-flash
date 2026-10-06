/* Ghidra analysis output; verify against original SH instructions. */

/* s32 wrap of s16(80EE)-s32(9218[u8 index]), clamped[-32768,32767].196 index/signed-wrap cases
   verified. */

int AscendingRequest_TargetError(uint param_1)

{
  int iVar1;
  
  iVar1 = (int)Phase_MeasuredSourceSample -
          *(int *)(PTR_Phase_ProducedReferenceWords_0004e310 + (param_1 & 0xff) * 4);
  if ((int)DAT_0004e2fa <
      (int)Phase_MeasuredSourceSample -
      *(int *)(PTR_Phase_ProducedReferenceWords_0004e310 + (param_1 & 0xff) * 4)) {
    iVar1 = (int)DAT_0004e2fa;
  }
  if (iVar1 < DAT_0004e2fc) {
    iVar1 = (int)DAT_0004e2fc;
  }
  return iVar1;
}

