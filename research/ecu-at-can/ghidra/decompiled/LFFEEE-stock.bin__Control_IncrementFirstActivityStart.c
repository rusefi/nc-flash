/* Ghidra analysis output; verify against original SH instructions. */

/* Executedall256bytes via1616C/2C384:660E incrementsmod256,criticalsectionrestoresSR.
   Schedulerhookordering notexecuted. */

void Control_IncrementFirstActivityStart(void)

{
  undefined *puVar1;
  undefined4 uVar2;
  
  uVar2 = (*(code *)PTR_FUN_0002c64c)(0x10);
  puVar1 = PTR_FUN_0002c654;
  *PTR_DAT_0002c650 = *PTR_DAT_0002c650 + '\x01';
  (*(code *)puVar1)(uVar2);
  return;
}

