/* Ghidra analysis output; verify against original SH instructions. */

/* If6E3A==1 AND6E2F==1,7C74=min(7A80-6E08,BFAE4); otherwise0. No lower clamp.45 cases;480 paired
   simultaneousCAN211/216 paths reach final spark and separate cut commands. */

uint CAN216_SelectSparkCorrection(void)

{
  uint uVar1;
  undefined4 extraout_fr0;
  
  uVar1 = (uint)(byte)*PTR_CAN216_NumericRequestActive_000529a4;
  if ((uVar1 == 1) && (uVar1 = (uint)(byte)*PTR_CAN216_SparkAdmission_000529a8, uVar1 == 1)) {
    uVar1 = (*(code *)PTR_FUN_000529b8)
                      (*(float *)PTR_DAT_000529b0 - *(float *)PTR_CAN216_InvertedModelValue_000529ac
                       ,*(undefined4 *)PTR_CAN216_SparkCorrectionUpperBound_000529b4);
    *(undefined4 *)PTR_CAN216_SparkCorrection_000529bc = extraout_fr0;
  }
  else {
    *(undefined4 *)PTR_CAN216_SparkCorrection_000529bc = 0;
  }
  return uVar1;
}

