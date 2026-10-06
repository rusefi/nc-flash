/* Ghidra analysis output; verify against original SH instructions. */

/* Subtract protected71C4 from71B4/71FC/71EC ->71B8/71BC/71C0.71C0 feeds AT request enable
   comparison. */

void Model_SubtractPublishedOffset(void)

{
  undefined *puVar1;
  float fVar2;
  
  fVar2 = (float)(*(code *)PTR_FUN_00040a0c)(PTR_CAN215_SharedModelOffset_00040a68);
  puVar1 = PTR_Model_UnscaledCurrentValue_00040a14;
  *(float *)PTR_Model_NetCountScaledValue_00040a70 =
       *(float *)PTR_CAN215_SecondModelInput_00040a28 - fVar2;
  *(float *)PTR_Model_NetUnscaledValue_00040a74 = *(float *)puVar1 - fVar2;
  *(float *)PTR_Model_NetBaselineValue_00040a78 =
       *(float *)PTR_CAN215_PrimaryModelInput_00040a20 - fVar2;
  return;
}

