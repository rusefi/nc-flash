/* Ghidra analysis output; verify against original SH instructions. */

/* Executedall256bytes via16178/2C3B4:660F incrementsmod256. Hookrolecandidate
   basedcountercomparison, notphysicalevent. */

void Control_IncrementFirstActivityEnd(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  uVar2 = (*(code *)PTR_FUN_0002c64c)(0x10);
  puVar1 = PTR_FUN_0002c654;
  *PTR_DAT_0002c65c = *PTR_DAT_0002c65c + '\x01';
  (*(code *)puVar1)(uVar2);
  return;
}

