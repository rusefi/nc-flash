/* Ghidra analysis output; verify against original SH instructions. */

/* Stock lookup A35A4 from6D28 to8010; every knot/interior/outside test; control-sources.txt.
   Physicalinput identity open. */

void Control_MapOverrideInput(void)

{
  undefined4 uVar1;
  
  uVar1 = (*(code *)PTR_FUN_000581fc)(PTR_Control_RawFirstAlternate_000581f8);
  uVar1 = (*(code *)PTR_Lookup_FloatCurve_00058204)(uVar1,DAT_00058200);
  *(undefined4 *)PTR_Control_MappedOverrideInput_00058208 = uVar1;
  return;
}

