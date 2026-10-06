/* Ghidra analysis output; verify against original SH instructions. */

/* Protected71C4=71CC+71D8+71E0+protected7258. Original protected read/write helpers execute. */

void Model_SumPublishedOffset(void)

{
  float fVar1;
  float fVar2;
  
  fVar1 = (float)(*(code *)PTR_FUN_00040a0c)(PTR_Model_ScaledAuxiliaryOffset_00040a10);
  fVar2 = *(float *)PTR_Model_CurrentAuxiliaryOffset_00040a60 + fVar1 +
          *(float *)PTR_Model_RatioOffset_00040a5c;
  fVar1 = (float)(*(code *)PTR_FUN_00040a0c)(PTR_DAT_00040a64);
  (*DAT_00040a6c)(fVar2 + fVar1,PTR_CAN215_SharedModelOffset_00040a68);
  return;
}

