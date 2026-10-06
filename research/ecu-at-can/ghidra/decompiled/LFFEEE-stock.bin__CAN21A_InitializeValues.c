/* Ghidra analysis output; verify against original SH instructions. */

/* Writes6A9C and protected6AA0 to-10000 via real15522 helper. */

void CAN21A_InitializeValues(void)

{
  undefined4 uVar1;
  undefined *puVar2;
  
  puVar2 = PTR_CAN21A_GatedWord1Value_00035790;
  uVar1 = DAT_00035788;
  *(undefined4 *)PTR_CAN21A_Word0Value_0003578c = DAT_00035788;
  (*(code *)PTR_FUN_00035794)(uVar1,puVar2);
  return;
}

