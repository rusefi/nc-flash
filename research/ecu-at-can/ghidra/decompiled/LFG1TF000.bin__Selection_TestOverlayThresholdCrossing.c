/* Ghidra analysis output; verify against original SH instructions. */

/* Unsigned9B3E word curves73F54/73FB4/74014, signed80EA measurement and unsigned9B3C category
   qualify indices2/1/0. Low-category alternatives can qualify negative measurements.1664 original
   cases; other index returns0. */

undefined4 Selection_TestOverlayThresholdCrossing(char param_1)

{
  byte bVar1;
  undefined *puVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  int iVar7;
  
  puVar2 = PTR_Lookup_InterpolateWordCurve_000464b0;
  iVar7 = (int)*(short *)PTR_Selection_ProposalLookupAxis_000464a8;
  iVar3 = (int)DAT_ffff80ea;
  bVar1 = *PTR_Selection_PreviousIndex_000464ac;
  if (param_1 == '\x02') {
    uVar4 = (*(code *)PTR_Lookup_InterpolateWordCurve_000464b0)
                      (iVar7,PTR_Selection_RetainedOverlayCurves_24__000464b4);
    if ((iVar3 < (int)(uVar4 & 0xffff)) && (3 < bVar1)) {
      return 0;
    }
  }
  else if (param_1 == '\x01') {
    uVar4 = (*(code *)PTR_Lookup_InterpolateWordCurve_000464b0)
                      (iVar7,PTR_Selection_RetainedOverlayCurves_24__000464b4);
    uVar5 = (*(code *)puVar2)(iVar7,PTR_Selection_RetainedOverlayCurves_72__00046574);
    if ((((bVar1 != 4) || (iVar3 < (int)(uVar4 & 0xffff))) &&
        ((bVar1 != 3 || (iVar3 < (int)(uVar5 & 0xffff))))) && (2 < bVar1)) {
      return 0;
    }
  }
  else {
    if (param_1 != '\0') {
      return 0;
    }
    uVar4 = (*(code *)PTR_Lookup_InterpolateWordCurve_000464b0)
                      (iVar7,PTR_Selection_RetainedOverlayCurves_24__000464b4);
    uVar5 = (*(code *)puVar2)(iVar7,PTR_Selection_RetainedOverlayCurves_72__00046574);
    uVar6 = (*(code *)puVar2)(iVar7,PTR_Selection_RetainedOverlayCurves_120__00046578);
    if (((bVar1 != 4) || (iVar3 < (int)(uVar4 & 0xffff))) &&
       (((bVar1 != 3 || (iVar3 < (int)(uVar5 & 0xffff))) &&
        (((bVar1 != 2 || (iVar3 < (int)(uVar6 & 0xffff))) && (1 < bVar1)))))) {
      return 0;
    }
  }
  return 1;
}

