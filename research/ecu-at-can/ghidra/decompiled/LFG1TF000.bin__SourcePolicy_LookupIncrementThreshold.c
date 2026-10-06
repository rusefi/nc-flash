/* Ghidra analysis output; verify against original SH instructions. */

/* Current proposal bank clamp0..4; source9B40==17 selects7533C else7542C,48-byte
   records,axis9C96,original108E6.848 boundary cases; tcu-source-selection.txt. */

undefined4 SourcePolicy_LookupIncrementThreshold(char param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  
  uVar1 = SourcePolicy_SelectCurveBank(0,(int)param_1);
  puVar3 = PTR_SourcePolicy_IncrementOtherCurves_00049958;
  if (*PTR_Selection_SourceCode_00049950 == '\x11') {
    puVar3 = PTR_SourcePolicy_Increment17Curves_00049954;
  }
  uVar2 = (*(code *)PTR_Lookup_InterpolateWordCurve_0004995c)
                    ((int)*(short *)(int)DAT_0004993a,puVar3 + (uVar1 & 0xff) * 0x30);
  return uVar2;
}

