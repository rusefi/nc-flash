/* Ghidra analysis output; verify against original SH instructions. */

/* Positive curvature outside
   deadband:6E08=71AC-iterative_root(max(71B0-6E04-71E0-71CC+protected71D0,0)/71A8). Otherwise
   holds.51 model/hold cases; full paired TCU sender to spark.3B5FE is interior, not entry. */

uint CAN216_InvertQuadraticModel(void)

{
  undefined *puVar1;
  uint uVar2;
  uint uVar3;
  float fVar4;
  float fVar5;
  float extraout_fr0;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  puVar1 = PTR_FUN_0003b6d4;
  fVar9 = 0.0;
  fVar10 = *(float *)PTR_Model_QuadraticCurvature_0003b6d0;
  uVar2 = (*(code *)PTR_FUN_0003b6d4)(fVar10,0,DAT_0003b6d8);
  if (((uVar2 & 0xff) != 0) && (0.0 < fVar10)) {
    fVar8 = *(float *)PTR_CAN216_SelectedNumericRequest_0003b6bc;
    fVar7 = *(float *)PTR_Model_QuadraticPeak_0003b6dc;
    fVar6 = *(float *)PTR_Model_RatioOffset_0003b6e0;
    fVar4 = *(float *)PTR_Model_CurrentAuxiliaryOffset_0003b6e4;
    fVar5 = (float)(*(code *)PTR_FUN_0003b6ec)(PTR_Model_ReferenceAuxiliaryOffset_0003b6e8);
    uVar2 = (*(code *)PTR_FUN_0003b6f0)((((fVar7 - fVar8) - fVar6) - fVar4) + fVar5,fVar9);
    fVar4 = 2.0;
    for (fVar5 = 1.0; fVar5 * fVar5 < extraout_fr0 / fVar10; fVar5 = fVar5 * 2.0) {
    }
    uVar3 = 1;
    fVar6 = fVar9;
    while ((uVar3 & 0xff) != 0) {
      fVar7 = fVar9 + fVar5;
      if (fVar7 * fVar7 <= extraout_fr0 / fVar10) {
        fVar9 = fVar7;
      }
      fVar5 = fVar5 / fVar4;
      uVar2 = (*(code *)puVar1)(fVar5,fVar6,DAT_0003b8e0);
      uVar3 = uVar2;
    }
    *(float *)PTR_CAN216_InvertedModelValue_0003b8e8 =
         *(float *)PTR_Model_QuadraticCenter_0003b8e4 - fVar9;
  }
  return uVar2;
}

