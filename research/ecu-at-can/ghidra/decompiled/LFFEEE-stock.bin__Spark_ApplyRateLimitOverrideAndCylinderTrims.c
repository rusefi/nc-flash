/* Ghidra analysis output; verify against original SH instructions. */

/* Normal path min(7A78,7ACC+lookupA2D70), diagnostic8B366 then7A74; adds stockD0594..D05A0 trims
   to7A9C/A0/A4/A8.20 CAN211 examples execute; ignition timer not simulated. */

void Spark_ApplyRateLimitOverrideAndCylinderTrims(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined *puVar5;
  float fVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  
  uVar8 = *(undefined4 *)PTR_DAT_0004fcec;
  if (((int)(char)*PTR_DAT_0004fd10 & 0x80U) == 0) {
    uVar7 = (*(code *)PTR_FUN_0004fd18)(PTR_DAT_0004fd14);
    fVar6 = (float)(*(code *)PTR_Lookup_FloatCurve_0004fd20)(uVar7,PTR_PTR_0004fd1c);
    puVar1 = PTR_FUN_0004fd28;
    *(float *)PTR_DAT_0004fd24 = fVar6;
    uVar7 = (*(code *)puVar1)(uVar8,fVar6 + *(float *)PTR_DAT_0004fcf8);
  }
  else {
    uVar7 = *(undefined4 *)PTR_DAT_0004fce4;
  }
  puVar2 = PTR_FUN_0004fd30;
  puVar1 = PTR_DAT_0004fce8;
  *(undefined4 *)PTR_DAT_0004fd2c = uVar7;
  fVar6 = (float)(*(code *)puVar2)();
  *(float *)puVar1 = fVar6;
  puVar5 = PTR_DAT_0004fd0c;
  puVar4 = PTR_DAT_0004fd08;
  puVar2 = PTR_DAT_0004fd04;
  puVar3 = PTR_Spark_Cylinder1Command_0004fcfc;
  *(float *)PTR_Spark_Cylinder1Command_0004fcfc = fVar6 + *(float *)PTR_DAT_0004fd00;
  *(float *)(puVar3 + 4) = *(float *)puVar1 + *(float *)puVar2;
  puVar2 = PTR_DAT_0004fcf8;
  *(float *)(puVar3 + 8) = *(float *)puVar1 + *(float *)puVar4;
  *(float *)(puVar3 + 0xc) = *(float *)puVar1 + *(float *)puVar5;
  *(undefined4 *)puVar2 = uVar8;
  return;
}

