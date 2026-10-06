/* Ghidra analysis output; verify against original SH instructions. */

/* Byte-decrement proposal then clamp0..4; source17 selects75C9C else75D8C. Stock
   constants0/4657/7263/11638/17692;1184 cases. */

undefined4 SourcePolicy_LookupEdgeFallback(char param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  
  uVar1 = SourcePolicy_SelectCurveBank(1,(int)param_1);
  puVar3 = PTR_SourcePolicy_EdgeOtherCurves_00049afc;
  if (*PTR_Selection_SourceCode_00049af4 == '\x11') {
    puVar3 = PTR_SourcePolicy_Edge17Curves_00049af8;
  }
  uVar2 = (*(code *)PTR_Lookup_InterpolateWordCurve_00049b00)
                    ((int)*(short *)(int)DAT_00049af0,puVar3 + (uVar1 & 0xff) * 0x30);
  return uVar2;
}

