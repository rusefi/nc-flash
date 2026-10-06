/* Ghidra analysis output; verify against original SH instructions. */

/* Combines local max/sumS;7AC4=S,7AC0=S+CAN2117D2C,7A94=S+AT7C74,7A90=S+both.480 paired
   producer-order cases plus8 fault cases reach spark/cut outputs; spark-interaction.txt. */

void Spark_AggregateCorrections(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  
  puVar1 = PTR_FUN_0004ff9c;
  fVar9 = *(float *)PTR_CAN211_SparkCorrection_0004ff94;
  fVar10 = *(float *)PTR_CAN216_SparkCorrection_0004ff98;
  uVar5 = (*(code *)PTR_FUN_0004ff9c)
                    (*(undefined4 *)PTR_DAT_0004ffa4,*(undefined4 *)PTR_DAT_0004ffa0);
  uVar6 = (*(code *)puVar1)(*(undefined4 *)PTR_DAT_0004ffac,*(undefined4 *)PTR_DAT_0004ffa8);
  uVar5 = (*(code *)puVar1)(uVar6,uVar5);
  uVar5 = (*(code *)puVar1)(*(undefined4 *)PTR_DAT_0004ffb0,uVar5);
  fVar7 = (float)(*(code *)puVar1)(*(undefined4 *)PTR_DAT_0004ffb4,uVar5);
  puVar4 = PTR_DAT_0004ffdc;
  puVar3 = PTR_DAT_0004ffd8;
  puVar2 = PTR_DAT_0004ffd4;
  puVar1 = PTR_DAT_0004ffb8;
  fVar7 = *(float *)PTR_DAT_0004ffc0 + *(float *)PTR_DAT_0004ffbc + *(float *)PTR_DAT_0004ffc4 +
          *(float *)PTR_DAT_0004ffc8 + *(float *)PTR_DAT_0004ffcc + *(float *)PTR_DAT_0004ffd0 +
          fVar7;
  *(float *)PTR_DAT_0004ffb8 = fVar7;
  fVar7 = fVar7 + fVar9;
  *(float *)puVar2 = fVar7;
  *(float *)puVar3 = *(float *)puVar1 + fVar10;
  *(float *)puVar4 = fVar7 + fVar10;
  fVar7 = *(float *)PTR_DAT_0004ffe0;
  fVar10 = (float)(*(code *)PTR_FUN_0004ffe8)(PTR_DAT_0004ffe4);
  fVar8 = *(float *)PTR_DAT_0004ffec;
  fVar9 = fVar7;
  if (0.0 < fVar10) {
    fVar8 = fVar8 - fVar10;
    fVar9 = fVar7 - fVar10;
    fVar7 = *(float *)PTR_DAT_0004fff4 + fVar7;
  }
  uVar5 = (*(code *)PTR_FUN_0004fff8)(fVar8,fVar9,1.0 - *(float *)PTR_DAT_0004fff0,0);
  puVar1 = PTR_DAT_00050000;
  *(undefined4 *)PTR_DAT_0004fffc = uVar5;
  uVar5 = (*(code *)PTR_FUN_00050004)(*(undefined4 *)puVar1,fVar7);
  puVar3 = PTR_DAT_00050008;
  fVar7 = (float)(*(code *)PTR_FUN_00050004)(*(undefined4 *)PTR_DAT_0004fffc,uVar5);
  puVar2 = PTR_DAT_0005000c;
  *(float *)puVar3 = fVar7;
  puVar4 = PTR_DAT_00050010;
  puVar1 = PTR_DAT_0004ffd4;
  *(float *)puVar2 = fVar7 - *(float *)PTR_DAT_0004ffdc;
  puVar2 = PTR_DAT_0004ffd8;
  *(float *)puVar4 = *(float *)puVar3 - *(float *)puVar1;
  *(float *)PTR_DAT_00050014 = *(float *)puVar3 - *(float *)puVar2;
  return;
}

