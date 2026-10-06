/* Ghidra analysis output; verify against original SH instructions. */

/* 6D20 indexesA1A0C lower8254 andA1A00 upper825C;original22F8 andprotected15522 executed. Stock
   lower0..4.5 andupper30..60. */

void Control_MapOverrideSourceBounds(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = (*(code *)PTR_FUN_0005c57c)(PTR_DAT_0005c578);
  uVar2 = (*(code *)PTR_Lookup_FloatCurve_0005c584)
                    (uVar1,PTR_Control_OverrideLowerMapDescriptor_0005c580);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_0005c584)
                    (uVar1,PTR_Control_OverrideUpperMapDescriptor_0005c588);
  (*(code *)PTR_FUN_0005c590)(uVar2,PTR_Control_OverrideSourceLowerBound_0005c58c);
  (*(code *)PTR_FUN_0005c590)(uVar1,PTR_Control_OverrideSourceUpperBound_0005c594);
  return;
}

