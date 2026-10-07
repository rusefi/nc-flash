/* Ghidra analysis output; verify against original SH instructions. */

/* 9B3E=(2*s16(809C))low16. OverrideFFFF
   ifs16(8098)>s16ROM772F8=25600,92C5bit1set,92D5bit7clear,92D3bit6clear.2520 direct cases.
   Verified8098 producer caps25600,sooverrideunreachablefromthatnormalproducer alone. */

void Selection_PublishProposalAxis(void)

{
  short sVar1;
  
  sVar1 = Comparison_ApplicationInput << 1;
  if ((((*(short *)PTR_Selection_FullAxisOverrideThreshold_00045120 < CAN201_Byte6ApplicationValue)
       && ((*PTR_DAT_00045124 & 2) != 0)) &&
      (((int)(char)*PTR_ApplicationFaultFlags92D5_00045128 & 0x80U) == 0)) &&
     ((*PTR_DAT_0004512c & 0x40) == 0)) {
    sVar1 = (short)PTR_DAT_00045130;
  }
  *(short *)PTR_Selection_ProposalLookupAxis_00045134 = sVar1;
  return;
}

