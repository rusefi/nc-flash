/* Ghidra analysis output; verify against original SH instructions. */

/* Stock quadratic maps at6DB4/6F20/7A84 plusD0/D8;7128 produces3/4,1/2,1/4 thresholds.81 producer
   cases. See traction-pattern.txt. */

void Pattern_BuildModelThresholds(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  undefined4 uVar9;
  float fVar10;
  float fVar11;
  undefined4 uVar12;
  
  puVar1 = PTR_FUN_0003f508;
  uVar6 = (*(code *)PTR_FUN_0003f508)(PTR_DAT_0003f50c);
  uVar12 = *(undefined4 *)PTR_DAT_0003f510;
  fVar11 = *(float *)PTR_DAT_0003f514;
  fVar7 = (float)(*(code *)puVar1)(PTR_Model_ReferenceAuxiliaryOffset_0003f518);
  fVar8 = (float)(*(code *)puVar1)(PTR_Model_ScaledAuxiliaryOffset_0003f51c);
  puVar2 = PTR_Lookup_FloatMap2D_0003f520;
  uVar9 = (*(code *)PTR_Lookup_FloatMap2D_0003f520)(uVar6,uVar12,PTR_Model_Map1_Curvature_0003f524);
  puVar1 = PTR_Model_Map1_Center_0003f52c;
  *(undefined4 *)PTR_DAT_0003f528 = uVar9;
  uVar9 = (*(code *)puVar2)(uVar6,uVar12,puVar1);
  puVar1 = PTR_Model_Map1_Peak_0003f534;
  *(undefined4 *)PTR_DAT_0003f530 = uVar9;
  fVar10 = (float)(*(code *)puVar2)(uVar6,uVar12,puVar1);
  puVar1 = PTR_DAT_0003f530;
  *(float *)PTR_DAT_0003f538 = fVar10;
  puVar3 = PTR_DAT_0003f540;
  fVar10 = fVar10 - *(float *)PTR_DAT_0003f528 * (*(float *)puVar1 - fVar11) *
                    (*(float *)puVar1 - fVar11);
  *(float *)PTR_DAT_0003f53c = fVar10;
  puVar1 = PTR_Model_Map0_Curvature_0003f544;
  *(float *)puVar3 = fVar10 + fVar7 + fVar8;
  uVar9 = (*(code *)puVar2)(uVar6,uVar12,puVar1);
  puVar1 = PTR_Model_Map0_Center_0003f54c;
  *(undefined4 *)PTR_DAT_0003f548 = uVar9;
  uVar9 = (*(code *)puVar2)(uVar6,uVar12,puVar1);
  puVar1 = PTR_Model_Map0_Peak_0003f554;
  *(undefined4 *)PTR_DAT_0003f550 = uVar9;
  fVar10 = (float)(*(code *)puVar2)(uVar6,uVar12,puVar1);
  *(float *)PTR_DAT_0003f558 = fVar10;
  puVar1 = PTR_FUN_0003f4d4;
  fVar10 = fVar10 - *(float *)PTR_DAT_0003f548 * (*(float *)PTR_DAT_0003f550 - fVar11) *
                    (*(float *)PTR_DAT_0003f550 - fVar11);
  *(float *)PTR_DAT_0003f55c = fVar10;
  (*(code *)puVar1)(fVar10 + fVar7 + fVar8,PTR_DAT_0003f4e0);
  puVar4 = PTR_DAT_0003f568;
  puVar3 = PTR_DAT_0003f564;
  puVar1 = PTR_DAT_0003f560;
  if (*PTR_DAT_0003f56c == '\x01') {
    uVar9 = (*(code *)puVar2)(uVar6,uVar12,PTR_Model_Map3_Curvature_0003f570);
    puVar5 = PTR_Model_Map3_Center_0003f574;
    *(undefined4 *)puVar3 = uVar9;
    uVar9 = (*(code *)puVar2)(uVar6,uVar12,puVar5);
    *(undefined4 *)puVar1 = uVar9;
    puVar5 = PTR_Model_Map3_Peak_0003f578;
  }
  else {
    uVar9 = (*(code *)puVar2)(uVar6,uVar12,PTR_Model_Map2_Curvature_0003f57c);
    puVar5 = PTR_Model_Map2_Center_0003f580;
    *(undefined4 *)puVar3 = uVar9;
    uVar9 = (*(code *)puVar2)(uVar6,uVar12,puVar5);
    *(undefined4 *)puVar1 = uVar9;
    puVar5 = PTR_Model_Map2_Peak_0003f584;
  }
  fVar10 = (float)(*(code *)puVar2)(uVar6,uVar12,puVar5);
  *(float *)puVar4 = fVar10;
  puVar2 = PTR_DAT_0003f58c;
  fVar10 = fVar10 - *(float *)puVar3 * (*(float *)puVar1 - fVar11) * (*(float *)puVar1 - fVar11);
  *(float *)PTR_DAT_0003f588 = fVar10;
  *(float *)puVar2 = fVar10 + fVar7 + fVar8;
  fVar7 = DAT_0003f590;
  *(float *)PTR_DAT_0003f598 = (*(float *)puVar2 * DAT_0003f594) / DAT_0003f590;
  *(float *)PTR_DAT_0003f59c = (*(float *)puVar2 * 2.0) / fVar7;
  *(float *)PTR_DAT_0003f5a0 = (*(float *)puVar2 * 1.0) / fVar7;
  return;
}

