/* Ghidra analysis output; verify against original SH instructions. */

/* If71A8 positive outside deadband,7174=71AC-iterative approximate
   sqrt(max(71B0-7170+71D0+71D8,0)/71A8). Otherwise retain7174.69 exact test cases. */

uint CAN211_InvertQuadraticModel(void)

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
  
  puVar1 = PTR_FUN_0003fbcc;
  fVar8 = 0.0;
  fVar9 = *(float *)PTR_Model_QuadraticCurvature_0003fbfc;
  uVar2 = (*(code *)PTR_FUN_0003fbcc)(fVar9,0,DAT_0003fc00);
  if (((uVar2 & 0xff) != 0) && (0.0 < fVar9)) {
    fVar7 = *(float *)PTR_DAT_0003fbf8;
    fVar6 = *(float *)PTR_Model_QuadraticPeak_0003fc04;
    fVar4 = (float)(*(code *)PTR_FUN_0003fbc0)(PTR_Model_ReferenceAuxiliaryOffset_0003fc08);
    fVar5 = (float)(*(code *)PTR_FUN_0003fbc0)(PTR_Model_ScaledAuxiliaryOffset_0003fc0c);
    uVar2 = (*(code *)PTR_FUN_0003fbe0)((fVar6 - fVar7) + fVar4 + fVar5,fVar8);
    fVar4 = 2.0;
    for (fVar5 = 1.0; fVar5 * fVar5 < extraout_fr0 / fVar9; fVar5 = fVar5 * 2.0) {
    }
    uVar3 = 1;
    fVar6 = fVar8;
    while ((uVar3 & 0xff) != 0) {
      fVar7 = fVar8 + fVar5;
      if (fVar7 * fVar7 <= extraout_fr0 / fVar9) {
        fVar8 = fVar7;
      }
      fVar5 = fVar5 / fVar4;
      uVar2 = (*(code *)puVar1)(fVar5,fVar6,DAT_0003fc10);
      uVar3 = uVar2;
    }
    *(float *)PTR_CAN211_InvertedModelValue_0003fc18 =
         *(float *)PTR_Model_QuadraticCenter_0003fc14 - fVar8;
  }
  return uVar2;
}

