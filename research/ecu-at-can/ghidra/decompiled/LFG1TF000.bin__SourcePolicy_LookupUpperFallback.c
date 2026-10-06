/* Ghidra analysis output; verify against original SH instructions. */

/* Current proposal bank clamp0..4; source17 selects75ABC else75BAC. Stock
   constants4191/7729/11361/16015/23744;288 cases. */

undefined4 SourcePolicy_LookupUpperFallback(char param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  
  uVar1 = SourcePolicy_SelectCurveBank(0,(int)param_1);
  puVar3 = PTR_SourcePolicy_UpperOtherCurves_00049a88;
  if (*PTR_Selection_SourceCode_00049a70 == '\x11') {
    puVar3 = PTR_SourcePolicy_Upper17Curves_00049a84;
  }
  uVar2 = (*(code *)PTR_Lookup_InterpolateWordCurve_00049a6c)
                    ((int)*(short *)(int)DAT_00049a5e,puVar3 + (uVar1 & 0xff) * 0x30);
  return uVar2;
}

