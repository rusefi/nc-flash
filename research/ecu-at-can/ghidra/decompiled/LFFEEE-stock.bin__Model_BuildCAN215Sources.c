/* Ghidra analysis output; verify against original SH instructions. */

/* 71FC=71F4+D0+D8;71EC=71F8+D0+D8;71B4=71FC*max(8-unsigned71F0,0)/8.2304 count/source cases plus
   stock-map feedback. */

undefined4 Model_BuildCAN215Sources(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined *puVar3;
  undefined4 uVar4;
  byte bVar5;
  float fVar6;
  float extraout_fr0;
  float extraout_fr0_00;
  undefined4 uVar7;
  
  bVar5 = *PTR_Model_PatternCount_00040a04;
  fVar6 = (float)(*(code *)PTR_FUN_00040a0c)(PTR_Model_ReferenceAuxiliaryOffset_00040a08);
  uVar4 = (*(code *)PTR_FUN_00040a0c)(PTR_Model_ScaledAuxiliaryOffset_00040a10);
  puVar3 = PTR_CAN215_PrimaryModelInput_00040a20;
  puVar2 = PTR_Model_AtBaselineSpark_00040a1c;
  puVar1 = PTR_Model_UnscaledCurrentValue_00040a14;
  *(float *)PTR_Model_UnscaledCurrentValue_00040a14 =
       *(float *)PTR_Model_AtCurrentSpark_00040a18 + fVar6 + extraout_fr0;
  *(float *)puVar3 = *(float *)puVar2 + fVar6 + extraout_fr0;
  if (bVar5 < 9) {
    bVar5 = 8 - bVar5;
  }
  else {
    bVar5 = 0;
  }
  if (bVar5 < 8) {
    uVar4 = 0;
    uVar7 = 0x3f800000;
    fVar6 = (float)(*(code *)PTR_FUN_00040a24)(0x3f800000,0);
    uVar4 = (*(code *)PTR_FUN_00040a24)(uVar7,uVar4,8);
    *(float *)PTR_CAN215_SecondModelInput_00040a28 = (*(float *)puVar1 * fVar6) / extraout_fr0_00;
  }
  else {
    *(undefined4 *)PTR_CAN215_SecondModelInput_00040a28 = *(undefined4 *)puVar1;
  }
  return uVar4;
}

