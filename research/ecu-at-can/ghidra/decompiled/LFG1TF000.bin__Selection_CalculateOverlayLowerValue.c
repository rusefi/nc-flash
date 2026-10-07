/* Ghidra analysis output; verify against original SH instructions. */

/* Wordcurve sums selectedby9889bit5/flag92D1bit3; source1 replaces sum.1800directcases;
   axesunsigned16,physicalunitsunproved. */

int Selection_CalculateOverlayLowerValue(byte param_1,char param_2,undefined4 param_3,short param_4)

{
  undefined *puVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  
  puVar1 = PTR_Lookup_InterpolateWordCurve_000461d0;
  iVar2 = (uint)param_1 * 0x14;
  iVar3 = (*(code *)PTR_Lookup_InterpolateWordCurve_000461d0)
                    ((int)param_4,PTR_Selection_OverlayWordCurves_000461d4 + iVar2);
  if ((*PTR_DAT_000461d8 & 0x20) == 0) {
    iVar4 = (*(code *)puVar1)(param_3,PTR_Selection_OverlayWordCurves_100__000461dc + iVar2);
    iVar3 = iVar3 + iVar4;
  }
  else {
    iVar4 = (*(code *)puVar1)(param_3,PTR_Selection_OverlayWordCurves_280__000461e0 + iVar2);
    iVar3 = iVar3 + iVar4;
    if (param_2 == '\x01') {
      iVar4 = (*(code *)puVar1)((int)*(short *)PTR_DAT_000461e4 << 1,
                                PTR_Selection_OverlayWordCurves_330__000461e8 + (uint)param_1 * 0x10
                               );
      iVar3 = iVar3 + iVar4;
    }
  }
  if (*PTR_Selection_SourceCode_000461ec == '\x01') {
    iVar3 = (*(code *)puVar1)((int)param_4,PTR_Selection_OverlayWordCurves_50__000461f0 + iVar2);
    iVar2 = (*(code *)puVar1)(param_3,PTR_Selection_OverlayWordCurves_150__000461f4 + iVar2);
    iVar3 = iVar3 + iVar2;
  }
  return iVar3;
}

