/* Ghidra analysis output; verify against original SH instructions. */

/* Stock12 maps in4 branches selected by718C/74F1/657E ->71A8/AC/B0. Computes c-a*(b-command)^2
   for7A74/7A80 ->71F4/F8.243 producer cases; model-sources.txt. */

void Model_SelectCoefficientsAndEvaluate(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  char cVar5;
  undefined *puVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  
  uVar7 = (*(code *)PTR_FUN_000406bc)(PTR_DAT_000406b8);
  puVar4 = PTR_Lookup_FloatMap2D_000406d0;
  puVar3 = PTR_Model_QuadraticCenter_000406cc;
  puVar2 = PTR_Model_QuadraticCurvature_000406c8;
  puVar1 = PTR_Model_QuadraticPeak_000406c4;
  uVar9 = *(undefined4 *)PTR_DAT_000406c0;
  cVar5 = (*(code *)PTR_FUN_000406d8)(PTR_DAT_000406d4);
  if (cVar5 == '\0') {
    uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map0_Curvature_000406dc);
    puVar6 = PTR_Model_Map0_Center_000406e0;
    *(undefined4 *)puVar2 = uVar8;
    uVar8 = (*(code *)puVar4)(uVar7,uVar9,puVar6);
    *(undefined4 *)puVar3 = uVar8;
    uVar7 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map0_Peak_000406e4);
    *(undefined4 *)puVar1 = uVar7;
  }
  else if (*PTR_Pattern_EventMask_000406e8 == '\0') {
    uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map1_Curvature_00040708);
    puVar6 = PTR_Model_Map1_Center_0004070c;
    *(undefined4 *)puVar2 = uVar8;
    uVar8 = (*(code *)puVar4)(uVar7,uVar9,puVar6);
    *(undefined4 *)puVar3 = uVar8;
    uVar7 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map1_Peak_00040710);
    *(undefined4 *)puVar1 = uVar7;
  }
  else {
    if (*PTR_DAT_000406ec == '\x01') {
      uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map3_Curvature_000406f0);
      *(undefined4 *)puVar2 = uVar8;
      uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map3_Center_000406f4);
      puVar6 = PTR_Model_Map3_Peak_000406f8;
      *(undefined4 *)puVar3 = uVar8;
    }
    else {
      uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map2_Curvature_000406fc);
      *(undefined4 *)puVar2 = uVar8;
      uVar8 = (*(code *)puVar4)(uVar7,uVar9,PTR_Model_Map2_Center_00040700);
      puVar6 = PTR_Model_Map2_Peak_00040704;
      *(undefined4 *)puVar3 = uVar8;
    }
    uVar7 = (*(code *)puVar4)(uVar7,uVar9,puVar6);
    *(undefined4 *)puVar1 = uVar7;
  }
  puVar4 = PTR_DAT_0004071c;
  *(float *)PTR_Model_AtCurrentSpark_00040718 =
       *(float *)puVar1 -
       *(float *)puVar2 * (*(float *)puVar3 - *(float *)PTR_DAT_00040714) *
       (*(float *)puVar3 - *(float *)PTR_DAT_00040714);
  *(float *)PTR_Model_AtBaselineSpark_00040720 =
       *(float *)puVar1 -
       *(float *)puVar2 * (*(float *)puVar3 - *(float *)puVar4) *
       (*(float *)puVar3 - *(float *)puVar4);
  return;
}

