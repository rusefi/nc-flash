/* Ghidra analysis output; verify against original SH instructions. */

/* Byte-decrement proposal then clamp0..4;916Fbit2 selects7551C else7560C,axis9C96. Stock constant
   rows3259/7449/10895/15271/23279;288 cases. */

undefined4 SourcePolicy_LookupDecrementThreshold(char param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  
  uVar1 = SourcePolicy_SelectCurveBank(1,(int)param_1);
  puVar3 = PTR_SourcePolicy_DecrementOtherCurves_00049a68;
  if ((*PTR_Request_CancellationFlags_00049a60 & 4) != 0) {
    puVar3 = PTR_SourcePolicy_DecrementFlagCurves_00049a64;
  }
  uVar2 = (*(code *)PTR_Lookup_InterpolateWordCurve_00049a6c)
                    ((int)*(short *)(int)DAT_00049a5e,puVar3 + (uVar1 & 0xff) * 0x30);
  return uVar2;
}

