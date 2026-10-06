/* Ghidra analysis output; verify against original SH instructions. */

/* Byte-decrement proposal then clamp0..4; source17 selects756FC else757EC. Stock
   constants1117/1397/1861/3538/4376;288 cases. */

undefined4 SourcePolicy_LookupLatchThreshold(char param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined *puVar3;
  
  uVar1 = SourcePolicy_SelectCurveBank(1,(int)param_1);
  puVar3 = PTR_SourcePolicy_LatchOtherCurves_00049a78;
  if (*PTR_Selection_SourceCode_00049a70 == '\x11') {
    puVar3 = PTR_SourcePolicy_Latch17Curves_00049a74;
  }
  uVar2 = (*(code *)PTR_Lookup_InterpolateWordCurve_00049a6c)
                    ((int)*(short *)(int)DAT_00049a5e,puVar3 + (uVar1 & 0xff) * 0x30);
  return uVar2;
}

