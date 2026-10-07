/* Ghidra analysis output; verify against original SH instructions. */

/* Stock7713A=0 makes final unsigned cmp/hs at36984 reject every count985A.65536 original inputs
   reach comparison and return0. Earlier gates9889bit0,8080=6,8081>=4,s16(80EE)in[3712,5120). */

undefined4 ClassAdjustment_UniformAdmission(void)

{
  undefined4 uVar1;
  
  uVar1 = 0;
  if (((((*PTR_DAT_00036994 & 1) == 1) && (TransmissionStateClass == 6)) &&
      (3 < CAN231_SixStateSource)) &&
     (((*(short *)PTR_DAT_00036998 <= Phase_MeasuredSourceSample &&
       (Phase_MeasuredSourceSample < *(short *)PTR_DAT_0003699c)) &&
      (*(ushort *)(int)DAT_0003698e < *(ushort *)PTR_DAT_000369a0)))) {
    uVar1 = 1;
  }
  return uVar1;
}

