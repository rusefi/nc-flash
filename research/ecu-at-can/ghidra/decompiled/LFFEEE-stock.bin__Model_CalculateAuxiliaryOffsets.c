/* Ghidra analysis output; verify against original SH instructions. */

/* A232C at6DB4/6D20 ->71CC,at6DB4/80 ->71D0. max(curveA2218-71D0,0)*curveA2224 ->71D8.48 varied
   producers and complete feedback execute. */

void Model_CalculateAuxiliaryOffsets(void)

{
  undefined *puVar1;
  undefined *puVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  float fVar5;
  float fVar6;
  
  puVar1 = PTR_FUN_00040844;
  uVar3 = (*(code *)PTR_FUN_00040844)(PTR_DAT_00040848);
  uVar4 = (*(code *)puVar1)(PTR_DAT_0004084c);
  uVar4 = (*(code *)PTR_Lookup_FloatMap2D_00040854)(uVar3,uVar4,PTR_Model_AuxiliaryMap_00040850);
  *(undefined4 *)PTR_Model_CurrentAuxiliaryOffset_00040858 = uVar4;
  uVar4 = (*(code *)PTR_Lookup_FloatMap2D_00040854)
                    (uVar3,DAT_0004085c,PTR_Model_AuxiliaryMap_00040850);
  (*(code *)PTR_FUN_00040864)(uVar4,PTR_Model_ReferenceAuxiliaryOffset_00040860);
  fVar5 = (float)(*(code *)PTR_Lookup_FloatCurve_0004086c)(uVar3,DAT_00040868);
  *(float *)PTR_DAT_00040870 = fVar5;
  fVar6 = (float)(*(code *)puVar1)(PTR_Model_ReferenceAuxiliaryOffset_00040860);
  fVar5 = (float)(*(code *)PTR_FUN_00040874)(fVar5 - fVar6,0);
  uVar3 = (*(code *)puVar1)(PTR_DAT_00040878);
  fVar6 = (float)(*(code *)PTR_Lookup_FloatCurve_0004086c)(uVar3,DAT_0004087c);
  puVar2 = PTR_Model_ScaledAuxiliaryOffset_00040884;
  puVar1 = PTR_FUN_00040864;
  *(float *)PTR_DAT_00040880 = fVar6;
  (*(code *)puVar1)(fVar6 * fVar5,puVar2);
  return;
}

